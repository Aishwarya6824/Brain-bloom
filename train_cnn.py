# train_cnn.py
import os, json
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import layers, models
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

DATA_DIR = "data/images"   # folder with subfolders per class
IMG_SIZE = (160,160)
BATCH = 32
EPOCHS = 12
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def make_generators():
    datagen = ImageDataGenerator(rescale=1./255, validation_split=0.2,
                                 rotation_range=15, width_shift_range=0.1,
                                 height_shift_range=0.1, horizontal_flip=True)
    train = datagen.flow_from_directory(DATA_DIR, target_size=IMG_SIZE,
                                        batch_size=BATCH, subset='training')
    val = datagen.flow_from_directory(DATA_DIR, target_size=IMG_SIZE,
                                      batch_size=BATCH, subset='validation')
    return train, val

def build_model(num_classes):
    base = MobileNetV2(input_shape=(*IMG_SIZE,3), include_top=False, weights='imagenet', pooling='avg')
    base.trainable = False
    inp = layers.Input(shape=(*IMG_SIZE,3))
    x = base(inp, training=False)
    x = layers.Dropout(0.3)(x)
    x = layers.Dense(128, activation='relu')(x)
    out = layers.Dense(num_classes, activation='softmax')(x)
    model = models.Model(inputs=inp, outputs=out)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train():
    train_gen, val_gen = make_generators()
    model = build_model(train_gen.num_classes)
    cp = ModelCheckpoint(os.path.join(MODEL_DIR,"cnn_model.h5"), save_best_only=True, monitor='val_accuracy')
    es = EarlyStopping(patience=4, restore_best_weights=True, monitor='val_accuracy')
    model.fit(train_gen, validation_data=val_gen, epochs=EPOCHS, callbacks=[cp, es])
    # Save mapping (class_indices gives name->index)
    mapping = train_gen.class_indices
    # convert to int->name mapping for convenience
    inv_map = {str(v): k for k, v in mapping.items()}
    with open(os.path.join(MODEL_DIR, "class_mapping.json"), "w") as f:
        json.dump(inv_map, f)
    print("Training finished. Model and mapping saved to 'models/'")

if __name__ == "__main__":
    train()
