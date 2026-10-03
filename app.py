import html as _html
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# =========================================================
# PAGE CONFIGURATION
# =========================================================
st.set_page_config(
    page_title="Space Mission Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# STYLES
# =========================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
    --bg: #060A12;
    --panel: #0D1424;
    --panel-2: #101A2E;
    --line: rgba(148,163,184,.14);
    --text: #F1F5F9;
    --muted: #8A98AE;
    --blue: #5EA8FF;
    --violet: #8B7CF6;
}

/* ---------- Base (font set on .stApp only, so icon fonts stay intact) ---------- */
.stApp {
    background:
        radial-gradient(1000px 520px at 88% -8%, rgba(94,168,255,.10), transparent 60%),
        radial-gradient(800px 480px at 0% 100%, rgba(139,124,246,.07), transparent 60%),
        var(--bg);
    color: var(--text);
    font-family: 'Inter', -apple-system, 'Segoe UI', sans-serif;
}
.stApp p, .stApp label, .stApp h1, .stApp h2, .stApp h3 { font-family: 'Inter', sans-serif; }

/* ---------- Hide native chrome (header kept transparent so sidebar toggle works) ---------- */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; height: 2.5rem; }

.block-container { max-width: 1180px; padding: 2rem 2rem 2rem; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: #080D18;
    border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div:first-child { padding-top: 0; }
[data-testid="stSidebarContent"] { overflow-y: auto; }
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"] { padding: 1.4rem 1rem 1rem; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: .35rem; }

.brand { display: flex; align-items: center; gap: .75rem; padding: 0 .25rem .9rem; }
.brand-mark {
    width: 38px; height: 38px; border-radius: 10px; display: flex;
    align-items: center; justify-content: center; font-size: 1.15rem;
    background: linear-gradient(135deg, rgba(94,168,255,.22), rgba(139,124,246,.22));
    border: 1px solid rgba(94,168,255,.28);
}
.brand-name { font-weight: 700; font-size: 1rem; line-height: 1.2; color: var(--text); }
.brand-sub { font-size: .72rem; color: var(--muted); }

.side-label {
    font-size: .68rem; font-weight: 600; letter-spacing: .1em; color: #5B6980;
    padding: .9rem .35rem .3rem; text-transform: uppercase;
}

/* Radio -> nav list */
[data-testid="stSidebar"] div[role="radiogroup"] { gap: .2rem; }
[data-testid="stSidebar"] div[role="radiogroup"] > label {
    width: 100%; padding: .55rem .75rem; border-radius: 10px;
    border: 1px solid transparent; cursor: pointer; margin: 0;
    transition: background .15s ease;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child { display: none; }
[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    color: #A9B6C9; font-size: .92rem; font-weight: 500;
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:hover { background: rgba(148,163,184,.07); }
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: rgba(94,168,255,.10); border-color: rgba(94,168,255,.28);
}
[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) p {
    color: #FFFFFF; font-weight: 600;
}

.status-card {
    background: var(--panel); border: 1px solid var(--line); border-radius: 12px;
    padding: .9rem 1rem; margin-top: .2rem;
}
.status-row { display: flex; justify-content: space-between; align-items: center; padding: .22rem 0; font-size: .82rem; }
.status-row span:first-child { color: var(--muted); }
.status-row span:last-child { color: var(--text); font-weight: 600; }
.dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: #34D399; margin-right: .4rem; }
.side-foot { color: #5B6980; font-size: .72rem; line-height: 1.5; padding: .9rem .35rem 0; }
.side-foot b { color: #8A98AE; font-weight: 600; }

/* ---------- Hero ---------- */
.hero {
    padding: 2.6rem 2.6rem 2.4rem; border-radius: 20px; border: 1px solid var(--line);
    background: linear-gradient(135deg, rgba(16,26,46,.95), rgba(10,15,28,.95));
}
.eyebrow { color: var(--blue); font-size: .74rem; font-weight: 600; letter-spacing: .14em; margin-bottom: .9rem; }
.hero h1 {
    margin: 0; padding: 0; color: #FFFFFF; font-weight: 700; letter-spacing: -.02em;
    font-size: clamp(2rem, 4.4vw, 3.3rem); line-height: 1.08;
}
.hero p { color: var(--muted); font-size: 1.02rem; line-height: 1.7; max-width: 640px; margin: 1rem 0 0; }

/* ---------- Sections & cards ---------- */
.section-title { color: var(--text); font-size: 1.05rem; font-weight: 600; margin: 2.2rem 0 .2rem; }
.section-sub { color: var(--muted); font-size: .88rem; margin: 0 0 1rem; }

.metric, .feature, .panel {
    background: var(--panel); border: 1px solid var(--line); border-radius: 14px;
}
.metric { padding: 1.2rem 1.3rem; height: 100%; }
.metric .m-label { color: var(--muted); font-size: .8rem; margin-bottom: .4rem; }
.metric .m-value { color: #FFFFFF; font-size: 1.55rem; font-weight: 700; letter-spacing: -.01em; }
.metric .m-note { color: #5B6980; font-size: .78rem; margin-top: .25rem; }

.feature { padding: 1.5rem; height: 100%; }
.feature h3 { margin: 0 0 .5rem; font-size: 1.05rem; font-weight: 600; color: #FFFFFF; }
.feature p { margin: 0; color: var(--muted); font-size: .92rem; line-height: 1.65; }
.feature .tag {
    display: inline-block; margin-top: 1rem; font-size: .76rem; color: var(--blue);
    background: rgba(94,168,255,.08); border: 1px solid rgba(94,168,255,.2);
    border-radius: 999px; padding: .2rem .65rem;
}

.panel { padding: 1.4rem 1.5rem; height: 100%; }
.panel h3 { margin: 0 0 .5rem; font-size: 1rem; font-weight: 600; color: #FFFFFF; }
.panel p { margin: 0 0 .45rem; color: var(--muted); font-size: .92rem; line-height: 1.65; }
.panel p b { color: var(--text); font-weight: 600; }

.steps { display: flex; flex-wrap: wrap; gap: .5rem; margin-top: .4rem; }
.chip {
    background: var(--panel-2); border: 1px solid var(--line); color: #C5D0E0;
    border-radius: 8px; padding: .4rem .8rem; font-size: .84rem; font-weight: 500;
}

/* ---------- Inputs ---------- */
.stTextInput label p, .stNumberInput label p { color: #C5D0E0; font-size: .86rem; font-weight: 500; }
div[data-baseweb="input"], div[data-baseweb="base-input"] {
    background: #0A1120 !important; border-radius: 10px !important;
}
div[data-baseweb="input"] { border: 1px solid var(--line) !important; }
div[data-baseweb="input"]:focus-within { border-color: rgba(94,168,255,.6) !important; }
div[data-baseweb="input"] input { color: var(--text) !important; }
div[data-testid="stNumberInput"] button { background: #0F192D; color: #C5D0E0; border: none; }

/* ---------- Buttons ---------- */
.stButton > button, .stButton > button[kind="primary"],
button[data-testid="stBaseButton-primary"] {
    border-radius: 12px; min-height: 3rem; font-weight: 600; font-size: .95rem;
    border: 1px solid transparent; color: #FFFFFF;
    background: linear-gradient(90deg, #2563EB, #6D5BF0);
    transition: filter .15s ease;
}
.stButton > button:hover { filter: brightness(1.12); border-color: transparent; color: #FFFFFF; }
.stButton > button:focus:not(:active) { border-color: transparent; color: #FFFFFF; }

/* ---------- Result card ---------- */
.result { border-radius: 16px; padding: 1.5rem 1.7rem; margin-top: 1.5rem; border: 1px solid var(--line); background: var(--panel); }
.result .r-label { color: var(--muted); font-size: .76rem; font-weight: 600; letter-spacing: .1em; text-transform: uppercase; }
.result .r-value { font-size: 1.9rem; font-weight: 700; margin: .3rem 0 .4rem; letter-spacing: -.01em; }
.result .r-note { color: #A9B6C9; font-size: .92rem; line-height: 1.6; margin: 0; }
.result-success { border-left: 4px solid #34D399; background: linear-gradient(90deg, rgba(52,211,153,.09), var(--panel) 60%); }
.result-success .r-value { color: #6EE7B7; }
.result-failure { border-left: 4px solid #F87171; background: linear-gradient(90deg, rgba(248,113,113,.09), var(--panel) 60%); }
.result-failure .r-value { color: #FCA5A5; }
.result-warning { border-left: 4px solid #FBBF24; background: linear-gradient(90deg, rgba(251,191,36,.09), var(--panel) 60%); }
.result-warning .r-value { color: #FCD34D; }
.result-neutral { border-left: 4px solid var(--blue); background: linear-gradient(90deg, rgba(94,168,255,.09), var(--panel) 60%); }
.result-neutral .r-value { color: #93C5FD; }

/* ---------- Expander / alerts ---------- */
[data-testid="stExpander"] { border: 1px solid var(--line); border-radius: 12px; background: var(--panel); margin-top: 1rem; }
[data-testid="stExpander"] summary p { color: #C5D0E0; font-weight: 500; }
[data-testid="stAlert"] { border-radius: 12px; }

/* ---------- Footer ---------- */
.site-footer {
    margin-top: 3rem; padding-top: 1.1rem; border-top: 1px solid var(--line);
    color: #5B6980; font-size: .78rem; line-height: 1.6; text-align: center;
}
.site-footer b { color: #8A98AE; font-weight: 600; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def render(markup: str) -> None:
    """Render HTML safely: strip indentation/newlines so Markdown never treats it as a code block."""
    flat = "".join(line.strip() for line in markup.strip().splitlines())
    st.markdown(flat, unsafe_allow_html=True)


def hero(eyebrow: str, title: str, subtitle: str) -> None:
    render(f"""
    <div class="hero">
        <div class="eyebrow">{eyebrow}</div>
        <h1>{title}</h1>
        <p>{subtitle}</p>
    </div>
    """)


def section(title: str, sub: str = "") -> None:
    sub_html = f'<div class="section-sub">{sub}</div>' if sub else ""
    render(f'<div class="section-title">{title}</div>{sub_html}')


def footer(text: str) -> None:
    render(f'<div class="site-footer">{text}</div>')


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
# NAVIGATION STATE
# =========================================================
PAGES = ["Overview", "Mission Prediction", "About Project"]


def go_to_prediction():
    st.session_state["page"] = "Mission Prediction"


# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    render("""
    <div class="brand">
        <div class="brand-mark">🚀</div>
        <div>
            <div class="brand-name">Space Mission</div>
            <div class="brand-sub">Mission Intelligence System</div>
        </div>
    </div>
    <div class="side-label">Navigation</div>
    """)

    page = st.radio(
        "Navigate",
        PAGES,
        key="page",
        label_visibility="collapsed",
    )

    render("""
    <div class="side-label">Model status</div>
    <div class="status-card">
        <div class="status-row"><span>Status</span><span><i class="dot"></i>Loaded</span></div>
        <div class="status-row"><span>Model</span><span>Random Forest</span></div>
        <div class="status-row"><span>Test accuracy</span><span>90.17%</span></div>
    </div>
    <div class="side-foot">
        <b>IBM SkillsBuild Academic Internship</b><br>
        Data Analytics with AI
    </div>
    """)

# =========================================================
# OVERVIEW
# =========================================================
if page == "Overview":
    hero(
        "AI · SPACE ANALYTICS · PREDICTION",
        "Space Mission Intelligence",
        "A machine learning system trained on historical launch records that "
        "predicts the outcome category of a space mission from its key characteristics.",
    )

    section("Model snapshot")
    c1, c2, c3 = st.columns(3)
    with c1:
        render("""
        <div class="metric">
            <div class="m-label">Machine learning model</div>
            <div class="m-value">Random Forest</div>
            <div class="m-note">Classifier</div>
        </div>
        """)
    with c2:
        render("""
        <div class="metric">
            <div class="m-label">Test accuracy</div>
            <div class="m-value">90.17%</div>
            <div class="m-note">On held-out data</div>
        </div>
        """)
    with c3:
        render("""
        <div class="metric">
            <div class="m-label">Prediction classes</div>
            <div class="m-value">4 outcomes</div>
            <div class="m-note">Mission outcome categories</div>
        </div>
        """)

    section("What you can do")
    c1, c2 = st.columns(2)
    with c1:
        render("""
        <div class="feature">
            <h3>Mission Prediction</h3>
            <p>Enter the company, launch site, rocket, mission, price and launch
            date to get a predicted mission outcome category.</p>
            <span class="tag">Data → Features → Model → Prediction</span>
        </div>
        """)
    with c2:
        render("""
        <div class="feature">
            <h3>Project Information</h3>
            <p>Review the project objective, dataset, preprocessing workflow,
            model choice and the technologies behind the app.</p>
            <span class="tag">Objective · Dataset · Model</span>
        </div>
        """)

    st.write("")
    st.button(
        "Open Mission Prediction",
        type="primary",
        use_container_width=True,
        on_click=go_to_prediction,
    )

    footer("Space Mission Intelligence · Data Analytics with AI")

# =========================================================
# MISSION PREDICTION
# =========================================================
elif page == "Mission Prediction":
    hero(
        "PREDICTION ENGINE",
        "Mission Outcome Prediction",
        "Provide the mission details below and the trained Random Forest model "
        "will estimate the mission outcome category.",
    )

    section("Mission details", "All fields are required.")

    col1, col2 = st.columns(2, gap="large")

    with col1:
        company = st.text_input("Company", placeholder="e.g. SpaceX")
        location = st.text_input("Launch Location", placeholder="e.g. Cape Canaveral")
        time = st.text_input("Launch Time", placeholder="e.g. 18:00:00")
        rocket = st.text_input("Rocket", placeholder="Enter rocket name")
        price = st.number_input(
            "Price (USD million)",
            min_value=0.0,
            value=50.0,
            step=1.0,
        )

    with col2:
        mission = st.text_input("Mission", placeholder="Enter mission name")
        rocket_status = st.text_input(
            "Rocket Status",
            placeholder="e.g. StatusActive",
        )
        year = st.number_input(
            "Year",
            min_value=1950,
            max_value=2100,
            value=2020,
            step=1,
        )
        month = st.number_input(
            "Month",
            min_value=1,
            max_value=12,
            value=1,
            step=1,
        )

    st.write("")
    predict = st.button(
        "Predict Mission Outcome",
        type="primary",
        use_container_width=True,
    )

    if predict:
        if not all([
            company.strip(),
            location.strip(),
            time.strip(),
            rocket.strip(),
            mission.strip(),
            rocket_status.strip(),
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
                "Month": month,
            }])

            try:
                prediction = model.predict(input_data)[0]

                if prediction == "Success":
                    box_class = "result-success"
                    icon = "✅"
                    note = "The model expects this mission to complete successfully."
                elif prediction == "Failure":
                    box_class = "result-failure"
                    icon = "❌"
                    note = "The model expects this mission to end in failure."
                elif prediction == "Partial Failure":
                    box_class = "result-warning"
                    icon = "⚠️"
                    note = "The model expects the mission to be only partly successful."
                elif prediction == "Prelaunch Failure":
                    box_class = "result-warning"
                    icon = "⚠️"
                    note = "The model expects a failure before the vehicle launches."
                else:
                    box_class = "result-neutral"
                    icon = "🔎"
                    note = "Predicted outcome category based on the details provided."

                safe_prediction = _html.escape(str(prediction))
                render(f"""
                <div class="result {box_class}">
                    <div class="r-label">Predicted mission outcome</div>
                    <div class="r-value">{icon} {safe_prediction}</div>
                    <p class="r-note">{note}</p>
                </div>
                """)

                with st.expander("🔍 View Entered Mission Details"):
                    st.dataframe(input_data, use_container_width=True)

            except Exception:
                st.error("❌ Prediction could not be generated.")

    footer(
        "<b>Random Forest</b> · Test accuracy 90.17%<br>"
        "Predictions reflect patterns in historical data and are not real-world risk assessments."
    )

# =========================================================
# ABOUT
# =========================================================
elif page == "About Project":
    hero(
        "PROJECT INFORMATION",
        "About the Project",
        "Space Mission Intelligence combines historical space mission analysis "
        "with a machine learning prediction workflow.",
    )

    section("Project overview")
    c1, c2 = st.columns(2)
    with c1:
        render("""
        <div class="panel">
            <h3>🎯 Project Objective</h3>
            <p>Analyze historical space mission data and develop a machine
            learning model that predicts the outcome category of a mission.</p>
        </div>
        """)
    with c2:
        render("""
        <div class="panel">
            <h3>🏢 Internship</h3>
            <p><b>IBM SkillsBuild Academic Internship</b></p>
            <p>Bharat Cares · IBM CSRBOX</p>
            <p>Data Analytics with AI</p>
        </div>
        """)

    section("Dataset and machine learning")
    c1, c2 = st.columns(2)
    with c1:
        render("""
        <div class="panel">
            <h3>📊 Dataset</h3>
            <p>Historical space mission information covering companies,
            launch locations, rockets, missions, launch time, price and
            mission outcomes.</p>
        </div>
        """)
    with c2:
        render("""
        <div class="panel">
            <h3>🤖 Machine Learning</h3>
            <p>Models explored: Logistic Regression and Random Forest Classifier.</p>
            <p><b>Selected model:</b> Random Forest</p>
            <p><b>Test accuracy:</b> 90.17%</p>
        </div>
        """)

    section("Data processing")
    steps = [
        "Duplicate removal",
        "Missing-value handling",
        "Price conversion",
        "Year/Month extraction",
        "One-hot encoding",
        "Numerical standardization",
        "Train-test splitting",
    ]
    chips = "".join(f'<span class="chip">{s}</span>' for s in steps)
    render(f"""
    <div class="panel">
        <h3>⚙️ Preprocessing workflow</h3>
        <div class="steps">{chips}</div>
    </div>
    """)

    section("Technologies used")
    technologies = ["Python", "Pandas", "NumPy", "Scikit-learn", "Joblib", "Streamlit", "Matplotlib"]
    tech_chips = "".join(f'<span class="chip">{t}</span>' for t in technologies)
    render(f'<div class="panel"><div class="steps">{tech_chips}</div></div>')

    footer(
        "Internship project demonstrating a machine learning workflow and Streamlit deployment.<br>"
        "Predictions are based on patterns in historical data and should not be treated as "
        "real-world mission risk assessments.<br>"
        "<b>Bharat Cares × IBM CSRBOX</b>"
    )
