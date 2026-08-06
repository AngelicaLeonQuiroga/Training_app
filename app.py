import streamlit as st
from modules.registration import registration_screen
from modules.initial_quiz import initial_quiz_screen
from modules.training_flow import training_flow
from modules.home import home_screen
from modules.dashboard import dashboard
from supabase_client import supabase
from modules.who_we_are import who_we_are
from modules.progress import get_progress
from modules.courses.biosecurity.biosecurity_initial_quiz import (
    initial_quiz_screen as biosecurity_initial_quiz
)

from modules.courses.biosecurity.biosecurity_training_flow import (
    training_flow as biosecurity_training
)
from modules.courses.chemical.chemicals_initial_quiz import (
    initial_quiz_screen as chemicals_initial_quiz
)

from modules.courses.chemical.chemicals_training_flow import (
    training_flow as chemicals_training
)

def load_css():
    with open("styles/main.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def get_progress_percentage():

    if st.session_state.get("course_name") in [
        "Bioseguridad",
        "Seguridad y manejo de químicos"
        ]:

        course_steps = [
            "video1",
            "quiz1",
            "video2",
            "quiz2",
            "video3",
            "quiz3",
            "completed"
        ]

    else:

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
        st.session_state.pop("progress_loaded", None)
        st.rerun()


    if st.button("📊 Panel de control y resultados"):
        st.session_state["selected_training"] = "dashboard"
        st.rerun()

    if st.button("👥 Quiénes somos"):
        st.session_state["selected_training"] = "about"
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
        progress = get_progress_percentage()
        st.progress(progress)
        st.caption(f"{int(progress * 100)}% completado")


# --------- FLUJO PRINCIPAL ---------
# --------- FLUJO PRINCIPAL ---------

# DASHBOARD (prioridad alta)
if st.session_state.get("selected_training") == "dashboard":
    dashboard()
#quienes sommos
elif st.session_state.get("selected_training") == "about":
    who_we_are()

# HOME
elif st.session_state["selected_training"] is None:
    home_screen()

# REGISTRO
elif "user" not in st.session_state:
    registration_screen()

# QUIZ INICIAL
# QUIZ INICIAL
elif not st.session_state["initial_quiz_done"]:

    if st.session_state.get("course_name") == "Bioseguridad":
        biosecurity_initial_quiz()

    elif st.session_state.get("course_name") == "Seguridad y manejo de químicos":
        chemicals_initial_quiz()

    else:
        initial_quiz_screen()

# TRAINING
else:

    if st.session_state.get("course_name") == "Bioseguridad":
        biosecurity_training()

    elif st.session_state.get("course_name") == "Seguridad y manejo de químicos":
        chemicals_training()

    else:
        training_flow()