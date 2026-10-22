import os
import sys
import numpy as np
import pandas as pd
from src.Airbnb.logger import logging
from src.Airbnb.utils.utils import load_object
from src.Airbnb.exception import customexception

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            artifacts_dir = os.path.join(base_dir, "Artifacts")
            preprocessor_path = os.path.join(artifacts_dir, "Preprocessor.pkl")
            model_path = os.path.join(artifacts_dir, "Model.pkl")
            preprocessor = load_object(preprocessor_path)
            model = load_object(model_path)
            logging.info('Preprocessor and Model Pickle files loaded')
            scaled_data = preprocessor.transform(features)
            logging.info('Data Scaled')
            pred = model.predict(scaled_data)
            return pred
        except Exception as e:
            raise customexception(e, sys)

class CustomData:
    def __init__(self,
                 property_type: str,
                 room_type: str,
                 amenities: int,
                 accommodates: int,
                 bathrooms: float,
                 bed_type: str,
                 cancellation_policy: str,
                 cleaning_fee: bool,
                 city: str,
                 host_has_profile_pic: str,
                 host_identity_verified: str,
                 host_response_rate: float,
                 instant_bookable: str,
                 latitude: float,
                 longitude: float,
                 number_of_reviews: int,
                 review_scores_rating: float,
                 bedrooms: int,
                 beds: int,
                 checkin_month: int = 12,
                 day_of_week: int = 5,
                 is_weekend: int = 1,
                 season_category: str = "peak"):

        self.property_type = property_type
        self.room_type = room_type
        self.amenities = amenities
        self.accommodates = accommodates
        self.bathrooms = bathrooms
        self.bed_type = bed_type
        self.cancellation_policy = cancellation_policy
        self.cleaning_fee = cleaning_fee
        self.city = city
        self.host_has_profile_pic = host_has_profile_pic
        self.host_identity_verified = host_identity_verified
        self.host_response_rate = host_response_rate
        self.instant_bookable = instant_bookable
        self.latitude = latitude
        self.longitude = longitude
        self.number_of_reviews = number_of_reviews
        self.review_scores_rating = review_scores_rating
        self.bedrooms = bedrooms
        self.beds = beds
        self.checkin_month = checkin_month
        self.day_of_week = day_of_week
        self.is_weekend = is_weekend
        self.season_category = season_category

    def get_data_as_dataframe(self):
        try:
            custom_data_input_dict = {
                'property_type': [self.property_type],
                'room_type': [self.room_type],
                'amenities': [self.amenities],
                'accommodates': [self.accommodates],
                'bathrooms': [self.bathrooms],
                'bed_type': [self.bed_type],
                'cancellation_policy': [self.cancellation_policy],
                'cleaning_fee': [self.cleaning_fee],
                'city': [self.city],
                'host_has_profile_pic': [self.host_has_profile_pic],
                'host_identity_verified': [self.host_identity_verified],
                'host_response_rate': [self.host_response_rate],
                'instant_bookable': [self.instant_bookable],
                'latitude': [self.latitude],
                'longitude': [self.longitude],
                'number_of_reviews': [self.number_of_reviews],
                'review_scores_rating': [self.review_scores_rating],
                'bedrooms': [self.bedrooms],
                'beds': [self.beds],
                'checkin_month': [self.checkin_month],
                'day_of_week': [self.day_of_week],
                'is_weekend': [self.is_weekend],
                'season_category': [self.season_category]
            }
            df = pd.DataFrame(custom_data_input_dict)
            logging.info('Dataframe Gathered')
            return df
        except Exception as e:
            logging.info('Exception Occurred in prediction pipeline')
            raise customexception(e, sys)
