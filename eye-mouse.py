import cv2
import ctypes

# Windows mouse control (built-in Python)
user32 = ctypes.windll.user32

# Load eye cascade correctly
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_eye.xml"
)

# Start webcam
cap = cv2.VideoCapture(0)

# Screen size
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in eyes:
        # Eye center
        cx = x + w // 2
        cy = y + h // 2

        # Map camera → screen coordinates
        screen_x = int(screen_w * cx / frame.shape[1])
        screen_y = int(screen_h * cy / frame.shape[0])

        # Move REAL cursor
        user32.SetCursorPos(screen_x, screen_y)

        # Draw box
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)

        break  # use first eye only

    cv2.imshow("Eye Mouse", frame)

    if cv2.waitKey(1) == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()