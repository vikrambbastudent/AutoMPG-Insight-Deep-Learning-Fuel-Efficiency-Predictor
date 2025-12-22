import streamlit as st
import pandas as pd
import tensorflow as tf
import pickle

# --------------------------------------------------
# Paths
# --------------------------------------------------
BASE_PATH = r"C:\Users\HP\Invoice extraction"

MODEL_PATH = f"{BASE_PATH}\\mpg_model.keras"
NORM_PATH = f"{BASE_PATH}\\norm.pkl"
CAR_LOOKUP_PATH = f"{BASE_PATH}\\car_lookup.pkl"

# --------------------------------------------------
# Load artifacts
# --------------------------------------------------
model = tf.keras.models.load_model(MODEL_PATH)
mean, std = pickle.load(open(NORM_PATH, "rb"))
car_lookup = pd.read_pickle(CAR_LOOKUP_PATH)

# --------------------------------------------------
# UI
# --------------------------------------------------
st.set_page_config(page_title="Fuel Efficiency Predictor", page_icon="🚗")
st.title("🚗 Fuel Efficiency Prediction")
st.write("Predict **Miles Per Gallon (MPG)** using a trained ML model")

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.header("Select Car")

car_names = sorted(car_lookup.index.tolist())
selected_car = st.sidebar.selectbox(
    "Car Name (optional)",
    ["Manual Entry"] + car_names
)

st.sidebar.header("Vehicle Specifications")

# --------------------------------------------------
# Default values
# --------------------------------------------------
defaults = {
    "cylinders": 4,
    "horsepower": 100,
    "weight": 3000,
    "acceleration": 15,
    "model year": 76,
    "origin": 1
}

if selected_car != "Manual Entry":
    specs = car_lookup.loc[selected_car].to_dict()
else:
    specs = defaults

# --------------------------------------------------
# Input fields (editable)
# --------------------------------------------------
cylinders = st.sidebar.number_input(
    "Cylinders", 2, 12, int(specs["cylinders"])
)

horsepower = st.sidebar.slider(
    "Horsepower", 40, 250, int(specs["horsepower"])
)

weight = st.sidebar.slider(
    "Weight (lbs)", 1500, 5500, int(specs["weight"])
)

acceleration = st.sidebar.slider(
    "Acceleration", 5.0, 25.0, float(specs["acceleration"])
)

model_year = st.sidebar.slider(
    "Model Year", 70, 82, int(specs["model year"])
)

origin_map = {1: "USA", 2: "Europe", 3: "Japan"}
origin_reverse = {v: k for k, v in origin_map.items()}

origin_label = st.sidebar.selectbox(
    "Origin",
    list(origin_reverse.keys()),
    index=list(origin_reverse.values()).index(int(specs["origin"]))
)

origin = origin_reverse[origin_label]

# --------------------------------------------------
# Prediction input
# --------------------------------------------------
input_df = pd.DataFrame([{
    "cylinders": cylinders,
    "horsepower": horsepower,
    "weight": weight,
    "acceleration": acceleration,
    "model year": model_year,
    "origin": origin
}])

# Align and normalize
input_df = input_df[mean.index]
input_df = ((input_df - mean) / std).astype("float32")

# --------------------------------------------------
# Predict
# --------------------------------------------------
if st.button("Predict MPG"):
    mpg = model.predict(input_df, verbose=0)[0][0]

    st.success(f"🚘 Predicted Fuel Efficiency: **{mpg:.2f} MPG**")

    if mpg >= 30:
        st.info("✅ Excellent fuel efficiency")
    elif mpg >= 20:
        st.warning("⚠️ Average fuel efficiency")
    else:
        st.error("❌ Low fuel efficiency")
