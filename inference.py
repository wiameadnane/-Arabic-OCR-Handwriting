import numpy as np
import cv2
import os
import re
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
import json

from tensorflow.keras.models import Model
from tensorflow.keras.layers import (
    Input, Conv2D, BatchNormalization, ReLU, Dropout, MaxPooling2D,
    DepthwiseConv2D, ZeroPadding2D, Reshape, Dense, Bidirectional,
    LSTM, Lambda
)
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras import backend as K
import tensorflow as tf
from tensorflow.keras.layers import Layer, Multiply, Permute, Lambda
import tensorflow.keras.backend as K
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from tensorflow.keras.utils import register_keras_serializable
import keras


# Register the loss function using tensorflow.keras.utils
@register_keras_serializable()
def ctc_loss(args):
    y_pred, labels, input_length, label_length = args
    y_pred = y_pred[:, 2:, :120]
    return K.ctc_batch_cost(labels, y_pred, input_length, label_length)

import json

# Get current script directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Load chars_to_codes
chars_to_codes_path = os.path.join(current_dir, "char_code_files", "chars_to_codes.json")
with open(chars_to_codes_path, 'r') as f:
    chars_to_codes = json.load(f)

# Load codes_to_chars (JSON stores keys as strings, convert back to int)
codes_to_chars_path = os.path.join(current_dir, "char_code_files", "codes_to_chars.json")
with open(codes_to_chars_path, 'r') as f:
    codes_to_chars = json.load(f)
    codes_to_chars = {int(k): v for k, v in codes_to_chars.items()}

latin_to_arabic = {
    "toB": "طـ", "haB": " حــ ", "aaElaM": "ـلاـ", "yaM": "ـيـ", "laA": "ل", "kaM": "ـقـ", "haA": "ح",
    "shB": "شـ", "shE": "ـش", "jaM": "ـجـ", "naM": "ـنـ", "baA": "ب", "faA": "ف", "heB": "هـ",
    "9A": "9", "saE": "ص", "jaB": "جـ", "heA": "ه", "shM": "ـشـ", "kaE": "ـق", "haMlaB": "لح",
    "taM": "ـتـ", "kaB": "قـ", "kaA": "ق", "maE": "ـم", "thM": "ـثـ", "dhE": "ـذ", "seM": "ـسـ",
    "zaM": "ـز",
    "aeElaB": "لأ",
    "waA": "و", "maA": "م", "saA": "ص", "baB": "بـ", "naE": "ـن",
    "seB": "سـ", "baM": "ـبـ",
    "0A": "0", "baE": "ـب", "raA": "ر", "khE": "ـخ", "taB": "تـ",
    "heE": "ـه",
    "deA": "ض",
    "jaMlaB": "لج", "toA": "ط", "keE": "ـك", "laB": "لـ", "laE": "ـل",
    "taA": "ت", "naA": "ن", "daA": "د",
    "hhA": "ء",
    "amA": "آ",
     "7A": "7",
    "ahElaB": "لإ",
    "raE": "ـر", "shA": "ش", "toE": "ـط", "maM": "ـمـ",
    "deB": "ض",
    "2A": "2",
    "khM": "ـخـ",
    "aeA": "أ", "saB": "صـ", "waE": "ـو", "faB": "فـ", "zaE": "ـز", "ayB": "عـ", "zaB": "ز",
    "ghB": "غـ",
    "aaElaB": "لا",
    "ayE": "ـع", "jaA": "ج", "aaA": "ا", "haM": "ـحـ", "saM": "ـصـ",
    "yaB": "يـ", "toM": "ـطـ", "maMlaB": "لم",
    "ahA": "إ",
    "jaE": "ـج",
    "alM": "ئ",
    "teA": "ة",
    "aaE": "ا",
    "laM": "ـلـ", "naB": "نـ", "haMmaMlaB": "لمح", "heM": "ـهـ", "faM": "ـفـ",
    "keM": "ـكـ", "ghM": "ـغـ",
    "8A": "8",
    "deM": "ـضـ",
    "ayA": "ع",
    "seE": "ـس", "teE": "ـة",
    "seA": "س",
    "6A": "6",
    "eeA": "ى",
    "yaE": "ـي", "faE": "ـف", "khA": "خ", "dhA": "ذ",
    "deE": "ض",
    "haE": "ـح",
    "ayM": "ـعـ",
    "maB": "مـ",
    "thA": "ث",
    "eeE": "ى",
    "1A": "1",
    "khB": "خـ", "keB": "كـ", "taE": "ـت", "yaA": "ي", "daE": "ـد", "thB": "ثـ", "khMlaB": "لخ",
    "zaA": "ز", "-": " "  # blank
}

def get_image(name, img_size=(100, 300)):
    img = cv2.imread(name, 0)
    img = cv2.resize(img, (img_size[1], img_size[0]), Image.LANCZOS)
    img = cv2.threshold(img, 255//2, 255, cv2.THRESH_BINARY)[1]
    img = cv2.bitwise_not(img)
    img = img.astype(np.float32) / 255.0
    return img[:, :, np.newaxis]

blank_index = 119

def ctc_decode(pred):
    out_best = np.argmax(pred, axis=2)[0]
    # print("argmax output:", out_best)

    out_best_filtered = [k for i, k in enumerate(out_best) if (k != blank_index and (i == 0 or k != out_best[i - 1]))]
    # print("Filtered output:", out_best_filtered)

    out_str = '|'.join([codes_to_chars.get(c, '') for c in out_best_filtered])
    # print("Predicted characters :", out_str)
    return out_str

custom_objects = {
    'ctc_loss': ctc_loss,
}

# Charger le modèle (format Keras V3)
model_path = os.path.join(current_dir, "ocr_model.keras")
model = keras.models.load_model(
    model_path,
    custom_objects=custom_objects,
    compile=False  # évite les erreurs liées à la loss custom
)
predict_model = Model(
    inputs=model.inputs[0],
    outputs=model.get_layer('softmax').output
)

predict_model = Model(inputs=model.inputs[0],  # First input = image
                      outputs=model.get_layer('softmax').output)


def infer_image(image_path):
    img = get_image(image_path)
    img = np.expand_dims(img, axis=0)  # shape: (1, 100, 300, 1)
    y_pred = predict_model.predict(img)
    y_pred = y_pred[:, :, :120]  # limit to valid characters

    decoded = ctc_decode(y_pred)  # Example output: "kaB|laB|yaE"
    print("greedy latin :", decoded)
    # Convert to Arabic using your dictionary
    tokens = decoded.split('|')
    arabic_chars = [latin_to_arabic.get(token, '?') for token in tokens]
    arabic_word = ''.join(arabic_chars)
    print("greedy arabic :", arabic_word)

    return arabic_word
