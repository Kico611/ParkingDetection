Parking Detection 🚗🅿️

Automatski sustav za detekciju zauzetih i slobodnih parking mjesta pomoću računalnog vida.
Projekt koristi OpenCV i Python za obradu videa te generira izlazni video s označenim slobodnim i zauzetim mjestima.

🚀 Značajke

✅ Detekcija slobodnih i zauzetih parking mjesta

✅ 100% točnost na dostupnim testnim podacima

✅ Vizualizacija pomoću bounding boxova (zeleno = slobodno, crveno = zauzeto)

✅ Brojač slobodnih i zauzetih mjesta

✅ Modularna arhitektura (backend + frontend)

✅ Generiranje renderiranog izlaznog videa koji se može preuzeti

🖼️ Demo



📂 Struktura projekta
ParkingDetection/
│── backend/ # Python kod za detekciju i logiku
│── frontend/ # Web sučelje (vizualizacija, upload videa)
│── data/ # Testne slike / video
│── models/ # (opcionalno) modeli za proširenje
│── README.md # Dokumentacija

⚙️ Instalacija i pokretanje

Kloniraj repozitorij:

git clone https://github.com/Kico611/ParkingDetection.git
cd ParkingDetection


Kreiraj virtualno okruženje i instaliraj ovisnosti:

python -m venv venv
source venv/bin/activate # (Linux/Mac)
venv\Scripts\activate # (Windows)
pip install -r requirements.txt


Pokreni backend:

python main.py


Otvori frontend i učitaj video (.mp4).
Nakon obrade, izlazni video se može preuzeti s označenim mjestima.

📊 Performanse

Točnost: 100% na dostupnim testnim podacima

Način rada: Obrada se radi offline – korisnik šalje MP4 video, sustav ga obradi i generira izlazni video

Latencija: Ovisi o duljini i rezoluciji videa (nije real-time)

Ograničenje: Testirano samo na snimkama iz jednog seta (isti uvjeti snimanja) – performanse u različitim vremenskim i svjetlosnim uvjetima još nisu evaluirane

🛠️ Tehnologije

Python 3.10+

OpenCV

NumPy

Flask / FastAPI (backend API)

HTML/CSS/JS (frontend)

🔮 Moguće nadogradnje

Testiranje na različitim vremenskim i svjetlosnim uvjetima

Implementacija real-time obrade (kamera → live detekcija)

Dodavanje YOLO/Mask R-CNN modela za automatsko prepoznavanje parking slotova

Integracija s mobilnom aplikacijom za korisnike

Deployment na Raspberry Pi + kamera za pametna parking rješenja

👨‍💻 Autor

Kristijan Balić

GitHub profil
