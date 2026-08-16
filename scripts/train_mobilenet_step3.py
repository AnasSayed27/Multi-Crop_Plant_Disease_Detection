"""
==============================================================================
STEP 3: MOBILE NET V2 TRAINING WITH AGGRESSIVE DATA AUGMENTATION
==============================================================================
This script is designed for Google Colab (GPU accelerated) or local GPU training.
It trains MobileNetV2 on the PlantVillage dataset with aggressive real-world 
augmentation (Color Jitter, Brightness, Contrast, Random Rotation/Zoom/Flip, Gaussian Noise)
to teach the model spatial and lighting invariances for field photographs.

Output Model Artifact: mobilenet_v2_plantvillage_step3.keras
==============================================================================
"""

import os
import json
import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ---------------------------------------------------------
# Configuration Parameters
# ---------------------------------------------------------
BATCH_SIZE = 32
IMAGE_SIZE = (224, 224)
EPOCHS_FREEZE = 8
EPOCHS_FINE_TUNE = 12
LEARNING_RATE_INITIAL = 1e-3
LEARNING_RATE_FINE_TUNE = 1e-5
MODEL_SAVE_PATH = "mobilenet_v2_plantvillage_step3.keras"
CLASS_NAMES_SAVE_PATH = "class_names_step3.json"

def build_augmentation_pipeline():
    """
    Step 3 Aggressive Real-World Augmentation Pipeline.
    Teaches the model:
    1. Spatial Invariances (Flips, 20% Rotations, 20% Zooms)
    2. Lighting & Color Invariances (20% Brightness, 20% Contrast variation)
    3. Camera/Sensor Noise Invariances (Gaussian Noise)
    """
    data_augmentation = tf.keras.Sequential([
        layers.RandomFlip("horizontal_and_vertical"),
        layers.RandomRotation(0.2),
        layers.RandomZoom(0.2),
        layers.RandomBrightness(factor=0.2),
        layers.RandomContrast(factor=0.2),
        layers.GaussianNoise(0.05), # Simulates camera sensor noise
    ], name="step3_aggressive_augmentation")
    return data_augmentation

def build_mobilenet_v2_model(num_classes):
    """
    Builds MobileNetV2 transfer learning model with preprocess_input and classification head.
    """
    augmentation = build_augmentation_pipeline()
    
    inputs = layers.Input(shape=(224, 224, 3))
    x = augmentation(inputs)
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
    
    model = models.Model(inputs=inputs, outputs=outputs, name="MobileNetV2_Step3_Augmented")
    return model, base_model

def train_step3_model(dataset_dir="plantvillage_dataset"):
    print("=" * 75)
    print(" STEP 3: TRAINING MOBILENET V2 WITH AGGRESSIVE DATA AUGMENTATION ")
    print("=" * 75)

    if not os.path.exists(dataset_dir):
        raise FileNotFoundError(
            f"Dataset directory '{dataset_dir}' not found. "
            "Please ensure PlantVillage dataset folder is present."
        )

    # 1. Load Training & Validation Datasets
    print("\n📂 Loading PlantVillage image dataset...")
    train_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="training",
        seed=123,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    val_ds = tf.keras.utils.image_dataset_from_directory(
        dataset_dir,
        validation_split=0.2,
        subset="validation",
        seed=123,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    class_names = train_ds.class_names
    num_classes = len(class_names)
    print(f"✅ Found {num_classes} plant-disease classes.")

    # Save class names JSON
    with open(CLASS_NAMES_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)

    # Prefetch dataset for GPU training performance
    AUTOTUNE = tf.data.AUTOTUNE
    train_ds = train_ds.prefetch(buffer_size=AUTOTUNE)
    val_ds = val_ds.prefetch(buffer_size=AUTOTUNE)

    # 2. Build Model
    model, base_model = build_mobilenet_v2_model(num_classes)
    model.summary()

    # 3. Phase 1: Train Classification Head (Base Frozen)
    print("\n🚀 Phase 1: Training Classification Head (Base Frozen)...")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_INITIAL),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks_phase1 = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
    ]

    history_p1 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_FREEZE,
        callbacks=callbacks_phase1
    )

    # 4. Phase 2: Fine-Tuning Top Backbone Layers
    print("\n🔓 Phase 2: Fine-Tuning Top Layers of MobileNetV2 Backbone...")
    base_model.trainable = True
    
    # Freeze the first 100 layers out of 154 layers in MobileNetV2
    fine_tune_at = 100
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE_FINE_TUNE),
        loss='sparse_categorical_crossentropy',
        metrics=['accuracy']
    )

    callbacks_phase2 = [
        tf.keras.callbacks.ModelCheckpoint(MODEL_SAVE_PATH, monitor='val_accuracy', save_best_only=True),
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=4, restore_best_weights=True)
    ]

    history_p2 = model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=EPOCHS_FINE_TUNE,
        callbacks=callbacks_phase2
    )

    # Save final model
    model.save(MODEL_SAVE_PATH)
    print(f"\n🎉 Step 3 Training Complete! Saved model artifact: '{MODEL_SAVE_PATH}'")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Train Step 3 MobileNetV2 with Aggressive Augmentation")
    parser.add_argument("--data-dir", type=str, default="plantvillage_dataset", help="Path to PlantVillage dataset folder")
    args = parser.parse_args()
    
    train_step3_model(dataset_dir=args.data_dir)
