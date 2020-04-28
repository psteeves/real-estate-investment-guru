from pathlib import Path

MAX_NUM_RESULTS = 10
COLUMNS_TO_DISPLAY = ["full_address", "city", "price", "predicted_rent_revenue", "url"]
ALLOWED_PROPERTY_TYPES = ["Condo / Apartment", "Loft / Studio"]
SERIALIZED_MODEL_PATH = Path(__file__).parent.parent / "serialized_models/rent_predictor.pkl"
