import numpy as np
import pandas as pd
from scipy import stats
from sklearn.preprocessing import LabelEncoder

from project_real_estate.constants import ALLOWED_PROPERTY_TYPES


class PropertyPreprocessor:
    def __init__(self):
        self._features = [
            "num_bathrooms",
            "num_bedrooms",
            "area",
            "year_built",
            "neighborhood",
        ]
        self._labels = ["rent"]
        self._label_encoder = LabelEncoder()
        self._label_encoder_mapping = {}

    def _encode_neighborhood(self, neighborhood):
        return self._label_encoder_mapping.get(neighborhood, np.nan)

    def _fit_neighborhood_encoder(self, series):
        self._label_encoder.fit(series)
        self._label_encoder_mapping = dict(
            zip(
                self._label_encoder.classes_,
                self._label_encoder.transform(self._label_encoder.classes_),
            )
        )

    def _extract_neigborhood_from_city(self, city_name):
        city_parts = city_name.split("(")
        if len(city_parts) == 1:
            return city_parts[0].strip()
        else:
            return city_parts[1].strip(")").strip()

    def _filter_data(self, data):
        """
        Remove duplicates, NaN values and outliers.
        """
        start_length = len(data)
        # Drop duplicate properties
        data = data.drop_duplicates(subset="mls_id")
        data = data.dropna(subset=self._features)
        zscores = stats.zscore(data.loc[:, self._features[:-1]])
        # Convert nan to 0. Can occur when all values are identical
        zscores = np.nan_to_num(zscores)
        data = data[(np.abs(zscores) < 2.5).all(axis=1)]
        end_length = len(data)
        print(f"Data filtered from {start_length} properties to {end_length}")
        return data

    def preprocess_rentals_data(self, data):
        data = data[data.property_type.isin(ALLOWED_PROPERTY_TYPES)]

        # Fit and encode neighborhood to numerical value
        data["neighborhood"] = data.city.apply(
            lambda x: self._extract_neigborhood_from_city(x)
        )
        self._fit_neighborhood_encoder(data.neighborhood)
        data["neighborhood"] = data.neighborhood.apply(self._encode_neighborhood)

        data = self._filter_data(data)
        return data.loc[:, self._features], data.loc[:, self._labels[0]]

    def _map_unit_descriptions_to_columns(self, unit_descriptions):
        avg_beds = 0
        avg_area = 0
        avg_baths = 0
        unit_counts = 0
        for unit_type in unit_descriptions:
            try:
                num_units, num_rooms = unit_type.split("x")
            except ValueError:
                # Empty description
                return np.nan, np.nan, np.nan, np.nan

            num_units = int(num_units.strip())
            try:
                num_rooms = int(num_rooms.strip()[0])
            except ValueError:
                # Loft or studio
                return np.nan, np.nan, np.nan, np.nan
            avg_beds += num_units * min(num_rooms - 2, 3)
            # Assume always one bathroom
            avg_baths += num_units
            # Assume 100 sqft per room
            avg_area += num_units * num_rooms * 100
            unit_counts += num_units

        return (
            avg_beds / unit_counts,
            avg_baths / unit_counts,
            avg_area / unit_counts,
            unit_counts,
        )

    def _conform_sales_data_to_rent_schema(self, data):
        unit_descriptions = data.num_residential_units.apply(
            lambda x: x.strip("{}").strip('"').split(",")
        )
        unit_descriptions = unit_descriptions.apply(
            self._map_unit_descriptions_to_columns
        )
        data[["num_bedrooms", "num_bathrooms", "area", "num_units"]] = pd.DataFrame(
            unit_descriptions.tolist(), index=unit_descriptions.index
        )
        return data

    def _convert_year_built(self, year):
        try:
            year = int(year)
        except ValueError:
            return np.nan
        else:
            return year

    def preprocess_sales_data(self, data):
        data["neighborhood"] = data.city.apply(self._extract_neigborhood_from_city)
        data["neighborhood"] = data.neighborhood.apply(self._encode_neighborhood)
        data["year_built"] = data.year_built.apply(self._convert_year_built)
        data = self._conform_sales_data_to_rent_schema(data)
        data = self._filter_data(data)
        return (
            data.loc[:, self._features],
            data.loc[:, "num_units"],
            data.loc[:, "claimed_revenue"],
        )
