import streamlit as st
import numpy as np
import cv2
from PIL import Image
import matplotlib.pyplot as plt

# App-Einstellungen
st.set_page_config(page_title="📱 Mobile Papier-Analyse", layout="centered")
st.title("📦📸 Papieranalyse mobil")
st.write("Mache 3 Bilder der Papierladung und erhalte eine Empfehlung.")

# Schwellenwerte
BRAUN_MIN = np.array([10, 50, 50])
BRAUN_MAX = np.array([30, 255, 255])
WEISS_MIN = np.array([0, 0, 180])
WEISS_MAX = np.array([180, 50, 255])
ROI_MIN = np.array([0, 0, 60])
ROI_MAX = np.array([180, 80, 255])

# Analysefunktion
def analysiere_bild(uploaded_file):
    image = Image.open(uploaded_file).convert("RGB")
    img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    roi = cv2.inRange(hsv, ROI_MIN, ROI_MAX)
    braun = cv2.inRange(hsv, BRAUN_MIN, BRAUN_MAX)
    weiss = cv2.inRange(hsv, WEISS_MIN, WEISS_MAX)

    braun_im_roi = cv2.bitwise_and(braun, roi)
    weiss_im_roi = cv2.bitwise_and(weiss, roi)

    braun_px = np.count_nonzero(braun_im_roi)
    weiss_px = np.count_nonzero(weiss_im_roi)
    relevant = braun_px + weiss_px

    if relevant == 0:
        return 0, 0
    return braun_px / relevant * 100, weiss_px / relevant * 100

# Upload-Feld – exakt 3 Bilder!
uploaded = st.file_uploader(
    "📷 Bitte genau 3 Bilder aufnehmen oder hochladen", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Auswertung
if uploaded and len(uploaded) == 3:
    st.success("3 Bilder erhalten – starte Analyse...")

    gesamt_braun = 0
    gesamt_weiss = 0

    for file in uploaded:
        braun, weiss = analysiere_bild(file)
        gesamt_braun += braun
        gesamt_weiss += weiss

    mittel_braun = gesamt_braun / 3
    mittel_weiss = gesamt_weiss / 3

    st.markdown("### 📊 Durchschnittswerte")
    st.write(f"🟫 Kartonage: **{mittel_braun:.2f}%**")
    st.write(f"⚪ Zeitung: **{mittel_weiss:.2f}%**")

    if mittel_braun > 70:
        st.success("✅ Empfehlung: **Verpressen**")
    else:
        st.warning("⚠️ Empfehlung: **Sortieren**")

else:
    st.info("Bitte lade genau 3 Bilder hoch, um die Analyse zu starten.")
