import streamlit as st
from modules.progress import (
    save_progress,
    get_progress,
    mark_completed
)
from supabase_client import supabase
from datetime import datetime


course_steps = [
    ("video1", "Video 1"),
    ("quiz1", "Quiz 1"),
    ("video2", "Video 2"),
    ("quiz2", "Quiz 2"),
    ("video3", "Video 3"),
    ("quiz3", "Quiz 3"),
    ("completed", "Finalizado")
]

def render_video_module(video_id, completed_key, next_step, module_title):
    st.header(module_title)

    if completed_key not in st.session_state:
        st.session_state[completed_key] = False

    if not st.session_state[completed_key]:
        # Mostrar el video
        st.video(f"https://youtu.be/{video_id}")
        st.info("Mira el video completo, despues click en continuar")
        st.markdown("---")

        #st.markdown("<br><br>", unsafe_allow_html=True)
        # Botón manual para continuar
        if st.button("Continuar"):
            st.session_state[completed_key] = True
            st.rerun()

    else:
        st.success("Video completado")
        st.markdown("---")
        #st.markdown("<br><br>", unsafe_allow_html=True)
        if st.button("Continue al Quiz"):
            st.session_state[completed_key] = False
            st.session_state["training_step"] = next_step
            save_progress(
                st.session_state["user"]["email"],
                st.session_state.get(
                    "course_name",
                    "Bioseguridad"
                ),
                next_step,
                pre_test_completed=True
            )
            st.rerun()

def training_flow():
    
    if "post_answers" not in st.session_state:
        st.session_state["post_answers"] = {}

    if "post_results" not in st.session_state:
        st.session_state["post_results"] = {}

    # Inicializar training_step 
    
    if "training_step" not in st.session_state:

        saved_progress = None

        if "user" in st.session_state:

            saved_progress = get_progress(
                st.session_state["user"]["email"],
                st.session_state.get(
                    "course_name",
                    "Bioseguridad"
                )
            )

        if saved_progress:

            if saved_progress.get("pre_test_completed"):
                st.session_state["initial_quiz_done"] = True

            st.session_state["training_step"] = (
                saved_progress["current_step"]
            )

        else:

            st.session_state["training_step"] = "video1"

    if "sidebar_open" not in st.session_state:
        st.session_state["sidebar_open"] = True

    step = st.session_state["training_step"]
    
    #botton desplegable    
    col_toggle, _ = st.columns([1, 10])

    with col_toggle:
        if st.button("☰"):
            st.session_state["sidebar_open"] = not st.session_state["sidebar_open"]
            st.rerun()
    
    #layout
    if st.session_state["sidebar_open"]:
        sidebar_col, main_col = st.columns([1, 3])
    else:
        sidebar_col, main_col = st.columns([0.2, 4])

    #sidebar
    with sidebar_col:
        if st.session_state["sidebar_open"]:

            st.markdown("### 📚 Progreso del curso")

            step_keys = [s[0] for s in course_steps]

            for key, label in course_steps:
                if key == step:
                    st.markdown(f"👉 **{label}**")
                elif step_keys.index(key) < step_keys.index(step):
                    st.markdown(f"✅ {label}")
                else:
                    st.markdown(f"⬜ {label}")

    #principal
    with main_col:
        st.title("Entrenamiento en progreso")

        # -------- VIDEO1 --------
        if step == "video1":
            render_video_module(
                video_id="OWW2OET7ms4",
                completed_key="video1_completed",
                next_step="quiz1",
                module_title="Módulo 1 – Que es la bioseguridad y porque importa"

        )
            # -------- QUIZ 1 --------
        elif step == "quiz1":
            
            st.header("Quiz 1")

            correct_answers = {
                "q4": "Minimizar la entrada y propagación de gérmenes para proteger animales y trabajadores",
                    "q5": "Falso",
                    "q6": "Conocer su origen y observarlos antes de juntarlos",
                    "q7": "Sí, pueden llegar con estiércol o bacterias pegadas en ruedas y equipo",
                    "q8": "Todas las anteriores",
            }

            with st.form("quiz1_form"):
                q4 = st.radio(
                    "1. ¿Cuál es el principal objetivo de un plan de bioseguridad en una granja lechera?",
                    ["Evitar que los trabajadores se enfermen", 
                    "Reducir la cantidad de medicamentos que se usan en los animales",
                    "Minimizar la entrada y propagación de gérmenes para proteger animales y trabajadores", 
                    "No sé "],
                    index=None
                )
                q5 = st.radio(
                    "2. Si una enfermedad ya está presente en la granja, es fácil eliminarla por completo",
                    ["Verdadero",
                    "Falso",
                    "No sé "],
                    index=None
                )
                q6 = st.radio(
                    "3. ¿Cuál de estas acciones es más importante cuando llegan animales nuevos a la granja?",
                    ["Mezclarlos de inmediato con el resto para que se adapten",
                    "Conocer su origen y observarlos antes de juntarlos",
                    "Darles alimento y agua limpia",
                    "No sé "],
                    index=None
                )
                q7 = st.radio(
                    "4. ¿Los vehículos representan un riesgo de bioseguridad?",
                    ["Sí, el ruido estresa a las vacas",
                    "Sí, pero solo cuando transportan animales",
                    "Sí, pueden llegar con estiércol o bacterias pegadas en ruedas y equipo",
                    "No, los vehículos no representan un riesgo",
                    "No sé "],
                    index=None
                )
                q8 = st.radio(
                     "5. ¿Cuál de estos animales es un vector de enfermedades?",
                    ["Insectos",
                    "Roedores y aves",
                    "Mascotas",
                    "Fauna silvestre",
                    "Todas las anteriores",
                    "No sé"],
                    index=None
                )

                submit = st.form_submit_button("Enviar")

                if submit:
                    
                # VALIDACIÓN
                    if None in [q4, q5, q6, q7, q8]:
                        st.error("Porfavor conteste todas las preguntas antes de continuar.")
                        st.stop()

                    answers = {"q4": q4, "q5": q5,
                            "q6": q6, "q7": q7,"q8": q8,}
                    for q in answers:
                        is_correct = answers[q] == correct_answers[q]
                        st.session_state["post_answers"][q] = answers[q]
                        st.session_state["post_results"][q + "_correct"] = is_correct
                    st.session_state["training_step"] = "video2"

                    save_progress(
                        st.session_state["user"]["email"],
                        st.session_state.get(
                            "course_name",
                            "Bioseguridad"
                        ),
                        "video2",
                        pre_test_completed=True
                    )

                    st.rerun()

        # -------- VIDEO2 --------
        elif step == "video2":
            render_video_module(
                video_id="INC6l01JVLE",
                completed_key="video2_completed",
                next_step="quiz2",
                module_title="Módulo 2 – Qué acciones concretas debe realizar el trabajador"
        )
        # -------- QUIZ 2 --------
        elif step == "quiz2":
            st.header("Quiz 2")

            correct_answers = {
                    "q9": "Prevenir la propagación de enfermedades y microorganismos",
                    "q10": "Lavarse las manos durante al menos 20 segundos",
                    "q11": "Cuando se cambie de tarea o exista riesgo de contaminación cruzada",
                    "q12": "Lavarse las manos y seguir el protocolo de bioseguridad de la granja",
                    "q13": "Lavar inmediatamente la herida, informar al supervisor y buscar atención médica"
                }

            with st.form("quiz2_form"):
                q9 = st.radio(
                    "6. ¿Cuál es el propósito principal de usar guantes y cubrebotas en la granja?",
                    ["Mantener la ropa limpia",
                    "Prevenir la propagación de enfermedades y microorganismos",
                    "Trabajar más rápido y que no se resbalen los implementos",
                    "Evitar mojarse las manos",
                    "No sé"],
                    index=None
                )
                q10 = st.radio(
                    "7. Antes de colocarse los guantes, se debe:",
                    ["Lavarse las manos durante al menos 20 segundos",
                    "Limpiar los guantes con agua",
                    "Usar desinfectante únicamente",
                    "Ninguna de las anteriores",
                    "No sé "],index=None
                )
                q11 = st.radio(
                    "8. ¿Cuándo debe cambiarse un par de guantes desechables?",
                    ["Solo cuando estén rotos",
                    "Al final de la semana",
                    "Cuando se cambie de tarea o exista riesgo de contaminación cruzada",
                    "Nunca es necesario cambiarlos",
                    "No sé "],index=None
                    
                )
                q12 = st.radio(
                    "9. ¿Qué deben hacer los visitantes antes de ingresar a las áreas de animales?",
                    ["Entrar directamente si tienen experiencia",
                    "Lavarse las manos y seguir el protocolo de bioseguridad de la granja",
                    "Solo usar botas limpias",
                    "Firmar un registro únicamente",
                    "No sé"]
                    ,index=None
                )
                q13 = st.radio(
                    "10. Si ocurre un pinchazo accidental con una aguja contaminada, la persona debe:",
                    ["Continuar trabajando normalmente",
                    "Tirar la aguja a la basura regular",
                    "Aplicar desinfectante y regresar al trabajo",
                    "Lavar inmediatamente la herida, informar al supervisor y buscar atención médica",
                    "No sé"]
                    ,index=None
                )

                submit = st.form_submit_button("Enviar")

                if submit:
                    
                    if None in [q9, q10, q11, q12, q13]:
                            st.error("Porfavor conteste todas las preguntas antes de continuar.")
                            st.stop()

                    answers = {"q9": q9, "q10": q10, "q11": q11, "q12": q12, "q13": q13}

                    for q in answers:
                        is_correct = answers[q] == correct_answers[q]
                        st.session_state["post_answers"][q] = answers[q]
                        st.session_state["post_results"][q + "_correct"] = is_correct                    
                    st.session_state["training_step"] = "video3"

                    save_progress(
                        st.session_state["user"]["email"],
                        st.session_state.get(
                            "course_name",
                            "Bioseguridad"
                        ),
                        "video3",
                        pre_test_completed=True
                    )

                    st.rerun()


        # -------- VIDEO 3 --------
        elif step == "video3":
            render_video_module(
                video_id="qKEnYE3WPKg",
                completed_key="video3_completed",
                next_step="quiz3",
                module_title="Módulo 3 – Qué hacer cuando se detecta una enfermedad"
        )
        # -------- QUIZ 3 --------
        elif step == "quiz3":
            st.header("Quiz 3")
            
            correct_answers = {
                    "q14": "Fiebre o temperatura corporal elevada",
                    "q15": "Reportarlo inmediatamente al supervisor o veterinario",
                    "q16": "Para evitar la propagación de enfermedades al resto del hato",
                    "q17": "La identificación, ubicación, síntomas observados y cuándo comenzaron los cambios",
                    "q18": "Lavarse las manos y seguir los procedimientos de higiene establecidos"
                }
            with st.form("quiz3_form"):
                q14 = st.radio(
                    "11. ¿Cuál de las siguientes es una señal de alerta que puede indicar que un animal está enfermo?",
                    ["Mayor consumo de alimento",
                    "Fiebre o temperatura corporal elevada",
                    "Aumento de actividad física",
                    "Mayor producción de leche",
                    "No sé"]
                    ,index=None
                )
                q15 = st.radio(
                    "12. Si observas un animal con signos de enfermedad, ¿qué debes hacer primero?",
                    ["Esperar varios días para confirmar que está enfermo",
                    "Administrarle medicamentos por tu cuenta",
                    "Reportarlo inmediatamente al supervisor o veterinario",
                    "Moverlo a otra área sin autorización",
                    "No sé "],
                    index=None
                )
                q16 = st.radio(
                    "13. ¿Por qué es importante aislar a los animales enfermos?",
                    ["Para facilitar la alimentación del animal",
                    "Para aumentar su producción de leche",
                    "Para evitar la propagación de enfermedades al resto del hato",
                    "Para reducir el trabajo del personal",
                    "No sé "],index=None
                )
                q17 = st.radio(
                    "14. ¿Qué información debe incluir un reporte efectivo de un animal enfermo?",
                    ["La identificación, ubicación, síntomas observados y cuándo comenzaron los cambios",
                    "Solo la identificación del animal",
                    "Únicamente los síntomas observados que es lo más importante",
                    "Solamente la ubicación del animal",
                    "No sé "],index=None
                )
                q18 = st.radio(
                    "15. ¿Qué práctica de bioseguridad debe realizarse antes y después de atender a un animal enfermo?",
                    [" Cambiar de corral al animal",
                    "Registrar el peso y estado del animal",
                    "Lavarse las manos y seguir los procedimientos de higiene establecidos",
                    "Alimentar a otros animales primero",
                    "No sé "],index=None
                )
                

                submit = st.form_submit_button("Enviar")

                if submit:                                    
                                      #validacion vacio                  
                                    if None in [q14, q15, q16, q17, q18]:
                                            st.error("Porfavor conteste todas las preguntas antes de continuar.")
                                            st.stop()
                
                                    answers = {"q14": q14, "q15": q15, "q16": q16,
                                               "q17": q17, "q18": q18}
                                    results = {}
                                    score = 0
                                    
                                    for q in answers:
                                                    is_correct = answers[q] == correct_answers[q]
                                                    st.session_state["post_answers"][q] = answers[q]
                                                    st.session_state["post_results"][q + "_correct"] = is_correct
                                    st.session_state["training_step"] = "completed"
                
                                    save_progress(
                                        st.session_state["user"]["email"],
                                        st.session_state.get(
                                            "course_name",
                                            "Bioseguridad"
                                        ),
                                        "completed",
                                        pre_test_completed=True
                                    )
                
                                    st.rerun()

        # -------- COMPLETED --------
        elif step == "completed":
                user_email = st.session_state["user"]["email"]

                st.header("Entrenamiento completado!")
                # ✅ GUARDAR POST COMPLETO
                answers = st.session_state.get("post_answers", {})
                results = st.session_state.get("post_results", {})

                if answers and results:
                    score = sum(v for v in results.values() if v is True)

                    post_data = {
                            "user": st.session_state["user"]["email"],  # FIX
                            "name": st.session_state["user"]["name"],
                            "course": st.session_state["course_name"],
                            **answers,
                            **results,
                            "score": score,
                            "type": "post",
                            "timestamp": str(datetime.now())
                        }
                    
                    #  GUARDAR EN SUPABASE
                    supabase.table("post_test").insert(post_data).execute() 
                    mark_completed(
                        st.session_state["user"]["email"],
                        st.session_state.get(
                            "course_name",
                            "Bioseguridad"
                        )
                    )                   
                    # ✅ limpiar datos después de guardar
                    st.session_state["post_answers"] = {}
                    st.session_state["post_results"] = {}

            # ✅ obtener hora de inicio
                start_time = st.session_state.get("training_start_time")

                if start_time:
                    end_time = datetime.now()

                    # ✅ calcular duración
                    duration = (end_time - start_time).total_seconds()
                    
                    # ✅ guardar en CSV
                    training_data = {
                            "user": st.session_state["user"]["email"],   # ID 
                            "name": st.session_state["user"]["name"],
                            "course": st.session_state.get("course_name"),
                            "start_time": str(start_time),
                            "end_time": str(end_time),
                            "duration_seconds": int(duration),
                            "status": "completed"
                        }
                    
                    # GUARDAR EN SUPABASE
                    supabase.table("training_sessions").insert(training_data).execute()


                    # evitar duplicados
                    st.session_state["training_start_time"] = None

                    # mostrar duración al usuario
                    minutes = int(duration // 60)
                    seconds = int(duration % 60)

                    st.info(f"⏱ Tiempo total: {minutes} min {seconds} sec")

                st.success("Acabas de finalizar, puedes ir a dashboard para ver tus resultados. Muchas gracias.")
                
                st.markdown("---")
                col1, col2, col3 = st.columns([1,2,1])
                with col2:
                        if st.button("Ver mis resultados"):
                            st.session_state["selected_training"] = "dashboard"
                            st.rerun()
                            
                        if st.button("Volver al inicio para ver más cursos"):
                            
                            # Reset del flujo
                            st.session_state.pop("training_step", None)
                            st.session_state.pop("course_name", None)
                            st.session_state.pop("selected_training", None)
                            
                            st.session_state["initial_quiz_done"] = False
                            st.session_state["course_started"] = False

                            st.rerun()
                        
                        





        