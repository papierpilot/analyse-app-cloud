import streamlit as st
import cv2
import numpy as np
from pathlib import Path

st.set_page_config(page_title="📦 Farb-Analyse", layout="centered")
st.title("📷 Klassische Papieranalyse")

BILDER_ORDNER = Path("bilder")

BRAUN_MIN = np.array([10, 50, 50])
BRAUN_MAX = np.array([30, 255, 255])
WEISS_MIN = np.array([0, 0, 180])
WEISS_MAX = np.array([180, 50, 255])
ROI_MIN = np.array([0, 0, 60])
ROI_MAX = np.array([180, 80, 255])

def analysiere_bild(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
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
    return braun_px / relevant * 100, weiss_px / relevant * 100

uploaded = st.file_uploader("Lade Bilder hoch", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if uploaded:
    gesamt_braun = 0
    gesamt_weiss = 0

    for bild in uploaded:
        img = cv2.imdecode(np.frombuffer(bild.read(), np.uint8), 1)
        b, w = analysiere_bild(img)
        gesamt_braun += b
        gesamt_weiss += w

    anzahl = len(uploaded)
    if anzahl > 0:
        st.markdown("### 📊 Durchschnittswerte:")
        st.write(f"🟫 Karton: **{gesamt_braun / anzahl:.1f} %**")
        st.write(f"📄 Zeitung: **{gesamt_weiss / anzahl:.1f} %**")
else:
    st.info("Bitte lade mindestens 1 Bild hoch.")
