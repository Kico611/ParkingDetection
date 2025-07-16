import os
import firebase_admin
from firebase_admin import credentials, firestore

# Postavi putanju do JSON ključa
BASE_DIR = os.path.dirname(__file__)
cred_path = os.path.join(BASE_DIR, "firebase_key.json")

# Inicijaliziraj Firebase aplikaciju
if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)

# Dohvati Firestore klijenta
db = firestore.client()
