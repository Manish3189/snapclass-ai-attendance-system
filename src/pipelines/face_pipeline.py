import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st

from src.database.db import get_all_students



# 1. LOAD DLIB MODELS
@st.cache_resource
def load_dlib_models():
    # Face detector
    detector = dlib.get_frontal_face_detector()
    # Facial landmark predictor
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    # Face recognition model
    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facerec

# 2. CREATE FACE EMBEDDINGS
def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    # Detect all faces in the image
    faces = detector(image_np, 1)

    encodings = []

    # Process every detected face
    for face in faces:

        # Find facial landmarks
        shape = sp(image_np, face)

        # Convert face into a 128-dimensional face embedding
        face_description = facerec.compute_face_descriptor(image_np, shape, 1)

        # Convert dlib vector into NumPy array
        encoding = np.array(face_description)

        encodings.append(encoding)

    return encodings

# 3. TRAIN SVM MODEL USING STUDENT DATA

@st.cache_resource
def get_trained_model():

    X = []
    y = []

    # Get all students from database
    student_db = get_all_students()

    # No students found
    if not student_db:
        return None

    # Extract face embeddings and student IDs
    for student in student_db:

        embedding = student.get("face_embedding")
        student_id = student.get("student_id")

        # Make sure both values exist
        if embedding is not None and student_id is not None:

            X.append(np.array(embedding))
            y.append(student_id)

    # No valid face embeddings
    if len(X) == 0:
        return None

    # At least 2 different students are required for SVM
    unique_students = set(y)

    if len(unique_students) < 2:
        return {
            "clf": None,
            "X": X,
            "y": y
        }

    # Create SVM classifier
    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        # Train SVM
        clf.fit(X, y)

    except ValueError as e:
        print("SVM training error:", e)
        return None

    # Return everything required for prediction
    return {
        "clf": clf,
        "X": X,
        "y": y
    }

# 4. RETRAIN CLASSIFIER

def train_classifier():

    # Clear cached model
    st.cache_resource.clear()

    # Train model again
    model_data = get_trained_model()

    # Return True if model was successfully created
    return model_data is not None

# 5. PREDICT ATTENDANCE

def predict_attendance(class_image_np):

# Step 1: Get face embeddings from classroom image

    encodings = get_face_embeddings(class_image_np)

    # Dictionary to store detected students
    detected_students = {}

    # Step 2: Get trained model

    model_data = get_trained_model()

    # No model
    if not model_data:

        return (
            detected_students,
            [],
            len(encodings)
        )

    
    # Step 3: Extract model data
    
    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    # Get unique student IDs
    all_students = sorted(list(set(y_train)))
    # Step 4: Process every detected face
    
    for encoding in encodings:
        # If SVM exists and there are multiple students
        if clf is not None and len(all_students) >= 2:
            # IMPORTANT:
            # encoding = ONE face
            # encodings = ALL faces
            predicted_id = clf.predict([encoding])[0]

            # If only one student exists
        
        elif len(all_students) == 1:
            predicted_id = all_students[0]
        else:
            continue        
        # Convert ID to same type if necessary        
        try:
            predicted_id = int(predicted_id)
        except (ValueError, TypeError):
            pass

        # Find stored embedding of predicted student

        try:

            student_index = y_train.index(predicted_id)

            student_embedding = X_train[student_index]

        except ValueError:

            continue

        # Calculate Euclidean distance

        distance = np.linalg.norm(
            student_embedding - encoding
        )

        # Face matching threshold
        resemblance_threshold = 0.6

        # If distance is small enough → accept

        if distance <= resemblance_threshold:

            detected_students[predicted_id] = True

    # Step 5: Return result

    return (
        detected_students,
        all_students,
        len(encodings)
    )