from sklearn.model_selection import train_test_split


class TrivialRentEstimator:
    def __call__(self, input_):
        return 1.0


class SKLearnRentEstimator:
    def __init__(self, preprocessor, estimator):
        self._preprocessor = preprocessor
        self._estimator = estimator

    def fit(self, properties, test_split=0.15):
        """
        :param properties: Rental properties.
        """
        X, y = self._preprocessor.preprocess_rentals_data(properties)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_split, random_state=100
        )
        self._estimator.fit(X_train, y_train)
        return self._estimator.score(X_test, y_test)

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
