import streamlit as st
from modules.registration import registration_screen
from modules.initial_quiz import initial_quiz_screen
from modules.training_flow import training_flow
from modules.home import home_screen
from modules.dashboard import dashboard
from supabase_client import supabase


def load_css():
    with open("styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_progress():
    course_steps = [
        "video1",
        "quiz1",
        "video2",
        "quiz2",
        "video3",
        "quiz3",
        "video4",
        "quiz4",
        "completed"
    ]

    current_step = st.session_state.get("training_step", "video1")

    if current_step not in course_steps:
        return 0

    return course_steps.index(current_step) / (len(course_steps) - 1)


st.set_page_config(
    page_title="Training Platform",
    layout="wide"
)

load_css()

# --------- ESTADOS ---------
if "selected_training" not in st.session_state:
    st.session_state["selected_training"] = None

if "go_to_registration" not in st.session_state:
    st.session_state["go_to_registration"] = False

if "initial_quiz_done" not in st.session_state:
    st.session_state["initial_quiz_done"] = False

# --------- SIDEBAR ---------
with st.sidebar:
    st.title("Plataforma de entrenamiento")

    if "user" in st.session_state:
        st.success(f"👤 {st.session_state['user']['name']}")
    # -------- NAVIGATION --------
    st.markdown("### Navegación")

    if st.button("🏠 Inicio"):
        st.session_state["selected_training"] = None
        st.session_state.pop("training_step", None)
        st.session_state.pop("course_name", None)
        st.session_state["initial_quiz_done"] = False
        st.rerun()


    if st.button("📊 Dashboard"):
        st.session_state["selected_training"] = "dashboard"
        st.rerun()

    # Curso
    if "course_name" in st.session_state:

        st.markdown(
            f"""
            <div style="
                background-color:#D3D3D3;
                padding:10px;
                border-radius:10px;
                margin-top:10px;
            ">
                <strong>{st.session_state['course_name']}</strong>
            </div>
            """,
            unsafe_allow_html=True
        )

        #  PROGRESO
        progress = get_progress()
        st.progress(progress)
        st.caption(f"{int(progress * 100)}% completado")


# --------- FLUJO PRINCIPAL ---------
# --------- FLUJO PRINCIPAL ---------

# DASHBOARD (prioridad alta)
if st.session_state.get("selected_training") == "dashboard":
    dashboard()

# HOME
elif st.session_state["selected_training"] is None:
    home_screen()

# REGISTRO
elif "user" not in st.session_state:
    registration_screen()

# QUIZ INICIAL
elif not st.session_state["initial_quiz_done"]:
    initial_quiz_screen()

# TRAINING
else:
    training_flow()