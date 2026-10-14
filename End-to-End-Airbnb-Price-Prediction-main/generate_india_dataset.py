import os
import numpy as np
import pandas as pd

np.random.seed(42)

# Define Indian destinations, coordinates, and market parameters
CITIES_INFO = {
    'Mumbai': {
        'lat': 19.0760, 'long': 72.8777, 'base': 5200, 
        'props': ['Apartment', 'Condominium', 'Loft', 'Serviced apartment', 'House']
    },
    'Goa': {
        'lat': 15.2993, 'long': 74.1240, 'base': 6800, 
        'props': ['Villa', 'Bungalow', 'Apartment', 'Guesthouse', 'Bed & Breakfast', 'Resort / Cottage']
    },
    'Delhi-NCR': {
        'lat': 28.6139, 'long': 77.2090, 'base': 4200, 
        'props': ['Apartment', 'House', 'Loft', 'Condominium', 'Townhouse']
    },
    'Bangalore': {
        'lat': 12.9716, 'long': 77.5946, 'base': 3900, 
        'props': ['Apartment', 'Condominium', 'House', 'Villa', 'Guesthouse']
    },
    'Jaipur': {
        'lat': 26.9124, 'long': 75.7873, 'base': 3600, 
        'props': ['Heritage Haveli', 'Villa', 'House', 'Apartment', 'Bed & Breakfast']
    },
    'Hyderabad': {
        'lat': 17.3850, 'long': 78.4867, 'base': 3400, 
        'props': ['Apartment', 'Condominium', 'House', 'Villa']
    },
    'Kolkata': {
        'lat': 22.5726, 'long': 88.3639, 'base': 2800, 
        'props': ['Apartment', 'House', 'Condominium', 'Bed & Breakfast']
    },
    'Manali / Shimla': {
        'lat': 32.2432, 'long': 77.1892, 'base': 4800, 
        'props': ['Cabin / Chalet', 'Cottage', 'Villa', 'House', 'Apartment']
    }
}

ROOM_TYPES = ['Entire home/apt', 'Private room', 'Shared room']
ROOM_WEIGHTS = [0.60, 0.35, 0.05]

BED_TYPES = ['Real Bed', 'Futon', 'Pull-out Sofa', 'Airbed']
BED_WEIGHTS = [0.88, 0.06, 0.04, 0.02]

CANCELLATIONS = ['flexible', 'moderate', 'strict', 'super_strict_30']
CANCEL_WEIGHTS = [0.45, 0.35, 0.16, 0.04]

ALL_PROPERTIES = [
    'Apartment', 'House', 'Condominium', 'Villa', 'Bungalow', 
    'Loft', 'Guesthouse', 'Bed & Breakfast', 'Serviced apartment', 
    'Heritage Haveli', 'Cabin / Chalet', 'Cottage', 'Resort / Cottage', 'Townhouse'
]

def generate_indian_airbnb_dataset(n_samples=25000):
    rows = []
    cities_list = list(CITIES_INFO.keys())
    
    for i in range(n_samples):
        city = np.random.choice(cities_list, p=[0.20, 0.18, 0.16, 0.16, 0.10, 0.08, 0.06, 0.06])
        c_info = CITIES_INFO[city]
        
        # Spatial jitter around the city center (~5-12km)
        lat = c_info['lat'] + np.random.normal(0, 0.045)
        long = c_info['long'] + np.random.normal(0, 0.045)
        
        property_type = np.random.choice(c_info['props'])
        room_type = np.random.choice(ROOM_TYPES, p=ROOM_WEIGHTS)
        bed_type = np.random.choice(BED_TYPES, p=BED_WEIGHTS)
        cancellation_policy = np.random.choice(CANCELLATIONS, p=CANCEL_WEIGHTS)
        
        # Accommodates, bedrooms, beds, bathrooms
        if room_type == 'Entire home/apt':
            bedrooms = np.random.choice([1, 2, 3, 4, 5], p=[0.38, 0.35, 0.18, 0.07, 0.02])
            accommodates = max(1, bedrooms * 2 + np.random.choice([-1, 0, 1, 2]))
            beds = max(1, bedrooms + np.random.choice([0, 1, 2]))
            bathrooms = float(max(1, bedrooms + np.random.choice([0, -1, 1]) if bedrooms > 1 else 1))
        elif room_type == 'Private room':
            bedrooms = 1
            accommodates = np.random.choice([1, 2, 3], p=[0.35, 0.55, 0.10])
            beds = np.random.choice([1, 2], p=[0.75, 0.25])
            bathrooms = float(np.random.choice([1.0, 1.5]))
        else: # Shared room
            bedrooms = 1
            accommodates = 1
            beds = 1
            bathrooms = 1.0
            
        amenities = int(np.clip(np.random.normal(18, 7), 3, 50))
        cleaning_fee = bool(np.random.choice([True, False], p=[0.72, 0.28]))
        host_has_profile_pic = np.random.choice(['t', 'f'], p=[0.97, 0.03])
        host_identity_verified = np.random.choice(['t', 'f'], p=[0.85, 0.15])
        instant_bookable = np.random.choice(['t', 'f'], p=[0.55, 0.45])
        
        host_response_rate = float(np.random.choice([100.0, 95.0, 90.0, 80.0, 70.0], p=[0.70, 0.15, 0.08, 0.05, 0.02]))
        number_of_reviews = int(np.random.exponential(24))
        review_scores_rating = float(np.clip(np.random.normal(94, 5), 65, 100))
        
        # Calculate realistic price in Indian Rupees (INR)
        base = c_info['base']
        
        # Multipliers based on market mechanics
        prop_mult = 1.6 if property_type in ['Villa', 'Heritage Haveli', 'Resort / Cottage'] else (1.2 if property_type in ['Loft', 'Bungalow', 'Cabin / Chalet'] else 1.0)
        room_mult = 1.0 if room_type == 'Entire home/apt' else (0.42 if room_type == 'Private room' else 0.22)
        bed_mult = 1.0 + (accommodates - 2) * 0.14 + (bedrooms - 1) * 0.18
        amenity_mult = 1.0 + (amenities - 15) * 0.012
        rating_mult = 1.0 + (review_scores_rating - 90) * 0.008 if review_scores_rating > 90 else 0.92
        host_mult = 1.05 if (host_identity_verified == 't' and instant_bookable == 't') else 1.0
        
        price_inr = base * prop_mult * room_mult * max(0.5, bed_mult) * amenity_mult * rating_mult * host_mult
        # Add realistic market noise
        noise = np.random.normal(1.0, 0.12)
        final_price_inr = max(650.0, round(price_inr * noise, -1)) # Round to nearest 10 rupees
        
        log_price = np.log(final_price_inr)
        
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
            'beds': beds
        })
        
    df = pd.DataFrame(rows)
    return df

if __name__ == '__main__':
    out_dir = r"c:\Users\komal\Downloads\End-to-End-Airbnb-Price-Prediction-main\End-to-End-Airbnb-Price-Prediction-main\Notebook_Experiments\Data"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "Airbnb_India_Data.csv")
    df = generate_indian_airbnb_dataset(30000)
    df.to_csv(out_path, index=False)
    print(f"Generated Indian Airbnb dataset with {len(df)} records at {out_path}")
    print(df[['city', 'property_type', 'price_inr']].head(10))
