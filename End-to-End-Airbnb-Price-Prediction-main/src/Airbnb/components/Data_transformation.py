import os
import sys
import numpy as np
import pandas as pd
from dataclasses import dataclass
from src.Airbnb.exception import customexception
from src.Airbnb.logger import logging
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from src.Airbnb.utils.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path = os.path.join('Artifacts', 'Preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def get_data_transformation(self):
        try:
            logging.info('Data Transformation initiated for India model')

            numerical_cols = [
                'amenities', 'accommodates', 'bathrooms', 'latitude', 'longitude', 
                'host_response_rate', 'number_of_reviews', 'review_scores_rating', 
                'bedrooms', 'beds'
            ]
            categorical_cols = [
                'property_type', 'room_type', 'bed_type', 'cancellation_policy', 
                'cleaning_fee', 'city', 'host_identity_verified', 'instant_bookable', 
                'host_has_profile_pic'
            ]

            property_type_cat = [
                'Apartment', 'House', 'Condominium', 'Villa', 'Bungalow', 
                'Loft', 'Guesthouse', 'Bed & Breakfast', 'Serviced apartment', 
                'Heritage Haveli', 'Cabin / Chalet', 'Cottage', 'Resort / Cottage', 'Townhouse'
            ]
            room_type_cat = ['Entire home/apt', 'Private room', 'Shared room']
            bed_type_cat = ['Real Bed', 'Futon', 'Pull-out Sofa', 'Airbed']
            cancellation_policy_cat = ['flexible', 'moderate', 'strict', 'super_strict_30']
            cleaning_fee_cat = [False, True]
            city_cat = ['Mumbai', 'Goa', 'Delhi-NCR', 'Bangalore', 'Jaipur', 'Hyderabad', 'Kolkata', 'Manali / Shimla']
            host_has_profile_pic_cat = ['t', 'f']
            host_identity_verified_cat = ['t', 'f']
            instant_bookable_cat = ['t', 'f']

            num_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])

            cat_pipeline = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('ordinalencoder', OrdinalEncoder(
                    categories=[
                        property_type_cat, 
                        room_type_cat, 
                        bed_type_cat, 
                        cancellation_policy_cat, 
                        cleaning_fee_cat, 
                        city_cat, 
                        host_identity_verified_cat, 
                        instant_bookable_cat,
                        host_has_profile_pic_cat
                    ],
                    handle_unknown='use_encoded_value',
                    unknown_value=-1
                ))
            ])

            preprocessor = ColumnTransformer([
                ('num_pipeline', num_pipeline, numerical_cols),
                ('cat_pipeline', cat_pipeline, categorical_cols)
            ])

            return preprocessor
        except Exception as e:
            raise customexception(e, sys)

    def initialize_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            preprocessing_obj = self.get_data_transformation()

            # Clean host_response_rate if string with %
            if train_df['host_response_rate'].dtype == object:
                train_df['host_response_rate'] = train_df['host_response_rate'].astype(str).str.replace('%', '', regex=False)
                train_df['host_response_rate'] = pd.to_numeric(train_df['host_response_rate'], errors='coerce').fillna(100)

            if test_df['host_response_rate'].dtype == object:
                test_df['host_response_rate'] = test_df['host_response_rate'].astype(str).str.replace('%', '', regex=False)
                test_df['host_response_rate'] = pd.to_numeric(test_df['host_response_rate'], errors='coerce').fillna(100)

            target_column_name = 'log_price'
            drop_cols = [col for col in [target_column_name, 'price_inr', 'id', 'name', 'description', 'first_review', 'host_since', 'last_review', 'neighbourhood', 'thumbnail_url', 'zipcode'] if col in train_df.columns]

            # Amenities count if string
            if train_df['amenities'].dtype == object:
                train_df['amenities'] = [len(str(a).split(',')) for a in train_df['amenities']]
            if test_df['amenities'].dtype == object:
                test_df['amenities'] = [len(str(a).split(',')) for a in test_df['amenities']]

            input_feature_train_df = train_df.drop(columns=drop_cols)
            target_feature_train_df = train_df[target_column_name]

            input_feature_test_df = test_df.drop(columns=drop_cols)
            target_feature_test_df = test_df[target_column_name]

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            os.makedirs(os.path.dirname(self.data_transformation_config.preprocessor_obj_file_path), exist_ok=True)
            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            logging.info("Indian Preprocessor pickle file saved successfully.")
            return train_arr, test_arr

        except Exception as e:
            logging.info("Exception occurred in Indian data transformation")
            raise customexception(e, sys)
