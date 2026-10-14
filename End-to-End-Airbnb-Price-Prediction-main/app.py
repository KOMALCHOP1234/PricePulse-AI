import os
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.Airbnb.pipelines.Prediction_Pipeline import CustomData, PredictPipeline

app = Flask(__name__)
CORS(app)

predict_pipeline = PredictPipeline()

# Realistic Indian tourism & metropolitan centers with high-demand micro-localities
INDIAN_CITIES = {
    "Goa": {
        "lat": 15.2993, "long": 74.1240, "name": "Goa", "state": "Goa", "desc": "Beachfront & Coastal Villas",
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
        "localities": [
            {"name": "Hauz Khas Village & Green Park", "lat": 28.5494, "long": 77.2001, "tag": "Heritage Lake & Nightlife"},
            {"name": "DLF Phase 5 & Golf Course Rd", "lat": 28.4595, "long": 77.0965, "tag": "Ultra-Luxury Condos"},
            {"name": "Connaught Place & Central Delhi", "lat": 28.6304, "long": 77.2177, "tag": "Colonial Business Heart"},
            {"name": "South Extension & Greater Kailash", "lat": 28.5672, "long": 77.2433, "tag": "Posh Residential Enclave"}
        ]
    },
    "Bangalore": {
        "lat": 12.9716, "long": 77.5946, "name": "Bangalore", "state": "Karnataka", "desc": "Indiranagar & Koramangala Lofts",
        "localities": [
            {"name": "Indiranagar 100ft Road", "lat": 12.9784, "long": 77.6408, "tag": "Microbreweries & Shopping"},
            {"name": "Koramangala 4th Block", "lat": 12.9352, "long": 77.6245, "tag": "Startup Hub & Trendy Lofts"},
            {"name": "Whitefield IT Corridor", "lat": 12.9698, "long": 77.7500, "tag": "Tech Parks & Expats"},
            {"name": "Lavelle Road & UB City", "lat": 12.9719, "long": 77.5990, "tag": "Ultra-Luxury Downtown"}
        ]
    },
    "Jaipur": {
        "lat": 26.9124, "long": 75.7873, "name": "Jaipur", "state": "Rajasthan", "desc": "Pink City & Heritage Havelis",
        "localities": [
            {"name": "C-Scheme & Civil Lines", "lat": 26.9054, "long": 75.8010, "tag": "High-End Diners & Embassies"},
            {"name": "Amer Road Heritage Belt", "lat": 26.9855, "long": 75.8513, "tag": "Palaces & Fort Views"},
            {"name": "Malviya Nagar & WTP", "lat": 26.8525, "long": 75.8053, "tag": "Modern Airport Corridor"}
        ]
    },
    "Manali / Shimla": {
        "lat": 32.2432, "long": 77.1892, "name": "Manali / Shimla", "state": "Himachal Pradesh", "desc": "Himalayan Mountain Cottages",
        "localities": [
            {"name": "Old Manali & Club House", "lat": 32.2530, "long": 77.1750, "tag": "Riverside Apple Orchards"},
            {"name": "Solang Valley Snow Point", "lat": 32.3160, "long": 77.1570, "tag": "Mountain Skiing & Chalets"},
            {"name": "Shimla Mall Road & Ridge", "lat": 31.1048, "long": 77.1734, "tag": "Colonial Promenade"},
            {"name": "Mashobra Cedar Woods", "lat": 31.1270, "long": 77.2290, "tag": "Secluded Pine Retreats"}
        ]
    },
    "Hyderabad": {
        "lat": 17.3850, "long": 78.4867, "name": "Hyderabad", "state": "Telangana", "desc": "Banjara Hills & Hitec City",
        "localities": [
            {"name": "Jubilee Hills & Film Nagar", "lat": 17.4319, "long": 78.4073, "tag": "Upscale Mansions & Clubs"},
            {"name": "Hitec City & Madhapur", "lat": 17.4483, "long": 78.3758, "tag": "Cyber Towers IT Corridor"},
            {"name": "Gachibowli Financial Hub", "lat": 17.4401, "long": 78.3489, "tag": "Corporate High-Rise Suites"}
        ]
    },
    "Kolkata": {
        "lat": 22.5726, "long": 88.3639, "name": "Kolkata", "state": "West Bengal", "desc": "Park Street & Salt Lake City",
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
        "service": "PricePulse AI - Airbnb India Price Prediction API",
        "version": "3.2.0 (Dynamic Seasonality & Market Intelligence)",
        "currency": "INR",
        "endpoints": ["/api/predict", "/api/cities"]
    })

@app.route("/api/cities", methods=["GET"])
def get_cities():
    return jsonify(INDIAN_CITIES)

@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data_json = request.get_json(force=True, silent=False) or {}
        
        city = data_json.get("city", "Goa")
        default_coords = INDIAN_CITIES.get(city, INDIAN_CITIES["Goa"])
        
        property_type = data_json.get("property_type", "Villa")
        room_type = data_json.get("room_type", "Entire home/apt")
        amenities = int(data_json.get("amenities", 20))
        accommodates = int(data_json.get("accommodates", 4))
        bathrooms = float(data_json.get("bathrooms", 2.0))
        bed_type = data_json.get("bed_type", "Real Bed")
        cancellation_policy = data_json.get("cancellation_policy", "flexible")
        
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
        bedrooms = int(data_json.get("bedrooms", 2))
        beds = int(data_json.get("beds", 2))
        
        # Feature 2 parameters: Seasonality & Weekend Surge
        season = data_json.get("season", "regular").lower()  # 'regular', 'peak', 'monsoon'
        raw_weekend = data_json.get("is_weekend", False)
        is_weekend = bool(raw_weekend) if not isinstance(raw_weekend, str) else raw_weekend.lower() in ("true", "1", "yes")
        locality_name = data_json.get("locality", "")

        custom_data = CustomData(
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
            beds=beds
        )

        df = custom_data.get_data_as_dataframe()
        raw_pred = predict_pipeline.predict(df)
        base_nightly_price = round(float(np.exp(raw_pred[0])), 0)

        # Feature 2 Calculation: Multipliers
        season_multiplier = 1.35 if season == "peak" else (0.80 if season == "monsoon" else 1.00)
        weekend_multiplier = 1.15 if is_weekend else 1.00
        combined_multiplier = round(season_multiplier * weekend_multiplier, 3)

        dynamic_nightly_price = round(base_nightly_price * combined_multiplier, 0)

        # Feature 4: Market Strategy & Confidence Range (Min, Median, Max)
        budget_price = round(dynamic_nightly_price * 0.85, 0)       # 90%+ target occupancy
        recommended_price = dynamic_nightly_price                    # Optimal ML sweet spot
        premium_price = round(dynamic_nightly_price * 1.22, 0)      # High margin / peak yield

        # Realistic Financial & Host Take-Home Breakdown
        cleaning_fee_suggested = round(max(500.0, dynamic_nightly_price * 0.12), 0) if cleaning_fee else 0.0
        platform_fee_3pct = round(dynamic_nightly_price * 0.03, 0)
        net_host_takehome_nightly = dynamic_nightly_price - platform_fee_3pct

        occupancy_rate = 0.84 if season == "peak" else (0.58 if season == "monsoon" else 0.72)
        weekly_inr = round(dynamic_nightly_price * 7 * (0.90 if not is_weekend else 0.95), 0)
        monthly_inr = round(dynamic_nightly_price * 30 * occupancy_rate, 0)

        # Market Demand Tier
        if dynamic_nightly_price > 12000:
            demand_tier = "💎 Super-Luxury Signature"
        elif dynamic_nightly_price > 6000:
            demand_tier = "🔥 Prime High-Yield Category"
        elif dynamic_nightly_price > 3000:
            demand_tier = "⭐ High-Demand Sweet Spot"
        else:
            demand_tier = "🏷️ Value / High-Occupancy Tier"

        return jsonify({
            "success": True,
            "currency": "INR",
            "currency_symbol": "₹",
            "base_nightly_price": base_nightly_price,
            "predicted_nightly_price": dynamic_nightly_price,
            "season": season,
            "season_multiplier": season_multiplier,
            "is_weekend": is_weekend,
            "weekend_multiplier": weekend_multiplier,
            "combined_multiplier": combined_multiplier,
            "market_range": {
                "budget": budget_price,
                "recommended": recommended_price,
                "premium": premium_price
            },
            "financial_breakdown": {
                "gross_nightly": dynamic_nightly_price,
                "cleaning_fee_suggested": cleaning_fee_suggested,
                "airbnb_service_fee_3pct": platform_fee_3pct,
                "net_host_takehome_nightly": net_host_takehome_nightly,
                "expected_occupancy_pct": round(occupancy_rate * 100, 1)
            },
            "weekly_estimate": weekly_inr,
            "monthly_estimate": monthly_inr,
            "cleaning_fee_suggested": cleaning_fee_suggested,
            "demand_tier": demand_tier,
            "details": {
                "city": city,
                "locality": locality_name,
                "property_type": property_type,
                "room_type": room_type,
                "accommodates": accommodates,
                "bedrooms": bedrooms,
                "beds": beds,
                "bathrooms": bathrooms
            }
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 400

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)

