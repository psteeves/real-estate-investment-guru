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
        :param properties: Properties for sale.
        """
        X, num_units = self._preprocessor.preprocess_sales_data(properties)
        average_rent = self._estimator.predict(X)
        return average_rent * num_units
