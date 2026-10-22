import os, sys, numpy as np, streamlit as st, pandas as pd, json
import plotly.graph_objects as go
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

st.set_page_config(
    page_title="PricePulse AI",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

CSS = """<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html,body,[class*="css"]{font-family:'Inter',sans-serif}
  .stApp{background:#111214}
  [data-testid="stSidebar"]{background:#18191c!important;border-right:1px solid #2a2b2e!important}
  [data-testid="stSidebar"] *{color:#d1d5db!important}
  .stSelectbox>div>div{background:#1f2023!important;color:#e5e7eb!important;border-color:#333!important}
  .stNumberInput input{background:#1f2023!important;color:#e5e7eb!important}
  h1,h2,h3,h4,p,label,div,span{color:#e5e7eb}
  .hero{background:linear-gradient(135deg,#ff5a5f 0%,#fc8254 100%);border-radius:18px;padding:34px 40px;text-align:center;margin-bottom:24px;box-shadow:0 16px 48px rgba(255,90,95,.25)}
  .hero h1{font-size:2.2rem;font-weight:800;color:#fff!important;margin:0}
  .hero p{color:rgba(255,255,255,.88)!important;margin:8px 0 0;font-size:.95rem}
  .card{background:#1c1d20;border:1px solid #2a2b2e;border-radius:14px;padding:20px 16px;text-align:center}
  .card .lbl{font-size:.68rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#6b7280!important;margin-bottom:6px}
  .card .val{font-size:1.7rem;font-weight:800;color:#ff5a5f!important}
  .card .sub{font-size:.72rem;color:#4b5563!important;margin-top:4px}
  .mcard{background:#1c1d20;border:1px solid #2a2b2e;border-top:3px solid #22c55e;border-radius:14px;padding:18px 14px;text-align:center}
  .mcard .lbl{font-size:.68rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#6b7280!important;margin-bottom:5px}
  .mcard .val{font-size:1.7rem;font-weight:800;color:#22c55e!important}
  .mcard .sub{font-size:.7rem;color:#4b5563!important;margin-top:3px}
  .wcard{background:#1c1d20;border:1px solid #2a2b2e;border-top:3px solid #ff5a5f;border-radius:14px;padding:18px 14px;text-align:center}
  .wcard .lbl{font-size:.68rem;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;color:#6b7280!important;margin-bottom:5px}
  .wcard .val{font-size:1.7rem;font-weight:800;color:#ff5a5f!important}
  .wcard .sub{font-size:.7rem;color:#4b5563!important;margin-top:3px}
  .model-winner{background:#1c1d20;border:2px solid #22c55e;border-radius:14px;padding:20px;text-align:center;box-shadow:0 0 24px rgba(34,197,94,.1)}
  .result{background:#1c1d20;border:2px solid #ff5a5f;border-radius:18px;padding:36px 32px;text-align:center;margin-top:16px;box-shadow:0 0 40px rgba(255,90,95,.12)}
  .result .rlbl{font-size:.78rem;letter-spacing:2.5px;text-transform:uppercase;color:#6b7280!important;margin-bottom:8px}
  .result .rval{font-size:4rem;font-weight:800;background:linear-gradient(135deg,#ff5a5f,#fc8254);-webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1}
  .result .rsub{color:#6b7280!important;margin-top:8px;font-size:.95rem}
  .sec{font-size:.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:#4b5563!important;border-bottom:1px solid #2a2b2e;padding-bottom:6px;margin:20px 0 10px}
  .ccard{background:#1c1d20;border:1px solid #2a2b2e;border-radius:10px;padding:11px 14px;margin-bottom:6px}
  .ccard-a{background:#1c1d20;border:1px solid #ff5a5f;border-radius:10px;padding:11px 14px;margin-bottom:6px;box-shadow:0 0 16px rgba(255,90,95,.12)}
  .tip{background:#1c1d20;border-left:3px solid #ff5a5f;border-radius:0 10px 10px 0;padding:10px 14px;margin-bottom:7px}
  .ph{background:#1c1d20;border:2px dashed #2a2b2e;border-radius:18px;padding:60px 32px;text-align:center;margin-top:8px}
  div[data-testid="stButton"]>button{background:linear-gradient(135deg,#ff5a5f,#fc8254)!important;color:#fff!important;border:none!important;border-radius:10px!important;font-size:1rem!important;font-weight:700!important;padding:12px!important;box-shadow:0 6px 20px rgba(255,90,95,.3)!important}
  .stTabs [data-baseweb="tab-list"]{background:#18191c;border-radius:10px;padding:4px;gap:4px}
  .stTabs [data-baseweb="tab"]{background:transparent;border-radius:8px;color:#9ca3af!important;font-weight:600;padding:8px 18px}
  .stTabs [aria-selected="true"]{background:#ff5a5f!important;color:#fff!important}
  footer{visibility:hidden}
  #MainMenu{visibility:hidden}
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

FEAT_COLS = ["property_type","room_type","amenities","accommodates","bathrooms",
             "bed_type","cancellation_policy","cleaning_fee","city",
             "host_has_profile_pic","host_identity_verified","host_response_rate",
             "instant_bookable","latitude","longitude","number_of_reviews",
             "review_scores_rating","bedrooms","beds"]

FEAT_LABELS = ["Amenities","Accommodates","Bathrooms","Latitude","Longitude",
               "Response Rate","Num Reviews","Review Score","Bedrooms","Beds",
               "Property Type","Room Type","Bed Type","Cancellation",
               "Cleaning Fee","City","Identity Verified","Instant Bookable","Profile Pic"]
CITIES = {
    "Goa": {
        "lat": 15.2993, "long": 74.1240, "emoji": "🏖", "desc": "Beachfront and Coastal Villas",
        "localities": [
            {"name": "Candolim & Sinquerim Beach", "lat": 15.5175, "long": 73.7634},
            {"name": "Baga & Calangute Strip", "lat": 15.5553, "long": 73.7517},
            {"name": "Anjuna & Vagator Cliffs", "lat": 15.5843, "long": 73.7438},
            {"name": "Panaji Heritage Fontainhas", "lat": 15.4989, "long": 73.8278},
            {"name": "Morjim & Ashwem Serenity", "lat": 15.6322, "long": 73.7371}
        ]
    },
    "Mumbai": {
        "lat": 19.0760, "long": 72.8777, "emoji": "🌆", "desc": "South Mumbai and Bandra Condos",
        "localities": [
            {"name": "Bandra West & Pali Hill", "lat": 19.0596, "long": 72.8295},
            {"name": "Juhu Beach & Tara Road", "lat": 19.0988, "long": 72.8264},
            {"name": "Colaba & Marine Drive", "lat": 18.9220, "long": 72.8347},
            {"name": "Powai Hiranandani", "lat": 19.1176, "long": 72.9060}
        ]
    },
    "Delhi-NCR": {
        "lat": 28.6139, "long": 77.2090, "emoji": "🕌", "desc": "Hauz Khas, Gurgaon and South Delhi",
        "localities": [
            {"name": "Hauz Khas Village", "lat": 28.5494, "long": 77.2001},
            {"name": "DLF Cyber City / Phase 5", "lat": 28.4595, "long": 77.0965},
            {"name": "Connaught Place Central", "lat": 28.6304, "long": 77.2177},
            {"name": "Greater Kailash Posh", "lat": 28.5672, "long": 77.2433}
        ]
    },
    "Bangalore": {
        "lat": 12.9716, "long": 77.5946, "emoji": "🌿", "desc": "Indiranagar and Koramangala Lofts",
        "localities": [
            {"name": "Indiranagar 100ft Rd", "lat": 12.9784, "long": 77.6408},
            {"name": "Koramangala 4th Block", "lat": 12.9352, "long": 77.6245},
            {"name": "Whitefield IT Corridor", "lat": 12.9698, "long": 77.7500},
            {"name": "Lavelle Road & UB City", "lat": 12.9719, "long": 77.5990}
        ]
    },
    "Jaipur": {
        "lat": 26.9124, "long": 75.7873, "emoji": "🏯", "desc": "Pink City and Heritage Havelis",
        "localities": [
            {"name": "C-Scheme & Civil Lines", "lat": 26.9054, "long": 75.8010},
            {"name": "Amer Road Heritage Belt", "lat": 26.9855, "long": 75.8513},
            {"name": "Malviya Nagar & WTP", "lat": 26.8525, "long": 75.8053}
        ]
    },
    "Manali / Shimla": {
        "lat": 32.2432, "long": 77.1892, "emoji": "🏔", "desc": "Himalayan Mountain Cottages",
        "localities": [
            {"name": "Old Manali Apple Orchards", "lat": 32.2530, "long": 77.1750},
            {"name": "Solang Valley Snow Point", "lat": 32.3160, "long": 77.1570},
            {"name": "Shimla Mall Road", "lat": 31.1048, "long": 77.1734},
            {"name": "Mashobra Pine Woods", "lat": 31.1270, "long": 77.2290}
        ]
    },
    "Hyderabad": {
        "lat": 17.3850, "long": 78.4867, "emoji": "💎", "desc": "Banjara Hills and Hitec City",
        "localities": [
            {"name": "Jubilee Hills Mansions", "lat": 17.4319, "long": 78.4073},
            {"name": "Hitec City / Madhapur", "lat": 17.4483, "long": 78.3758},
            {"name": "Gachibowli Financial Hub", "lat": 17.4401, "long": 78.3489}
        ]
    },
    "Kolkata": {
        "lat": 22.5726, "long": 88.3639, "emoji": "🎭", "desc": "Park Street and Salt Lake City",
        "localities": [
            {"name": "Park Street & Camac St", "lat": 22.5510, "long": 88.3530},
            {"name": "Salt Lake Sector V IT Hub", "lat": 22.5804, "long": 88.4378},
            {"name": "Ballygunge Southern Ave", "lat": 22.5280, "long": 88.3650}
        ]
    }
}
PROP_TYPES = ["Villa","Apartment","House","Condominium","Loft","Boutique hotel","Guesthouse","Hostel","Bungalow","Cottage"]
ROOM_TYPES = ["Entire home/apt","Private room","Shared room"]
BED_TYPES  = ["Real Bed","Futon","Pull-out Sofa","Airbed","Couch"]
CANCEL_POL = ["flexible","moderate","strict","super_strict_30","super_strict_60"]

PD = dict(paper_bgcolor="#1c1d20", plot_bgcolor="#1c1d20",
          font=dict(color="#9ca3af", family="Inter"),
          xaxis=dict(gridcolor="#2a2b2e", zerolinecolor="#2a2b2e"),
          yaxis=dict(gridcolor="#2a2b2e", zerolinecolor="#2a2b2e"),
          margin=dict(l=20, r=20, t=40, b=20))

MODEL_COLORS = {"Linear Regression": "#6b7280", "XGBoost": "#fc8254", "CatBoost (Selected)": "#22c55e"}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
ARTIFACTS_DIR = os.path.join(BASE_DIR, "Artifacts")

@st.cache_resource(show_spinner=False)
def load_all():
    from src.Airbnb.pipelines.Prediction_Pipeline import CustomData, PredictPipeline
    from src.Airbnb.utils.utils import load_object
    import pickle
    pp   = PredictPipeline()
    prep = load_object(os.path.join(ARTIFACTS_DIR, "Preprocessor.pkl"))
    cb   = load_object(os.path.join(ARTIFACTS_DIR, "Model.pkl"))
    lr   = pickle.load(open(os.path.join(ARTIFACTS_DIR, "LR_Model.pkl"),  "rb"))
    xgb  = pickle.load(open(os.path.join(ARTIFACTS_DIR, "XGB_Model.pkl"), "rb"))
    return pp, CustomData, prep, cb, lr, xgb

@st.cache_data(show_spinner=False)
def load_data():
    raw   = pd.read_csv(os.path.join(ARTIFACTS_DIR, "raw_data.csv"))
    test  = pd.read_csv(os.path.join(ARTIFACTS_DIR, "test_data.csv"))
    preds = pd.read_csv(os.path.join(ARTIFACTS_DIR, "model_predictions.csv"))
    comp  = json.load(open(os.path.join(ARTIFACTS_DIR, "model_comparison.json")))
    return raw, test, preds, comp

with st.spinner("Loading PricePulse AI..."):
    predict_pipeline, CustomData, preprocessor, catboost, lr_model, xgb_model = load_all()
    raw_df, test_df, preds_df, comp = load_data()


# Hero
st.markdown("""<div class="hero">
  <h1>💰 PricePulse AI &mdash; Rental Price Prediction Engine</h1>
  <p>End-to-end Revenue Optimization System &mdash; 30,000 Indian Property Listings &middot; 3-Model Comparison &middot; CatBoost R&sup2; = 0.977</p>
</div>""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🏠 Property Details")
    st.markdown('<div class="sec">Location & Micro-Market</div>', unsafe_allow_html=True)
    city = st.selectbox("City", list(CITIES.keys()))
    ci = CITIES[city]
    
    # Feature 3: Micro-Locality Selector
    loc_names = [l["name"] for l in ci.get("localities", [])]
    selected_locality = st.selectbox("Prime Micro-Locality", loc_names) if loc_names else "City Center"
    loc_coords = next((l for l in ci.get("localities", []) if l["name"] == selected_locality), None)
    active_lat = loc_coords["lat"] if loc_coords else ci["lat"]
    active_long = loc_coords["long"] if loc_coords else ci["long"]
    st.caption(f"{ci['emoji']} {ci['desc']} (GPS: {active_lat:.3f}°N, {active_long:.3f}°E)")

    # Feature 2: Dynamic Seasonality & Weekend Factors
    st.markdown('<div class="sec">Dynamic Pricing Factors</div>', unsafe_allow_html=True)
    season_opt = st.selectbox(
        "Demand Season",
        ["☀️ Regular Season (1.0x)", "🔥 Peak / Holiday Surge (+35%)", "🌧 Monsoon / Off-Peak (-20%)"]
    )
    is_weekend = st.checkbox("⚡ Weekend Stay? (Fri–Sun, +15% surge)", True)
    
    season_mult = 1.35 if "Peak" in season_opt else (0.80 if "Monsoon" in season_opt else 1.00)
    weekend_mult = 1.15 if is_weekend else 1.00
    combined_mult = round(season_mult * weekend_mult, 3)

    st.markdown('<div class="sec">Property</div>', unsafe_allow_html=True)
    property_type = st.selectbox("Property Type", PROP_TYPES)
    room_type     = st.selectbox("Room Type", ROOM_TYPES)
    c1, c2 = st.columns(2)
    with c1:
        bedrooms = st.number_input("Bedrooms", 0, 15, 2)
        beds     = st.number_input("Beds", 1, 25, 2)
    with c2:
        bathrooms    = st.number_input("Bathrooms", 0.5, 15.0, 2.0, 0.5)
        accommodates = st.number_input("Guests", 1, 30, 4)

    # Physical threshold validation bounds
    val_warnings = []
    if accommodates > (beds * 2):
        val_warnings.append(f"⚠️ Guests ({accommodates}) exceeds capacity for {beds} bed(s) (Max {beds * 2}).")
    if bedrooms > 0 and beds < bedrooms:
        val_warnings.append(f"⚠️ Beds ({beds}) cannot be less than bedrooms ({bedrooms}).")
    if bathrooms > (bedrooms + 2):
        val_warnings.append(f"⚠️ Bathrooms ({bathrooms}) is high for {bedrooms} bedroom(s).")
    for w in val_warnings:
        st.warning(w)
    amenities     = st.slider("Amenities", 0, 60, 20)
    bed_type      = st.selectbox("Bed Type", BED_TYPES)
    cancel_policy = st.selectbox("Cancellation Policy", CANCEL_POL)
    cleaning_fee  = st.checkbox("Cleaning Fee?", True)
    st.markdown('<div class="sec">Host Info</div>', unsafe_allow_html=True)
    host_response_rate     = st.slider("Response Rate (%)", 0, 100, 95)
    host_has_profile_pic   = st.checkbox("Has Profile Picture?", True)
    host_identity_verified = st.checkbox("Identity Verified?", True)
    instant_bookable       = st.checkbox("Instant Bookable?", True)
    st.markdown('<div class="sec">Reviews</div>', unsafe_allow_html=True)
    number_of_reviews    = st.number_input("Number of Reviews", 0, 1000, 25)
    review_scores_rating = st.slider("Review Score (out of 100)", 0, 100, 90)
    st.markdown("---")
    predict_btn = st.button("🔮 Predict Dynamic Price", use_container_width=True)

# Helper
def run_pred(br=None, rs=None):
    cd = CustomData(
        property_type=property_type, room_type=room_type, amenities=amenities,
        accommodates=accommodates, bathrooms=bathrooms, bed_type=bed_type,
        cancellation_policy=cancel_policy, cleaning_fee=cleaning_fee, city=city,
        host_has_profile_pic="t" if host_has_profile_pic else "f",
        host_identity_verified="t" if host_identity_verified else "f",
        host_response_rate=host_response_rate,
        instant_bookable="t" if instant_bookable else "f",
        latitude=active_lat, longitude=active_long,
        number_of_reviews=number_of_reviews,
        review_scores_rating=rs if rs is not None else review_scores_rating,
        bedrooms=br if br is not None else bedrooms,
        beds=br if br is not None else beds)
    return round(float(np.exp(predict_pipeline.predict(cd.get_data_as_dataframe())[0])), 0)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "💰  Price Prediction",
    "📊  Model Comparison",
    "🔥  Feature Importance",
    "🏙  Market Insights",
])

# ═══════════════════════════════════════════════════════════════════
# TAB 1 – PRICE PREDICTION
# ═══════════════════════════════════════════════════════════════════
with tab1:
    left, right = st.columns([3, 2], gap="large")
    with left:
        if predict_btn:
            with st.spinner("Calculating valuation..."):
                try:
                    base_price   = run_pred()
                    dynamic_price = round(base_price * combined_mult, 0)
                    
                    # Transparent Host Financial Ledger
                    cfee         = round(max(500.0, dynamic_price * 0.12), 0) if cleaning_fee else 0.0
                    service_fee  = round(dynamic_price * 0.03, 0)
                    net_takehome = dynamic_price - service_fee

                    # Dynamic Result Card
                    st.markdown(f"""<div class="result">
                      <div class="rlbl">Suggested Dynamic Nightly Rate</div>
                      <div class="rval">&#8377;{dynamic_price:,.0f}</div>
                      <div class="rsub">
                        per night &middot; {city} ({selected_locality}) &middot; {room_type}<br>
                        <span style="color:#22c55e;font-weight:700">Base ML: &#8377;{base_price:,.0f}</span> &middot; 
                        <span style="color:#fc8254;font-weight:700">{combined_mult}x Multiplier ({season_opt.split()[0]} {is_weekend and '+ Weekend' or ''})</span>
                      </div>
                    </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    


                    # Feature 4.2: Host Financial Ledger
                    st.markdown("#### 📋 Host Net Payout Ledger (Per Night)")
                    l1, l2, l3, l4 = st.columns(4)
                    for col, lbl, val, sub in zip(
                        [l1, l2, l3, l4],
                        ["Guest Nightly Tariff", "Cleaning Fee", "Platform Fee (3%)", "Net Host Payout"],
                        [f"&#8377;{dynamic_price:,.0f}", f"&#8377;{cfee:,.0f}", f"-&#8377;{service_fee:,.0f}", f"&#8377;{net_takehome:,.0f}"],
                        ["gross charged", "turnover fee", "platform deduction", "your take-home"]):
                        with col:
                            cls = "mcard" if lbl == "Net Host Payout" else "card"
                            st.markdown(
                                f'<div class="{cls}"><div class="lbl">{lbl}</div>'
                                f'<div class="val" style="font-size:1.25rem">{val}</div><div class="sub">{sub}</div></div>',
                                unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)
                    

                    st.markdown("**🛏 Bedroom Sensitivity Analysis**")
                    bed_range  = list(range(1, 7))
                    bed_prices = [round(run_pred(br=b) * combined_mult, 0) for b in bed_range]
                    fig_s = go.Figure(go.Bar(
                        x=[f"{b} BR" for b in bed_range], y=bed_prices,
                        marker_color=["#ff5a5f" if b == bedrooms else "#374151" for b in bed_range],
                        text=[f"&#8377;{p:,.0f}" for p in bed_prices], textposition="outside"))
                    fig_s.update_layout(**PD, height=260, showlegend=False)
                    st.plotly_chart(fig_s, use_container_width=True)

                    st.markdown("**📋 Input Summary**")
                    st.dataframe(pd.DataFrame({
                        "Feature": ["City","Micro-Locality","Season","Weekend Surge","Property","Room","Bedrooms","Beds",
                                    "Bathrooms","Guests","Amenities","Cancel","Response","Reviews","Score"],
                        "Value":   [str(city), str(selected_locality), str(season_opt), str(is_weekend), str(property_type), str(room_type),
                                    str(bedrooms), str(beds), str(bathrooms), str(accommodates),
                                    str(amenities), str(cancel_policy), f"{host_response_rate}%",
                                    str(number_of_reviews), f"{review_scores_rating}/100"]}),
                        use_container_width=True, hide_index=True)
                except Exception as e:
                    st.error(f"Prediction failed: {e}")
        else:
            st.markdown(
                '<div class="ph"><div style="font-size:3rem">🏡</div>'
                '<h3 style="color:#e5e7eb;margin:12px 0 6px">Ready to Predict</h3>'
                '<p style="color:#6b7280">Fill in details in the sidebar (including Locality & Season) and click Predict Dynamic Price</p></div>',
                unsafe_allow_html=True)

    with right:
        st.markdown("**🗺 City Insights**")
        for name, meta in CITIES.items():
            cls = "ccard-a" if name == city else "ccard"
            st.markdown(
                f'<div class="{cls}"><span style="font-size:1.1rem">{meta["emoji"]}</span>'
                f'<strong style="color:#e5e7eb;margin-left:8px">{name}</strong>'
                f'<div style="color:#6b7280;font-size:.76rem;margin-top:3px">{meta["desc"]}</div></div>',
                unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("**💡 Pricing Tips**")
        for icon, title, detail in [
            ("📸","Add profile picture","Builds trust with guests"),
            ("✅","Enable instant book","Boosts bookings by ~20%"),
            ("⭐","Collect 20+ reviews","Signals quality"),
            ("🛁","List all amenities","Raises predicted price"),
            ("🧹","Clean fee at ~12%","Optimal benchmark"),
        ]:
            st.markdown(
                f'<div class="tip"><span>{icon}</span>'
                f'<strong style="color:#e5e7eb;font-size:.86rem;margin-left:6px">{title}</strong>'
                f'<div style="color:#6b7280;font-size:.75rem;margin-top:2px">{detail}</div></div>',
                unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 2 – MODEL COMPARISON (3 Models)
# ═══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### 📊 Model Comparison — 3 Algorithms")
    st.caption("All models trained on the same 24,000 listings and evaluated on the same 6,000 held-out test listings")

    model_names = [v["label"] for v in comp.values()]
    r2_vals   = [v["r2"]   for v in comp.values()]
    rmse_vals = [v["rmse"] for v in comp.values()]
    mae_vals  = [v["mae"]  for v in comp.values()]
    mape_vals = [v["mape"] for v in comp.values()]
    colors_bar = [MODEL_COLORS[n] for n in model_names]

    # Winner banner
    st.markdown("""<div class="model-winner">
      <div style="font-size:1.5rem;font-weight:800;color:#22c55e">🏆 CatBoost Selected as Best Model</div>
      <div style="color:#9ca3af;margin-top:4px;font-size:.9rem">Highest R&sup2; (0.9768) &middot; Lowest RMSE (0.1245) &middot; Lowest MAPE (10.0%)</div>
    </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Metric cards per model
    col1, col2, col3 = st.columns(3)
    for col, key, m in zip([col1, col2, col3], comp.keys(), comp.values()):
        is_best = key == "CatBoost"
        card_cls = "mcard" if is_best else "wcard" if m["r2"] < 0.92 else "card"
        badge = " 🏆" if is_best else ""
        with col:
            st.markdown(
                f'<div class="{card_cls}">'
                f'<div class="lbl">{m["label"]}{badge}</div>'
                f'<div class="val">R² = {m["r2"]}</div>'
                f'<div class="sub">RMSE: {m["rmse"]} &middot; MAPE: {m["mape"]}%</div>'
                f'</div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Side-by-side bar charts
    bc1, bc2 = st.columns(2)
    with bc1:
        st.markdown("**R² Score Comparison (Higher is Better)**")
        fig_r2 = go.Figure(go.Bar(
            x=model_names, y=r2_vals, marker_color=colors_bar,
            text=[f"{v:.4f}" for v in r2_vals], textposition="outside"))
        fig_r2.update_layout(**PD, height=300)
        fig_r2.update_yaxes(range=[0.8, 1.0])
        st.plotly_chart(fig_r2, use_container_width=True)

    with bc2:
        st.markdown("**MAPE % Comparison (Lower is Better)**")
        fig_mape = go.Figure(go.Bar(
            x=model_names, y=mape_vals, marker_color=colors_bar,
            text=[f"{v:.1f}%" for v in mape_vals], textposition="outside"))
        fig_mape.update_layout(**PD, height=300, yaxis_title="MAPE %")
        st.plotly_chart(fig_mape, use_container_width=True)

    # Full metrics table
    st.markdown("**📋 Complete Metrics Table**")
    metrics_df = pd.DataFrame({
        "Model":    model_names,
        "R² Score": [str(v) for v in r2_vals],
        "RMSE (log)": [str(v) for v in rmse_vals],
        "MAE (log)":  [str(v) for v in mae_vals],
        "MAPE %":     [f"{v}%" for v in mape_vals],
        "RMSE (INR)": [f"₹{v['rmse_inr']:,.0f}" for v in comp.values()],
        "MAE (INR)":  [f"₹{v['mae_inr']:,.0f}" for v in comp.values()],
    })
    st.dataframe(metrics_df, use_container_width=True, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Actual vs Predicted scatter for all 3 models
    st.markdown("**Actual vs Predicted — All 3 Models (sample of 600)**")
    sc1, sc2, sc3 = st.columns(3)
    sample = preds_df.sample(600, random_state=42)
    mn = float(preds_df["y_true"].min())
    mx = float(preds_df["y_true"].max())
    for col, pred_col, name, clr in zip(
        [sc1, sc2, sc3],
        ["lr_pred", "xgb_pred", "catboost_pred"],
        model_names, colors_bar):
        with col:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=sample["y_true"], y=sample[pred_col], mode="markers",
                marker=dict(color=clr, size=4, opacity=0.5), name=name))
            fig.add_trace(go.Scatter(
                x=[mn, mx], y=[mn, mx], mode="lines",
                line=dict(color="#ffffff", dash="dash", width=1.5), name="Perfect"))
            r2 = r2_score(preds_df["y_true"], preds_df[pred_col])
            fig.update_layout(**PD, height=260, showlegend=False,
                title=dict(text=f"{name}<br>R²={r2:.4f}", font=dict(size=12, color=clr)))
            st.plotly_chart(fig, use_container_width=True)

    # Residual comparison
    st.markdown("**Residual Distribution — All 3 Models**")
    fig_res = go.Figure()
    for pred_col, name, clr in zip(
        ["lr_pred", "xgb_pred", "catboost_pred"], model_names, colors_bar):
        residuals = preds_df[pred_col] - preds_df["y_true"]
        fig_res.add_trace(go.Histogram(
            x=residuals, name=name, marker_color=clr, opacity=0.65, nbinsx=60))
    fig_res.add_vline(x=0, line_dash="dash", line_color="#ffffff", line_width=1.5)
    fig_res.update_layout(**PD, height=320, barmode="overlay",
        xaxis_title="Residual (predicted - actual)", yaxis_title="Count",
        legend=dict(x=0.75, y=0.95))
    st.plotly_chart(fig_res, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 3 – FEATURE IMPORTANCE
# ═══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 🔥 Feature Importance Analysis")
    st.caption("CatBoost built-in importances — shows which inputs drive the price prediction most")

    fi    = catboost.feature_importances_
    fi_df = pd.DataFrame({"Feature": FEAT_LABELS, "Importance": fi}).sort_values("Importance", ascending=True)
    q75   = fi_df["Importance"].quantile(0.75)
    q50   = fi_df["Importance"].quantile(0.50)
    colors = ["#ff5a5f" if v > q75 else "#fc8254" if v > q50 else "#374151" for v in fi_df["Importance"]]

    fig_fi = go.Figure(go.Bar(
        x=fi_df["Importance"], y=fi_df["Feature"], orientation="h",
        marker_color=colors,
        text=[f"{v:.2f}%" for v in fi_df["Importance"]], textposition="outside"))
    fig_fi.update_layout(**PD, height=540,
        xaxis_title="Importance Score (%)", title="CatBoost Feature Importances")
    st.plotly_chart(fig_fi, use_container_width=True)

    ft1, ft2 = st.columns(2)
    with ft1:
        st.markdown("**🎯 Top 5 Most Important**")
        for _, row in fi_df.tail(5)[::-1].iterrows():
            st.markdown(
                f'<div class="tip"><strong style="color:#ff5a5f">{row["Feature"]}</strong>'
                f'<div style="color:#9ca3af;font-size:.8rem">{row["Importance"]:.2f}% importance</div></div>',
                unsafe_allow_html=True)
    with ft2:
        st.markdown("**📉 5 Least Important**")
        for _, row in fi_df.head(5).iterrows():
            st.markdown(
                f'<div class="ccard"><strong style="color:#9ca3af">{row["Feature"]}</strong>'
                f'<div style="color:#6b7280;font-size:.8rem">{row["Importance"]:.2f}%</div></div>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("**⭐ Rating Impact on Predicted Price**")
    rating_range  = list(range(60, 101, 5))
    rating_prices = [run_pred(rs=rs) for rs in rating_range]
    fig_rat = go.Figure()
    fig_rat.add_trace(go.Scatter(
        x=rating_range, y=rating_prices, mode="lines+markers",
        line=dict(color="#ff5a5f", width=2.5), marker=dict(color="#fc8254", size=9),
        fill="tozeroy", fillcolor="rgba(255,90,95,0.08)"))
    fig_rat.update_layout(**PD, height=280,
        xaxis_title="Review Score (out of 100)", yaxis_title="Predicted Price (INR)")
    st.plotly_chart(fig_rat, use_container_width=True)

# ═══════════════════════════════════════════════════════════════════
# TAB 4 – MARKET INSIGHTS
# ═══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("### 🏙 Market Insights Dashboard")
    st.caption("Aggregated from 30,000 real Indian Property Listings")

    i1, i2, i3, i4 = st.columns(4)
    for col, lbl, val, sub in zip(
        [i1, i2, i3, i4],
        ["Total Listings","Median Price","Cities","Property Types"],
        [f"{len(raw_df):,}", f"₹{raw_df['price_inr'].median():,.0f}",
         str(raw_df["city"].nunique()), str(raw_df["property_type"].nunique())],
        ["in dataset","per night INR","across India","in dataset"]):
        with col:
            st.markdown(
                f'<div class="card"><div class="lbl">{lbl}</div>'
                f'<div class="val">{val}</div><div class="sub">{sub}</div></div>',
                unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    r1, r2 = st.columns(2)
    with r1:
        st.markdown("**Median Price by City**")
        cs = raw_df.groupby("city")["price_inr"].median().sort_values(ascending=True).reset_index()
        fig_c = go.Figure(go.Bar(
            x=cs["price_inr"], y=cs["city"], orientation="h", marker_color="#ff5a5f",
            text=[f"₹{v:,.0f}" for v in cs["price_inr"]], textposition="outside"))
        fig_c.update_layout(**PD, height=320, xaxis_title="Median Price (INR)")
        st.plotly_chart(fig_c, use_container_width=True)

    with r2:
        st.markdown("**Top Property Types**")
        pc = raw_df["property_type"].value_counts().head(8).reset_index()
        pc.columns = ["property_type","count"]
        clrs = ["#ff5a5f","#fc8254","#f97316","#fb923c","#374151","#374151","#374151","#374151"]
        fig_p = go.Figure(go.Bar(x=pc["property_type"], y=pc["count"], marker_color=clrs[:len(pc)]))
        fig_p.update_layout(**PD, height=320, xaxis_tickangle=-30, yaxis_title="Count")
        st.plotly_chart(fig_p, use_container_width=True)

    r3, r4 = st.columns(2)
    with r3:
        st.markdown("**Price by Room Type**")
        fig_box = go.Figure()
        for rt, clr in zip(ROOM_TYPES, ["#ff5a5f","#fc8254","#6b7280"]):
            s = raw_df[raw_df["room_type"] == rt]["price_inr"]
            fig_box.add_trace(go.Box(y=s, name=rt, marker_color=clr, line_color=clr))
        fig_box.update_layout(**PD, height=340, yaxis_title="Price (INR)")
        fig_box.update_yaxes(range=[0, raw_df["price_inr"].quantile(0.95)])
        st.plotly_chart(fig_box, use_container_width=True)

    with r4:
        st.markdown("**Review Score vs Price**")
        sdf = raw_df.sample(2000, random_state=42)
        fig_rv = go.Figure(go.Scatter(
            x=sdf["review_scores_rating"], y=sdf["price_inr"],
            mode="markers", marker=dict(color="#ff5a5f", size=3, opacity=0.4)))
        fig_rv.update_layout(**PD, height=340, xaxis_title="Review Score", yaxis_title="Price (INR)")
        fig_rv.update_yaxes(range=[0, raw_df["price_inr"].quantile(0.95)])
        st.plotly_chart(fig_rv, use_container_width=True)

    st.markdown("**City x Room Type Heatmap (Median INR)**")
    heat = raw_df.groupby(["city","room_type"])["price_inr"].median().unstack(fill_value=0)
    fig_h = go.Figure(go.Heatmap(
        z=heat.values, x=heat.columns.tolist(), y=heat.index.tolist(),
        colorscale=[[0,"#1c1d20"],[0.5,"#fc8254"],[1,"#ff5a5f"]],
        text=[[f"₹{v:,.0f}" for v in row] for row in heat.values],
        texttemplate="%{text}"))
    fig_h.update_layout(**PD, height=300)
    st.plotly_chart(fig_h, use_container_width=True)
