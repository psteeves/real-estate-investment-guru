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

    model.fit(data)
    error_tolerance = 0.1
    r2, percentage_correct_preds = model.score(data, error_tolerance=error_tolerance)
    print(f"Model obtained a R2 score of {r2:.2f} on the test set. {percentage_correct_preds:.3f} fall within {100*error_tolerance:.0f}% of our predictions")

    model_path = (SERIALIZED_MODEL_DIR / args.name).with_suffix(".pkl")
    pickle.dump(model, open(model_path, "wb"))
    print(f"Model saved to {model_path}.")


if __name__ == "__main__":
    main()
