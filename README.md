Samo izvoli. Uredio sam cijeli README.md fajl, uključujući promjene koje smo napravili u sekciji za instalaciju, i dodao nekoliko sitnih poboljšanja za bolju čitljivost i profesionalniji izgled.

Parking Detection 🚗🅿️
Automatski sustav za detekciju zauzetih i slobodnih parking mjesta pomoću računalnog vida.

Projekt koristi Python i OpenCV za obradu videa te generira izlazni video s označenim slobodnim i zauzetim mjestima.

🚀 Značajke
✅ Detekcija slobodnih i zauzetih parking mjesta

✅ Vizualizacija pomoću bounding boxova - 🟢 zeleno = slobodno

🔴 crveno = zauzeto

✅ Brojač slobodnih i zauzetih mjesta

✅ Generiranje renderiranog izlaznog videa koji se može preuzeti

✅ Modularna arhitektura (backend + frontend)

✅ 100% točnost na dostupnim testnim podacima

🖼️ Demo
Screenshot
Video
Demo Video

Live verzija
Live Site

📂 Struktura projekta
YAML

ParkingDetection/
│── backend/
│ │── model/ # Trening.py i model.pkl
│ │── main.py # Glavni Python skript za pokretanje
│── frontend/ # Web sučelje (upload videa i vizualizacija)
│── data/ # Testne slike / video
│── README.md # Dokumentacija
⚙️ Instalacija i pokretanje
Kloniraj repozitorij:

Bash

git clone https://github.com/Kico611/ParkingDetection.git
cd ParkingDetection
Instaliraj potrebne pakete:

Bash

pip install -r requirements.txt
Pokreni backend:

Bash

python backend/main.py
Otvori frontend u pregledniku i uploadaj video za detekciju.

📊 Performanse
Točnost: 100% na dostupnim testnim podacima

Način rada: Offline – korisnik šalje MP4 video, sustav ga obradi i generira izlazni video

Latencija: Ovisi o duljini i rezoluciji videa (nije real-time)

Ograničenje: Testirano samo na jednom setu snimki – performanse u različitim uvjetima još nisu evaluirane.

🛠️ Tehnologije
Python 3.10+

OpenCV

NumPy

Flask / FastAPI (backend API)

HTML / CSS / JavaScript (frontend)

🔮 Moguće nadogradnje
Testiranje u različitim vremenskim i svjetlosnim uvjetima

Real-time obrada (kamera → live detekcija)

Integracija YOLO / Mask R-CNN modela za automatsko prepoznavanje parking slotova

Integracija s mobilnom aplikacijom

Deployment na Raspberry Pi + kamera za pametna parking rješenja

👨‍💻 Autor
Kristijan Balić
