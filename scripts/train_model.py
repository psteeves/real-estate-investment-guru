from project_real_estate.models.rent_estimator import SKLearnRentEstimator
from project_real_estate.models.preprocessor import PropertyPreprocessor
from sklearn.ensemble import RandomForestRegressor
from project_real_estate.db import pull_data
import argparse
import pickle
from project_real_estate.constants import SERIALIZED_MODEL_DIR


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True, help="Name of the model.")
    args = parser.parse_args()

    data = pull_data("rentals", max_rows=None)
    print("Data loaded.")
    estimator = RandomForestRegressor(n_estimators=100, max_depth=30)
    preprocessor = PropertyPreprocessor()
    model = SKLearnRentEstimator(estimator=estimator, preprocessor=preprocessor)

    score = model.fit(data)
    print(f"Model obtained a score of {score:.2f} on the test set.")

    model_path = SERIALIZED_MODEL_DIR / args.name
    pickle.dump(model, open(model_path, "wb"))
    print(f"Model saved to {model_path}.")


if __name__ == "__main__":
    main()