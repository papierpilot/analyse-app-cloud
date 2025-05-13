import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from PIL import Image

# Farbschwellenwerte
BRAUN_MIN = np.array([10, 50, 50])
BRAUN_MAX = np.array([30, 255, 255])
WEISS_MIN = np.array([0, 0, 180])
WEISS_MAX = np.array([180, 50, 255])
ROI_MIN = np.array([0, 0, 60])
ROI_MAX = np.array([180, 80, 255])

# Auswertung eines Bildes
def analysiere_bild(uploaded_file):
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    bild = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    hsv = cv2.cvtColor(bild, cv2.COLOR_BGR2HSV)

    roi_mask = cv2.inRange(hsv, ROI_MIN, ROI_MAX)
    braun = cv2.inRange(hsv, BRAUN_MIN, BRAUN_MAX)
    weiss = cv2.inRange(hsv, WEISS_MIN, WEISS_MAX)

    braun_im_haufen = cv2.bitwise_and(braun, roi_mask)
    weiss_im_haufen = cv2.bitwise_and(weiss, roi_mask)

    gesamt = np.count_nonzero(roi_mask)
    braun_px = np.count_nonzero(braun_im_haufen)
    weiss_px = np.count_nonzero(weiss_im_haufen)

    relevant = braun_px + weiss_px
    if relevant == 0:
        return 0, 0

    braun_quote = braun_px / relevant * 100
    weiss_quote = weiss_px / relevant * 100
    return braun_quote, weiss_quote

# Streamlit UI
st.set_page_config(page_title="📦 Farbwert-Analyse", layout="centered")
st.title("🧪 Klassische Farbwert-Analyse")
st.write("Analysiere den Farbanteil von Karton (braun) und Zeitung (weiß).")

uploaded_files = st.file_uploader("📷 Bitte 1–5 Bilder hochladen", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded_files:
    gesamt_braun = 0
    gesamt_weiss = 0

    for file in uploaded_files:
        braun, weiss = analysiere_bild(file)
        gesamt_braun += braun
        gesamt_weiss += weiss
        st.write(f"📸 **{file.name}** — 🟫 Karton: {braun:.1f} % | 📰 Zeitung: {weiss:.1f} %")

    # Durchschnitt berechnen
    anzahl = len(uploaded_files)
    mittel_braun = gesamt_braun / anzahl
    mittel_weiss = gesamt_weiss / anzahl

    st.markdown("### 📊 Durchschnitt über alle Bilder:")
    st.success(f"🟫 **Karton (braun): {mittel_braun:.1f} %**")
    st.info(f"📰 **Zeitung (weiß): {mittel_weiss:.1f} %**")

    if mittel_braun >= 60:
        st.success("✅ Empfehlung: **Verpressen**")
    else:
        st.warning("⚠️ Empfehlung: **Sortieren**")
else:
    st.info("Lade bitte mindestens ein Bild hoch.")
