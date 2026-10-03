
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
# CUSTOM UI
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 85% 10%, rgba(56,189,248,.10), transparent 25%),
        radial-gradient(circle at 15% 80%, rgba(139,92,246,.08), transparent 25%),
        #070B14;
    color: #F8FAFC;
    font-family: 'Inter', sans-serif;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1120 0%, #080C16 100%);
    border-right: 1px solid rgba(148,163,184,.12);
}

[data-testid="stSidebar"] * {
    font-family: 'Inter', sans-serif;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

.hero {
    padding: 2.8rem 2.8rem 2.5rem;
    border-radius: 24px;
    border: 1px solid rgba(56,189,248,.18);
    background:
        linear-gradient(135deg, rgba(15,23,42,.96), rgba(17,24,39,.84)),
        radial-gradient(circle at 85% 25%, rgba(56,189,248,.16), transparent 35%);
    box-shadow: 0 20px 60px rgba(0,0,0,.28);
}

.eyebrow {
    color: #38BDF8;
    font-size: .78rem;
    font-weight: 800;
    letter-spacing: .16em;
    text-transform: uppercase;
    margin-bottom: .8rem;
}

.hero h1 {
    font-size: clamp(2.2rem, 5vw, 4.3rem);
    line-height: 1.02;
    margin: 0;
    font-weight: 800;
}

.hero p {
    color: #94A3B8;
    font-size: 1.05rem;
    max-width: 720px;
    line-height: 1.7;
    margin-top: 1.1rem;
}

.section-label {
    color: #94A3B8;
    font-size: .78rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    margin: 2rem 0 .75rem;
}

.card {
    background: rgba(17,24,39,.76);
    border: 1px solid rgba(148,163,184,.12);
    border-radius: 18px;
    padding: 1.35rem 1.4rem;
    min-height: 125px;
    box-shadow: 0 12px 35px rgba(0,0,0,.18);
}

.card .label {
    color: #94A3B8;
    font-size: .82rem;
    margin-bottom: .45rem;
}

.card .value {
    color: #F8FAFC;
    font-size: 1.35rem;
    font-weight: 750;
}

.card .accent {
    color: #38BDF8;
}

.info-card {
    background: linear-gradient(135deg, rgba(17,24,39,.9), rgba(15,23,42,.72));
    border: 1px solid rgba(148,163,184,.11);
    border-radius: 18px;
    padding: 1.45rem;
    height: 100%;
}

.info-card h3 {
    margin-top: 0;
    font-size: 1.05rem;
}

.info-card p, .info-card li {
    color: #94A3B8;
    line-height: 1.65;
}


.result-success, .result-failure, .result-warning, .result-neutral {
    border-radius: 20px;
    padding: 1.6rem 1.7rem;
    margin-top: 1.2rem;
    border: 1px solid rgba(255,255,255,.10);
}

.result-success {
    background: rgba(16,185,129,.10);
    border-color: rgba(52,211,153,.30);
}
.result-failure {
    background: rgba(239,68,68,.10);
    border-color: rgba(248,113,113,.30);
}
.result-warning {
    background: rgba(245,158,11,.10);
    border-color: rgba(251,191,36,.30);
}
.result-neutral {
    background: rgba(56,189,248,.08);
    border-color: rgba(56,189,248,.22);
}

.result-label {
    color: #94A3B8;
    font-size: .76rem;
    letter-spacing: .13em;
    font-weight: 700;
    text-transform: uppercase;
}

.result-value {
    font-size: 2rem;
    font-weight: 800;
    margin-top: .25rem;
}

.footer {
    text-align: center;
    color: #64748B;
    font-size: .78rem;
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid rgba(148,163,184,.08);
}

div[data-testid="stMetric"] {
    background: rgba(17,24,39,.72);
    border: 1px solid rgba(148,163,184,.11);
    padding: 1rem 1.1rem;
    border-radius: 16px;
}

div[data-testid="stMetricLabel"] {
    color: #94A3B8;
}

div[data-testid="stMetricValue"] {
    color: #F8FAFC;
}

.stButton > button {
    border-radius: 12px;
    font-weight: 700;
    min-height: 3rem;
    border: 1px solid rgba(56,189,248,.25);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #0284C7, #7C3AED);
    border: none;
}

div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div {
    background: #0B1220;
    border-color: rgba(148,163,184,.16);
    border-radius: 10px;
}

.stTextInput label, .stNumberInput label {
    color: #CBD5E1;
    font-weight: 600;
}

hr {
    border-color: rgba(148,163,184,.10);
}
</style>
""", unsafe_allow_html=True)

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
except Exception:
    st.error("⚠️ Unable to load the trained model.")
    st.write("Please check the package versions in requirements.txt.")
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("## 🚀 Space Mission")
    st.caption("MISSION INTELLIGENCE SYSTEM")
    st.divider()

    page = st.radio(
        "Navigate",
        ["🏠 Overview", "🔮 Mission Prediction", "ℹ️ About Project"],
        label_visibility="visible"
    )

    st.divider()

    st.markdown("### 🤖 Model Status")
    st.success("Model loaded")
    st.caption("Random Forest")
    st.caption("Test accuracy · 90.17%")

    st.divider()
    st.caption("IBM SkillsBuild Academic Internship")
    st.caption("Data Analytics with AI")

# =========================================================
# OVERVIEW
# =========================================================
if page == "🏠 Overview":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">AI · SPACE ANALYTICS · PREDICTION</div>
        <h1>Space Mission<br>Intelligence</h1>
        <p>
            Explore historical mission data and use a machine learning model
            to predict the outcome category of a space mission.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Model Snapshot</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
            <div class="label">Machine Learning Model</div>
            <div class="value accent">Random Forest</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
            <div class="label">Test Accuracy</div>
            <div class="value">90.17%</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
            <div class="label">Prediction Classes</div>
            <div class="value">4 Outcomes</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Explore the system</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="info-card">
            <h3>🔮 Mission Prediction</h3>
            <p>
                Enter mission characteristics such as company, launch location,
                rocket, mission, price, launch time and date information.
            </p>
            <p><b>Output:</b> predicted mission outcome category.</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Project Intelligence</h3>
            <p>
                Review the project objective, dataset, preprocessing workflow,
                machine learning approach and technologies used.
            </p>
            <p><b>Workflow:</b> Data → Features → Model → Prediction.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Start</div>', unsafe_allow_html=True)
    if st.button("🚀 Open Mission Prediction", type="primary", use_container_width=True):
        st.info("Use the **Mission Prediction** page from the sidebar to enter mission details.")

    st.markdown(
        '<div class="footer">SPACE MISSION INTELLIGENCE · DATA ANALYTICS WITH AI</div>',
        unsafe_allow_html=True
    )

# =========================================================
# MISSION PREDICTION
# =========================================================
elif page == "🔮 Mission Prediction":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">PREDICTION ENGINE</div>
        <h1>Mission Outcome<br>Prediction</h1>
        <p>
            Provide the mission details below and let the trained Random Forest
            model estimate the mission outcome category.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Mission Details</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        company = st.text_input("Company", placeholder="e.g. SpaceX")
        location = st.text_input("Launch Location", placeholder="e.g. Cape Canaveral")
        time = st.text_input("Launch Time", placeholder="e.g. 18:00:00")
        rocket = st.text_input("Rocket", placeholder="Enter rocket name")
        price = st.number_input(
            "Price (USD million)",
            min_value=0.0,
            value=50.0,
            step=1.0
        )

    with col2:
        mission = st.text_input("Mission", placeholder="Enter mission name")
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

    st.write("")
    predict = st.button(
        "🚀 Predict Mission Outcome",
        type="primary",
        use_container_width=True
    )

    if predict:
        if not all([
            company.strip(),
            location.strip(),
            time.strip(),
            rocket.strip(),
            mission.strip(),
            rocket_status.strip()
        ]):
            st.warning("⚠️ Please fill in all mission details.")
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

                if prediction == "Success":
                    box_class = "result-success"
                    icon = "✅"
                elif prediction == "Failure":
                    box_class = "result-failure"
                    icon = "❌"
                elif prediction in ["Partial Failure", "Prelaunch Failure"]:
                    box_class = "result-warning"
                    icon = "⚠️"
                else:
                    box_class = "result-neutral"
                    icon = "🔎"

                st.markdown(f"""
                <div class="{box_class}">
                    <div class="result-label">Predicted Mission Outcome</div>
                    <div class="result-value">{icon} {prediction}</div>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("🔍 View Entered Mission Details"):
                    st.dataframe(input_data, use_container_width=True)

            except Exception:
                st.error("❌ Prediction could not be generated.")

    st.markdown(
        '<div class="footer">MODEL · RANDOM FOREST · TEST ACCURACY 90.17%</div>',
        unsafe_allow_html=True
    )

# =========================================================
# ABOUT
# =========================================================
elif page == "ℹ️ About Project":
    st.markdown("""
    <div class="hero">
        <div class="eyebrow">PROJECT INFORMATION</div>
        <h1>About the Project</h1>
        <p>
            Space Mission Intelligence combines historical space mission
            analysis with a machine learning prediction workflow.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Project Overview</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="info-card">
            <h3>🎯 Objective</h3>
            <p>
                Analyze historical space mission data and develop a machine
                learning model that predicts the outcome category of a mission.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h3>🏢 Internship</h3>
            <p><b>IBM SkillsBuild Academic Internship</b></p>
            <p>Bharat Cares · IBM CSRBOX</p>
            <p>Data Analytics with AI</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Dataset & Machine Learning</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.markdown("""
        <div class="info-card">
            <h3>📊 Dataset</h3>
            <p>
                Historical space mission information covering companies,
                launch locations, rockets, missions, launch time, price and
                mission outcomes.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="info-card">
            <h3>🤖 Machine Learning</h3>
            <p>
                Models explored: Logistic Regression and Random Forest Classifier.
            </p>
            <p><b>Selected model:</b> Random Forest</p>
            <p><b>Test accuracy:</b> 90.17%</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Data Processing</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card">
        <h3>⚙️ Preprocessing Workflow</h3>
        <p>
            Duplicate removal · Missing-value handling · Price conversion ·
            Year/Month extraction · One-hot encoding · Numerical standardization ·
            Train-test splitting
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Technology Stack</div>', unsafe_allow_html=True)

    tech = st.columns(7)
    technologies = ["Python", "Pandas", "NumPy", "Scikit-learn", "Joblib", "Streamlit", "Matplotlib"]
    for col, tech_name in zip(tech, technologies):
        with col:
            st.markdown(
                f'<div class="card" style="min-height:0;text-align:center;padding:.9rem .5rem;">'
                f'<div class="value" style="font-size:.9rem;">{tech_name}</div></div>',
                unsafe_allow_html=True
            )

    st.info(
        "This application is an internship project demonstrating a Machine Learning "
        "workflow and Streamlit-based deployment. Predictions are based on patterns "
        "learned from historical data and should not be interpreted as real-world "
        "mission risk assessments."
    )

    st.markdown(
        '<div class="footer">SPACE MISSION INTELLIGENCE · BHARAT CARES × IBM CSRBOX</div>',
        unsafe_allow_html=True
    )
