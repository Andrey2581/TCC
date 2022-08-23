import cv2
import mediapipe as mp

# Start camera
capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

# Start Mediapipe
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.6) as face_detection:

    # Endless Loop
    while capture.isOpened():
        success, image = capture.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert color and save detection results in a variable
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = face_detection.process(image)

        # Draw the face detection annotations on the image and flip the image
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.detections:
            for detection in results.detections:
                mp_drawing.draw_detection(image, detection)
            image = cv2.flip(image, 1)

        # If no faces are detected, flip the image and write a text on it
        else:
            image = cv2.flip(image, 1)
            cv2.putText(image, "No Face Detected", (100, 100),
                        cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, 255, 2)

        # Show the image with the annotations or text
        cv2.imshow('MediaPipe Face Detection', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

# End the program
capture.release()
cv2.destroyAllWindows()
