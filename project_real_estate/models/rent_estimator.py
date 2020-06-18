import numpy as np
from sklearn.model_selection import train_test_split


class TrivialRentEstimator:
    def __call__(self, input_):
        return 1.0


class SKLearnRentEstimator:
    def __init__(self, preprocessor, estimator):
        self._preprocessor = preprocessor
        self._estimator = estimator
        self._random_seed = 100

    def fit(self, properties, test_split=0.15):
        """
        :param properties: Rental properties.
        """
        X, y = self._preprocessor.preprocess_rentals_data(properties)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_split, random_state=self._random_seed
        )
        self._estimator.fit(X_train, y_train)

    def score(self, properties, test_split=0.15, error_tolerance=0.1):
        """
        Get R2 score and % of samples from test set which fall within a certain error of the prediction.
        """
        X, y = self._preprocessor.preprocess_rentals_data(properties)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_split, random_state=self._random_seed
        )
        r2 = self._estimator.score(X_test, y_test)

        test_preds = self._estimator.predict(X_test)
        accurate_predictions = np.all(
            [
                test_preds * (1 - error_tolerance) < y_test,
                y_test < test_preds * (1 + error_tolerance),
            ],
            axis=0,
        ).sum()
        return r2, accurate_predictions / len(y_test)

    def predict(self, properties):
        """
        Predict the potential revenue for a property. We take the minimum of the estimated gross revenue on Centris and
        our prediction.

        :param properties: Properties for sale.
        """
        (
            X,
            num_units,
            centris_claimed_revenue,
        ) = self._preprocessor.preprocess_sales_data(properties)
        centris_claimed_monthly_revenue = centris_claimed_revenue / 12
        average_rent = self._estimator.predict(X)
        predicted_revenue = average_rent * num_units

        # Take minimum of prediction and Centris prediction
        predicted_revenue = predicted_revenue.combine(
            centris_claimed_monthly_revenue, func=min
        )
        predicted_revenue.name = "predicted_rent_revenue"
        return predicted_revenue
