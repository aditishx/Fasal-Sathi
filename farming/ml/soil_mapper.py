def map_soil_inputs(fertility, soil_type, climate, rainfall):
    # Fertility → NPK
    fertility_map = {
        "low":    (30, 30, 30),
        "medium": (70, 60, 60),
        "high":   (110, 100, 100)
    }

    # Soil type adjustments
    soil_adjustment = {
        "sandy": (-10, -10, -10),
        "loamy": (0, 0, 0),
        "clay":  (10, 10, 10)
    }

    # Climate → temperature
    climate_map = {
        "cold": 18,
        "moderate": 25,
        "hot": 32
    }

    # Rainfall mapping
    rainfall_map = {
        "low": 50,
        "medium": 120,
        "heavy": 200
    }

    # pH mapping based on soil type
    ph_map = {
        "sandy": 6.5,
        "loamy": 7.0,
        "clay": 7.5
    }

    N, P, K = fertility_map[fertility]
    dN, dP, dK = soil_adjustment[soil_type]

    return [
        N + dN,                 # Nitrogen
        P + dP,                 # Phosphorus
        K + dK,                 # Potassium
        climate_map[climate],   # Temperature
        70,                     # Humidity (avg assumption)
        ph_map[soil_type],      # pH
        rainfall_map[rainfall]  # Rainfall
    ]
