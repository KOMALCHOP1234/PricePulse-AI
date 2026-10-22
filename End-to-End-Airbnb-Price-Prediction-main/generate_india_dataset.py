import os
import numpy as np
import pandas as pd

np.random.seed(42)

# Destination information with empirical baselines and seasonal dynamics
CITIES_INFO = {
    'Mumbai': {
        'lat': 19.0760, 'long': 72.8777, 'base': 5200,
        'peak_months': [11, 12, 1, 2], 'monsoon_months': [7, 8],
        'peak_mult': 1.25, 'monsoon_mult': 0.82, 'weekend_mult': 1.12,
        'props': ['Apartment', 'Condominium', 'Loft', 'Serviced apartment', 'House']
    },
    'Goa': {
        'lat': 15.2993, 'long': 74.1240, 'base': 6800,
        'peak_months': [11, 12, 1, 2], 'monsoon_months': [6, 7, 8],
        'peak_mult': 1.48, 'monsoon_mult': 0.65, 'weekend_mult': 1.20,
        'props': ['Villa', 'Bungalow', 'Apartment', 'Guesthouse', 'Bed & Breakfast', 'Resort / Cottage']
    },
    'Delhi-NCR': {
        'lat': 28.6139, 'long': 77.2090, 'base': 4200,
        'peak_months': [10, 11, 12, 1, 2], 'monsoon_months': [7, 8],
        'peak_mult': 1.28, 'monsoon_mult': 0.85, 'weekend_mult': 1.10,
        'props': ['Apartment', 'House', 'Loft', 'Condominium', 'Townhouse']
    },
    'Bangalore': {
        'lat': 12.9716, 'long': 77.5946, 'base': 3900,
        'peak_months': [10, 11, 12, 1], 'monsoon_months': [6, 7, 8],
        'peak_mult': 1.20, 'monsoon_mult': 0.88, 'weekend_mult': 1.12,
        'props': ['Apartment', 'Condominium', 'House', 'Villa', 'Guesthouse']
    },
    'Jaipur': {
        'lat': 26.9124, 'long': 75.7873, 'base': 3600,
        'peak_months': [10, 11, 12, 1, 2], 'monsoon_months': [6, 7, 8],
        'peak_mult': 1.40, 'monsoon_mult': 0.72, 'weekend_mult': 1.16,
        'props': ['Heritage Haveli', 'Villa', 'House', 'Apartment', 'Bed & Breakfast']
    },
    'Hyderabad': {
        'lat': 17.3850, 'long': 78.4867, 'base': 3400,
        'peak_months': [10, 11, 12, 1, 2], 'monsoon_months': [6, 7, 8],
        'peak_mult': 1.20, 'monsoon_mult': 0.85, 'weekend_mult': 1.10,
        'props': ['Apartment', 'Condominium', 'House', 'Villa']
    },
    'Kolkata': {
        'lat': 22.5726, 'long': 88.3639, 'base': 2800,
        'peak_months': [10, 11, 12, 1], 'monsoon_months': [6, 7, 8],
        'peak_mult': 1.35, 'monsoon_mult': 0.80, 'weekend_mult': 1.12,
        'props': ['Apartment', 'House', 'Condominium', 'Bed & Breakfast']
    },
    'Manali / Shimla': {
        'lat': 32.2432, 'long': 77.1892, 'base': 4800,
        'peak_months': [5, 6, 12, 1], 'monsoon_months': [7, 8],
        'peak_mult': 1.55, 'monsoon_mult': 0.52, 'weekend_mult': 1.22,
        'props': ['Cabin / Chalet', 'Cottage', 'Villa', 'House', 'Apartment']
    }
}

ROOM_TYPES = ['Entire home/apt', 'Private room', 'Shared room']
ROOM_WEIGHTS = [0.60, 0.35, 0.05]

BED_TYPES = ['Real Bed', 'Futon', 'Pull-out Sofa', 'Airbed']
BED_WEIGHTS = [0.88, 0.06, 0.04, 0.02]

CANCELLATIONS = ['flexible', 'moderate', 'strict', 'super_strict_30']
CANCEL_WEIGHTS = [0.45, 0.35, 0.16, 0.04]

def generate_dynamic_rental_dataset(n_samples=30000):
    rows = []
    cities_list = list(CITIES_INFO.keys())

    for i in range(n_samples):
        city = np.random.choice(cities_list, p=[0.20, 0.18, 0.16, 0.16, 0.10, 0.08, 0.06, 0.06])
        c_info = CITIES_INFO[city]

        # Spatial coordinates around destination hub
        lat = c_info['lat'] + np.random.normal(0, 0.045)
        long = c_info['long'] + np.random.normal(0, 0.045)

        property_type = np.random.choice(c_info['props'])
        room_type = np.random.choice(ROOM_TYPES, p=ROOM_WEIGHTS)
        bed_type = np.random.choice(BED_TYPES, p=BED_WEIGHTS)
        cancellation_policy = np.random.choice(CANCELLATIONS, p=CANCEL_WEIGHTS)

        # Architectural specs strictly obeying real-world rental physics
        if room_type == 'Entire home/apt':
            bedrooms = int(np.random.choice([1, 2, 3, 4, 5], p=[0.38, 0.35, 0.18, 0.07, 0.02]))
            beds = int(np.random.choice([bedrooms, bedrooms + 1, bedrooms + 2], p=[0.55, 0.35, 0.10]))
            # Accommodates strictly <= beds * 2 and <= bedrooms * 2 + 2
            max_acc = min(beds * 2, bedrooms * 2 + 2)
            min_acc = max(1, bedrooms * 2 - 1)
            accommodates = int(np.random.randint(min_acc, max_acc + 1))
            bathrooms = float(np.random.choice([float(bedrooms), float(bedrooms + 0.5), float(min(bedrooms + 1, 6.0))], p=[0.60, 0.25, 0.15]))
        elif room_type == 'Private room':
            bedrooms = 1
            beds = int(np.random.choice([1, 2], p=[0.75, 0.25]))
            accommodates = int(np.random.choice([1, 2, 3], p=[0.35, 0.55, 0.10]))
            accommodates = min(accommodates, beds * 2)
            bathrooms = float(np.random.choice([1.0, 1.5], p=[0.85, 0.15]))
        else: # Shared room
            bedrooms = 1
            beds = 1
            accommodates = 1
            bathrooms = 1.0

        amenities = int(np.clip(np.random.normal(18, 7), 3, 50))
        cleaning_fee = bool(np.random.choice([True, False], p=[0.72, 0.28]))
        host_has_profile_pic = np.random.choice(['t', 'f'], p=[0.97, 0.03])
        host_identity_verified = np.random.choice(['t', 'f'], p=[0.85, 0.15])
        instant_bookable = np.random.choice(['t', 'f'], p=[0.55, 0.45])

        host_response_rate = float(np.random.choice([100.0, 95.0, 90.0, 80.0, 70.0], p=[0.70, 0.15, 0.08, 0.05, 0.02]))
        number_of_reviews = int(np.random.exponential(24))
        review_scores_rating = float(np.clip(np.random.normal(94, 5), 65, 100))

        # ==========================================================
        # TRUE DYNAMIC TEMPORAL FEATURES (Calendar & Seasonality)
        # ==========================================================
        # Sample month uniformly 1-12
        checkin_month = int(np.random.randint(1, 13))
        # Day of week: 0=Mon, 1=Tue, ..., 4=Fri, 5=Sat, 6=Sun
        day_of_week = int(np.random.randint(0, 7))
        is_weekend_val = 1 if day_of_week in [4, 5, 6] else 0  # Fri, Sat, Sun

        # Classify season category for this destination
        if checkin_month in c_info['peak_months']:
            season_category = 'peak'
            temporal_season_mult = c_info['peak_mult']
        elif checkin_month in c_info['monsoon_months']:
            season_category = 'monsoon'
            temporal_season_mult = c_info['monsoon_mult']
        else:
            season_category = 'regular'
            temporal_season_mult = 1.00

        temporal_weekend_mult = c_info['weekend_mult'] if is_weekend_val == 1 else 1.00
        combined_dynamic_mult = temporal_season_mult * temporal_weekend_mult

        # Realistic Base Price Formulation
        base = c_info['base']
        prop_mult = 1.6 if property_type in ['Villa', 'Heritage Haveli', 'Resort / Cottage'] else (1.2 if property_type in ['Loft', 'Bungalow', 'Cabin / Chalet'] else 1.0)
        room_mult = 1.0 if room_type == 'Entire home/apt' else (0.42 if room_type == 'Private room' else 0.22)
        bed_mult = 1.0 + (accommodates - 2) * 0.14 + (bedrooms - 1) * 0.18
        amenity_mult = 1.0 + (amenities - 15) * 0.012
        rating_mult = 1.0 + (review_scores_rating - 90) * 0.008 if review_scores_rating > 90 else 0.92
        host_mult = 1.05 if (host_identity_verified == 't' and instant_bookable == 't') else 1.0

        base_property_price = base * prop_mult * room_mult * max(0.5, bed_mult) * amenity_mult * rating_mult * host_mult

        # Final dynamic price integrates temporal seasonality directly into training target
        dynamic_target_price = base_property_price * combined_dynamic_mult
        noise = np.random.normal(1.0, 0.08)
        final_price_inr = max(650.0, round(dynamic_target_price * noise, -1))
        log_price = float(np.log(final_price_inr))

        rows.append({
            'id': 100000 + i,
            'log_price': log_price,
            'price_inr': final_price_inr,
            'property_type': property_type,
            'room_type': room_type,
            'amenities': amenities,
            'accommodates': accommodates,
            'bathrooms': bathrooms,
            'bed_type': bed_type,
            'cancellation_policy': cancellation_policy,
            'cleaning_fee': cleaning_fee,
            'city': city,
            'host_has_profile_pic': host_has_profile_pic,
            'host_identity_verified': host_identity_verified,
            'host_response_rate': host_response_rate,
            'instant_bookable': instant_bookable,
            'latitude': round(lat, 6),
            'longitude': round(long, 6),
            'number_of_reviews': number_of_reviews,
            'review_scores_rating': review_scores_rating,
            'bedrooms': bedrooms,
            'beds': beds,
            'checkin_month': checkin_month,
            'day_of_week': day_of_week,
            'is_weekend': is_weekend_val,
            'season_category': season_category
        })

    return pd.DataFrame(rows)

if __name__ == '__main__':
    base_dir = r"c:\Users\komal\Downloads\End-to-End-Airbnb-Price-Prediction-main\End-to-End-Airbnb-Price-Prediction-main"
    out_dir = os.path.join(base_dir, "Notebook_Experiments", "Data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Airbnb_India_Data.csv")

    df = generate_dynamic_rental_dataset(30000)
    df.to_csv(out_path, index=False)
    print(f"Generated Indian dynamic rental dataset with {len(df)} records at {out_path}")
    print(df[['city', 'property_type', 'season_category', 'is_weekend', 'price_inr']].head(10))
