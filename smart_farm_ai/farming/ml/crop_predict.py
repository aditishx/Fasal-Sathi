# import pickle


# model = pickle.load(open("farming/ml/crop_model.pkl", "rb"))

# def predict_crop(data):
#     prediction = model.predict([data])
#     return prediction[0]

import pickle
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "crop_model.pkl")

_model = None  # lazy-loaded model


def load_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError("crop_model.pkl not found")

        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)

    return _model


def predict_crops(features, top_k=3):
    """
    Predict top K suitable crops with confidence scores.

    features: list or array of input features
    top_k: number of crops to recommend
    """

    model = load_model()

    # Convert to numpy array
    X = np.array(features).reshape(1, -1)

    # Validate feature count
    if hasattr(model, "n_features_in_"):
        if X.shape[1] != model.n_features_in_:
            raise ValueError(
                f"Expected {model.n_features_in_} features, got {X.shape[1]}"
            )

    # If model supports probabilities (best case)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)[0]
        class_labels = model.classes_

        top_indices = np.argsort(probs)[-top_k:][::-1]

        results = [
            {
                "crop": class_labels[i],
                
            }
            for i in top_indices
        ]

    else:
        # Fallback for models without probabilities
        prediction = model.predict(X)[0]
        results = [{"crop": prediction.title()}]

    return results

