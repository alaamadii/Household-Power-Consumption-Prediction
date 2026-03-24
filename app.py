import streamlit as st
import pandas as pd
from data_preparation import load_data
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title="Energy Consumption Predictor",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI design
st.markdown("""
<style>
    /* Main container background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header styling */
    h1 {
        font-family: 'Inter', sans-serif;
        color: #2c3e50;
        text-align: center;
        padding-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    p.subtitle {
        text-align: center;
        color: #34495e;
        font-size: 1.2rem;
        margin-bottom: 40px;
    }

    /* Input styling */
    .stNumberInput {
        background-color: transparent;
    }

    /* Button styling */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 18px;
        font-weight: bold;
        padding: 12px 24px;
        border: none;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease 0s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: translateY(-2px);
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3);
        color: #f1f1f1;
    }

    /* Metric card styling */
    div[data-testid="metric-container"] {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border: 1px solid #e1e4e8;
    }
    
    .prediction-card {
        background: white;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 30px;
        border-top: 5px solid #667eea;
    }
    .prediction-value {
        font-size: 48px;
        font-weight: 800;
        background: -webkit-linear-gradient(#667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 10px 0;
    }
    .prediction-label {
        font-size: 20px;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_resource
def train_model():
    """Loads data and trains the linear regression model. Cached for performance."""
    x, y = load_data("data/household_power_consumption.txt")
    model = LinearRegression()
    model.fit(x, y)
    return model, list(x.columns)

st.title("⚡ Household Power Consumption Predictor")
st.markdown("<p class='subtitle'>Predict Global Active Power based on household usage parameters</p>", unsafe_allow_html=True)

with st.spinner("Loading data and training model... This may take a minute on the first run."):
    try:
        model, feature_cols = train_model()
        model_loaded = True
    except Exception as e:
        st.error(f"Error loading data: {e}. Please ensure the dataset exists in data/household_power_consumption.txt")
        model_loaded = False

if model_loaded:
    st.sidebar.markdown("### 🎛️ Input Features")
    st.sidebar.markdown("Provide the household electrical usage metrics below:")

    with st.sidebar:
        st.markdown("#### Power & Voltage")
        global_reactive = st.number_input("Global Reactive Power (kVAR)", min_value=0.0, max_value=5.0, value=0.1, step=0.01)
        voltage = st.number_input("Voltage (Volts)", min_value=200.0, max_value=260.0, value=240.0, step=0.1)
        global_intensity = st.number_input("Global Intensity (Amps)", min_value=0.0, max_value=100.0, value=4.0, step=0.1)
        
        st.markdown("---")
        st.markdown("#### Sub-metering (Watt-hours)")
        sub1 = st.number_input("Sub Metering 1 (Kitchen)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        sub2 = st.number_input("Sub Metering 2 (Laundry)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)
        sub3 = st.number_input("Sub Metering 3 (Water/AC)", min_value=0.0, max_value=100.0, value=0.0, step=1.0)

        predict_btn = st.button("Predict Consumption")

    # Main Content Area
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(label="Global Reactive Power", value=f"{global_reactive:.2f} kVAR")
        st.metric(label="Sub Metering 1", value=f"{sub1:.0f} Wh", help="Kitchen appliances")
    with col2:
        st.metric(label="Voltage", value=f"{voltage:.1f} V")
        st.metric(label="Sub Metering 2", value=f"{sub2:.0f} Wh", help="Laundry room appliances")
    with col3:
        st.metric(label="Global Intensity", value=f"{global_intensity:.1f} A")
        st.metric(label="Sub Metering 3", value=f"{sub3:.0f} Wh", help="Water heater & AC")

    if predict_btn:
        with st.spinner("Calculating prediction..."):
            # Prepare the input data frame
            input_data = pd.DataFrame([{
                "Global_reactive_power": global_reactive,
                "Voltage": voltage,
                "Global_intensity": global_intensity,
                "Sub_metering_1": sub1,
                "Sub_metering_2": sub2,
                "Sub_metering_3": sub3
            }])
            
            # Ensure column order matches training data
            input_df = input_data[feature_cols]
            prediction = model.predict(input_df)[0]
            
            st.markdown(f"""
            <div class="prediction-card">
                <div class="prediction-label">Estimated Global Active Power</div>
                <div class="prediction-value">{prediction:.3f} kW</div>
                <div style="color: #95a5a6; margin-top: 10px;">Based on your current inputs</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("👈 Adjust the parameters in the sidebar and click **Predict Consumption** to see the estimated global active power.")
