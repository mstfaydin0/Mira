# python detect_mask_image.py --image image.png
import os
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import argparse
import cv2
import time  # time modülü ile bekletmeler yapıyoruz
from pygame import mixer  # mp3 dosyalarını oynatmak için kullanıyoruz

mixer.init()

takemask = r"src\audio\take-mask.mp3"
thxformask = r"src\audio\thxformask.mp3"

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
ap.add_argument("-f", "--face", type=str,
                default="face_detector",
                help="path to face detector model directory")
ap.add_argument("-m", "--model", type=str,
                default="face_detector\\mask_detector.model",
                help="path to trained face mask detector model")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
                help="minimum probability to filter weak detections")
args = vars(ap.parse_args())
# yüz tanıma modelimizi yüklüyoruz
prototxtPath = os.path.sep.join([args["face"], "deploy.prototxt"])
weightsPath = os.path.sep.join([args["face"],
                                "res10_300x300_ssd_iter_140000.caffemodel"])
net = cv2.dnn.readNet(prototxtPath, weightsPath)
# maske tesbit modelini yüklüyoruz
model = load_model(args["model"])

# diskteki fotoğrafı yüklüyoruz
image = cv2.imread(args["image"])
orig = image.copy()
(h, w) = image.shape[:2]

# görüntüden yuvarlak oluşturuyoruz
blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                             (104.0, 177.0, 123.0))

# yuvarlağı ağ üzerinden geçirip yüz algılamasını yapıyoruz
print("[Bilgi] Maske Tespit Islemi Baslatildi !")
net.setInput(blob)
detections = net.forward()

# algılamalar üzerinden döngü
for i in range(0, detections.shape[2]):

    confidence = detections[0, 0, i, 2]

    # zayıf algılamları filtreliyoruz
    if confidence > args["confidence"]:
        # x, y koordinatlarını hesaplıyoruz
        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
        (startX, startY, endX, endY) = box.astype("int")

        (startX, startY) = (max(0, startX), max(0, startY))
        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

        # yeniden boyutlandırıyoruz ve bgr den rgbye dönüştürüyoruz
        face = image[startY:endY, startX:endX]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = preprocess_input(face)
        face = np.expand_dims(face, axis=0)

        # maske var mı yok mu kontrol ediyoruz
        (mask, withoutMask) = model.predict(face)[0]

        # maskenin olup olmadığına göre label adlı değişkenimiz değişiyor
        label = 0 if mask > withoutMask \
            else 1  # labeli seslendirme oraya mp3 dosyalarını koy maske tak
        if label == 0:
            mixer.music.load(thxformask)
            mixer.music.play()
            time.sleep(3.9)
            mixer.music.unload()
        else:
            mixer.music.load(takemask)
            mixer.music.play()
            time.sleep(2.3)
            mixer.music.unload()

cv2.waitKey(1)
