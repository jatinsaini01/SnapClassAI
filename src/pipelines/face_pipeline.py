import streamlit as st
import dlib
import numpy as np
import face_recognition_models
from sklearn.svm import SVC
from src.database.db import get_all_students
@st.cache_resource
def load_all_models():
    detector = dlib.get_frontal_face_detector()
    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )
    facrec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )
    return detector, sp, facrec


def get_face_embeddings(photo_source):
    detector, sp, facrec = load_all_models()
    faces = detector(photo_source, 1)
    embeddings = []
    for face in faces:
        shape = sp(photo_source, face)
        face_descriptor = facrec.compute_face_descriptor(photo_source, shape, 2)
        embeddings.append(np.array(face_descriptor))
    return embeddings


@st.cache_resource
def get_trainned_models():
    X = []
    y = []
    student_db = get_all_students()
    if not student_db:
        return None
    for student in student_db:
        embedding = student.get('face_embedding')
        if embedding:
            X.append(np.array(embedding))
            y.append(student.get('student_id'))
    if len(X) == 0:
        return None

    X = np.array(X)
    y = np.array(y)

    # SVC needs at least 2 classes to fit
    if len(set(y)) < 2:
        return {"model": None, "X": X, "y": y}

    model = SVC(kernel="linear", probability=True, class_weight='balanced')
    try:
        model.fit(X, y)
    except ValueError:
        return None
    return {"model": model, "X": X, "y": y}


def train_model():
    st.cache_resource.clear()
    model_data = get_trainned_models()
    return model_data is not None


def predict_attendance(photo_source):
    embeddings = get_face_embeddings(photo_source)
    detected_students = {}
    model_data = get_trainned_models()

    if not model_data:
        return {}, [], len(embeddings)

    model = model_data['model']
    X_train = model_data['X']
    y_train = model_data['y']
    all_students = sorted(list(set(y_train)))

    resemblance_threshold = 0.6

    for embedding in embeddings:
        if model is not None and len(all_students) >= 2:
            predicted_id = model.predict([embedding])[0]
            # confirm with distance check too, to avoid false positives
            same_class_idx = np.where(y_train == predicted_id)[0]
            best_match_score = np.min(
                np.linalg.norm(X_train[same_class_idx] - embedding, axis=1)
            )
        else:
            # only one known student enrolled — fall back to pure distance check
            predicted_id = all_students[0]
            best_match_score = np.min(
                np.linalg.norm(X_train - embedding, axis=1)
            )

        if best_match_score <= resemblance_threshold:
            detected_students[predicted_id] = True

    return detected_students, all_students, len(embeddings)