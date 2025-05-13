import os
import shutil
from PIL import Image
from tqdm import tqdm

# ⚙️ Konfiguration
DATENQUELLE = "Trainingsbilder 12.05.2025"
ZIELORDNER = "vorbereitete_bilder"
BILDGROESSE = (180, 180)

# 📁 Zielordner leeren oder anlegen
if os.path.exists(ZIELORDNER):
    shutil.rmtree(ZIELORDNER)
os.makedirs(ZIELORDNER)

# 🔁 Klassenordner verarbeiten
klassen = os.listdir(DATENQUELLE)

for klasse in klassen:
    ordner = os.path.join(DATENQUELLE, klasse)
    bilder = [os.path.join(ordner, f) for f in os.listdir(ordner)
              if f.lower().endswith((".jpg", ".jpeg", ".png"))]

    ziel_klasse_ordner = os.path.join(ZIELORDNER, klasse)
    os.makedirs(ziel_klasse_ordner, exist_ok=True)

    print(f"📂 Bearbeite Klasse: {klasse} ({len(bilder)} Bilder)")
    for i, bildpfad in enumerate(tqdm(bilder, desc=f"🔄 Verarbeite {klasse}")):
        try:
            img = Image.open(bildpfad).convert("RGB")
            img = img.resize(BILDGROESSE)
            ziel_pfad = os.path.join(ziel_klasse_ordner, f"{klasse}_{i+1:04d}.jpg")
            img.save(ziel_pfad)
        except Exception as e:
            print(f"⚠️ Fehler bei {bildpfad}: {e}")

print("\n✅ Alle Bilder wurden erfolgreich vorbereitet.")
