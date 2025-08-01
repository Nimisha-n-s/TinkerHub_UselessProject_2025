import cv2
import random

# ✅ Your IP Webcam stream URL
IP_CAM_URL = "http://100.71.82.54:8080/video"

# Open the video stream from your phone
cap = cv2.VideoCapture(IP_CAM_URL)

if not cap.isOpened():
    print("Error: Could not open video stream.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Convert to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Invert to detect dark crumbs on light background
    _, thresh = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Find contours (crumbs)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    centers = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 30 < area < 3000:  # Adjust as needed for crumb size
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

    # Shuffle & connect crumbs
    random.shuffle(centers)
    for i in range(len(centers) - 1):
        cv2.line(frame, centers[i], centers[i + 1], (255, 0, 0), 2)

    # Optionally close the loop
    if len(centers) > 2:
        cv2.line(frame, centers[-1], centers[0], (255, 0, 0), 2)

    cv2.putText(frame, f'Crumbs: {len(centers)}', (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    cv2.putText(frame, "Bread Crumb Mapper (Phone Cam)", (20, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow("Bread Crumb Mapper LIVE (Phone Cam)", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
