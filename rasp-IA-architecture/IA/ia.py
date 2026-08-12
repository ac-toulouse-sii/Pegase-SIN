import cv2
import onnxruntime as ort


URL_STREAM = "http://192.168.8.129:81/stream"


# Chargement modèle ONNX
session = ort.InferenceSession("yolo11s.onnx")

print("Modèle ONNX chargé")

input_name = session.get_inputs()[0].name
print("Entrée modèle :", input_name)


# Chargement classes COCO
with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]


# Ouverture caméra
cap = cv2.VideoCapture(URL_STREAM)

if not cap.isOpened():
    print("Erreur lors de l'ouverture du flux vidéo.")
    exit(1)

print("Flux vidéo ouvert avec succès.")


while True:

    ret, frame = cap.read()

    if not ret:
        print("Erreur lecture flux")
        break


    # Préparation image YOLO
    img = cv2.resize(frame, (640, 640))

    img = img[:, :, ::-1]          # BGR -> RGB
    img = img.transpose(2, 0, 1)   # HWC -> CHW
    img = img.astype("float32") / 255.0
    img = img[None, ...]           # ajout batch


    # Inférence
    outputs = session.run(
        None,
        {input_name: img}
    )


    # Sortie YOLO : (1,84,8400)
    detections = outputs[0][0].T


    boxes = []
    scores = []
    names = []


    # Analyse des 8400 propositions
    for det in detections:

        x, y, w, h = det[:4]

        class_scores = det[4:]

        classe = class_scores.argmax()
        confiance = float(class_scores[classe])


        if confiance > 0.5:

            x1 = int(x - w / 2)
            y1 = int(y - h / 2)

            boxes.append([
                x1,
                y1,
                int(w),
                int(h)
            ])

            scores.append(confiance)
            names.append(classes[classe])


    # Suppression doublons
    indices = cv2.dnn.NMSBoxes(
        boxes,
        scores,
        0.5,
        0.45
    )


    for i in indices:
        if isinstance(i, (list, tuple)):
            i = i[0]

        print(
            names[i],
            round(scores[i], 2)
        )


cap.release()