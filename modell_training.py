import tensorflow as tf
from tensorflow.keras import layers, models

# 📁 Pfad zum vorbereiteten Datensatz
datensatz_pfad = "vorbereitete_bilder"

# 📦 Datensatz laden
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
    datensatz_pfad,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(180, 180),
    batch_size=8
)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
    datensatz_pfad,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(180, 180),
    batch_size=8
)

# 🔍 Klassen extrahieren
klassen_namen = train_ds.class_names
print("🔍 Gefundene Klassen:", klassen_namen)

# 🚀 Pipeline optimieren
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.cache().shuffle(100).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

# 🧠 Modell definieren
modell = models.Sequential([
    layers.Input(shape=(180, 180, 3)),
    layers.Rescaling(1./255),
    layers.Conv2D(16, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Conv2D(32, 3, activation='relu'),
    layers.MaxPooling2D(),
    layers.Flatten(),
    layers.Dense(64, activation='relu'),
    layers.Dense(len(klassen_namen), activation='softmax')
])

modell.compile(optimizer='adam',
               loss='sparse_categorical_crossentropy',
               metrics=['accuracy'])

# 🎓 Training starten
modell.fit(train_ds, validation_data=val_ds, epochs=10)

# 💾 Modell speichern
modell.save("papier_klassifizierer.keras")
print("✅ Modell wurde gespeichert unter: papier_klassifizierer.keras")
