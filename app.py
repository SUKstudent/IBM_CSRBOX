import streamlit as st
import pandas as pd
import joblib
from pathlib import Path


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Space Mission Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# MODEL LOADING
# =========================================================

MODEL_PATH = Path(__file__).parent / "space_mission_model.pkl"


@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


if not MODEL_PATH.exists():
    st.error("❌ space_mission_model.pkl not found.")
    st.info(
        "Please keep app.py and space_mission_model.pkl "
        "in the same GitHub repository."
    )
    st.stop()


try:
    model = load_model()

except Exception as e:
    st.error("⚠️ Unable to load the trained model.")
    st.write("Please check the package versions in requirements.txt.")
    st.stop()


# =========================================================
# SIDEBAR NAVIGATION
# =========================================================

st.sidebar.title("🚀 Space Mission")
st.sidebar.caption("Mission Intelligence System")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Welcome",
        "🔮 Mission Prediction",
        "ℹ️ About Project"
    ]
)

st.sidebar.divider()

st.sidebar.subheader("🤖 Model Information")
st.sidebar.write("**Model:** Random Forest")
st.sidebar.write("**Test Accuracy:** 90.17%")

st.sidebar.divider()

st.sidebar.caption(
    "IBM SkillsBuild Academic Internship – "
    "Data Analytics with AI"
)


# =========================================================
# WELCOME PAGE
# =========================================================

if page == "🏠 Welcome":

    st.title("🚀 Space Mission Intelligence")

    st.subheader("Mission Outcome Prediction")

    st.write(
        "Welcome to the Space Mission Intelligence system. "
        "This application uses Machine Learning to predict "
        "the outcome category of a space mission based on "
        "historical mission information."
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "ML Model",
            "Random Forest"
        )

    with col2:
        st.metric(
            "Test Accuracy",
            "90.17%"
        )

    with col3:
        st.metric(
            "Prediction Classes",
            "4"
        )

    st.divider()

    st.header("🛰️ What can you do here?")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 🔮 Mission Prediction

            Enter mission details such as:

            - Company
            - Launch Location
            - Launch Time
            - Rocket
            - Mission
            - Rocket Status
            - Price
            - Year
            - Month

            The trained Random Forest model will generate
            a predicted mission outcome.
            """
        )

    with col2:

        st.markdown(
            """
            ### 📊 Project Information

            This project demonstrates:

            - Data preprocessing
            - Feature engineering
            - Machine Learning
            - Model evaluation
            - Confusion matrix analysis
            - Streamlit deployment

            Use the **Navigation menu** on the left
            to explore the application.
            """
        )

    st.divider()

    st.info(
        "👈 Use the Navigation menu from the sidebar "
        "to start a mission prediction or learn more "
        "about the project."
    )

    st.caption(
        "Space Mission Intelligence | "
        "Data Analytics with AI"
    )


# =========================================================
# MISSION PREDICTION PAGE
# =========================================================

elif page == "🔮 Mission Prediction":

    st.title("🔮 Mission Outcome Prediction")

    st.write(
        "Enter the mission information below and click "
        "**Predict Mission Outcome**."
    )

    st.divider()

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

    if st.button(
        "🚀 Predict Mission Outcome",
        type="primary",
        use_container_width=True
    ):

        # Validate categorical inputs
        if not all([
            company.strip(),
            location.strip(),
            time.strip(),
            rocket.strip(),
            mission.strip(),
            rocket_status.strip()
        ]):

            st.warning(
                "⚠️ Please fill in all mission details."
            )

        else:

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

            try:

                prediction = model.predict(input_data)[0]

                st.divider()

                st.header("📊 Prediction Result")

                if prediction == "Success":

                    st.success(
                        f"✅ Predicted Mission Outcome: **{prediction}**"
                    )

                elif prediction == "Failure":

                    st.error(
                        f"❌ Predicted Mission Outcome: **{prediction}**"
                    )

                elif prediction == "Partial Failure":

                    st.warning(
                        f"⚠️ Predicted Mission Outcome: **{prediction}**"
                    )

                elif prediction == "Prelaunch Failure":

                    st.warning(
                        f"⚠️ Predicted Mission Outcome: **{prediction}**"
                    )

                else:

                    st.info(
                        f"Predicted Mission Outcome: **{prediction}**"
                    )

                with st.expander("🔍 View Entered Mission Details"):

                    st.dataframe(
                        input_data,
                        use_container_width=True
                    )

            except Exception as e:

                st.error(
                    "❌ Prediction could not be generated."
                )


# =========================================================
# ABOUT PROJECT PAGE
# =========================================================

elif page == "ℹ️ About Project":

    st.title("ℹ️ About the Project")

    st.subheader(
        "Space Mission Intelligence — Mission Outcome Prediction"
    )

    st.write(
        "This project was developed as part of the "
        "IBM SkillsBuild Academic Internship in "
        "Data Analytics with AI."
    )

    st.divider()

    st.header("🎯 Project Objective")

    st.write(
        "The objective of this project is to analyze historical "
        "space mission data and develop a Machine Learning model "
        "that predicts the outcome category of a mission."
    )

    st.header("🏢 Internship Information")

    st.markdown(
        """
        **Internship:** IBM SkillsBuild Academic Internship – Data Analytics with AI

        **Organization:** Bharat Cares

        **CSR Partner:** IBM CSRBOX
        """
    )

    st.header("📊 Dataset")

    st.write(
        "The project uses a historical space missions dataset "
        "containing information related to companies, launch "
        "locations, rockets, missions, launch time, price and "
        "mission outcomes."
    )

    st.header("🤖 Machine Learning")

    st.markdown(
        """
        The project experimented with:

        - Logistic Regression
        - Random Forest Classifier

        The Random Forest model achieved a test accuracy of
        **90.17%** on the held-out test dataset.
        """
    )

    st.header("⚙️ Data Processing")

    st.markdown(
        """
        The preprocessing workflow included:

        - Removing duplicate records
        - Handling missing values
        - Converting price values to numeric format
        - Extracting Year and Month from Date
        - One-hot encoding categorical features
        - Standardizing numerical features
        - Train-test splitting
        """
    )

    st.header("🛠️ Technologies Used")

    st.markdown(
        """
        - Python
        - Pandas
        - NumPy
        - Scikit-learn
        - Joblib
        - Streamlit
        - Matplotlib
        """
    )

    st.divider()

    st.info(
        "This application is an internship project demonstrating "
        "a Machine Learning workflow and Streamlit-based deployment. "
        "Predictions are based on patterns learned from historical data "
        "and should not be interpreted as real-world mission risk assessments."
    )

    st.caption(
        "Space Mission Intelligence | Bharat Cares × IBM CSRBOX"
    )
