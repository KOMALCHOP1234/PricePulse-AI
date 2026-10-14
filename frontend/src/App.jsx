import React, { useState, useEffect } from 'react';
import { 
  Building2, 
  MapPin, 
  ShieldCheck, 
  Zap, 
  Sparkles, 
  Users, 
  CheckCircle2, 
  Info, 
  Sliders, 
  Calendar, 
  Sun, 
  Flame, 
  CloudRain, 
  TrendingUp, 
  BarChart3, 
  Award, 
  Layers, 
  Compass, 
  ChevronRight,
  ArrowRight,
  ArrowLeft
} from 'lucide-react';
import confetti from 'canvas-confetti';

const INDIAN_CITIES = {
  "Goa": { 
    name: "Goa", state: "Goa", icon: "🏖️",
    desc: "Beachfront and Coastal Villas",
    lat: 15.2993, long: 74.1240, medianPrice: 6800,
    localities: [
      { name: "Candolim & Sinquerim Beach", lat: 15.5175, long: 73.7634, tag: "Beachside Luxury" },
      { name: "Baga & Calangute Strip", lat: 15.5553, long: 73.7517, tag: "Nightlife & Sports" },
      { name: "Anjuna & Vagator Cliffs", lat: 15.5843, long: 73.7438, tag: "Boho Cafes" },
      { name: "Panaji Heritage Fontainhas", lat: 15.4989, long: 73.8278, tag: "Portuguese Heritage" },
      { name: "Morjim & Ashwem Serenity", lat: 15.6322, long: 73.7371, tag: "Quiet Coastal" }
    ]
  },
  "Mumbai": { 
    name: "Mumbai", state: "Maharashtra", icon: "🌆",
    desc: "South Mumbai and Bandra Condos",
    lat: 19.0760, long: 72.8777, medianPrice: 5200,
    localities: [
      { name: "Bandra West & Pali Hill", lat: 19.0596, long: 72.8295, tag: "Celebrity Enclave" },
      { name: "Juhu Beach & Tara Road", lat: 19.0988, long: 72.8264, tag: "Seafront High-Rise" },
      { name: "Colaba & Marine Drive", lat: 18.9220, long: 72.8347, tag: "Historic South" },
      { name: "Powai Hiranandani", lat: 19.1176, long: 72.9060, tag: "Lakeside Modern" }
    ]
  },
  "Delhi-NCR": { 
    name: "Delhi-NCR", state: "Delhi", icon: "🏛️",
    desc: "Hauz Khas, Gurgaon and South Delhi",
    lat: 28.6139, long: 77.2090, medianPrice: 4200,
    localities: [
      { name: "Hauz Khas Village", lat: 28.5494, long: 77.2001, tag: "Heritage Lake" },
      { name: "DLF Cyber City / Ph 5", lat: 28.4595, long: 77.0965, tag: "Ultra-Luxury" },
      { name: "Connaught Place Central", lat: 28.6304, long: 77.2177, tag: "Colonial Heart" },
      { name: "Greater Kailash", lat: 28.5672, long: 77.2433, tag: "Posh Residential" }
    ]
  },
  "Bangalore": { 
    name: "Bangalore", state: "Karnataka", icon: "💻",
    desc: "Indiranagar and Koramangala Lofts",
    lat: 12.9716, long: 77.5946, medianPrice: 3900,
    localities: [
      { name: "Indiranagar 100ft Road", lat: 12.9784, long: 77.6408, tag: "Breweries & Diners" },
      { name: "Koramangala 4th Block", lat: 12.9352, long: 77.6245, tag: "Startup Hub" },
      { name: "Whitefield IT Corridor", lat: 12.9698, long: 77.7500, tag: "Tech Parks" },
      { name: "Lavelle Road & UB City", lat: 12.9719, long: 77.5990, tag: "Downtown Luxury" }
    ]
  },
  "Jaipur": { 
    name: "Jaipur", state: "Rajasthan", icon: "🏯",
    desc: "Pink City and Heritage Havelis",
    lat: 26.9124, long: 75.7873, medianPrice: 3600,
    localities: [
      { name: "C-Scheme & Civil Lines", lat: 26.9054, long: 75.8010, tag: "High-End Diners" },
      { name: "Amer Road Heritage Belt", lat: 26.9855, long: 75.8513, tag: "Palace Views" },
      { name: "Malviya Nagar & WTP", lat: 26.8525, long: 75.8053, tag: "Airport Corridor" }
    ]
  },
  "Manali / Shimla": { 
    name: "Manali/Shimla", state: "Himachal", icon: "🏔️",
    desc: "Himalayan Mountain Cottages",
    lat: 32.2432, long: 77.1892, medianPrice: 4800,
    localities: [
      { name: "Old Manali Apple Orchards", lat: 32.2530, long: 77.1750, tag: "Riverside" },
      { name: "Solang Valley Snow Point", lat: 32.3160, long: 77.1570, tag: "Skiing & Chalets" },
      { name: "Shimla Mall Road & Ridge", lat: 31.1048, long: 77.1734, tag: "Colonial Promenade" },
      { name: "Mashobra Pine Woods", lat: 31.1270, long: 77.2290, tag: "Secluded Retreats" }
    ]
  },
  "Hyderabad": { 
    name: "Hyderabad", state: "Telangana", icon: "💎",
    desc: "Banjara Hills and Hitec City",
    lat: 17.3850, long: 78.4867, medianPrice: 3400,
    localities: [
      { name: "Jubilee Hills Mansions", lat: 17.4319, long: 78.4073, tag: "Upscale Clubs" },
      { name: "Hitec City / Madhapur", lat: 17.4483, long: 78.3758, tag: "Cyber Towers" },
      { name: "Gachibowli Financial Hub", lat: 17.4401, long: 78.3489, tag: "Corporate Suites" }
    ]
  },
  "Kolkata": { 
    name: "Kolkata", state: "West Bengal", icon: "🎭",
    desc: "Park Street and Salt Lake City",
    lat: 22.5726, long: 88.3639, medianPrice: 2800,
    localities: [
      { name: "Park Street & Camac St", lat: 22.5510, long: 88.3530, tag: "Heritage Cafes" },
      { name: "Salt Lake Sector V IT Hub", lat: 22.5804, long: 88.4378, tag: "Planned Township" },
      { name: "Ballygunge Southern Ave", lat: 22.5280, long: 88.3650, tag: "Classic South" }
    ]
  }
};

const MODEL_BENCHMARK = [
  { name: "Linear Regression", r2: 0.8937, rmse: 0.2665, mae: 0.2119, mape: 21.31, rmse_inr: 2230, mae_inr: 1315, color: "#64748B", rank: "#3" },
  { name: "XGBoost", r2: 0.9755, rmse: 0.1280, mae: 0.1016, mape: 10.28, rmse_inr: 987, mae_inr: 613, color: "#FB923C", rank: "#2" },
  { name: "CatBoost (Selected)", r2: 0.9768, rmse: 0.1245, mae: 0.0987, mape: 10.00, rmse_inr: 950, mae_inr: 594, color: "#10B981", rank: "🏆 #1 Winner" }
];

const FEATURE_IMPORTANCES = [
  { feature: "Accommodates (Guests)", score: 26.8, color: "#FF385C" },
  { feature: "Bathrooms", score: 18.4, color: "#FF385C" },
  { feature: "Bedrooms", score: 15.2, color: "#FB923C" },
  { feature: "Room Type (Entire vs Private)", score: 12.6, color: "#FB923C" },
  { feature: "Indian City / Market", score: 9.8, color: "#FBBF24" },
  { feature: "Amenities Count", score: 6.4, color: "#60A5FA" },
  { feature: "Review Score Rating", score: 4.2, color: "#34D399" },
  { feature: "Cancellation Policy", score: 2.5, color: "#94A3B8" },
  { feature: "Host Identity Verified", score: 1.8, color: "#94A3B8" },
  { feature: "Instant Bookable", score: 1.2, color: "#94A3B8" },
  { feature: "Bed Type", score: 0.7, color: "#CBD5E1" },
  { feature: "Host Profile Pic", score: 0.4, color: "#CBD5E1" }
];

const PRESETS = [
  {
    name: "Goa Beach Villa",
    city: "Goa",
    locality: "Candolim & Sinquerim Beach",
    property_type: "Villa",
    room_type: "Entire home/apt",
    accommodates: 6,
    bedrooms: 3,
    beds: 3,
    bathrooms: 3,
    amenities: 28,
    season: "peak",
    is_weekend: true
  },
  {
    name: "Bandra Sea-View Condo",
    city: "Mumbai",
    locality: "Bandra West & Pali Hill",
    property_type: "Apartment",
    room_type: "Entire home/apt",
    accommodates: 3,
    bedrooms: 2,
    beds: 2,
    bathrooms: 2,
    amenities: 22,
    season: "regular",
    is_weekend: true
  },
  {
    name: "Jaipur Royal Haveli",
    city: "Jaipur",
    locality: "Amer Road Heritage Belt",
    property_type: "Heritage Haveli",
    room_type: "Entire home/apt",
    accommodates: 8,
    bedrooms: 4,
    beds: 5,
    bathrooms: 4,
    amenities: 32,
    season: "peak",
    is_weekend: false
  },
  {
    name: "Manali Pine Chalet",
    city: "Manali / Shimla",
    locality: "Old Manali Apple Orchards",
    property_type: "Cabin / Chalet",
    room_type: "Entire home/apt",
    accommodates: 4,
    bedrooms: 2,
    beds: 2,
    bathrooms: 2,
    amenities: 18,
    season: "regular",
    is_weekend: true
  },
  {
    name: "Bangalore Tech Studio",
    city: "Bangalore",
    locality: "Koramangala 4th Block",
    property_type: "Apartment",
    room_type: "Entire home/apt",
    accommodates: 2,
    bedrooms: 1,
    beds: 1,
    bathrooms: 1,
    amenities: 16,
    season: "regular",
    is_weekend: false
  }
];

export default function App() {
  const [mainTab, setMainTab] = useState("predict"); // 'predict', 'models', 'features', 'market'
  const [activeStep, setActiveStep] = useState(1);

  const [formData, setFormData] = useState({
    city: "Goa",
    locality: "Candolim & Sinquerim Beach",
    property_type: "Villa",
    room_type: "Entire home/apt",
    amenities: 25,
    accommodates: 6,
    bedrooms: 3,
    beds: 3,
    bathrooms: 3,
    bed_type: "Real Bed",
    cancellation_policy: "flexible",
    cleaning_fee: true,
    host_has_profile_pic: "t",
    host_identity_verified: "t",
    host_response_rate: 100,
    instant_bookable: "t",
    latitude: 15.5175,
    longitude: 73.7634,
    number_of_reviews: 42,
    review_scores_rating: 97,
    season: "peak",
    is_weekend: true
  });

  const [loading, setLoading] = useState(false);
  const [prediction, setPrediction] = useState({
    nightly: 27666,
    base_nightly: 17826,
    weekly: 183979,
    monthly: 697183,
    cleaning: 3320,
    service_fee: 830,
    net_takehome: 26836,
    occupancy_pct: 84,
    demand_tier: "💎 Super-Luxury Signature",
    market_range: {
      budget: 23516,
      recommended: 27666,
      premium: 33753
    },
    season_mult: 1.35,
    weekend_mult: 1.15,
    combined_mult: 1.552
  });

  const [selectedPreset, setSelectedPreset] = useState("Goa Beach Villa");
  const [apiError, setApiError] = useState(null);

  const handleCitySelect = (cityName) => {
    const cityData = INDIAN_CITIES[cityName];
    const defaultLoc = cityData?.localities?.[0];
    setFormData(prev => ({
      ...prev,
      city: cityName,
      locality: defaultLoc ? defaultLoc.name : "",
      latitude: defaultLoc ? defaultLoc.lat : cityData.lat,
      longitude: defaultLoc ? defaultLoc.long : cityData.long
    }));
  };

  const handleLocalitySelect = (loc) => {
    setFormData(prev => ({
      ...prev,
      locality: loc.name,
      latitude: loc.lat,
      longitude: loc.long
    }));
  };

  const applyPreset = (preset) => {
    setSelectedPreset(preset.name);
    const cityData = INDIAN_CITIES[preset.city];
    const targetLoc = cityData?.localities?.find(l => l.name === preset.locality) || cityData?.localities?.[0];
    
    setFormData(prev => ({
      ...prev,
      ...preset,
      locality: targetLoc ? targetLoc.name : "",
      latitude: targetLoc ? targetLoc.lat : cityData.lat,
      longitude: targetLoc ? targetLoc.long : cityData.long
    }));
  };

  const runPrediction = async () => {
    setLoading(true);
    setApiError(null);
    try {
      const res = await fetch("http://127.0.0.1:5000/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData)
      });
      const data = await res.json();
      if (data.success) {
        setPrediction({
          nightly: data.predicted_nightly_price,
          base_nightly: data.base_nightly_price || Math.round(data.predicted_nightly_price / (data.combined_multiplier || 1)),
          weekly: data.weekly_estimate,
          monthly: data.monthly_estimate,
          cleaning: data.cleaning_fee_suggested,
          service_fee: data.financial_breakdown?.airbnb_service_fee_3pct || Math.round(data.predicted_nightly_price * 0.03),
          net_takehome: data.financial_breakdown?.net_host_takehome_nightly || (data.predicted_nightly_price - Math.round(data.predicted_nightly_price * 0.03)),
          occupancy_pct: data.financial_breakdown?.expected_occupancy_pct || 75,
          demand_tier: data.demand_tier || "⭐ High-Demand Sweet Spot",
          market_range: data.market_range || {
            budget: Math.round(data.predicted_nightly_price * 0.85),
            recommended: data.predicted_nightly_price,
            premium: Math.round(data.predicted_nightly_price * 1.22)
          },
          season_mult: data.season_multiplier || 1.0,
          weekend_mult: data.weekend_multiplier || 1.0,
          combined_mult: data.combined_multiplier || 1.0
        });

        confetti({
          particleCount: 40,
          spread: 60,
          origin: { y: 0.85 },
          colors: ['#FF385C', '#10B981', '#3B82F6']
        });
      } else {
        setApiError(data.error || "Prediction request was rejected");
      }
    } catch (err) {
      setApiError("Unable to connect to Flask API server at http://127.0.0.1:5000.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runPrediction();
  }, []);

  const currentCityData = INDIAN_CITIES[formData.city] || INDIAN_CITIES["Goa"];

  return (
    <div>
      {/* Top Header */}
      <header className="header-nav">
        <a href="#" className="brand">
          <svg width="28" height="28" viewBox="0 0 32 32" fill="currentColor">
            <path d="M16 1c2.008 0 3.463.963 4.751 3.269l.533 1.025c1.954 3.83 4.29 8.65 6.079 12.69 1.157 2.614 1.83 4.887 1.83 6.816 0 4.542-3.411 7.2-7.994 7.2-3.155 0-5.46-1.554-6.845-3.328l-.354-.467-.354.467c-1.385 1.774-3.69 3.328-6.845 3.328-4.583 0-7.994-2.658-7.994-7.2 0-1.929.673-4.202 1.83-6.816l.51-1.144C2.934 12.77 5.27 7.95 7.224 4.12l.533-1.025C9.045 1.794 10.5 1 12.508 1h3.484zM16 3.125c-1.314 0-2.316.657-3.279 2.457l-.462.89C10.36 10.15 8.04 14.93 6.275 18.92c-1.056 2.385-1.572 4.294-1.572 5.88 0 3.264 2.314 4.975 5.494 4.975 2.508 0 4.417-1.385 5.409-3.385l.394-.852.394.852c.992 2 2.901 3.385 5.409 3.385 3.18 0 5.494-1.711 5.494-4.975 0-1.586-.516-3.495-1.572-5.88l-.49-1.096c-1.765-3.99-4.085-8.77-5.986-12.448l-.462-.89C19.824 3.782 18.822 3.125 17.508 3.125H16zm0 13.625c1.782 0 3.228 1.446 3.228 3.229 0 1.55-1.107 2.842-2.574 3.161l-.229.023-.425.045c-1.782 0-3.228-1.446-3.228-3.229 0-1.55 1.107-2.842 2.574-3.161l.229-.023.425-.045z" />
          </svg>
          <span>PricePulse <span style={{ color: 'var(--dark)' }}>AI</span></span>
        </a>

        {/* 4 Application Top Tabs */}
        <div style={{ display: 'flex', gap: '6px', background: '#F1F5F9', padding: '4px', borderRadius: '10px' }}>
          <button 
            className={`tab-btn ${mainTab === 'predict' ? 'active' : ''}`}
            onClick={() => setMainTab('predict')}
            style={{ padding: '6px 14px', fontSize: '0.82rem' }}
          >
            💰 Price Prediction
          </button>
          <button 
            className={`tab-btn ${mainTab === 'models' ? 'active' : ''}`}
            onClick={() => setMainTab('models')}
            style={{ padding: '6px 14px', fontSize: '0.82rem' }}
          >
            📊 Model Comparison
          </button>
          <button 
            className={`tab-btn ${mainTab === 'features' ? 'active' : ''}`}
            onClick={() => setMainTab('features')}
            style={{ padding: '6px 14px', fontSize: '0.82rem' }}
          >
            🔥 Feature Importance
          </button>
          <button 
            className={`tab-btn ${mainTab === 'market' ? 'active' : ''}`}
            onClick={() => setMainTab('market')}
            style={{ padding: '6px 14px', fontSize: '0.82rem' }}
          >
            🏙 Market Insights
          </button>
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <span className="brand-badge">CatBoost Engine • R² 0.976</span>
        </div>
      </header>

      {/* Main Container */}
      <main className="app-container">
        
        {/* TAB 1: PRICE PREDICTION WORKFLOW */}
        {mainTab === 'predict' && (
          <div>
            <div className="hero-compact">
              <div>
                <h1>Indian Airbnb Dynamic Revenue Engine</h1>
                <p>Simulate pricing with seasonal multipliers, micro-neighborhood intelligence, and market confidence tiers.</p>
              </div>
              <div style={{ fontSize: '0.82rem', color: 'var(--muted)' }}>
                Target: <strong style={{ color: 'var(--dark)' }}>{formData.city}</strong> • {formData.locality}
              </div>
            </div>

            {/* Presets Strip */}
            <div className="presets-strip">
              <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase', marginRight: '4px' }}>
                Quick Presets:
              </span>
              {PRESETS.map((p) => (
                <button
                  key={p.name}
                  className={`preset-chip ${selectedPreset === p.name ? 'active' : ''}`}
                  onClick={() => applyPreset(p)}
                >
                  <Sparkles size={12} color={selectedPreset === p.name ? '#FFF' : 'var(--primary)'} />
                  {p.name}
                </button>
              ))}
            </div>

            {apiError && (
              <div style={{
                background: '#FEE2E2', color: '#991B1B', padding: '12px 16px', borderRadius: '10px',
                marginBottom: '18px', fontSize: '0.85rem', fontWeight: 500, display: 'flex', alignItems: 'center', gap: '8px'
              }}>
                <Info size={16} />
                <span>{apiError}</span>
              </div>
            )}

            <div className="main-grid">
              
              {/* Left Form: Step-based Workflow */}
              <div>
                <div className="tabs-container">
                  <button 
                    className={`tab-btn ${activeStep === 1 ? 'active' : ''}`}
                    onClick={() => setActiveStep(1)}
                  >
                    <MapPin size={16} color={activeStep === 1 ? 'var(--primary)' : 'currentColor'} />
                    <span>1. Location & Space</span>
                  </button>
                  <button 
                    className={`tab-btn ${activeStep === 2 ? 'active' : ''}`}
                    onClick={() => setActiveStep(2)}
                  >
                    <TrendingUp size={16} color={activeStep === 2 ? 'var(--primary)' : 'currentColor'} />
                    <span>2. Dynamic Season</span>
                  </button>
                  <button 
                    className={`tab-btn ${activeStep === 3 ? 'active' : ''}`}
                    onClick={() => setActiveStep(3)}
                  >
                    <Sliders size={16} color={activeStep === 3 ? 'var(--primary)' : 'currentColor'} />
                    <span>3. Amenities & Badges</span>
                  </button>
                </div>

                <div className="form-card">
                  {/* Step 1: Location & Space */}
                  {activeStep === 1 && (
                    <div className="tab-panel">
                      <div>
                        <div className="panel-header">
                          <h3 className="panel-title">
                            <MapPin size={18} color="var(--primary)" /> Indian Tourist & Business Centers
                          </h3>
                          <p className="panel-subtitle">Select your city and primary micro-market locality</p>
                        </div>

                        <div className="city-grid" style={{ marginTop: '12px' }}>
                          {Object.entries(INDIAN_CITIES).map(([cityKey, cityInfo]) => {
                            const isSelected = formData.city === cityKey;
                            return (
                              <div
                                key={cityKey}
                                className={`city-card ${isSelected ? 'active' : ''}`}
                                onClick={() => handleCitySelect(cityKey)}
                              >
                                <span className="city-card-icon">{cityInfo.icon}</span>
                                <span className="city-card-name">{cityInfo.name}</span>
                                <span className="city-card-state">{cityInfo.state}</span>
                              </div>
                            );
                          })}
                        </div>
                      </div>

                      <div className="locality-box">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <label className="field-label" style={{ marginBottom: 0 }}>
                            Prime Micro-Localities in {formData.city}
                          </label>
                          <span style={{ fontSize: '0.72rem', color: 'var(--muted)' }}>
                            GPS: {formData.latitude.toFixed(3)}°N, {formData.longitude.toFixed(3)}°E
                          </span>
                        </div>

                        <div className="locality-chips-wrapper">
                          {currentCityData.localities?.map((loc) => {
                            const isSelected = formData.locality === loc.name;
                            return (
                              <button
                                key={loc.name}
                                type="button"
                                className={`locality-chip ${isSelected ? 'active' : ''}`}
                                onClick={() => handleLocalitySelect(loc)}
                              >
                                <span>{loc.name}</span>
                                <span className="locality-tag">{loc.tag}</span>
                              </button>
                            );
                          })}
                        </div>
                      </div>

                      <div className="input-row">
                        <div className="field-group">
                          <label className="field-label">Property Architecture</label>
                          <select 
                            className="field-select"
                            value={formData.property_type}
                            onChange={(e) => setFormData({ ...formData, property_type: e.target.value })}
                          >
                            <option value="Villa">Luxury Villa</option>
                            <option value="Apartment">Modern Apartment</option>
                            <option value="Heritage Haveli">Heritage Haveli</option>
                            <option value="Cabin / Chalet">Mountain Cabin/Chalet</option>
                            <option value="Condominium">Condominium</option>
                            <option value="Bungalow">Independent Bungalow</option>
                            <option value="Loft">Penthouse / Loft</option>
                            <option value="Cottage">Cottage / Farmhouse</option>
                            <option value="Bed & Breakfast">Homestay / B&B</option>
                          </select>
                        </div>

                        <div className="field-group">
                          <label className="field-label">Listing Privacy Type</label>
                          <select 
                            className="field-select"
                            value={formData.room_type}
                            onChange={(e) => setFormData({ ...formData, room_type: e.target.value })}
                          >
                            <option value="Entire home/apt">Entire Place (Full Home)</option>
                            <option value="Private room">Private Room</option>
                            <option value="Shared room">Shared Room / Dorm</option>
                          </select>
                        </div>
                      </div>

                      <div>
                        <label className="field-label" style={{ marginBottom: '8px', display: 'block' }}>
                          Capacity Configuration
                        </label>
                        <div className="input-row">
                          <div className="counter-box">
                            <span style={{ fontSize: '0.82rem', color: 'var(--muted)' }}>Guests</span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <button 
                                type="button" className="counter-btn" disabled={formData.accommodates <= 1}
                                onClick={() => setFormData(p => ({ ...p, accommodates: p.accommodates - 1 }))}
                              >-</button>
                              <span className="counter-val">{formData.accommodates}</span>
                              <button 
                                type="button" className="counter-btn" disabled={formData.accommodates >= 16}
                                onClick={() => setFormData(p => ({ ...p, accommodates: p.accommodates + 1 }))}
                              >+</button>
                            </div>
                          </div>

                          <div className="counter-box">
                            <span style={{ fontSize: '0.82rem', color: 'var(--muted)' }}>Bedrooms</span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <button 
                                type="button" className="counter-btn" disabled={formData.bedrooms <= 0}
                                onClick={() => setFormData(p => ({ ...p, bedrooms: p.bedrooms - 1 }))}
                              >-</button>
                              <span className="counter-val">{formData.bedrooms}</span>
                              <button 
                                type="button" className="counter-btn" disabled={formData.bedrooms >= 10}
                                onClick={() => setFormData(p => ({ ...p, bedrooms: p.bedrooms + 1 }))}
                              >+</button>
                            </div>
                          </div>

                          <div className="counter-box">
                            <span style={{ fontSize: '0.82rem', color: 'var(--muted)' }}>Beds</span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <button 
                                type="button" className="counter-btn" disabled={formData.beds <= 1}
                                onClick={() => setFormData(p => ({ ...p, beds: p.beds - 1 }))}
                              >-</button>
                              <span className="counter-val">{formData.beds}</span>
                              <button 
                                type="button" className="counter-btn" disabled={formData.beds >= 16}
                                onClick={() => setFormData(p => ({ ...p, beds: p.beds + 1 }))}
                              >+</button>
                            </div>
                          </div>

                          <div className="counter-box">
                            <span style={{ fontSize: '0.82rem', color: 'var(--muted)' }}>Bathrooms</span>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                              <button 
                                type="button" className="counter-btn" disabled={formData.bathrooms <= 1}
                                onClick={() => setFormData(p => ({ ...p, bathrooms: Math.max(1, p.bathrooms - 1) }))}
                              >-</button>
                              <span className="counter-val">{formData.bathrooms}</span>
                              <button 
                                type="button" className="counter-btn" disabled={formData.bathrooms >= 8}
                                onClick={() => setFormData(p => ({ ...p, bathrooms: p.bathrooms + 1 }))}
                              >+</button>
                            </div>
                          </div>
                        </div>
                      </div>

                      <div className="step-nav-footer">
                        <span style={{ fontSize: '0.78rem', color: 'var(--muted)' }}>Step 1 of 3</span>
                        <button type="button" className="btn-primary-step" onClick={() => setActiveStep(2)}>
                          <span>Next: Dynamic Pricing</span>
                          <ArrowRight size={15} />
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Step 2: Dynamic Season & Surge */}
                  {activeStep === 2 && (
                    <div className="tab-panel">
                      <div className="panel-header">
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                          <h3 className="panel-title">
                            <TrendingUp size={18} color="var(--primary)" /> Seasonal Demand & Surge Factors
                          </h3>
                          <span className="brand-badge">{prediction.combined_mult}x Rate Multiplier</span>
                        </div>
                        <p className="panel-subtitle">Model seasonal influxes, festival peaks, and weekend stay surcharges</p>
                      </div>

                      <div className="season-grid">
                        <div 
                          className={`season-card ${formData.season === 'regular' ? 'active' : ''}`}
                          onClick={() => setFormData({ ...formData, season: 'regular' })}
                        >
                          <div className="season-card-header">
                            <span className="season-card-title"><Sun size={15} color="#F59E0B" /> Regular</span>
                            <span className="season-mult-pill">1.00x Base</span>
                          </div>
                          <p className="season-card-desc">Standard tourist demand with steady occupancy (~72%).</p>
                        </div>

                        <div 
                          className={`season-card ${formData.season === 'peak' ? 'active' : ''}`}
                          onClick={() => setFormData({ ...formData, season: 'peak' })}
                        >
                          <div className="season-card-header">
                            <span className="season-card-title"><Flame size={15} color="#FF385C" /> Peak Surge</span>
                            <span className="season-mult-pill">+35% Surge</span>
                          </div>
                          <p className="season-card-desc">Diwali, Christmas/New Year, Sunburn, Long Holidays.</p>
                        </div>

                        <div 
                          className={`season-card ${formData.season === 'monsoon' ? 'active' : ''}`}
                          onClick={() => setFormData({ ...formData, season: 'monsoon' })}
                        >
                          <div className="season-card-header">
                            <span className="season-card-title"><CloudRain size={15} color="#3B82F6" /> Monsoon / Low</span>
                            <span className="season-mult-pill">-20% Discount</span>
                          </div>
                          <p className="season-card-desc">Stabilization discount to preserve occupancy (~58%).</p>
                        </div>
                      </div>

                      <div 
                        className={`weekend-toggle-bar ${formData.is_weekend ? 'active' : ''}`}
                        onClick={() => setFormData(p => ({ ...p, is_weekend: !p.is_weekend }))}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                          <div style={{
                            width: '32px', height: '32px', borderRadius: '50%',
                            background: formData.is_weekend ? '#3B82F6' : '#E2E8F0',
                            color: formData.is_weekend ? '#FFF' : '#64748B',
                            display: 'flex', alignItems: 'center', justifyContent: 'center'
                          }}>
                            <Calendar size={16} />
                          </div>
                          <div>
                            <h4 style={{ fontSize: '0.86rem', fontWeight: 700, color: 'var(--dark)' }}>
                              Weekend Leisure Stay (Friday – Sunday)
                            </h4>
                            <p style={{ fontSize: '0.74rem', color: 'var(--muted)' }}>
                              Applies an automated +15% surge tariff for high-demand leisure weekend stays
                            </p>
                          </div>
                        </div>

                        <label className="switch">
                          <input type="checkbox" checked={formData.is_weekend} readOnly />
                          <span className="slider"></span>
                        </label>
                      </div>

                      <div style={{
                        background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)',
                        padding: '12px 14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.82rem'
                      }}>
                        <div>
                          <span style={{ color: 'var(--muted)' }}>Base ML Rate: </span>
                          <strong style={{ color: 'var(--dark)' }}>₹{prediction.base_nightly.toLocaleString('en-IN')}</strong>
                        </div>
                        <div style={{ color: 'var(--muted)' }}>
                          Formula: Base × {prediction.season_mult}x {formData.is_weekend ? "× 1.15x" : ""}
                        </div>
                        <div>
                          <span style={{ color: 'var(--muted)' }}>Dynamic Rate: </span>
                          <strong style={{ color: 'var(--primary)' }}>₹{prediction.nightly.toLocaleString('en-IN')}</strong>
                        </div>
                      </div>

                      <div className="step-nav-footer">
                        <button type="button" className="btn-secondary" onClick={() => setActiveStep(1)}>
                          <ArrowLeft size={14} style={{ display: 'inline', marginRight: '4px' }} /> Back
                        </button>
                        <button type="button" className="btn-primary-step" onClick={() => setActiveStep(3)}>
                          <span>Next: Amenities</span>
                          <ArrowRight size={15} />
                        </button>
                      </div>
                    </div>
                  )}

                  {/* Step 3: Amenities & Standards */}
                  {activeStep === 3 && (
                    <div className="tab-panel">
                      <div className="panel-header">
                        <h3 className="panel-title">
                          <Sliders size={18} color="var(--primary)" /> Amenities, Policies & Host Trust
                        </h3>
                        <p className="panel-subtitle">Configure verified amenities, policies, and host reputation</p>
                      </div>

                      <div className="input-row">
                        <div className="field-group">
                          <label className="field-label">Amenities Count ({formData.amenities})</label>
                          <input 
                            type="range" min="3" max="50" value={formData.amenities}
                            onChange={(e) => setFormData({ ...formData, amenities: parseInt(e.target.value) })}
                            style={{ accentColor: 'var(--primary)' }}
                          />
                          <span style={{ fontSize: '0.74rem', color: 'var(--muted)' }}>WiFi, AC, Power Backup, Pool, Kitchen</span>
                        </div>

                        <div className="field-group">
                          <label className="field-label">Cancellation Policy</label>
                          <select 
                            className="field-select" value={formData.cancellation_policy}
                            onChange={(e) => setFormData({ ...formData, cancellation_policy: e.target.value })}
                          >
                            <option value="flexible">Flexible (Highest conversion)</option>
                            <option value="moderate">Moderate</option>
                            <option value="strict">Strict</option>
                            <option value="super_strict_30">Super Strict 30</option>
                          </select>
                        </div>

                        <div className="field-group">
                          <label className="field-label">Guest Rating Score ({formData.review_scores_rating}%)</label>
                          <input 
                            type="range" min="65" max="100" value={formData.review_scores_rating}
                            onChange={(e) => setFormData({ ...formData, review_scores_rating: parseInt(e.target.value) })}
                            style={{ accentColor: 'var(--primary)' }}
                          />
                          <span style={{ fontSize: '0.74rem', color: 'var(--muted)' }}>Overall guest satisfaction rating</span>
                        </div>

                        <div className="field-group">
                          <label className="field-label">Total Verified Reviews</label>
                          <input 
                            type="number" className="field-input" min="0" max="500" value={formData.number_of_reviews}
                            onChange={(e) => setFormData({ ...formData, number_of_reviews: parseInt(e.target.value) || 0 })}
                          />
                        </div>
                      </div>

                      <div className="toggle-grid">
                        <div 
                          className={`toggle-item ${formData.instant_bookable === 't' ? 'checked' : ''}`}
                          onClick={() => setFormData(p => ({ ...p, instant_bookable: p.instant_bookable === 't' ? 'f' : 't' }))}
                        >
                          <div className="toggle-info">
                            <h4>Instant Booking</h4>
                            <p>Direct reservation</p>
                          </div>
                          <label className="switch">
                            <input type="checkbox" checked={formData.instant_bookable === 't'} readOnly />
                            <span className="slider"></span>
                          </label>
                        </div>

                        <div 
                          className={`toggle-item ${formData.cleaning_fee ? 'checked' : ''}`}
                          onClick={() => setFormData(p => ({ ...p, cleaning_fee: !p.cleaning_fee }))}
                        >
                          <div className="toggle-info">
                            <h4>Housekeeping Fee</h4>
                            <p>Turnover cleaning</p>
                          </div>
                          <label className="switch">
                            <input type="checkbox" checked={formData.cleaning_fee} readOnly />
                            <span className="slider"></span>
                          </label>
                        </div>

                        <div 
                          className={`toggle-item ${formData.host_identity_verified === 't' ? 'checked' : ''}`}
                          onClick={() => setFormData(p => ({ ...p, host_identity_verified: p.host_identity_verified === 't' ? 'f' : 't' }))}
                        >
                          <div className="toggle-info">
                            <h4>Aadhaar / ID Verified</h4>
                            <p>Government verified</p>
                          </div>
                          <label className="switch">
                            <input type="checkbox" checked={formData.host_identity_verified === 't'} readOnly />
                            <span className="slider"></span>
                          </label>
                        </div>

                        <div 
                          className={`toggle-item ${formData.host_has_profile_pic === 't' ? 'checked' : ''}`}
                          onClick={() => setFormData(p => ({ ...p, host_has_profile_pic: p.host_has_profile_pic === 't' ? 'f' : 't' }))}
                        >
                          <div className="toggle-info">
                            <h4>Host Profile Picture</h4>
                            <p>Authentic verified photo</p>
                          </div>
                          <label className="switch">
                            <input type="checkbox" checked={formData.host_has_profile_pic === 't'} readOnly />
                            <span className="slider"></span>
                          </label>
                        </div>
                      </div>

                      <div className="step-nav-footer">
                        <button type="button" className="btn-secondary" onClick={() => setActiveStep(2)}>
                          <ArrowLeft size={14} style={{ display: 'inline', marginRight: '4px' }} /> Back
                        </button>
                        <button 
                          type="button" 
                          className="btn-primary-step" 
                          style={{ background: 'var(--primary)' }}
                          onClick={runPrediction}
                        >
                          <Sparkles size={15} />
                          <span>Recalculate Price</span>
                        </button>
                      </div>
                    </div>
                  )}

                </div>
              </div>

              {/* Right Valuation Panel */}
              <div className="sticky-summary">
                <div className="price-display-wrapper">
                  <span className="price-tag-sub">Suggested Nightly Tariff</span>
                  <div className="price-main">
                    <span className="price-currency">₹</span>
                    <span className="price-amount">{prediction.nightly.toLocaleString('en-IN')}</span>
                    <span className="price-unit">/ night</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'center', gap: '6px', marginTop: '6px', flexWrap: 'wrap' }}>
                    <span className="status-badge premium">{prediction.demand_tier}</span>
                    <span className="status-badge instant">
                      <Zap size={11} fill="currentColor" /> {formData.room_type}
                    </span>
                  </div>
                </div>

                {/* Market Strategy Band */}
                <div className="strategy-band">
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--dark)' }}>
                      Market Strategy Spread
                    </span>
                    <span style={{ fontSize: '0.68rem', color: '#059669', fontWeight: 700 }}>
                      ±18% Confidence Band
                    </span>
                  </div>

                  <div className="strategy-grid">
                    <div className="strategy-col">
                      <div className="strategy-name">Budget Fill</div>
                      <div className="strategy-val">₹{prediction.market_range.budget.toLocaleString('en-IN')}</div>
                      <div className="strategy-sub">90%+ Occupancy</div>
                    </div>

                    <div className="strategy-col active">
                      <div className="strategy-name">Sweet Spot</div>
                      <div className="strategy-val" style={{ color: 'var(--primary)' }}>
                        ₹{prediction.market_range.recommended.toLocaleString('en-IN')}
                      </div>
                      <div className="strategy-sub">Max Profit</div>
                    </div>

                    <div className="strategy-col">
                      <div className="strategy-name">Peak Yield</div>
                      <div className="strategy-val">₹{prediction.market_range.premium.toLocaleString('en-IN')}</div>
                      <div className="strategy-sub">High Margin</div>
                    </div>
                  </div>
                </div>

                {/* Host Net Financial Ledger */}
                <div className="ledger-box">
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ fontSize: '0.78rem', fontWeight: 700, color: 'var(--dark)' }}>
                      Host Financial Payout
                    </span>
                    <span style={{ fontSize: '0.7rem', color: 'var(--muted)' }}>Per Night</span>
                  </div>

                  <div className="ledger-row">
                    <span>Guest Tariff</span>
                    <span>₹{prediction.nightly.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="ledger-row">
                    <span>Housekeeping Fee</span>
                    <span>+₹{prediction.cleaning.toLocaleString('en-IN')}</span>
                  </div>
                  <div className="ledger-row">
                    <span>Airbnb Fee (3%)</span>
                    <span style={{ color: '#EF4444' }}>-₹{prediction.service_fee.toLocaleString('en-IN')}</span>
                  </div>

                  <div className="ledger-row total">
                    <span>Net Host Payout</span>
                    <span>₹{prediction.net_takehome.toLocaleString('en-IN')}</span>
                  </div>

                  <div style={{ marginTop: '10px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.72rem', color: 'var(--muted)' }}>
                      <span>Forecasted Occupancy</span>
                      <span style={{ fontWeight: 700, color: '#059669' }}>{prediction.occupancy_pct}% Rate</span>
                    </div>
                    <div className="occupancy-meter-bar">
                      <div className="occupancy-meter-fill" style={{ width: `${prediction.occupancy_pct}%` }}></div>
                    </div>
                  </div>
                </div>

                {/* Projections */}
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px' }}>
                  <div style={{ background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', padding: '10px 12px' }}>
                    <span style={{ fontSize: '0.7rem', color: 'var(--muted)', fontWeight: 600, textTransform: 'uppercase' }}>Weekly Est.</span>
                    <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--dark)', marginTop: '2px' }}>
                      ₹{prediction.weekly.toLocaleString('en-IN')}
                    </div>
                  </div>
                  <div style={{ background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-sm)', padding: '10px 12px' }}>
                    <span style={{ fontSize: '0.7rem', color: 'var(--muted)', fontWeight: 600, textTransform: 'uppercase' }}>Monthly Est.</span>
                    <div style={{ fontSize: '1.05rem', fontWeight: 800, color: 'var(--dark)', marginTop: '2px' }}>
                      ₹{prediction.monthly.toLocaleString('en-IN')}
                    </div>
                  </div>
                </div>

                <button className="btn-predict" disabled={loading} onClick={runPrediction}>
                  {loading ? (
                    <>
                      <svg className="spinner" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                        <circle cx="12" cy="12" r="10" stroke="currentColor" strokeOpacity="0.25"></circle>
                        <path d="M12 2a10 10 0 0 1 10 10" stroke="currentColor"></path>
                      </svg>
                      <span>Updating Valuation...</span>
                    </>
                  ) : (
                    <>
                      <Sparkles size={17} />
                      <span>Update Valuation (₹)</span>
                    </>
                  )}
                </button>
              </div>

            </div>
          </div>
        )}

        {/* TAB 2: MODEL COMPARISON (3 ALGORITHMS) */}
        {mainTab === 'models' && (
          <div className="form-card" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--dark)' }}>
                  📊 Model Comparison — 3 Algorithms
                </h2>
                <span className="brand-badge">Evaluation on 6,000 Test Listings</span>
              </div>
              <p style={{ color: 'var(--muted)', fontSize: '0.86rem', marginTop: '4px' }}>
                All models evaluated with 5-fold cross-validation on identical held-out test splits.
              </p>
            </div>

            {/* Winner Banner */}
            <div style={{
              background: '#F0FDF4', border: '2px solid #22C55E', borderRadius: 'var(--radius-md)',
              padding: '18px 24px', textAlign: 'center', boxShadow: '0 4px 16px rgba(34,197,94,0.1)'
            }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#15803D' }}>
                🏆 CatBoost Selected as Best Performing Model
              </div>
              <div style={{ color: '#4B5563', fontSize: '0.85rem', marginTop: '4px' }}>
                Highest R² (0.9768) • Lowest RMSE (0.1245) • Lowest Mean Absolute Percentage Error (10.0%)
              </div>
            </div>

            {/* Model Comparison Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '14px' }}>
              {MODEL_BENCHMARK.map((m) => (
                <div key={m.name} style={{
                  background: '#FFFFFF', border: `1.5px solid ${m.r2 > 0.97 ? '#10B981' : '#E2E8F0'}`,
                  borderRadius: 'var(--radius-md)', padding: '18px 16px', textAlign: 'center'
                }}>
                  <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase' }}>
                    {m.name}
                  </div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: m.color, margin: '8px 0 4px' }}>
                    R² = {m.r2.toFixed(4)}
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--muted)' }}>
                    RMSE: {m.rmse} • MAPE: {m.mape}%
                  </div>
                  <div style={{ fontSize: '0.78rem', color: 'var(--dark)', fontWeight: 600, marginTop: '6px' }}>
                    MAE: ₹{m.mae_inr.toLocaleString('en-IN')}
                  </div>
                </div>
              ))}
            </div>

            {/* Side-by-Side Visual Bar Comparison */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
              <div style={{ background: '#F8FAFC', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
                <h4 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '14px' }}>R² Score (Higher is Better)</h4>
                {MODEL_BENCHMARK.map(m => (
                  <div key={m.name} style={{ marginBottom: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '4px' }}>
                      <span style={{ fontWeight: 600 }}>{m.name}</span>
                      <strong style={{ color: m.color }}>{m.r2.toFixed(4)}</strong>
                    </div>
                    <div style={{ width: '100%', height: '10px', background: '#E2E8F0', borderRadius: '9999px', overflow: 'hidden' }}>
                      <div style={{ width: `${(m.r2 / 1.0) * 100}%`, height: '100%', background: m.color, borderRadius: '9999px' }}></div>
                    </div>
                  </div>
                ))}
              </div>

              <div style={{ background: '#F8FAFC', padding: '16px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
                <h4 style={{ fontSize: '0.9rem', fontWeight: 700, marginBottom: '14px' }}>MAPE % Error (Lower is Better)</h4>
                {MODEL_BENCHMARK.map(m => (
                  <div key={m.name} style={{ marginBottom: '12px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '4px' }}>
                      <span style={{ fontWeight: 600 }}>{m.name}</span>
                      <strong style={{ color: m.color }}>{m.mape}%</strong>
                    </div>
                    <div style={{ width: '100%', height: '10px', background: '#E2E8F0', borderRadius: '9999px', overflow: 'hidden' }}>
                      <div style={{ width: `${(m.mape / 25.0) * 100}%`, height: '100%', background: m.color, borderRadius: '9999px' }}></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Complete Metrics Table */}
            <div>
              <h4 style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: '10px' }}>📋 Complete Model Benchmark Table</h4>
              <div style={{ overflowX: 'auto', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
                  <thead>
                    <tr style={{ background: '#F8FAFC', borderBottom: '1px solid var(--border)', textAlign: 'left' }}>
                      <th style={{ padding: '10px 14px' }}>Algorithm</th>
                      <th style={{ padding: '10px 14px' }}>R² Score</th>
                      <th style={{ padding: '10px 14px' }}>RMSE (Log)</th>
                      <th style={{ padding: '10px 14px' }}>MAE (Log)</th>
                      <th style={{ padding: '10px 14px' }}>MAPE (%)</th>
                      <th style={{ padding: '10px 14px' }}>RMSE (INR)</th>
                      <th style={{ padding: '10px 14px' }}>MAE (INR)</th>
                      <th style={{ padding: '10px 14px' }}>Verdict</th>
                    </tr>
                  </thead>
                  <tbody>
                    {MODEL_BENCHMARK.map((m, idx) => (
                      <tr key={m.name} style={{ borderBottom: idx < 2 ? '1px solid var(--border)' : 'none' }}>
                        <td style={{ padding: '10px 14px', fontWeight: 600 }}>{m.name}</td>
                        <td style={{ padding: '10px 14px', color: m.color, fontWeight: 700 }}>{m.r2.toFixed(4)}</td>
                        <td style={{ padding: '10px 14px' }}>{m.rmse}</td>
                        <td style={{ padding: '10px 14px' }}>{m.mae}</td>
                        <td style={{ padding: '10px 14px' }}>{m.mape}%</td>
                        <td style={{ padding: '10px 14px' }}>₹{m.rmse_inr.toLocaleString('en-IN')}</td>
                        <td style={{ padding: '10px 14px' }}>₹{m.mae_inr.toLocaleString('en-IN')}</td>
                        <td style={{ padding: '10px 14px', fontWeight: 700, color: m.color }}>{m.rank}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}

        {/* TAB 3: FEATURE IMPORTANCE */}
        {mainTab === 'features' && (
          <div className="form-card" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--dark)' }}>
                🔥 Feature Importance Analysis
              </h2>
              <p style={{ color: 'var(--muted)', fontSize: '0.86rem', marginTop: '4px' }}>
                CatBoost built-in feature importance scores displaying which property attributes drive Airbnb prices most.
              </p>
            </div>

            {/* Horizontal Bar Chart */}
            <div style={{ background: '#F8FAFC', padding: '20px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
              {FEATURE_IMPORTANCES.map((item) => (
                <div key={item.feature} style={{ marginBottom: '12px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.84rem', marginBottom: '4px' }}>
                    <span style={{ fontWeight: 600, color: 'var(--dark)' }}>{item.feature}</span>
                    <strong style={{ color: item.color }}>{item.score}%</strong>
                  </div>
                  <div style={{ width: '100%', height: '9px', background: '#E2E8F0', borderRadius: '9999px', overflow: 'hidden' }}>
                    <div style={{ width: `${(item.score / 28) * 100}%`, height: '100%', background: item.color, borderRadius: '9999px' }}></div>
                  </div>
                </div>
              ))}
            </div>

            {/* Insights Cards */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '16px' }}>
              <div style={{ background: '#FFF5F6', border: '1px solid #FECDD3', borderRadius: 'var(--radius-md)', padding: '16px' }}>
                <h4 style={{ color: 'var(--primary)', fontSize: '0.92rem', fontWeight: 700, marginBottom: '6px' }}>
                  🎯 Primary Price Drivers (Top 3 = 60.4%)
                </h4>
                <p style={{ fontSize: '0.82rem', color: '#4B5563', lineHeight: 1.5 }}>
                  <strong>Accommodates (26.8%)</strong> and <strong>Bathrooms (18.4%)</strong> are the strongest predictors. In the Indian market, high-capacity group bookings and private en-suite washrooms command the highest nightly premiums.
                </p>
              </div>

              <div style={{ background: '#F0FDF4', border: '1px solid #BBF7D0', borderRadius: 'var(--radius-md)', padding: '16px' }}>
                <h4 style={{ color: '#15803D', fontSize: '0.92rem', fontWeight: 700, marginBottom: '6px' }}>
                  💡 Host Optimization Takeaway
                </h4>
                <p style={{ fontSize: '0.82rem', color: '#4B5563', lineHeight: 1.5 }}>
                  Increasing amenities from 10 to 30 adds an estimated <strong>+₹800 to ₹1,400/night</strong> in predicted value. Maintaining a 95%+ review score further unlocks peak pricing potential.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* TAB 4: MARKET INSIGHTS */}
        {mainTab === 'market' && (
          <div className="form-card" style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div>
              <h2 style={{ fontSize: '1.45rem', fontWeight: 800, color: 'var(--dark)' }}>
                🏙 Indian Airbnb Market Insights
              </h2>
              <p style={{ color: 'var(--muted)', fontSize: '0.86rem', marginTop: '4px' }}>
                Aggregated market intelligence across 30,000 listings in major tourism and business regions.
              </p>
            </div>

            {/* Summary Metrics */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '12px' }}>
              <div style={{ background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '14px', textAlign: 'center' }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase' }}>Listings Evaluated</div>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--dark)', marginTop: '2px' }}>30,000</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--muted)' }}>Indian Destinations</div>
              </div>

              <div style={{ background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '14px', textAlign: 'center' }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase' }}>Median Price</div>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--primary)', marginTop: '2px' }}>₹4,800</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--muted)' }}>Per Night Across India</div>
              </div>

              <div style={{ background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '14px', textAlign: 'center' }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase' }}>Top Yield Market</div>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#059669', marginTop: '2px' }}>Goa</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--muted)' }}>Median ₹6,800/night</div>
              </div>

              <div style={{ background: '#F8FAFC', border: '1px solid var(--border)', borderRadius: 'var(--radius-md)', padding: '14px', textAlign: 'center' }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 700, color: 'var(--muted)', textTransform: 'uppercase' }}>Top Architecture</div>
                <div style={{ fontSize: '1.4rem', fontWeight: 800, color: '#3B82F6', marginTop: '2px' }}>Villas & Apts</div>
                <div style={{ fontSize: '0.68rem', color: 'var(--muted)' }}>68% of bookings</div>
              </div>
            </div>

            {/* City Median Price Chart */}
            <div style={{ background: '#F8FAFC', padding: '18px', borderRadius: 'var(--radius-md)', border: '1px solid var(--border)' }}>
              <h4 style={{ fontSize: '0.92rem', fontWeight: 700, marginBottom: '14px' }}>Median Nightly Price by City (₹ INR)</h4>
              {Object.entries(INDIAN_CITIES).sort((a, b) => b[1].medianPrice - a[1].medianPrice).map(([cKey, cInfo]) => (
                <div key={cKey} style={{ marginBottom: '10px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '3px' }}>
                    <span>{cInfo.icon} {cInfo.name} ({cInfo.state})</span>
                    <strong>₹{cInfo.medianPrice.toLocaleString('en-IN')}</strong>
                  </div>
                  <div style={{ width: '100%', height: '8px', background: '#E2E8F0', borderRadius: '9999px', overflow: 'hidden' }}>
                    <div style={{ width: `${(cInfo.medianPrice / 7000) * 100}%`, height: '100%', background: 'var(--primary)', borderRadius: '9999px' }}></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </main>
    </div>
  );
}
