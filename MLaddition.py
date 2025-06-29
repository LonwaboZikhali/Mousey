import cv2

camera = cv2.VideoCapture(0)

while True:
    ret, frame = camera.read()
    cv2.imshow('webcam', frame)
    if cv2.waitKey(40) & 0xFF == ord('q'):
        break

    # to quit, just press 'q'

camera.release()
cv2.destroyAllWindows()