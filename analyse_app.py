import streamlit as st
import numpy as np
import cv2
from PIL import Image
from tensorflow.keras.models import load_model

# Modell laden
modell = load_model("papier_klassifizierer.h5")

# Bildgröße
BILD_GROESSE = (180, 180)

# Streamlit Konfiguration
st.set_page_config(page_title="📱 Mobile Papier-Analyse", layout="centered")
st.title("📦📸 Papieranalyse mobil")
st.write("Mache 5 Bilder der Papierladung und erhalte eine Empfehlung.")

# Bilder vorbereiten
def vorbereiten(img):
    img = img.resize(BILD_GROESSE)
    img_array = np.expand_dims(np.array(img) / 255.0, axis=0)
    return img_array

# Vorhersage
def vorhersage(img):
    array = vorbereiten(img)
    prediction = modell.predict(array)[0]
    klassen = ["gemischt", "karton", "zeitung"]
    index = np.argmax(prediction)
    return klassen[index], prediction[index] * 100

# Upload
uploaded = st.file_uploader(
    "📷 Bitte genau 5 Bilder aufnehmen oder hochladen",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Analyse
if uploaded and len(uploaded) == 5:
    st.success("5 Bilder erhalten – starte Analyse...")

    ergebnisse = {"karton": 0, "zeitung": 0, "gemischt": 0}

    for bild in uploaded:
        img = Image.open(bild).convert("RGB")
        klasse, wahrscheinlichkeit = vorhersage(img)
        ergebnisse[klasse] += 1

    st.markdown("### 📊 Analyse-Ergebnisse:")
    for klasse in ergebnisse:
        st.write(f"🔹 {klasse.capitalize()}: **{ergebnisse[klasse]} von 5 Bildern**")

    # Entscheidung
    if ergebnisse["karton"] >= 3:  # also 3 oder mehr von 5 → >= 60%
        st.success("✅ Empfehlung: **Verpressen**")
    else:
        st.warning("⚠️ Empfehlung: **Sortieren**")
else:
    st.info("Bitte lade genau 5 Bilder hoch, um die Analyse zu starten.")
