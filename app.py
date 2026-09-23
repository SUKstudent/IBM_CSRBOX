import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Space Mission Intelligence",
    page_icon="🚀",
    layout="wide"
)


# -----------------------------
# Load Trained Model
# -----------------------------
MODEL_PATH = Path(__file__).parent / "space_mission_model.pkl"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


if not MODEL_PATH.exists():
    st.error("Model file 'space_mission_model.pkl' was not found.")
    st.info("Please keep app.py and space_mission_model.pkl in the same folder.")
    st.stop()

model = load_model()


# -----------------------------
# Header
# -----------------------------
st.title("🚀 Space Mission Intelligence")
st.subheader("Mission Outcome Prediction")

st.write(
    "Enter the mission details below to predict the expected mission outcome "
    "using a trained Random Forest machine learning model."
)

st.divider()


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("🤖 Model Information")

    st.write("**Model:** Random Forest Classifier")
    st.write("**Test Accuracy:** 90.17%")

    st.divider()

    st.caption(
        "The accuracy shown above is based on the held-out test dataset "
        "used during model evaluation."
    )


# -----------------------------
# Input Section
# -----------------------------
st.header("🛰️ Mission Details")

col1, col2 = st.columns(2)

with col1:
    company = st.text_input(
        "Company",
        placeholder="e.g. SpaceX"
    )

    location = st.text_input(
        "Location",
        placeholder="Enter launch location"
    )

    time = st.text_input(
        "Time",
        placeholder="e.g. 18:00:00"
    )

    rocket = st.text_input(
        "Rocket",
        placeholder="Enter rocket name"
    )

    price = st.number_input(
        "Price",
        min_value=0.0,
        value=0.0,
        step=1.0
    )


with col2:
    mission = st.text_input(
        "Mission",
        placeholder="Enter mission name"
    )

    rocket_status = st.text_input(
        "Rocket Status",
        placeholder="e.g. StatusActive"
    )

    year = st.number_input(
        "Year",
        min_value=1950,
        max_value=2100,
        value=2020,
        step=1
    )

    month = st.number_input(
        "Month",
        min_value=1,
        max_value=12,
        value=1,
        step=1
    )


st.divider()


# -----------------------------
# Prediction
# -----------------------------
if st.button(
    "🔮 Predict Mission Outcome",
    type="primary",
    use_container_width=True
):

    # Check categorical inputs
    if not all([
        company.strip(),
        location.strip(),
        time.strip(),
        rocket.strip(),
        mission.strip(),
        rocket_status.strip()
    ]):
        st.warning("⚠️ Please fill in all mission details before predicting.")

    else:

        # Create input dataframe
        input_data = pd.DataFrame([{
            "Company": company,
            "Location": location,
            "Time": time,
            "Rocket": rocket,
            "Mission": mission,
            "RocketStatus": rocket_status,
            "Price": price,
            "Year": year,
            "Month": month
        }])

        # Prediction
        prediction = model.predict(input_data)[0]

        st.divider()

        st.header("📊 Prediction Result")

        if prediction == "Success":
            st.success(f"✅ Predicted Mission Outcome: **{prediction}**")

        elif prediction == "Failure":
            st.error(f"❌ Predicted Mission Outcome: **{prediction}**")

        elif prediction == "Partial Failure":
            st.warning(f"⚠️ Predicted Mission Outcome: **{prediction}**")

        elif prediction == "Prelaunch Failure":
            st.warning(f"⚠️ Predicted Mission Outcome: **{prediction}**")

        else:
            st.info(f"Predicted Mission Outcome: **{prediction}**")

        # Show entered information
        with st.expander("🔍 View Mission Input"):
            st.dataframe(
                input_data,
                use_container_width=True
            )


# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "Space Mission Intelligence — Mission Outcome Prediction | "
    "Machine Learning + Streamlit"
)

st.caption(
    "Note: This prediction reflects patterns learned from historical data "
    "and is not a real-world mission risk assessment."
)
