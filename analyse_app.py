import streamlit as st
import numpy as np
import cv2
from PIL import Image

# Farbdefinitionen im HSV
BRAUN_MIN = np.array([10, 50, 50])
BRAUN_MAX = np.array([30, 255, 255])

WEISS_MIN = np.array([0, 0, 180])
WEISS_MAX = np.array([180, 50, 255])

ROI_MIN = np.array([0, 0, 60])
ROI_MAX = np.array([180, 80, 255])

# Streamlit UI
st.set_page_config(page_title="📦📄 Farb-Analyse mobil", layout="centered")
st.title("📦📄 Farb-Analyse: Karton vs. Zeitung")
st.write("Lade 5 Bilder hoch. Das System analysiert den Farbanteil für Kartonage (braun) und Zeitung (weiß).")

# 🔍 Bildanalyse
def analysiere_bild(img: Image.Image):
    bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)

    roi_mask = cv2.inRange(hsv, ROI_MIN, ROI_MAX)
    braun = cv2.inRange(hsv, BRAUN_MIN, BRAUN_MAX)
    weiss = cv2.inRange(hsv, WEISS_MIN, WEISS_MAX)

    braun_im_roi = cv2.bitwise_and(braun, roi_mask)
    weiss_im_roi = cv2.bitwise_and(weiss, roi_mask)

    gesamt = np.count_nonzero(roi_mask)
    braun_px = np.count_nonzero(braun_im_roi)
    weiss_px = np.count_nonzero(weiss_im_roi)

    relevant = braun_px + weiss_px
    if relevant == 0:
        return 0.0, 0.0

    braun_prozent = braun_px / relevant * 100
    weiss_prozent = weiss_px / relevant * 100
    return braun_prozent, weiss_prozent

# 📤 Upload
uploaded = st.file_uploader(
    "📷 Bitte genau 5 Bilder hochladen",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

# Analyse starten
if uploaded and len(uploaded) == 5:
    st.success("5 Bilder erhalten – starte Farb-Analyse...")

    gesamt_braun = 0
    gesamt_weiss = 0

    for bild in uploaded:
        img = Image.open(bild).convert("RGB")
        braun, weiss = analysiere_bild(img)
        gesamt_braun += braun
        gesamt_weiss += weiss

    mittel_braun = gesamt_braun / 5
    mittel_weiss = gesamt_weiss / 5

    st.markdown("### 📊 Durchschnittswerte:")
    st.write(f"🟫 **Kartonage (braun)**: {mittel_braun:.2f} %")
    st.write(f"⬜ **Zeitung (weiß)**: {mittel_weiss:.2f} %")

    # Empfehlung
    if mittel_braun >= 60:
        st.success("✅ Empfehlung: **Verpressen** (über 60 % Karton)")
    else:
        st.warning("⚠️ Empfehlung: **Sortieren** (unter 60 % Karton)")
else:
    st.info("Bitte lade genau 5 Bilder hoch.")
