import numpy as np
from PIL import Image


def analyze_image_features(image_path):
    img = Image.open(image_path).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img).astype(float)

    r = img_array[:, :, 0]
    g = img_array[:, :, 1]
    b = img_array[:, :, 2]

    r_mean, g_mean, b_mean = r.mean(), g.mean(), b.mean()
    r_std, g_std, b_std = r.std(), g.std(), b.std()

    brightness = (r_mean + g_mean + b_mean) / 3
    greenness = g_mean - (r_mean + b_mean) / 2
    redness = r_mean - b_mean
    yellowness = (r_mean + g_mean) / 2 - b_mean

    edges_h = np.abs(np.diff(r, axis=1)).sum()
    edges_v = np.abs(np.diff(r, axis=0)).sum()
    edge_density = (edges_h + edges_v) / 1_000_000

    spot_pixels = (
        (np.abs(r - r_mean) > 40) |
        (np.abs(g - g_mean) > 40) |
        (np.abs(b - b_mean) > 40)
    ).sum()

    spot_ratio = spot_pixels / (224 * 224)

    return {
        "r_mean": r_mean,
        "g_mean": g_mean,
        "b_mean": b_mean,
        "r_std": r_std,
        "g_std": g_std,
        "b_std": b_std,
        "brightness": brightness,
        "greenness": greenness,
        "redness": redness,
        "yellowness": yellowness,
        "edge_density": edge_density,
        "spot_ratio": spot_ratio,
    }


def predict_disease(image_path):
    try:
        f = analyze_image_features(image_path)

        # ---------- TOMATO DISEASES (STRICT ORDER) ----------

        if f["yellowness"] > 28 and f["g_mean"] > 140 and f["brightness"] > 145:
            return "Tomato___Yellow_Leaf_Curl_Virus", 76

        if (
            f["brightness"] > 165 and
            f["edge_density"] < 0.15 and
            (f["r_std"] + f["g_std"] + f["b_std"]) < 35
        ):
            return "Tomato___Mosaic_virus", 74

        if f["brightness"] < 115 and f["greenness"] < 8 and f["spot_ratio"] > 0.18:
            return "Tomato___Late_blight", 81

        if (
            10 < f["redness"] < 30 and
            120 < f["brightness"] < 150 and
            f["spot_ratio"] > 0.12
        ):
            return "Tomato___Early_blight", 80

        if (
            0.20 < f["edge_density"] < 0.45 and
            0.10 < f["spot_ratio"] < 0.25
        ):
            return "Tomato___Septoria_leaf_spot", 77

        if (
            0.35 < f["edge_density"] < 0.55 and
            0.15 < f["spot_ratio"] < 0.35
        ):
            return "Tomato___Target_Spot", 78

        if (
            150 < f["brightness"] < 165 and
            8 < f["redness"] < 18 and
            f["edge_density"] < 0.25
        ):
            return "Tomato___Leaf_Mold", 75

        if f["yellowness"] > 15 and f["edge_density"] > 0.25 and f["redness"] > 8:
            return "Tomato___Spider_mites", 72

        if (
            f["edge_density"] > 0.55 and
            f["spot_ratio"] > 0.20 and
            f["brightness"] < 135 and
            f["redness"] > 12
        ):
            return "Tomato___Bacterial_spot", 79

        if f["greenness"] > 25 and f["redness"] < 5 and f["spot_ratio"] < 0.08:
            return "Tomato___Healthy", 87

        # ---------- CORN ----------
        if f["g_mean"] > 145 and f["r_mean"] > 135:
            return "Corn___Common_rust", 71

        if f["greenness"] > 18:
            return "Corn___Healthy", 73

        # ---------- APPLE ----------
        if f["redness"] > 30:
            return "Apple___Black_rot", 70

        if f["yellowness"] > 25:
            return "Apple___Cedar_apple_rust", 69

        # ---------- FALLBACK ----------
        return "Healthy Leaf", 60

    except Exception as e:
        raise Exception(f"Prediction failed: {str(e)}")
