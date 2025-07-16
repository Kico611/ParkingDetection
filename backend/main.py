from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import io
from detect_parking import detect_parking_and_render_video, process_parking_image
from datetime import datetime
import os
import uuid
import firebase_admin
from firebase_admin import credentials, firestore
from supabase import create_client
from io import BytesIO


# === Supabase konfiguracija ===
SUPABASE_URL = "https://tqlmwaywxkxtfpdfjrpc.supabase.co"
SUPABASE_ANON_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InRxbG13YXl3eGt4dGZwZGZqcnBjIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTI3MDAzODIsImV4cCI6MjA2ODI3NjM4Mn0.sUkFC6hozij9GOCc_3GSPHun7a98ddeMCWtvcFCEZMo"
SUPABASE_BUCKET = "parking"

supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

# === Firebase Firestore konfiguracija ===
cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # u produkciji ograničiti domene
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

OUTPUT_FOLDER = "rendered_videos"  # ili neka druga mapa gdje želiš spremati video


@app.post("/render-and-download")
async def render_and_download(file: UploadFile = File(...)):
    try:
        video_bytes = await file.read()
        output_bytes = detect_parking_and_render_video(video_bytes)

        filename = f"{uuid.uuid4()}.mp4"
        output_path = os.path.join(OUTPUT_FOLDER, filename)

        with open(output_path, "wb") as f:
            f.write(output_bytes)

        return FileResponse(
            path=output_path,
            media_type="video/mp4",
            filename=filename,
            headers={"Content-Disposition": f'attachment; filename="{filename}"'}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/last-result")
async def get_last_result():
    docs = db.collection("parking_detection")\
             .order_by("timestamp", direction=firestore.Query.DESCENDING)\
             .limit(1).stream()

    for doc in docs:
        data = doc.to_dict()
        return {
            "free_slots": data.get("free_slots"),
            "occupied_slots": data.get("occupied_slots"),
            "total_slots": data.get("total_slots"),
            "image_url": data.get("image_url"),
            "timestamp": data.get("timestamp")
        }

    return JSONResponse(content={"message": "Nema pohranjenih rezultata."}, status_code=404)


def upload_image_to_supabase(image_bytes: bytes) -> str:
    unique_filename = f"processed_images/{uuid.uuid4()}.jpg"

    response = supabase.storage.from_(SUPABASE_BUCKET).upload(
        path=unique_filename,
        file=image_bytes
    )

    if hasattr(response, 'error') and response.error:
        raise Exception(f"Neuspješan upload: {response.error}")

    public_url_response = supabase.storage.from_(SUPABASE_BUCKET).get_public_url(unique_filename)
    public_url = public_url_response # ispravno dohvaćanje URL-a

    if not public_url:
        raise Exception("Nije moguće dohvatiti javni URL slike.")

    return public_url

@app.post("/process_parking_image/")
async def process_parking_image_endpoint(file: UploadFile = File(...)):
    try:
        content = await file.read()
        processed_image_bytes, free, occupied, total = process_parking_image(content)

        image_url = upload_image_to_supabase(processed_image_bytes)

        doc_ref = db.collection("parking_detection").document()
        doc_ref.set({
            "free_slots": free,
            "occupied_slots": occupied,
            "total_slots": total,
            "timestamp": datetime.now(),  # pohranjuj kao Firestore timestamp
            "image_url": image_url
        })

        return StreamingResponse(io.BytesIO(processed_image_bytes), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
