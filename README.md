## Parking Detection 🚗🅿️

Automatski sustav za detekciju zauzetih i slobodnih parking mjesta pomoću računalnog vida.  
Projekt koristi **Python** i **OpenCV** za obradu videa te generira izlazni video s označenim slobodnim i zauzetim mjestima.

---

## 🚀 Značajke

- ✅ Detekcija slobodnih i zauzetih parking mjesta  
- ✅ Vizualizacija pomoću **bounding boxova**  
  - 🟢 zeleno = slobodno  
  - 🔴 crveno = zauzeto  
- ✅ Brojač slobodnih i zauzetih mjesta  
- ✅ Generiranje renderiranog izlaznog videa koji se može preuzeti  
- ✅ Modularna arhitektura (backend + frontend)  
- ✅ 100% točnost na dostupnim testnim podacima  

---

## 🖼️ Demo

### Screenshot
![Demo Screenshot](backend/rendered_videos/Picture1.jpg)

### GIF
![Demo GIF](backend/rendered_videos/Demo2.gif)

### Live verzija
[Live Site](https://tvoj-live-link.com)

---

## 📂 Struktura projekta

- **backend/model/** – Sadrži sve što je vezano uz strojno učenje: trening skriptu i spremljeni model.
- **backend/detect_parking.py** – Implementacija glavnih funkcija detekcije.
- **backend/utils.py** – Pomoćne funkcije za obradu podataka i podršku glavnom algoritmu. 
- **backend/main.py** – Pokreće cijeli backend sustav, uključujući učitavanje modela, obradu videa/slika i generiranje outputa.  
- **frontend/** – React-based web aplikacija za prikaz rezultata detekcije, upload videa i vizualizaciju slobodnih/zauzetih mjesta.  .  
- **.gitignore** – Definira koje datoteke i mape Git ignorira (npr. venv, temp files).  
- **README.md** – Dokumentacija projekta s opisom, uputama za pokretanje i primjerima outputa.

---

## ⚙️ Instalacija i pokretanje

```
1. Kloniraj repozitorij
git clone https://github.com/Kico611/ParkingDetection.git
cd ParkingDetection
```

```
2. Instaliraj potrebne pakete za backend
pip install -r requirements.txt
```

```
3. Pokreni FastAPI backend
uvicorn backend.main:app --reload
Backend će biti dostupan na http://127.0.0.1:8000
```

```
4. Pokreni React frontend
cd frontend
npm install
npm run dev
Frontend će biti dostupan na adresi koju terminal prikazuje (obično http://localhost:5173)
```

---

## 📊 Performanse
Točnost: 100% na dostupnim testnim podacima

Način rada: Offline – korisnik šalje MP4 video, sustav ga obradi i generira izlazni video

Latencija: Ovisi o duljini i rezoluciji videa (nije real-time)

Ograničenje: Testirano samo na jednom setu snimki – performanse u različitim uvjetima još nisu evaluirane

---

## 🛠️ Tehnologije
- **Python 3.10+**
  
- **OpenCV**
  
- **NumPy**
  
- **FastAPI**
  
- **React (HTML / CSS / JavaScript)**

---

## 🔮 Moguće nadogradnje
Testiranje u različitim vremenskim i svjetlosnim uvjetima

Real-time obrada (kamera → live detekcija)

Integracija YOLO / Mask R-CNN modela za automatsko prepoznavanje parking slotova

Integracija s mobilnom aplikacijom

Deployment na Raspberry Pi + kamera za pametna parking rješenja

---
