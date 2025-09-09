import cv2
import numpy as np
from tempfile import NamedTemporaryFile
from util import get_parking_spots_bboxes, empty_or_not

# Funkcija za računanje razlike između dva izreza parkirnog mjesta
# -> koristi se da detektiramo gdje je došlo do promjene (npr. auto došao ili otišao)
def calc_diff(im1, im2):
    return np.abs(np.mean(im1) - np.mean(im2))

# Putanja do maske koja definira parking mjesta
MASK_PATH = './mask_1920_1080.png'

# Funkcija za obradu JEDNE slike parkinga
def process_parking_image(image_bytes: bytes, mask_path=MASK_PATH):
    # Dekodiraj bajtove u OpenCV sliku (BGR format)
    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if frame is None:
        raise ValueError("Ne može se dekodirati slika")

    # Učitaj masku (binarnu sliku) i pronađi parking mjesta pomoću connected components
    mask = cv2.imread(mask_path, 0)
    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    spots = get_parking_spots_bboxes(connected_components)

    # Provjeri za svako parking mjesto je li prazno ili zauzeto
    spots_status = [empty_or_not(frame[y:y+h, x:x+w]) for (x,y,w,h) in spots]

    # Brojanje rezultata
    total = len(spots_status)
    free = sum(spots_status)         # True = prazno
    occupied = total - free

    # Crtanje bounding boxeva i boja (zeleno = slobodno, crveno = zauzeto)
    for i, (x, y, w, h) in enumerate(spots):
        color = (0, 255, 0) if spots_status[i] else (0, 0, 255)
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)

    # Overlay s brojem slobodnih i zauzetih mjesta
    cv2.rectangle(frame, (50, 20), (600, 80), (0, 0, 0), -1)
    cv2.putText(frame,
                f"Free: {free} | Occupied: {occupied} | Total: {total}",
                (60, 60),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255,255,255),
                2)

    # Enkodiranje slike natrag u JPEG bytes
    success, encoded = cv2.imencode('.jpg', frame)
    if not success:
        raise RuntimeError("Neuspjelo enkodiranje slike")

    return encoded.tobytes(), free, occupied, total


# Funkcija za obradu VIDEA parkinga i vraćanje renderiranog outputa
# Koristi heuristiku da ne provjerava sva mjesta u svakom frameu,
# nego samo kad se detektira veća promjena -> optimizacija performansi
def detect_parking_and_render_video(video_bytes: bytes, mask_path='./mask_1920_1080.png', step=30) -> bytes:
    # Spremi ulazni video privremeno na disk (OpenCV treba file path)
    with NamedTemporaryFile(delete=False, suffix=".mp4") as input_tmp:
        input_tmp.write(video_bytes)
        input_tmp_path = input_tmp.name

    # Otvori video file
    cap = cv2.VideoCapture(input_tmp_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Priprema output videa (isti fps i dimenzije kao ulaz)
    output_tmp = NamedTemporaryFile(delete=False, suffix=".mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_tmp.name, fourcc, fps, (width, height))

    # Detekcija parking mjesta iz maske
    mask = cv2.imread(mask_path, 0)
    connected_components = cv2.connectedComponentsWithStats(mask, 4, cv2.CV_32S)
    spots = get_parking_spots_bboxes(connected_components)

    # Inicijalne strukture za spremanje stanja parking mjesta
    diffs = [None for _ in spots]       # razlike između frameova
    spots_status = [None for _ in spots] # statusi parking mjesta
    previous_frame = None
    frame_nmr = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Svakih 'step' frameova uspoređujemo promjene
        if frame_nmr % step == 0 and previous_frame is not None:
            for i, (x1, y1, w, h) in enumerate(spots):
                spot_crop = frame[y1:y1 + h, x1:x1 + w]
                prev_crop = previous_frame[y1:y1 + h, x1:x1 + w]
                diffs[i] = calc_diff(spot_crop, prev_crop)

        # Svakih 'step' frameova ažuriramo status parking mjesta
        if frame_nmr % step == 0:
            if previous_frame is None:
                # Prvi prolaz -> provjeri sva mjesta
                arr_ = range(len(spots))
            else:
                # Kasnije -> provjeri samo ona mjesta gdje je detektirana značajna promjena
                arr_ = [j for j in np.argsort(diffs) if diffs[j] / np.amax(diffs) > 0.4]

            for i in arr_:
                x1, y1, w, h = spots[i]
                crop = frame[y1:y1 + h, x1:x1 + w]
                spots_status[i] = empty_or_not(crop)

            # Zapamti frame za usporedbu u sljedećem krugu
            previous_frame = frame.copy()

        # Crtanje oznaka parking mjesta na trenutnom frameu
        for i, (x1, y1, w, h) in enumerate(spots):
            status = spots_status[i]
            color = (0, 255, 0) if status else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x1 + w, y1 + h), color, 2)

        # Brojanje slobodnih i zauzetih mjesta
        total = len(spots_status)
        free = sum(spots_status)
        occupied = total - free

        # Overlay s rezultatima
        cv2.rectangle(frame, (50, 20), (600, 80), (0, 0, 0), -1)
        cv2.putText(frame,
                    f"Free: {free} | Occupied: {occupied} | Total: {total}",
                    (60, 60),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 255, 255),
                    2)

        # Snimi frame u output video
        out.write(frame)
        frame_nmr += 1

    # Oslobodi resurse
    cap.release()
    out.release()

    # Vrati output video u obliku bajtova
    with open(output_tmp.name, "rb") as f:
        output_video_bytes = f.read()

    return output_video_bytes
