import os
import pickle
from skimage.io import imread
from skimage.transform import resize
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

# --- 1. Postavke ---
input_dir = 'clf-data'
categories = ['empty', 'not_empty']

print("[INFO] Početak učitavanja podataka...")

# --- 2. Učitavanje slika ---
data = []
labels = []
for category_idx, category in enumerate(categories):
    folder_path = os.path.join(input_dir, category)
    print(f"[INFO] Učitavam slike iz kategorije '{category}'...")
    for file in os.listdir(folder_path):
        img_path = os.path.join(folder_path, file)
        img = imread(img_path)
        img = resize(img, (15, 15))
        data.append(img.flatten())
        labels.append(category_idx)

print(f"[INFO] Ukupno učitanih uzoraka: {len(data)}")

data = np.asarray(data)
labels = np.asarray(labels)

# --- 3. Train/Test split ---
print("[INFO] Dijelim podatke na train/test skup...")
x_train, x_test, y_train, y_test = train_test_split(
    data, labels, test_size=0.2, shuffle=True, stratify=labels
)
print(f"[INFO] Train set: {x_train.shape[0]} uzoraka, Test set: {x_test.shape[0]} uzoraka")

# --- 4. Trening klasifikatora ---
print("[INFO] Pokrećem GridSearch za SVM...")
classifier = SVC()
parameters = [{'gamma': [0.01, 0.001, 0.0001], 'C': [1, 10, 100, 1000]}]

grid_search = GridSearchCV(classifier, parameters, verbose=1)  # verbose=1 -> ispisuje napredak
grid_search.fit(x_train, y_train)

# --- 5. Rezultati ---
print("[INFO] GridSearch završen!")
print(f"[INFO] Najbolji parametri: {grid_search.best_params_}")

best_estimator = grid_search.best_estimator_

print("[INFO] Evaluiram model na testnom skupu...")
y_prediction = best_estimator.predict(x_test)

score = accuracy_score(y_prediction, y_test)
print(f"[INFO] Točnost: {score * 100:.2f}% primjera je točno kategorizirano")

# --- 6. Spremanje modela ---
pickle.dump(best_estimator, open('./model.p', 'wb'))
print("[INFO] Model je spremljen u 'model.p'")


# Rezultati izvođenja (primjer):
# [INFO] Početak učitavanja podataka...
# [INFO] Učitavam slike iz kategorije 'empty'...
# [INFO] Učitavam slike iz kategorije 'not_empty'...
# [INFO] Ukupno učitanih uzoraka: 6090
# [INFO] Dijelim podatke na train/test skup...
# [INFO] Train set: 4872 uzoraka, Test set: 1218 uzoraka
# [INFO] Pokrećem GridSearch za SVM...
# Fitting 5 folds for each of 12 candidates, totalling 60 fits
# [INFO] GridSearch završen!
# [INFO] Najbolji parametri: {'C': 10, 'gamma': 0.01}
# [INFO] Evaluiram model na testnom skupu...
# [INFO] Točnost: 100.00% primjera je točno kategorizirano
# [INFO] Model je spremljen u 'model.p'
