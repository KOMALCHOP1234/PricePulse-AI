import os, sys, numpy as np, streamlit as st, pandas as pd

st.set_page_config(page_title='Airbnb India Price Predictor', page_icon='🏠', layout='wide', initial_sidebar_state='expanded')

CSS = '''<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background: #111214; }
  [data-testid="stSidebar"] { background: #18191c !important; border-right: 1px solid #2a2b2e !important; }
  [data-testid="stSidebar"] * { color: #d1d5db !important; }
  section[data-testid="stSidebar"] .stSelectbox div, section[data-testid="stSidebar"] .stNumberInput input { background:#1f2023 !important; color:#e5e7eb !important; border:1px solid #333 !important; }
  .stSelectbox > div > div { background:#1f2023 !important; color:#e5e7eb !important; border-color:#333 !important; }
  .stNumberInput input { background:#1f2023 !important; color:#e5e7eb !important; }
  .stSlider [data-baseweb='slider'] div { background:#ff5a5f !important; }
  .stCheckbox span { border-color:#ff5a5f !important; }
  h1,h2,h3,h4,p,label,div,span { color:#e5e7eb; }
  .hero { background: linear-gradient(135deg, #ff5a5f 0%, #fc8254 100%); border-radius:18px; padding:36px 40px; text-align:center; margin-bottom:24px; box-shadow:0 16px 48px rgba(255,90,95,.25); }
  .hero h1 { font-size:2.5rem; font-weight:800; color:#fff!important; margin:0; letter-spacing:-0.5px; }
  .hero p { color:rgba(255,255,255,.88)!important; margin:8px 0 0; font-size:1rem; }
  .card { background:#1c1d20; border:1px solid #2a2b2e; border-radius:14px; padding:22px 18px; text-align:center; transition:transform .2s; }
  .card:hover { transform:translateY(-3px); }
  .card .lbl { font-size:.72rem; font-weight:700; letter-spacing:1.5px; text-transform:uppercase; color:#6b7280!important; margin-bottom:6px; }
  .card .val { font-size:1.85rem; font-weight:800; color:#ff5a5f!important; }
  .card .sub { font-size:.76rem; color:#4b5563!important; margin-top:4px; }
  .result { background:#1c1d20; border:2px solid #ff5a5f; border-radius:18px; padding:36px 32px; text-align:center; margin-top:16px; box-shadow:0 0 40px rgba(255,90,95,.15); }
  .result .rlbl { font-size:.78rem; letter-spacing:2.5px; text-transform:uppercase; color:#6b7280!important; margin-bottom:8px; }
  .result .rval { font-size:4rem; font-weight:800; background:linear-gradient(135deg,#ff5a5f,#fc8254); -webkit-background-clip:text; -webkit-text-fill-color:transparent; line-height:1.1; }
  .result .rsub { color:#6b7280!important; margin-top:8px; font-size:.95rem; }
  .sec { font-size:.68rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; color:#4b5563!important; border-bottom:1px solid #2a2b2e; padding-bottom:6px; margin:20px 0 10px; }
  .city-card { background:#1c1d20; border-radius:10px; padding:11px 14px; margin-bottom:6px; }
  .city-card-active { background:#1c1d20; border-radius:10px; padding:11px 14px; margin-bottom:6px; border:1px solid #ff5a5f; box-shadow:0 0 16px rgba(255,90,95,.12); }
  .tip { background:#1c1d20; border-left:3px solid #ff5a5f; border-radius:0 10px 10px 0; padding:10px 14px; margin-bottom:7px; }
  .placeholder { background:#1c1d20; border:2px dashed #2a2b2e; border-radius:18px; padding:60px 32px; text-align:center; margin-top:8px; }
  div[data-testid="stButton"]>button { background:linear-gradient(135deg,#ff5a5f,#fc8254)!important; color:#fff!important; border:none!important; border-radius:10px!important; font-size:1rem!important; font-weight:700!important; padding:12px!important; box-shadow:0 6px 20px rgba(255,90,95,.3)!important; transition:transform .15s, box-shadow .15s !important; }
  div[data-testid="stButton"]>button:hover { transform:translateY(-2px)!important; box-shadow:0 10px 28px rgba(255,90,95,.45)!important; }
  .stDataFrame { background:#1c1d20 !important; border-radius:12px !important; }
  footer { visibility:hidden; }
  #MainMenu { visibility:hidden; }
</style>'''
st.markdown(CSS, unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_pipeline():
    from src.Airbnb.pipelines.Prediction_Pipeline import CustomData, PredictPipeline
    return PredictPipeline(), CustomData

with st.spinner('Loading model...'):
    predict_pipeline, CustomData = load_pipeline()

CITIES = {
    'Goa':             {'lat':15.2993,'long':74.1240,'emoji':'🏖','desc':'Beachfront and Coastal Villas'},
    'Mumbai':          {'lat':19.0760,'long':72.8777,'emoji':'🌆','desc':'South Mumbai and Bandra Condos'},
    'Delhi-NCR':       {'lat':28.6139,'long':77.2090,'emoji':'🕌','desc':'Hauz Khas, Gurgaon and South Delhi'},
    'Bangalore':       {'lat':12.9716,'long':77.5946,'emoji':'🌿','desc':'Indiranagar and Koramangala Lofts'},
    'Jaipur':          {'lat':26.9124,'long':75.7873,'emoji':'🏯','desc':'Pink City and Heritage Havelis'},
    'Manali / Shimla': {'lat':32.2432,'long':77.1892,'emoji':'🏔','desc':'Himalayan Mountain Cottages'},
    'Hyderabad':       {'lat':17.3850,'long':78.4867,'emoji':'💎','desc':'Banjara Hills and Hitec City'},
    'Kolkata':         {'lat':22.5726,'long':88.3639,'emoji':'🎭','desc':'Park Street and Salt Lake City'},
}

PROP_TYPES  = ['Villa','Apartment','House','Condominium','Loft','Boutique hotel','Guesthouse','Hostel','Bungalow','Cottage']
ROOM_TYPES  = ['Entire home/apt','Private room','Shared room']
BED_TYPES   = ['Real Bed','Futon','Pull-out Sofa','Airbed','Couch']
CANCEL_POL  = ['flexible','moderate','strict','super_strict_30','super_strict_60']

st.markdown('<div class="hero"><h1>🏠 Airbnb India Price Predictor</h1><p>AI-powered nightly price estimate trained on real Indian Airbnb listings</p></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('## 🏠 Property Details')
    st.markdown('<div class="sec">Location</div>', unsafe_allow_html=True)
    city = st.selectbox('City', list(CITIES.keys()))
    ci = CITIES[city]
    st.caption(f"{ci['emoji']}  {ci['desc']}")
    st.markdown('<div class="sec">Property</div>', unsafe_allow_html=True)
    property_type = st.selectbox('Property Type', PROP_TYPES)
    room_type     = st.selectbox('Room Type', ROOM_TYPES)
    c1,c2 = st.columns(2)
    with c1:
        bedrooms = st.number_input('Bedrooms', 0, 20, 2)
        beds     = st.number_input('Beds', 1, 30, 2)
    with c2:
        bathrooms    = st.number_input('Bathrooms', 0.0, 20.0, 1.0, 0.5)
        accommodates = st.number_input('Guests', 1, 30, 4)
    amenities     = st.slider('Amenities', 0, 60, 20)
    bed_type      = st.selectbox('Bed Type', BED_TYPES)
    cancel_policy = st.selectbox('Cancellation Policy', CANCEL_POL)
    cleaning_fee  = st.checkbox('Cleaning Fee Charged?', True)
    st.markdown('<div class="sec">Host Info</div>', unsafe_allow_html=True)
    host_response_rate     = st.slider('Response Rate (%)', 0, 100, 95)
    host_has_profile_pic   = st.checkbox('Has Profile Picture?', True)
    host_identity_verified = st.checkbox('Identity Verified?', True)
    instant_bookable       = st.checkbox('Instant Bookable?', True)
    st.markdown('<div class="sec">Reviews</div>', unsafe_allow_html=True)
    number_of_reviews    = st.number_input('Number of Reviews', 0, 1000, 25)
    review_scores_rating = st.slider('Review Score (out of 100)', 0, 100, 90)
    st.markdown('---')
    predict_btn = st.button('🔮  Predict Price', use_container_width=True)

main_col, info_col = st.columns([3,2], gap='large')

with main_col:
    if predict_btn:
        with st.spinner('Calculating...'):
            try:
                cd = CustomData(
                    property_type=property_type, room_type=room_type, amenities=amenities,
                    accommodates=accommodates, bathrooms=bathrooms, bed_type=bed_type,
                    cancellation_policy=cancel_policy, cleaning_fee=cleaning_fee, city=city,
                    host_has_profile_pic='t' if host_has_profile_pic else 'f',
                    host_identity_verified='t' if host_identity_verified else 'f',
                    host_response_rate=host_response_rate,
                    instant_bookable='t' if instant_bookable else 'f',
                    latitude=ci['lat'], longitude=ci['long'],
                    number_of_reviews=number_of_reviews,
                    review_scores_rating=review_scores_rating,
                    bedrooms=bedrooms, beds=beds)
                df = cd.get_data_as_dataframe()
                raw = predict_pipeline.predict(df)
                price   = round(float(np.exp(raw[0])), 0)
                weekly  = round(price * 7 * 0.90, 0)
                monthly = round(price * 30 * 0.72, 0)
                cfee    = round(max(500.0, price * 0.12), 0) if cleaning_fee else 0.0
                st.markdown(f'''<div class="result">
                  <div class="rlbl">Predicted Nightly Rate</div>
                  <div class="rval">&#8377;{price:,.0f}</div>
                  <div class="rsub">per night &middot; {city} &middot; {room_type}</div>
                </div>''', unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)
                k1,k2,k3 = st.columns(3)
                for col,lbl,val,sub in zip([k1,k2,k3],
                    ['Weekly Estimate','Monthly Estimate','Suggested Cleaning'],
                    [f'&#8377;{weekly:,.0f}',f'&#8377;{monthly:,.0f}',f'&#8377;{cfee:,.0f}' if cleaning_fee else '&#8377;0'],
                    ['90% occupancy','72% occupancy','one-time fee']):
                    with col:
                        st.markdown(f'<div class="card"><div class="lbl">{lbl}</div><div class="val">{val}</div><div class="sub">{sub}</div></div>', unsafe_allow_html=True)
                st.markdown('<br>', unsafe_allow_html=True)
                st.markdown('#### 📋 Input Summary')
                st.dataframe(pd.DataFrame({'Feature':['City','Property','Room','Bedrooms','Beds','Bathrooms','Guests','Amenities','Cancel','Response','Reviews','Score'],'Value':[city,property_type,room_type,bedrooms,beds,bathrooms,accommodates,amenities,cancel_policy,f'{host_response_rate}%',number_of_reviews,f'{review_scores_rating}/100']}), use_container_width=True, hide_index=True)
            except Exception as e:
                st.error(f'Prediction failed: {e}')
    else:
        st.markdown('<div class="placeholder"><div style="font-size:3rem;">🏡</div><h3 style="color:#e5e7eb;margin:12px 0 6px;">Ready to Predict</h3><p style="color:#6b7280;">Fill in details in the sidebar and click Predict Price</p></div>', unsafe_allow_html=True)

with info_col:
    st.markdown('#### 🗺 City Insights')
    for name, meta in CITIES.items():
        cls = 'city-card-active' if name==city else 'city-card'
        st.markdown(f'<div class="{cls}"><span style="font-size:1.1rem;">{meta["emoji"]}</span><strong style="color:#e5e7eb;margin-left:8px;">{name}</strong><div style="color:#6b7280;font-size:.76rem;margin-top:3px;">{meta["desc"]}</div></div>', unsafe_allow_html=True)
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown('#### 💡 Pricing Tips')
    for icon,title,detail in [('📸','Add profile picture','Builds trust with guests'),('✅','Enable instant book','Boosts bookings by ~20%'),('⭐','Collect 20+ reviews','Signals quality to guests'),('🛁','List all amenities','Directly raises predicted price'),('🧹','Set cleaning fee at ~12%','Optimal pricing benchmark')]:
        st.markdown(f'<div class="tip"><span>{icon}</span><strong style="color:#e5e7eb;font-size:.86rem;margin-left:6px;">{title}</strong><div style="color:#6b7280;font-size:.75rem;margin-top:2px;">{detail}</div></div>', unsafe_allow_html=True)
