# ==============================================================================
# GOOGLE COLAB TRAINING SCRIPT — STEP 3: AGGRESSIVE DATA AUGMENTATION RETRAIN
# ==============================================================================
# Paste or upload this notebook into Google Colab (with GPU T4 acceleration enabled).
# 
# Step 3 Goals:
# 1. Base dataset: Same PlantVillage dataset (39 classes).
# 2. Aggressive Training Augmentations:
#    - RandomFlip ("horizontal_and_vertical")
#    - RandomRotation (0.2 -> ~10-15° variations)
#    - RandomZoom (0.2 -> 20% zoom variation)
#    - RandomBrightness (factor=0.2 -> ±20% brightness)
#    - RandomContrast (factor=0.2 -> ±20% contrast)
#    - GaussianNoise (0.05 -> simulates sensor/focus blur)
# 3. Transfer Learning on MobileNetV2 (Frozen Base -> Fine-Tuning Phase).
# 4. Exports artifact: mobilenet_v2_plantvillage_step3.keras
# ==============================================================================

# CELL 1: Setup & Dataset Download (Run in Colab)
"""
!pip install -q kaggle
import os

# Download PlantVillage dataset (if using Kaggle API or direct zip link)
# Option A: Upload your kaggle.json or download plantvillage dataset zip
!npx -y kaggle datasets download -d emmarex/plantdisease -p dataset_temp --unzip
"""

# CELL 2: Step 3 Training Pipeline Code
import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# Parameters
BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)
EPOCHS_FREEZE = 8
EPOCHS_FINE_TUNE = 12
LEARNING_RATE_INITIAL = 1e-3
LEARNING_RATE_FINE_TUNE = 1e-5
MODEL_SAVE_PATH = "mobilenet_v2_plantvillage_step3.keras"

# 1. Define Step 3 Aggressive Data Augmentation Pipeline
data_augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal_and_vertical"),
    layers.RandomRotation(0.2),
    layers.RandomZoom(0.2),
    layers.RandomBrightness(factor=0.2),
    layers.RandomContrast(factor=0.2),
    layers.GaussianNoise(0.05),
], name="step3_aggressive_augmentation")

print("✅ Aggressive Data Augmentation Pipeline Created:")
for layer in data_augmentation.layers:
    print(f"   • {layer.name}")

# 2. Load PlantVillage Dataset
# Update 'DATASET_PATH' to your extracted PlantVillage dataset folder on Colab
DATASET_PATH = "PlantVillage" # or "dataset_temp/PlantVillage"

print(f"\n📂 Loading dataset from: {DATASET_PATH}...")
train_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    DATASET_PATH,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
num_classes = len(class_names)
print(f"\n✅ Successfully loaded {num_classes} plant-disease classes.")

# Optimize data loading pipeline
AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

# 3. Build MobileNetV2 Architecture
inputs = layers.Input(shape=(224, 224, 3))
x = data_augmentation(inputs)
x = preprocess_input(x)

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights='imagenet'
)
base_model.trainable = False  # Freeze base backbone initially

x = base_model(x, training=False)
x = layers.GlobalAveragePooling2D()(x)
x = layers.Dropout(0.3)(x)
outputs = layers.Dense(num_classes, activation='softmax')(x)

model = models.Model(inputs=inputs, outputs=outputs, name="MobileNetV2_Step3")

# 4. Phase 1: Train Classification Head (Base Frozen)
print("\n🚀 PHASE 1: Training Classification Head (Backbone Frozen)...")
model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_INITIAL),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks_p1 = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
]

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS_FREEZE,
    callbacks=callbacks_p1
)

# 5. Phase 2: Fine-Tuning Top Backbone Layers
print("\n🔓 PHASE 2: Fine-Tuning MobileNetV2 Top Backbone Layers...")
base_model.trainable = True

# Freeze first 100 layers out of 154
fine_tune_at = 100
for layer in base_model.layers[:fine_tune_at]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_FINE_TUNE),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

callbacks_p2 = [
    tf.keras.callbacks.ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True),
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)
]

model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS_FINE_TUNE,
    callbacks=callbacks_p2
)

# 6. Save Final Model Artifact
model.save(MODEL_SAVE_PATH)
print(f"\n🎉 TRAINING COMPLETE! Model artifact saved as: '{MODEL_SAVE_PATH}'")
print(f"👉 Download '{MODEL_SAVE_PATH}' from Colab and place it in your local 'models_assets/' directory!")
