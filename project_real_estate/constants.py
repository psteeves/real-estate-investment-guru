from pathlib import Path

COLUMNS_TO_DISPLAY = [
    "City",
    "Price",
    "Initial Investment",
    "Gross Revenue",
    "Net Income",
    "Net Cash",
    "Cash Return",
    "ROE",
    "Cap Rate",
    "URL",
]
ALLOWED_PROPERTY_TYPES = ["Condo / Apartment", "Loft / Studio"]
SERIALIZED_MODEL_DIR = Path(__file__).parent.parent / "serialized_models"
SERIALIZED_MODEL_PATH = SERIALIZED_MODEL_DIR / "rent_predictor.pkl"
