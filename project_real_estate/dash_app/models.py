import pickle

from project_real_estate.constants import SERIALIZED_MODEL_PATH

rent_model = pickle.load(open(SERIALIZED_MODEL_PATH, "rb"))
