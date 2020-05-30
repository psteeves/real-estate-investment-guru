from pathlib import Path

MAX_NUM_RESULTS = 20
COLUMNS_TO_DISPLAY = [
    "City",
    "Price",
    "Initial Investment",
    "Gross Revenue",
    "Net Income",
    "Net Cash",
    "Cash Return",
    "ROE",
    "URL",
]
ALLOWED_PROPERTY_TYPES = ["Condo / Apartment", "Loft / Studio"]
SERIALIZED_MODEL_PATH = (
    Path(__file__).parent.parent / "serialized_models/rent_predictor.pkl"
)
