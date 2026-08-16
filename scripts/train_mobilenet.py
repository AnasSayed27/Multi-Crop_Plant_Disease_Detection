import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import classification_report, confusion_matrix, precision_recall_fscore_support

# ---------------------------------------------------------
# Configuration & Constants
# ---------------------------------------------------------
SEED = 42
IMAGE_SIZE = (224, 224)
BATCH_SIZE = 32
DATASET_DIR = r"d:\Projects\AI-ML Portfolio\Potato_disease\Dataset\Plant_leave_diseases_dataset_without_augmentation"
MODELS_ASSETS_DIR = "models_assets"
MODEL_SAVE_PATH = os.path.join(MODELS_ASSETS_DIR, "mobilenet_v2_plantvillage.keras")
CLASS_NAMES_PATH = os.path.join(MODELS_ASSETS_DIR, "class_names.json")
METRICS_SAVE_PATH = os.path.join(MODELS_ASSETS_DIR, "evaluation_metrics.json")

os.makedirs(MODELS_ASSETS_DIR, exist_ok=True)
tf.keras.utils.set_random_seed(SEED)

def main():
    print("=" * 70)
    print(" STEP 1 — ML TRAINING PIPELINE (MobileNetV2 Transfer Learning) ")
    print("=" * 70)

    # ---------------------------------------------------------
    # 1. Native Keras Three-Way Split (Train 70% / Val 15% / Test 15%)
    # ---------------------------------------------------------
    print("\n--- Step 1.1: Creating 3-Way Native Keras Dataset Split ---")
    raw_train_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.30,
        subset="training",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    temp_ds = tf.keras.utils.image_dataset_from_directory(
        DATASET_DIR,
        validation_split=0.30,
        subset="validation",
        seed=SEED,
        image_size=IMAGE_SIZE,
        batch_size=BATCH_SIZE
    )

    class_names = raw_train_ds.class_names
    num_classes = len(class_names)
    print(f"\nDiscovered {num_classes} dataset classes directly from directory.")

    # Export class_names.json directly from dataset
    with open(CLASS_NAMES_PATH, "w", encoding="utf-8") as f:
        json.dump(class_names, f, indent=2)
    print(f"Saved class names to '{CLASS_NAMES_PATH}'")

    # Split temp_ds (30%) equally into Val (15%) and Test (15%)
    temp_batches = tf.data.experimental.cardinality(temp_ds).numpy()
    val_batches = temp_batches // 2

    val_ds = temp_ds.take(val_batches)
    test_ds = temp_ds.skip(val_batches)

    print(f"Dataset Cardinality (Batches of {BATCH_SIZE}):")
    print(f"  Train Batches: {tf.data.experimental.cardinality(raw_train_ds).numpy()}")
    print(f"  Val Batches:   {tf.data.experimental.cardinality(val_ds).numpy()}")
    print(f"  Test Batches:  {tf.data.experimental.cardinality(test_ds).numpy()}")

    # Apply .cache() and .prefetch() to all three datasets
    train_ds = raw_train_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    val_ds = val_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)
    test_ds = test_ds.cache().prefetch(buffer_size=tf.data.AUTOTUNE)

    # ---------------------------------------------------------
    # 2. Class Imbalance Handling (Balanced Class Weights)
    # ---------------------------------------------------------
    print("\n--- Step 1.2: Computing Balanced Class Weights ---")
    class_counts = []
    for c_name in class_names:
        c_dir = os.path.join(DATASET_DIR, c_name)
        cnt = len([f for f in os.listdir(c_dir) if os.path.isfile(os.path.join(c_dir, f))])
        class_counts.append(max(1, cnt))

    total_samples = sum(class_counts)
    class_weight_dict = {}
    for i, count in enumerate(class_counts):
        class_weight_dict[i] = total_samples / (num_classes * count)
    print(f"Computed balanced class weights for {len(class_weight_dict)} classes without RAM overhead.")

    # ---------------------------------------------------------
    # 3. MobileNetV2 Architecture & Exclusive Preprocessing
    # ---------------------------------------------------------
    print("\n--- Step 1.3: Building MobileNetV2 Model Architecture ---")
    inputs = layers.Input(shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3), name="input_image")

    # Data Augmentation (training mode only)
    x = layers.RandomFlip("horizontal_and_vertical", seed=SEED)(inputs)
    x = layers.RandomRotation(0.2, seed=SEED)(x)
    x = layers.RandomZoom(0.2, seed=SEED)(x)

    # EXCLUSIVE MobileNetV2 Preprocessing Layer (Applied EXACTLY ONCE)
    x = layers.Lambda(
        tf.keras.applications.mobilenet_v2.preprocess_input,
        name="mobilenet_v2_preprocess"
    )(x)

    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False  # Freeze base in Phase 1

    x = base_model(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.BatchNormalization()(x)
    x = layers.Dropout(0.3, seed=SEED)(x)
    x = layers.Dense(128, activation="relu")(x)
    outputs = layers.Dense(num_classes, activation="softmax", name="predictions")(x)

    model = models.Model(inputs=inputs, outputs=outputs, name="MobileNetV2_PlantVillage")

    # ---------------------------------------------------------
    # 4. Phase 1: Train Classification Head
    # ---------------------------------------------------------
    print("\n--- Phase 1: Training Classification Head (10 Epochs) ---")
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name="top_3_accuracy")]
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=10,
        class_weight=class_weight_dict,
        verbose=2
    )

    # ---------------------------------------------------------
    # 5. Phase 2: Fine-Tuning Top Base Layers
    # ---------------------------------------------------------
    print("\n--- Phase 2: Fine-Tuning Top MobileNetV2 Layers (5 Epochs) ---")
    base_model.trainable = True
    for layer in base_model.layers[:-30]:
        layer.trainable = False

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy", tf.keras.metrics.SparseTopKCategoricalAccuracy(k=3, name="top_3_accuracy")]
    )

    model.fit(
        train_ds,
        validation_data=val_ds,
        epochs=5,
        class_weight=class_weight_dict,
        verbose=2
    )

    # ---------------------------------------------------------
    # 6. Evaluation on Held-Out Test Set (test_ds)
    # ---------------------------------------------------------
    print("\n--- Step 1.4: Evaluating Model on Held-Out Test Set ---")
    test_loss, test_acc, test_top3_acc = model.evaluate(test_ds, verbose=0)

    # Predictions for Precision, Recall, F1, and Confusion Matrix
    y_test_list = []
    for _, labels in test_ds:
        y_test_list.extend(labels.numpy())
    y_test = np.array(y_test_list)

    test_preds = model.predict(test_ds, verbose=0)
    y_pred = np.argmax(test_preds, axis=1)

    precision, recall, f1, _ = precision_recall_fscore_support(y_test, y_pred, average="weighted")
    cm = confusion_matrix(y_test, y_pred).tolist()

    print("\n" + "=" * 60)
    print(" FINAL HELD-OUT TEST EVALUATION METRICS ")
    print("=" * 60)
    print(f" Test Loss:           {test_loss:.4f}")
    print(f" Test Accuracy:       {test_acc * 100:.2f}%")
    print(f" Test Top-3 Accuracy: {test_top3_acc * 100:.2f}%")
    print(f" Weighted Precision:  {precision:.4f}")
    print(f" Weighted Recall:     {recall:.4f}")
    print(f" Weighted F1-Score:   {f1:.4f}")
    print("=" * 60)

    metrics_payload = {
        "test_loss": round(float(test_loss), 4),
        "test_accuracy": round(float(test_acc * 100.0), 2),
        "test_top3_accuracy": round(float(test_top3_acc * 100.0), 2),
        "weighted_precision": round(float(precision), 4),
        "weighted_recall": round(float(recall), 4),
        "weighted_f1_score": round(float(f1), 4),
        "confusion_matrix": cm
    }

    with open(METRICS_SAVE_PATH, "w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)
    print(f"Saved evaluation metrics to '{METRICS_SAVE_PATH}'")

    # ---------------------------------------------------------
    # 7. Save Keras Model Artifact
    # ---------------------------------------------------------
    model.save(MODEL_SAVE_PATH)
    print(f"\nModel successfully saved to '{MODEL_SAVE_PATH}'")

if __name__ == "__main__":
    main()
