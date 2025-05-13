import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import os

# 🔁 Klassennamen aus Training
klassen_namen = ["gemischt", "karton", "zeitung"]

# 🧠 Modell laden
modell = tf.keras.models.load_model("PapierDataset/papier_klassifizierer.h5")

# 📷 Pfad zum Testbild (z. B. aus einem der Ordner)
bild_pfad = "vorbereitete_bilder/karton/karton_0001.jpg"  # <- hier ggf. anpassen

# 🖼️ Bild vorbereiten
img = image.load_img(bild_pfad, target_size=(180, 180))
img_array = image.img_to_array(img)
img_array = tf.expand_dims(img_array, 0)  # Batch-Dimension hinzufügen

# 🤖 Vorhersage
vorhersage = modell.predict(img_array)
klasse_index = np.argmax(vorhersage[0])
wahrscheinlichkeit = np.max(vorhersage[0])

# 📣 Ausgabe
print(f"🔎 Vorhersage: {klassen_namen[klasse_index]}")
print(f"📊 Wahrscheinlichkeit: {wahrscheinlichkeit * 100:.2f}%")
