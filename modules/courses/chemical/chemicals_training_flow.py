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
                    "Seguridad y manejo de químicos"
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
                    "Seguridad y manejo de químicos"
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
                video_id="zanBawbOyrQ",
                completed_key="video1_completed",
                next_step="quiz1",
                module_title="Módulo 1 – ¿Qué debes saber sobre seguridad y manejo de químicos?"

        )
            # -------- QUIZ 1 --------
        elif step == "quiz1":
            
            st.header("Quiz 1")

            correct_answers = {
                "q4": "Preguntar a su supervisor antes de continuar",
                "q5": "Estar apurado",
                "q6": "Informar primero a su supervisor",
                "q7": "Danger",
                "q8": "No usar el producto y reportarlo al supervisor",
            }

            with st.form("quiz1_form"):
                q4 = st.radio(
                    "1. Si no ha recibido entrenamiento para trabajar con un químico o no está seguro, ¿qué debe hacer?",
                    ["Continuar con cuidado usando conocimientos generales de otros químicos", 
                    "Preguntar a un compañero que lo haya usado antes",
                    "Preguntar a su supervisor antes de continuar", 
                    "No sé "],
                    index=None
                )
                q5 = st.radio(
                    "2. ¿Cuál de las siguientes situaciones aumenta más su riesgo de sufrir una lesión por químicos?",
                    ["Trabajar en un área ventilada",
                    "Usar guantes de nitrilo",
                    "Trabajar cerca de una estación de lavado",
                    "Estar apurado",
                    "No sé "],
                    index=None
                )
                q6 = st.radio(
                    "3. Si estás embarazada, crees que podrías estarlo o estás amamantando, ¿qué debes hacer antes de manipular químicos?",
                    ["Usar guantes de goma más gruesos",
                    "Informar primero a su supervisor",
                    "Manipular solo los químicos con la palabra “Warning”",
                    "Evitar únicamente los productos que tienen el pictograma de peligro para la salud",
                    "No sé "],
                    index=None
                )
                q7 = st.radio(
                    "4. ¿Qué palabra de señal indica que un químico puede causar lesiones graves, daños permanentes o incluso la muerte?",
                    ["Danger",
                    "Caution",
                    "Dispose",
                    "Careful",
                    "No sé "],
                    index=None
                )
                q8 = st.radio(
                    "5. Si la etiqueta de un envase está dañada o no puede leerse, ¿Qué debe hacer?",
                    ["Utilizar el químico con precaución",
                    "Preguntar a un compañero qué contiene",
                    "No usar el producto y reportarlo al supervisor",
                    "Cambiar el contenido a otro recipiente",
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
                            "Seguridad y manejo de químicos"
                        ),
                        "video2",
                        pre_test_completed=True
                    )

                    st.rerun()

        # -------- VIDEO2 --------
        elif step == "video2":
            render_video_module(
                video_id="CGEx4HEq-60",
                completed_key="video2_completed",
                next_step="quiz2",
                module_title="Módulo 2 – Uso correcto de EPPs y respuesta a derrames de químicos"
        )
        # -------- QUIZ 2 --------
        elif step == "quiz2":
            st.header("Quiz 2")

            correct_answers = {
                    "q9": "Guantes de goma o nitrilo, protección para los ojos y un mandil resistente a químicos",
                    "q10": "Ponerse el EPP adecuado",
                    "q11": "Todas las anteriores son derrames mayores",
                    "q12": "15 minutos",
                    "q13": "Hacer que la persona afectada vomite"
                }

            with st.form("quiz2_form"):
                q9 = st.radio(
                    "6. Al manejar químicos corrosivos o tóxicos, ¿Qué EPP se requiere normalmente como mínimo?",
                    ["Guantes de goma o nitrilo y un mandil resistente a químicos",
                    "Solo guantes de goma o nitrilo",
                    "Guantes de goma o nitrilo, protección para los ojos y un mandil resistente a químicos",
                    "Ninguno de los anteriores",
                    "No sé"],
                    index=None
                )
                q10 = st.radio(
                    "7. Después de avisar a los compañeros cercanos sobre un derrame menor, ¿cuál es la siguiente acción?",
                    ["Limpiar inmediatamente el derrame",
                    "Llamar al 911",
                    "Ponerse el EPP adecuado",
                    "Diluirlo con agua",
                    "No sé "],index=None
                )
                q11 = st.radio(
                    "8. ¿Cuál de los siguientes se considera un derrame químico mayor?",
                    ["Derrame de un químico inflamable",
                    "Derrame de un químico tóxico",
                    "Derrame de un químico desconocido",
                    "Derrame de un químico que necesita atención médica inmediata",
                    "Todas las anteriores son derrames mayores",
                    "No sé "],index=None
                    
                )
                q12 = st.radio(
                    "9. En caso de exposición a los ojos, ¿durante cuánto tiempo debe enjuagarse?",
                    ["Hasta que deje de arder (normalmente 1-2 minutos)",
                    "5 minutos",
                    "15 minutos",
                    "No sé"]
                    ,index=None
                )
                q13 = st.radio(
                    "10. Si una persona traga un químico, ¿qué debe evitar hacer, a menos que la etiqueta lo indique?",
                    ["Enjuagar la boca con agua",
                    "Hacer que la persona afectada vomite",
                    "Llamar por ayuda",
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
                            "Seguridad y manejo de químicos"
                        ),
                        "video3",
                        pre_test_completed=True
                    )

                    st.rerun()


        # -------- VIDEO 3 --------
        elif step == "video3":
            render_video_module(
                video_id="7nnTHvtlVyU",
                completed_key="video3_completed",
                next_step="quiz3",
                module_title="Módulo 3 – Buenas prácticas para el manejo de químicos"
        )
        # -------- QUIZ 3 --------
        elif step == "quiz3":
            st.header("Quiz 3")
            
            correct_answers = {
                    "q14": "Verdadero",
                    "q15": "Agregar siempre el químico al agua y mezclar lentamente",
                    "q16": "Limpiar primero y luego desinfectar",
                    "q17": "Almacenarlos en envases etiquetados y en un área fresca, seca y ventilada",
                    "q18": "Seguir las instrucciones de la etiqueta y llevarlos a una instalación autorizada"
                }
            with st.form("quiz3_form"):
                q14 = st.radio(
                    "11. Responda verdadero o falso. ¿Después de enjuagar los ojos o piel durante 15 minutos tras una exposición química debe buscar atención medica inmediata?",
                    ["Verdadero",
                    "Falso",
                    "No sé"]
                    ,index=None
                )
                q15 = st.radio(
                    "12. Al mezclar o diluir químicos, ¿cuál es la práctica correcta?",
                    ["Agregar agua al químico concentrado",
                    "Mezclar para terminar rápido",
                    "Adivinar la proporción",
                    "Agregar siempre el químico al agua y mezclar lentamente",
                    "No sé "],
                    index=None
                )
                q16 = st.radio(
                    "13. ¿Cuál es el orden correcto para limpiar y desinfectar equipos y superficies?",
                    ["Desinfectar y luego limpiar el residuo",
                    "Limpiar primero y luego desinfectar",
                    "Desinfectar y secar",
                    "Limpiar y secar",
                    "No sé "],index=None
                )
                q17 = st.radio(
                    "14. ¿Cuál de las siguientes practicas es correcta al almacenar químicos?",
                    ["Guardarlos en envases de bebidas para ahorrar espacio",
                    "Almacenarlos junto con medicamentos veterinario",
                    "Almacenarlos en envases etiquetados y en un área fresca, seca y ventilada",
                    "Guardarlos cerca de las áreas de contacto con la leche",
                    "No sé "],index=None
                )
                q18 = st.radio(
                    "15. ¿Qué debe hacerse con los desechos químicos?",
                    ["Mezclarlos para reducir espacio",
                    "Desecharlos por el desagüe con abundante agua",
                    "Seguir las instrucciones de la etiqueta y llevarlos a una instalación autorizada",
                    "Enterrarlos en la granja",
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
                                            "Seguridad y manejo de químicos"
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
                            "Seguridad y manejo de químicos"
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
                        
                        





        