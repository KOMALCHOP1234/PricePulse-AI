import os
import sys
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from src.Airbnb.pipelines.Prediction_Pipeline import CustomData, PredictPipeline
from src.Airbnb.utils.utils import load_object

app = Flask(__name__)
CORS(app)

predict_pipeline = PredictPipeline()

# Load trained CatBoost model for feature importance extraction
MODEL_PATH = os.path.join(BASE_DIR, "Artifacts", "Model.pkl")
catboost_model = None
try:
    catboost_model = load_object(MODEL_PATH)
except Exception as e:
    print(f"Warning: Could not load CatBoost model: {e}")

FEATURE_NAMES = [
    'amenities', 'accommodates', 'bathrooms', 'latitude', 'longitude', 
    'host_response_rate', 'number_of_reviews', 'review_scores_rating', 
    'bedrooms', 'beds', 'checkin_month', 'day_of_week', 'is_weekend',
    'property_type', 'room_type', 'bed_type', 'cancellation_policy', 
    'cleaning_fee', 'city', 'host_identity_verified', 'instant_bookable', 
    'host_has_profile_pic', 'season_category'
]

FEATURE_DISPLAY_LABELS = {
    'room_type': 'Room Type (Entire vs Private/Shared)',
    'property_type': 'Property Type',
    'accommodates': 'Guest Capacity (Accommodates)',
    'city': 'Destination City',
    'season_category': 'Demand Season (Peak / Regular / Monsoon)',
    'is_weekend': 'Weekend Stay Indicator',
    'checkin_month': 'Check-in Month (Seasonality)',
    'day_of_week': 'Day of Week',
    'longitude': 'Longitude (Micro-Location)',
    'latitude': 'Latitude (Micro-Location)',
    'bedrooms': 'Bedrooms Count',
    'bathrooms': 'Bathrooms Count',
    'amenities': 'Amenities Count',
    'review_scores_rating': 'Review Score Rating',
    'beds': 'Beds Count',
    'number_of_reviews': 'Number of Reviews',
    'instant_bookable': 'Instant Bookable Flag',
    'host_identity_verified': 'Host Identity Verified',
    'host_response_rate': 'Host Response Rate (%)',
    'cancellation_policy': 'Cancellation Policy',
    'bed_type': 'Bed Type',
    'cleaning_fee': 'Cleaning Fee Required',
    'host_has_profile_pic': 'Host Profile Picture'
}

INDIAN_CITIES = {
    "Goa": {
        "lat": 15.2993, "long": 74.1240, "name": "Goa", "state": "Goa", "desc": "Beachfront & Coastal Villas",
        "peak_months": "Nov-Feb (Sunburn, Beach Season)",
        "monsoon_months": "Jun-Aug (Heavy Monsoon)",
        "localities": [
            {"name": "Candolim & Sinquerim Beach", "lat": 15.5175, "long": 73.7634, "tag": "Beachside Luxury"},
            {"name": "Baga & Calangute Strip", "lat": 15.5553, "long": 73.7517, "tag": "Nightlife & Water Sports"},
            {"name": "Anjuna & Vagator Cliffs", "lat": 15.5843, "long": 73.7438, "tag": "Boho & Sunset Cafes"},
            {"name": "Panaji Heritage Fontainhas", "lat": 15.4989, "long": 73.8278, "tag": "Portuguese Architecture"},
            {"name": "Morjim & Ashwem Serenity", "lat": 15.6322, "long": 73.7371, "tag": "Quiet Coastal Villas"}
        ]
    },
    "Mumbai": {
        "lat": 19.0760, "long": 72.8777, "name": "Mumbai", "state": "Maharashtra", "desc": "South Mumbai & Bandra Condos",
        "peak_months": "Oct-Feb (Winter Peak)",
        "monsoon_months": "Jul-Aug (Monsoon)",
        "localities": [
            {"name": "Bandra West & Pali Hill", "lat": 19.0596, "long": 72.8295, "tag": "Celebrity & Boutique Cafes"},
            {"name": "Juhu Beach & Tara Road", "lat": 19.0988, "long": 72.8264, "tag": "Seafront High-Rise"},
            {"name": "Colaba & Marine Drive", "lat": 18.9220, "long": 72.8347, "tag": "Historic South Bombay"},
            {"name": "Powai Hiranandani", "lat": 19.1176, "long": 72.9060, "tag": "Lakeside Modern Townships"},
            {"name": "Andheri West Lokhandwala", "lat": 19.1363, "long": 72.8277, "tag": "Media Hub & Connectivity"}
        ]
    },
    "Delhi-NCR": {
        "lat": 28.6139, "long": 77.2090, "name": "Delhi-NCR", "state": "Delhi", "desc": "Hauz Khas, Gurgaon & South Delhi",
        "peak_months": "Oct-Mar (Winter Tourist Season)",
        "monsoon_months": "Jul-Aug (Monsoon)",
        "localities": [
            {"name": "Hauz Khas Village & Green Park", "lat": 28.5494, "long": 77.2001, "tag": "Heritage Lake & Nightlife"},
            {"name": "DLF Phase 5 & Golf Course Rd", "lat": 28.4595, "long": 77.0965, "tag": "Ultra-Luxury Condos"},
            {"name": "Connaught Place & Central Delhi", "lat": 28.6304, "long": 77.2177, "tag": "Colonial Business Heart"},
            {"name": "South Extension & Greater Kailash", "lat": 28.5672, "long": 77.2433, "tag": "Posh Residential Enclave"}
        ]
    },
    "Bangalore": {
        "lat": 12.9716, "long": 77.5946, "name": "Bangalore", "state": "Karnataka", "desc": "Indiranagar & Koramangala Lofts",
        "peak_months": "Oct-Jan (Tech Conferences & Mild Winter)",
        "monsoon_months": "Jun-Aug (Monsoon)",
        "localities": [
            {"name": "Indiranagar 100ft Road", "lat": 12.9784, "long": 77.6408, "tag": "Microbreweries & Shopping"},
            {"name": "Koramangala 4th Block", "lat": 12.9352, "long": 77.6245, "tag": "Startup Hub & Trendy Lofts"},
            {"name": "Whitefield IT Corridor", "lat": 12.9698, "long": 77.7500, "tag": "Tech Parks & Expats"},
            {"name": "Lavelle Road & UB City", "lat": 12.9719, "long": 77.5990, "tag": "Ultra-Luxury Downtown"}
        ]
    },
    "Jaipur": {
        "lat": 26.9124, "long": 75.7873, "name": "Jaipur", "state": "Rajasthan", "desc": "Pink City & Heritage Havelis",
        "peak_months": "Oct-Mar (Palaces & Literary Festival)",
        "monsoon_months": "Jun-Aug (Low Season)",
        "localities": [
            {"name": "C-Scheme & Civil Lines", "lat": 26.9054, "long": 75.8010, "tag": "High-End Diners & Embassies"},
            {"name": "Amer Road Heritage Belt", "lat": 26.9855, "long": 75.8513, "tag": "Palaces & Fort Views"},
            {"name": "Malviya Nagar & WTP", "lat": 26.8525, "long": 75.8053, "tag": "Modern Airport Corridor"}
        ]
    },
    "Manali / Shimla": {
        "lat": 32.2432, "long": 77.1892, "name": "Manali / Shimla", "state": "Himachal Pradesh", "desc": "Himalayan Mountain Cottages",
        "peak_months": "May-Jun & Dec-Jan (Snow & Summer Escape)",
        "monsoon_months": "Jul-Aug (Landslide Season)",
        "localities": [
            {"name": "Old Manali & Club House", "lat": 32.2530, "long": 77.1750, "tag": "Riverside Apple Orchards"},
            {"name": "Solang Valley Snow Point", "lat": 32.3160, "long": 77.1570, "tag": "Mountain Skiing & Chalets"},
            {"name": "Shimla Mall Road & Ridge", "lat": 31.1048, "long": 77.1734, "tag": "Colonial Promenade"},
            {"name": "Mashobra Cedar Woods", "lat": 31.1270, "long": 77.2290, "tag": "Secluded Pine Retreats"}
        ]
    },
    "Hyderabad": {
        "lat": 17.3850, "long": 78.4867, "name": "Hyderabad", "state": "Telangana", "desc": "Banjara Hills & Hitec City",
        "peak_months": "Oct-Feb (Winter Conventions)",
        "monsoon_months": "Jun-Aug (Monsoon)",
        "localities": [
            {"name": "Jubilee Hills & Film Nagar", "lat": 17.4319, "long": 78.4073, "tag": "Upscale Mansions & Clubs"},
            {"name": "Hitec City & Madhapur", "lat": 17.4483, "long": 78.3758, "tag": "Cyber Towers IT Corridor"},
            {"name": "Gachibowli Financial Hub", "lat": 17.4401, "long": 78.3489, "tag": "Corporate High-Rise Suites"}
        ]
    },
    "Kolkata": {
        "lat": 22.5726, "long": 88.3639, "name": "Kolkata", "state": "West Bengal", "desc": "Park Street & Salt Lake City",
        "peak_months": "Oct-Jan (Durga Puja & Winter)",
        "monsoon_months": "Jun-Aug (Monsoon)",
        "localities": [
            {"name": "Park Street & Camac Street", "lat": 22.5510, "long": 88.3530, "tag": "Heritage Nightlife & Cafes"},
            {"name": "Salt Lake Sector V", "lat": 22.5804, "long": 88.4378, "tag": "IT Hub & Planned Avenues"},
            {"name": "Ballygunge & Southern Ave", "lat": 22.5280, "long": 88.3650, "tag": "Old Aristocratic South Cal"}
        ]
    }
}

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "online",
        "service": "Dynamic Pricing AI - Short-Term Rental AI Valuation Engine",
        "version": "5.0.0 (Native Dynamic Temporal Model, CatBoost R2=0.9903)",
        "currency": "INR",
        "endpoints": ["/api/predict", "/api/cities", "/api/feature_importance"]
    })

@app.route("/api/cities", methods=["GET"])
def get_cities():
    return jsonify(INDIAN_CITIES)

@app.route("/api/feature_importance", methods=["GET"])
def get_feature_importance():
    try:
        if catboost_model is None or not hasattr(catboost_model, "feature_importances_"):
            return jsonify({"success": False, "error": "Model not loaded"}), 500

        importances = catboost_model.feature_importances_
        feature_data = []
        for name, score in zip(FEATURE_NAMES, importances):
            feature_data.append({
                "feature": name,
                "label": FEATURE_DISPLAY_LABELS.get(name, name),
                "importance": round(float(score), 3)
            })

        feature_data.sort(key=lambda x: x["importance"], reverse=True)

        return jsonify({
            "success": True,
            "model": "CatBoostRegressor (Dynamic Temporal)",
            "r2_score": 0.9903,
            "features": feature_data
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data_json = request.get_json(force=True, silent=False) or {}

        city = data_json.get("city", "Goa")
        default_coords = INDIAN_CITIES.get(city, INDIAN_CITIES["Goa"])

        property_type = data_json.get("property_type", "Villa")
        room_type = data_json.get("room_type", "Entire home/apt")
        accommodates = int(data_json.get("accommodates", 4))
        bedrooms = int(data_json.get("bedrooms", 2))
        beds = int(data_json.get("beds", 2))
        bathrooms = float(data_json.get("bathrooms", 2.0))
        amenities = int(data_json.get("amenities", 20))
        bed_type = data_json.get("bed_type", "Real Bed")
        cancellation_policy = data_json.get("cancellation_policy", "flexible")

        # =========================================================================
        # REAL-WORLD ARCHITECTURAL & CAPACITY VALIDATION BOUNDS
        # (Derived from physical rental standards & training dataset distribution)
        # =========================================================================
        validation_errors = []

        if room_type == "Shared room":
            if bedrooms != 1:
                validation_errors.append("A Shared room must have exactly 1 bedroom.")
            if beds > 1:
                validation_errors.append("A Shared room booking corresponds to 1 bed.")
            if accommodates > 1:
                validation_errors.append("A Shared room listing corresponds to 1 guest capacity.")
            if bathrooms > 1.0:
                validation_errors.append("A Shared room cannot exceed 1.0 bathroom.")

        elif room_type == "Private room":
            if bedrooms != 1:
                validation_errors.append("A Private room listing must have exactly 1 private bedroom.")
            if beds > 2:
                validation_errors.append("A Private room cannot have more than 2 beds (single/double).")
            if accommodates > 3:
                validation_errors.append("A Private room cannot accommodate more than 3 guests.")
            if bathrooms > 2.0:
                validation_errors.append("A Private room cannot exceed 2.0 bathrooms.")

        elif room_type == "Entire home/apt":
            if bedrooms < 1 or bedrooms > 5:
                validation_errors.append(f"Bedrooms ({bedrooms}) must be between 1 and 5.")

            max_guests_allowed = bedrooms * 2 + 2
            max_beds_allowed = bedrooms + 2
            max_baths_allowed = float(bedrooms + 1)

            if accommodates > max_guests_allowed:
                validation_errors.append(
                    f"A {bedrooms}-bedroom property cannot accommodate {accommodates} guests. "
                    f"Maximum allowed capacity is {max_guests_allowed} guests (up to 2 per bedroom + living sleeper)."
                )

            if beds > max_beds_allowed:
                validation_errors.append(
                    f"A {bedrooms}-bedroom property cannot have {beds} beds. Maximum allowed is {max_beds_allowed} beds."
                )

            if beds < bedrooms:
                validation_errors.append(
                    f"Number of beds ({beds}) cannot be less than number of bedrooms ({bedrooms})."
                )

            if bathrooms > max_baths_allowed:
                validation_errors.append(
                    f"A {bedrooms}-bedroom property cannot have {bathrooms} bathrooms. Maximum realistic is {max_baths_allowed} bathrooms."
                )

        if accommodates > (beds * 2):
            validation_errors.append(
                f"Guest count ({accommodates}) exceeds capacity for {beds} bed(s) (Maximum {beds * 2} guests, 2 per bed)."
            )

        if validation_errors:
            return jsonify({
                "success": False,
                "error": "Validation failed: " + " | ".join(validation_errors),
                "validation_errors": validation_errors
            }), 422

        raw_clean = data_json.get("cleaning_fee", True)
        cleaning_fee = bool(raw_clean) if not isinstance(raw_clean, str) else raw_clean.lower() in ("true", "1", "yes")

        raw_profile_pic = data_json.get("host_has_profile_pic", "t")
        host_has_profile_pic = "t" if str(raw_profile_pic).lower() in ("t", "true", "1", "yes") else "f"

        raw_verified = data_json.get("host_identity_verified", "t")
        host_identity_verified = "t" if str(raw_verified).lower() in ("t", "true", "1", "yes") else "f"

        host_response_rate = float(data_json.get("host_response_rate", 100))
        raw_instant = data_json.get("instant_bookable", "t")
        instant_bookable = "t" if str(raw_instant).lower() in ("t", "true", "1", "yes") else "f"

        latitude = float(data_json.get("latitude", default_coords["lat"]))
        longitude = float(data_json.get("longitude", default_coords["long"]))
        number_of_reviews = int(data_json.get("number_of_reviews", 30))
        review_scores_rating = float(data_json.get("review_scores_rating", 95))

        # Temporal Inputs mapping into the native ML feature space
        season_category = str(data_json.get("season", "regular")).lower()
        if season_category not in ["regular", "peak", "monsoon"]:
            season_category = "regular"

        raw_weekend = data_json.get("is_weekend", False)
        is_weekend_bool = bool(raw_weekend) if not isinstance(raw_weekend, str) else raw_weekend.lower() in ("true", "1", "yes")
        is_weekend_int = 1 if is_weekend_bool else 0
        day_of_week = 5 if is_weekend_bool else 2  # Friday/Sat vs Tuesday

        # Representative month for seasonality: Peak=December (12), Monsoon=July (7), Regular=April (4)
        if season_category == "peak":
            checkin_month = 12
        elif season_category == "monsoon":
            checkin_month = 7
        else:
            checkin_month = 4

        locality_name = data_json.get("locality", "")

        # 1. Native ML Dynamic Prediction (CatBoost model natively evaluated)
        custom_data_dynamic = CustomData(
            property_type=property_type,
            room_type=room_type,
            amenities=amenities,
            accommodates=accommodates,
            bathrooms=bathrooms,
            bed_type=bed_type,
            cancellation_policy=cancellation_policy,
            cleaning_fee=cleaning_fee,
            city=city,
            host_has_profile_pic=host_has_profile_pic,
            host_identity_verified=host_identity_verified,
            host_response_rate=host_response_rate,
            instant_bookable=instant_bookable,
            latitude=latitude,
            longitude=longitude,
            number_of_reviews=number_of_reviews,
            review_scores_rating=review_scores_rating,
            bedrooms=bedrooms,
            beds=beds,
            checkin_month=checkin_month,
            day_of_week=day_of_week,
            is_weekend=is_weekend_int,
            season_category=season_category
        )

        df_dyn = custom_data_dynamic.get_data_as_dataframe()
        raw_pred_dyn = predict_pipeline.predict(df_dyn)
        dynamic_nightly_price = round(float(np.exp(raw_pred_dyn[0])), 0)

        # Baseline Comparison (Regular Season Weekday Baseline evaluated natively)
        custom_data_base = CustomData(
            property_type=property_type,
            room_type=room_type,
            amenities=amenities,
            accommodates=accommodates,
            bathrooms=bathrooms,
            bed_type=bed_type,
            cancellation_policy=cancellation_policy,
            cleaning_fee=cleaning_fee,
            city=city,
            host_has_profile_pic=host_has_profile_pic,
            host_identity_verified=host_identity_verified,
            host_response_rate=host_response_rate,
            instant_bookable=instant_bookable,
            latitude=latitude,
            longitude=longitude,
            number_of_reviews=number_of_reviews,
            review_scores_rating=review_scores_rating,
            bedrooms=bedrooms,
            beds=beds,
            checkin_month=4,
            day_of_week=2,
            is_weekend=0,
            season_category="regular"
        )
        df_base = custom_data_base.get_data_as_dataframe()
        raw_pred_base = predict_pipeline.predict(df_base)
        base_nightly_price = round(float(np.exp(raw_pred_base[0])), 0)

        # Ratio learned natively by CatBoost
        dynamic_ratio = round(dynamic_nightly_price / max(1.0, base_nightly_price), 3)

        # Payout ledger
        platform_fee_pct = 0.03
        platform_fee_amount = round(dynamic_nightly_price * platform_fee_pct, 0)
        net_host_takehome = dynamic_nightly_price - platform_fee_amount

        city_meta = INDIAN_CITIES.get(city, INDIAN_CITIES["Goa"])

        return jsonify({
            "success": True,
            "currency": "INR",
            "currency_symbol": "₹",
            "base_nightly_price": base_nightly_price,
            "predicted_nightly_price": dynamic_nightly_price,
            "dynamic_factors": {
                "destination": city,
                "season": season_category,
                "checkin_month": checkin_month,
                "is_weekend": is_weekend_bool,
                "dynamic_surge_ratio": dynamic_ratio,
                "market_context": city_meta["peak_months"] if season_category == "peak" else (city_meta["monsoon_months"] if season_category == "monsoon" else "Standard Off-Peak Baseline")
            },
            "financial_breakdown": {
                "gross_nightly": dynamic_nightly_price,
                "platform_service_fee": platform_fee_amount,
                "platform_service_fee_pct": 3.0,
                "net_host_takehome_nightly": net_host_takehome
            },
            "property_summary": {
                "city": city,
                "locality": locality_name,
                "property_type": property_type,
                "room_type": room_type,
                "accommodates": accommodates,
                "bedrooms": bedrooms,
                "beds": beds,
                "bathrooms": bathrooms,
                "amenities_count": amenities
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
