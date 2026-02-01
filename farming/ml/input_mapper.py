def map_farmer_inputs(fertility, climate, humidity, soil_ph, rainfall):
    fertility_map = {
        "low":    (30, 20, 30),
        "medium": (70, 50, 60),
        "high":   (110, 90, 100)
    }

    temperature_map = {
        "cool": 18,
        "moderate": 26,
        "hot": 34
    }

    humidity_map = {
        "low": 40,
        "medium": 65,
        "high": 85
    }

    ph_map = {
        "acidic": 5.5,
        "neutral": 6.8,
        "alkaline": 8.0
    }

    rainfall_map = {
        "low": 50,
        "medium": 120,
        "heavy": 220
    }

    N, P, K = fertility_map[fertility]

    return [
        N,
        P,
        K,
        temperature_map[climate],
        humidity_map[humidity],
        ph_map[soil_ph],
        rainfall_map[rainfall]
    ]
