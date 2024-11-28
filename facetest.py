import os
import cv2
import face_recognition
import numpy as np
import serial
import time
import speech_recognition as sr

# Initialize serial communication with Arduino
arduino_port = 'COM4'  # Replace with your Arduino's serial port
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)
time.sleep(2)  # Wait for the serial connection to initialize

# Load known faces and their names
known_face_encodings = []
known_face_names = []

# Path to the directory containing known face images
faces_dir = "faces/"

# Load images and encode faces
for filename in os.listdir(faces_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):  # Check for image files
        image_path = os.path.join(faces_dir, filename)
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:  # Check if at least one face is found in the image
            face_encoding = face_encodings[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])  # Use the filename (without extension) as the name

# Initialize variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

# Initialize speech recognition
recognizer = sr.Recognizer()

def recognize_speech_from_mic():
    with sr.Microphone() as source:
        print("Say something:")
        audio = recognizer.listen(source)

        try:
            command = recognizer.recognize_google(audio)
            print("You said: " + command)
            return command.lower()
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio")
        except sr.RequestError:
            print("Sorry, my speech service is down")
        return None

# Initialize webcam
video_capture = cv2.VideoCapture(0)

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # Use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame

    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Send command to Arduino if known face is recognized
    if "Person1" in face_names:  # Replace "Person1" with the actual name
        ser.write(b'L')  # Send 'L' for light on
        print("Facial Recognition: Light ON")
        break

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()

# Voice control after facial recognition
while True:
    command = recognize_speech_from_mic()
    if command:
        if "light on" in command:
            ser.write(b'L')  # Send 'L' for light on
            print("Voice Command: Light ON")
        elif "light off" in command:
            ser.write(b'O')  # Send 'O' for light off
            print("Voice Command: Light OFF")
#if __name__ == "__main__":
    #main()