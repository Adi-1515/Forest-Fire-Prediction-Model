import streamlit as st
import time
import sys
import os

# Add root directory to path to allow absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.predict import ForestFirePredictor

# Set page config to use wide layout
st.set_page_config(page_title="Forest Fire Predictor", page_icon="🔥", layout="wide")

# Custom CSS for styling to match design.tsx
st.markdown("""
<style>
    /* Global Background and Text */
    [data-testid="stAppViewContainer"] {
        background-color: #0a0c0a;
        color: #e2e8f0;
        background-image: linear-gradient(to right, #0a0c0a, rgba(10, 12, 10, 0.8)), linear-gradient(to top, #0a0c0a, rgba(10, 12, 10, 0.5)), url("https://images.unsplash.com/photo-1542273917363-3b1817f69a2d?q=80&w=2948&auto=format&fit=crop");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    
    [data-testid="stHeader"] {
        background: rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }

    [data-testid="stSidebar"] {
        background-color: rgba(10, 12, 10, 0.9);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    h1, h2, h3, p, span {
        font-family: sans-serif;
    }

    /* Hero Text */
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -0.025em;
        margin-bottom: 1rem;
        color: white;
    }
    .hero-gradient {
        background: linear-gradient(to right, #fb923c, #ef4444);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    /* Panels */
    .glass-panel {
        background: rgba(17, 19, 17, 0.8);
        backdrop-filter: blur(24px);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 1rem;
        padding: 1.5rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
        margin-bottom: 2rem;
    }

    /* Disclaimer */
    .disclaimer-box {
        background: rgba(69, 26, 3, 0.2);
        border: 1px solid rgba(120, 53, 15, 0.3);
        border-radius: 0.75rem;
        padding: 1rem;
        display: flex;
        gap: 0.75rem;
        margin-top: 1.5rem;
        margin-bottom: 1.5rem;
    }
    .disclaimer-title {
        color: #f59e0b;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0 0 0.25rem 0;
    }
    .disclaimer-text {
        color: #cbd5e1;
        font-size: 0.75rem;
        line-height: 1.6;
        margin: 0;
    }

    /* Input Styling */
    .stNumberInput > div > div > input, .stSelectbox > div > div > div {
        background-color: rgba(30, 41, 59, 0.8) !important;
        border: 1px solid rgba(51, 65, 85, 0.5) !important;
        color: #f1f5f9 !important;
        border-radius: 0.375rem !important;
    }
    .stNumberInput label, .stSelectbox label {
        color: #cbd5e1 !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }
    
    /* Section Headers */
    .section-header {
        font-size: 0.875rem;
        font-weight: 500;
        color: #e2e8f0;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(to right, #ea580c, #dc2626);
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        border: none;
        padding: 0.75rem 2rem;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 10px 15px -3px rgba(153, 27, 27, 0.5);
    }
    .stButton>button:hover {
        background: linear-gradient(to right, #f97316, #ef4444);
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(234, 88, 12, 0.5);
        color: white;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(15, 23, 42, 0.4) !important;
        border: 1px solid rgba(30, 41, 59, 0.5) !important;
        border-radius: 0.75rem !important;
        color: #cbd5e1 !important;
    }
    .streamlit-expanderContent {
        background: transparent !important;
        border: 1px solid rgba(30, 41, 59, 0.5) !important;
        border-top: none !important;
        border-radius: 0 0 0.75rem 0.75rem !important;
        color: #94a3b8 !important;
    }
    
    /* Custom Result Cards */
    .result-card {
        background: rgba(15, 23, 42, 0.5);
        border: 1px solid rgba(30, 41, 59, 0.8);
        border-radius: 0.75rem;
        padding: 1.5rem;
        text-align: center;
        display: flex;
        flex-direction: column;
        align-items: center;
        height: 100%;
    }
    .result-label {
        font-size: 0.875rem;
        font-weight: 500;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    .result-value {
        font-size: 3rem;
        font-weight: 800;
        color: white;
        font-family: monospace;
        letter-spacing: -0.025em;
        line-height: 1;
        margin-bottom: 0.5rem;
    }
    .risk-pill {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.875rem;
        font-weight: 700;
        background: rgba(2, 6, 23, 0.5);
        border: 1px solid rgba(30, 41, 59, 1);
    }
    .risk-low { color: #34d399; }
    .risk-mod { color: #fbbf24; }
    .risk-high { color: #f97316; }
    .risk-ext { color: #ef4444; }

    /* Progress bar */
    .risk-bar-container {
        height: 0.5rem;
        width: 100%;
        background-color: #1e293b;
        border-radius: 9999px;
        display: flex;
        overflow: hidden;
        position: relative;
        margin-top: 2rem;
    }
    .risk-bar-segment { height: 100%; width: 25%; }
    .segment-1 { background-color: #10b981; }
    .segment-2 { background-color: #f59e0b; }
    .segment-3 { background-color: #f97316; }
    .segment-4 { background-color: #dc2626; }
    .risk-indicator {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        width: 1rem;
        height: 1rem;
        background-color: white;
        border-radius: 9999px;
        box-shadow: 0 0 10px rgba(255,255,255,0.5);
        border: 2px solid #0f172a;
        transition: left 1s ease-out;
    }
    .risk-labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.625rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #64748b;
        margin-top: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_predictor():
    return ForestFirePredictor()

try:
    predictor = load_predictor()
except Exception as e:
    st.error(f"Failed to load models. Ensure you have run the training scripts in `src/`. Error: {e}")
    st.stop()

# Helper to determine risk level colors and text
def get_risk_details(probability):
    prob = float(probability)
    if prob < 25: return {'level': 'Low Risk', 'class': 'risk-low'}
    if prob < 50: return {'level': 'Moderate Risk', 'class': 'risk-mod'}
    if prob < 75: return {'level': 'High Risk', 'class': 'risk-high'}
    return {'level': 'Very High Risk', 'class': 'risk-ext'}


# Create layout
st.write("") # Top padding
left_col, right_col = st.columns([5, 7], gap="large")

with left_col:
    # Top tags
    st.markdown("""
    <div style="display: inline-flex; align-items: center; gap: 8px; padding: 4px 12px; border-radius: 9999px; background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(51, 65, 85, 0.5); font-size: 11px; color: #cbd5e1; font-weight: 500;">
        <span style="width: 6px; height: 6px; border-radius: 50%; background-color: #10b981;"></span>
        ML Prediction Model • UCI Forest Fires Dataset
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Title
    st.markdown("""
    <h2 class="hero-title">
        Predict Forest Fire Risk <br/>
        <span class="hero-gradient">& Burned Area</span>
    </h2>
    <p style="color: #94a3b8; font-size: 1.125rem; line-height: 1.625; max-width: 32rem; margin-bottom: 2rem;">
        Assess wildfire risk and estimate potential burned area using localized meteorological and environmental conditions.
    </p>
    """, unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer-box">
        <div style="margin-top: 2px;">⚠️</div>
        <div>
            <h3 class="disclaimer-title">Important Dataset Limitation</h3>
            <p class="disclaimer-text">
                This model was trained on the UCI Forest Fires Dataset, representing conditions from the Montesinho Natural Park region of northeast Portugal. Predictions reflect patterns learned from that specific dataset and may not generalize accurately to other environments, geographies, or climates.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Explanation Expander
    with st.expander("ℹ️ What do these parameters mean?"):
        st.markdown("""
        **Spatial & Temporal**  
        Coordinates (X,Y) represent a 9x9 grid map of the park. Month and day capture seasonal variations.
        
        **Fire Weather Index (FWI)**  
        * **FFMC:** Fine Fuel Moisture Code (moisture content of litter/fine fuels).  
        * **DMC:** Duff Moisture Code (moisture of shallow organic layers).  
        * **DC:** Drought Code (moisture of deep organic layers).  
        * **ISI:** Initial Spread Index (expected rate of fire spread).
        
        **Meteorological Conditions**  
        Local weather metrics recorded at the time. Temperature, humidity, wind, and rain significantly impact fire behavior.
        """)

with right_col:
    # We wrap the inputs in a custom div to simulate the glass panel if possible, but st.markdown can't contain streamlit widgets.
    # We will use st.container to group them and apply global css for structure.
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1.5rem;">
        <h2 style="font-size: 1.125rem; font-weight: 600; color: white; display: flex; align-items: center; gap: 0.5rem; margin: 0;">
            <span style="color: #f97316;">⚡</span> Prediction Parameters
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">📍 Spatial & Temporal</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: X = st.number_input("X Coord (1-9)", min_value=1, max_value=9, value=5)
    with col2: Y = st.number_input("Y Coord (1-9)", min_value=1, max_value=9, value=5)
    with col3: month = st.selectbox("Month", options=list(range(1, 13)), index=7, format_func=lambda x: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][x-1])
    with col4: day = st.selectbox("Day", options=list(range(1, 8)), index=4, format_func=lambda x: ['Mon','Tue','Wed','Thu','Fri','Sat','Sun'][x-1])

    st.markdown('<hr style="border-color: rgba(51, 65, 85, 0.5); margin: 1.5rem 0;">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">🔥 Fire Weather Index</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: FFMC = st.number_input("FFMC", min_value=18.0, max_value=100.0, value=85.0)
    with col2: DMC = st.number_input("DMC", min_value=1.0, max_value=300.0, value=110.0)
    with col3: DC = st.number_input("DC", min_value=7.0, max_value=900.0, value=500.0)
    with col4: ISI = st.number_input("ISI", min_value=0.0, max_value=60.0, value=8.0)

    st.markdown('<hr style="border-color: rgba(51, 65, 85, 0.5); margin: 1.5rem 0;">', unsafe_allow_html=True)

    st.markdown('<div class="section-header">💨 Meteorological Conditions</div>', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1: temp = st.number_input("Temp (°C)", min_value=-10.0, max_value=45.0, value=20.0)
    with col2: RH = st.number_input("Humidity (%)", min_value=0, max_value=100, value=50)
    with col3: wind = st.number_input("Wind (km/h)", min_value=0.0, max_value=20.0, value=5.0)
    with col4: rain = st.number_input("Rain (mm/m2)", min_value=0.0, max_value=10.0, value=0.0)
    
    st.markdown("<br/>", unsafe_allow_html=True)
    
    submit = st.button("Predict Fire Risk")
    
    st.markdown('</div>', unsafe_allow_html=True)

    if submit:
        with st.spinner('Analyzing patterns and calculating risk...'):
            time.sleep(1.5)
            
            input_data = {
                'X': X, 'Y': Y, 'month': month, 'day': day, 
                'FFMC': FFMC, 'DMC': DMC, 'DC': DC, 'ISI': ISI, 
                'temp': temp, 'RH': RH, 'wind': wind, 'rain': rain
            }
            
            try:
                results = predictor.predict(input_data)
                prob_raw = results['fire_probability'] * 100
                area_pred = results['estimated_area_burned_ha']
                
                details = get_risk_details(prob_raw)
                
                st.markdown('<div class="glass-panel" style="margin-top: 2rem;">', unsafe_allow_html=True)
                st.markdown("""
                <div style="padding-bottom: 1rem; border-bottom: 1px solid rgba(255,255,255,0.05); margin-bottom: 1.5rem;">
                    <h2 style="font-size: 1.125rem; font-weight: 600; color: white; margin: 0;">Prediction Results</h2>
                </div>
                """, unsafe_allow_html=True)
                
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-label">Likelihood of Fire</div>
                        <div class="result-value">{prob_raw:.1f}<span style="font-size: 1.5rem; color: #64748b; margin-left: 0.25rem;">%</span></div>
                        <div class="risk-pill {details['class']}">{details['level']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                with res_col2:
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="result-label">Estimated Area Burned</div>
                        <div class="result-value">{area_pred:.2f}</div>
                        <div style="font-size: 0.875rem; color: #64748b; background: rgba(2, 6, 23, 0.5); padding: 0.25rem 0.75rem; border-radius: 9999px; border: 1px solid rgba(30, 41, 59, 1); margin-top: 0.5rem;">
                            hectares &bull; If fire occurs
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Progress bar
                indicator_left = max(0, min(100, prob_raw))
                st.markdown(f"""
                <div class="risk-bar-container">
                    <div class="risk-bar-segment segment-1"></div>
                    <div class="risk-bar-segment segment-2"></div>
                    <div class="risk-bar-segment segment-3"></div>
                    <div class="risk-bar-segment segment-4"></div>
                    <div class="risk-indicator" style="left: calc({indicator_left}% - 0.5rem);"></div>
                </div>
                <div class="risk-labels">
                    <span>Low</span>
                    <span>Moderate</span>
                    <span>High</span>
                    <span>Extreme</span>
                </div>
                """, unsafe_allow_html=True)
                
                # Interpretation panel
                st.markdown(f"""
                <div style="margin-top: 2rem; background: rgba(30, 41, 59, 0.3); border-left: 2px solid #475569; border-radius: 0 0.5rem 0.5rem 0; padding: 1rem; font-size: 0.875rem; color: #cbd5e1; line-height: 1.6;">
                    <strong class="{details['class']}" style="margin-right: 0.25rem;">{details['level']} detected.</strong>
                    The current meteorological and fire-weather inputs indicate a {prob_raw:.1f}% probability of fire occurrence.
                    {' Should a fire ignite under these specific conditions, the model estimates approximately ' + f"{area_pred:.2f}" + ' hectares of area may be burned.' if area_pred > 0 else ' Based on these metrics, widespread burning is less likely even if ignition occurs, though localized risk remains.'}
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error making prediction: {e}")

# Footer
st.markdown("""
<div style="margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center;">
    <div style="color: #64748b; font-size: 0.75rem; font-weight: 500;">
        🔥 Forest Fire Prediction • Machine Learning Project
    </div>
    <div style="color: #64748b; font-size: 0.75rem;">
        Interface styled for professional environmental risk assessment.
    </div>
</div>
""", unsafe_allow_html=True)
