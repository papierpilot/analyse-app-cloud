import streamlit as st
import cv2
import numpy as np
from pathlib import Path
from PIL import Image

# 📁 Uploadordner simulieren
UPLOAD_ORDNER = Path("upload")
UPLOAD_ORDNER.mkdir(exist_ok=True)

# 🎨 Farbbereiche (HSV)
BRAUN_MIN = np.array([10, 50, 50])
BRAUN_MAX = np.array([30, 255, 255])
WEISS_MIN = np.array([0, 0, 180])
WEISS_MAX = np.array([180, 50, 255])
ROI_MIN = np.array([0, 0, 60])
ROI_MAX = np.array([180, 80, 255])

# 🔍 Analysefunktion
def analysiere_bild_array(img_array):
    img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

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

# 🖼️ Streamlit UI
st.set_page_config(page_title="📦 Farb-Analyse", layout="centered")
st.title("🧪 Farb-Analyse von Papierladungen")
st.write("Lade bis zu 5 Bilder hoch, um den Anteil von **Karton** und **Zeitung** zu berechnen.")

bilder = st.file_uploader("📷 Lade bis zu 5 Bilder hoch", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if bilder and len(bilder) > 0:
    gesamt_braun = 0
    gesamt_weiss = 0

    st.success(f"{len(bilder)} Bilder erhalten – starte Analyse...")

    for bild in bilder:
        img = Image.open(bild).convert("RGB")
        img_array = np.array(img)

        b, w = analysiere_bild_array(img_array)
        gesamt_braun += b
        gesamt_weiss += w

        st.image(img, caption=f"Karton: {b:.1f}% | Zeitung: {w:.1f}%", use_column_width=True)

    mittel_braun = gesamt_braun / len(bilder)
    mittel_weiss = gesamt_weiss / len(bilder)

    st.markdown("### 📊 Durchschnittswerte:")
    st.write(f"🟫 **Karton**: {mittel_braun:.1f} %")
    st.write(f"⬜ **Zeitung**: {mittel_weiss:.1f} %")

    if mittel_braun >= 60:
        st.success("✅ Empfehlung: **Verpressen**")
    else:
        st.warning("⚠️ Empfehlung: **Sortieren**")
else:
    st.info("Bitte lade mindestens ein Bild hoch.")
