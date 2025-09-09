# ParkingDetection

**ParkingDetection** je sustav za automatsku detekciju slobodnih i zauzetih parkirnih mjesta koristeći računalni vid i strojno učenje. Projekt omogućuje praćenje parkirališta u stvarnom vremenu i vizualno označavanje statusa mjesta, čime se poboljšava efikasnost upravljanja prostorom i korisničko iskustvo.

## 🎯 Cilj projekta

Cilj projekta je stvoriti sustav koji:
- Automatski prepoznaje zauzeta i slobodna parkirna mjesta.
- Omogućuje vizualni prikaz stanja parkirališta.
- Može se integrirati u web ili mobilne aplikacije za prikaz informacija korisnicima.

## 🏗️ Arhitektura

Projekt je podijeljen na dva glavna dijela:

### 1. Backend
- **Detekcija parkirnih mjesta**: koristi OpenCV za obradu slike i identifikaciju bounding boxeva parkirnih mjesta.  
- **Model strojog učenja**: klasificira svako parkirno mjesto kao slobodno ili zauzeto.  
- **Obrada videa i slika**: omogućuje analizu pojedinačnih slika ili video feedova i vraćanje vizualnih rezultata.  
- **Integracija s bazom podataka i cloud storageom**: pohranjuje rezultate i generirane slike/videozapise (Firebase Firestore i Supabase).

### 2. Frontend
- Prikazuje rezultate detekcije u vizualnom obliku.
- Može prikazati overlay s brojem slobodnih i zauzetih mjesta.
- Omogućuje preuzimanje generiranih videozapisa i slika.

## ⚡ Funkcionalnosti

- Prepoznavanje slobodnih i zauzetih parkirnih mjesta u stvarnom vremenu.
- Prikaz bounding boxeva na parkirnim mjestima (zeleno = slobodno, crveno = zauzeto).
- Ažuriranje broja slobodnih i zauzetih mjesta.
- Optimizacija performansi za video feedove pomoću provjere samo značajnih promjena.
- Integracija s cloud servisima za pohranu i dohvat podataka.

## 💡 Primjena

- Pametna parkirališta u gradovima.
- Integracija u mobilne aplikacije ili web platforme za vozače.
- Analiza zauzetosti parkirališta tijekom dana.
- Automatizacija upravljanja parkirnim prostorom.

## 📊 Tehnologije

- Python (backend logika)
- OpenCV (računalni vid)
- NumPy (numeričke operacije)
- Pickle (učitavanje modela)
- Firebase / Supabase (cloud pohrana)
