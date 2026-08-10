import cv2

URL_STREAM = "http://192.168.1.100:8080/stream"

cap = cv2.VideoCapture(URL_STREAM)

if not cap.isOpened():
    print("Erreur lors de l'ouverture du flux vidéo.")
    exit(1)

print("Flux vidéo ouvert avec succès.")

while True:

    ret, frame = cap.read()
    if not ret:
        print("Erreur lors de la lecture du flux vidéo.")
        break

    cv2.imshow('Flux vidéo', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()