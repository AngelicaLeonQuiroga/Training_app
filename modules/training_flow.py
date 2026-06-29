import streamlit as st
#from utils import save_in_csv
from supabase_client import supabase
from datetime import datetime


course_steps = [
    ("video1", "Video 1"),
    ("quiz1", "Quiz 1"),
    ("video2", "Video 2"),
    ("quiz2", "Quiz 2"),
    ("video3", "Video 3"),
    ("quiz3", "Quiz 3"),
    ("video4", "Video 4"),
    ("quiz4", "Quiz 4"),
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
            st.rerun()

def training_flow():
    
    if "post_answers" not in st.session_state:
        st.session_state["post_answers"] = {}

    if "post_results" not in st.session_state:
        st.session_state["post_results"] = {}

    # Inicializar training_step 
    
    if "training_step" not in st.session_state:
        st.session_state["training_step"] = "video1"


    if "sidebar_open" not in st.session_state:
        st.session_state["sidebar_open"] = True

    # Obtener paso actual
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
                video_id="Bxfk5FafrVE",
                completed_key="video1_completed",
                next_step="quiz1",
                module_title="Módulo 1 – Tipos de extintores"

        )
            # -------- QUIZ 1 --------
        elif step == "quiz1":
            
            st.header("Quiz 1")

            correct_answers = {
                "q1": "Verdadero",
                "q2": "Materiales comunes como madera y papel (A), líquidos inflamables como aceite o gasolina (B) y equipos eléctricos (C) ",
                "q3": "Porque el calor se acumula por dentro y enciende el material (combustión espontánea)",
                "q4": "Usar un extintor ABC"
            }

            with st.form("quiz1_form"):
                q1 = st.radio(
                    "1.  Responda Verdadero o Falso: Existen diferentes clases de incendio/fuego (A, B, C, D) según lo que se quema, y un mismo extintor no sirve para todas. Por eso se usan los extintores ABC, que cubren las clases más comunes.",
                    ["Verdadero", "Falso", "No sé "],index=None
                )
                q2 = st.radio(
                    "2. ¿Qué tipos de fuego puede apagar un extintor ABC? ",
                    ["Materiales comunes como madera y papel (A), líquidos inflamables como aceite o gasolina (B) y equipos eléctricos (C) ",
                    "Solo fuegos eléctricos", "Solo fuegos de papel y madera",
                    "Sirve para todos los fuegos, incluidos los de metales",
                    "No sé "],index=None
                )
                q3 = st.radio(
                    "3. ¿Por qué una pila de heno húmedo o de estiércol puede incendiarse sola, sin chispa ni llama?",
                    ["Porque el sol la calienta por fuera",
                    "Porque el viento la enciende",
                    "Porque el calor se acumula por dentro y enciende el material (combustión espontánea)",
                    "El heno y el estiércol nunca se incendian solos ",
                        "No sé "],index=None
                )
                q4 = st.radio(
                    "4. En la sala de descanso comienza a incendiarse un papel dentro de un basurero. ¿Qué debo hacer?",
                    ["El agua no me serviria para apagarlo",
                    "Usar un extintor ABC",
                    "Cubrir el basurero para que el fuego se apague",
                    "No usar ningun extintor ",
                    "No sé "],index=None
                )

                submit = st.form_submit_button("Enviar")

                if submit:
                    
                # VALIDACIÓN
                    if None in [q1, q2, q3, q4]:
                        st.error("Porfavor conteste todas las preguntas antes de continuar.")
                        st.stop()

                    answers = {"q1": q1, "q2": q2,
                            "q3": q3, "q4": q4,}
                    for q in answers:
                        is_correct = answers[q] == correct_answers[q]
                        st.session_state["post_answers"][q] = answers[q]
                        st.session_state["post_results"][q + "_correct"] = is_correct
                    st.session_state["training_step"] = "video2"
                    st.rerun()

        # -------- VIDEO2 --------
        elif step == "video2":
            render_video_module(
                video_id="-WNqzmxy9No",
                completed_key="video2_completed",
                next_step="quiz2",
                module_title="Módulo 2 – Como usar un extintor de incendios"
        )
        # -------- QUIZ 2 --------
        elif step == "quiz2":
            st.header("Quiz 2")

            correct_answers = {
                    "q5": "Revisando el manómetro (medidor de presión): la aguja debe estar en la zona verde",
                    "q6": "Hacia la base del fuego ",
                    "q7": "Verdadero "
                }

            with st.form("quiz2_form"):
                q5 = st.radio(
                    "5. ¿Cómo puede saber si un extintor está cargado y listo para usarse?",
                    ["Agitándolo para escuchar si tiene polvo",
                    "Por la etiqueta de mantenimiento",
                    "No se puede saber hasta que se usa ",
                    "Revisando el manómetro (medidor de presión): la aguja debe estar en la zona verde",
                    "No sé "],index=None
                )
                q6 = st.radio(
                    "6. ¿Hacia dónde debe apuntarse la boquilla del extintor a la hora de apagar un fuego? ",
                    ["Hacia la parte más alta de las llamas ",
                    "Hacia el humo",
                    "Hacia la base del fuego ",
                    "Hacia cualquier sitio del incendio, lo importante es actuar ",
                    "No sé "],index=None
                )
                q7 = st.radio(
                    "7. Responda Verdadero o Falso: Para apagar un incendio debo barrer la base del fuego moviendo el extintor de lado a lado.",
                    ["Verdadero ",
                    "Falso",
                    "No sé "],index=None
                )

                submit = st.form_submit_button("Enviar")

                if submit:
                    
                    if None in [q5, q6, q7]:
                            st.error("Porfavor conteste todas las preguntas antes de continuar.")
                            st.stop()

                    answers = {"q5": q5, "q6": q6, "q7": q7}

                    for q in answers:
                        is_correct = answers[q] == correct_answers[q]
                        st.session_state["post_answers"][q] = answers[q]
                        st.session_state["post_results"][q + "_correct"] = is_correct                    
                    st.session_state["training_step"] = "video3"
                    st.rerun()


        # -------- VIDEO 3 --------
        elif step == "video3":
            render_video_module(
                video_id="bFUBN7CKVIw",
                completed_key="video3_completed",
                next_step="quiz3",
                module_title="Módulo 3 – Prevención de riesgos"
        )
        # -------- QUIZ 3 --------
        elif step == "quiz3":
            st.header("Quiz 3")
            
            correct_answers = {
                    "q8": "Reportarlo inmediatamente al supervisor y reemplazarlo por un extintor nuevo para luego seguir trabajando ",
                    "q9": "Mantener limpia la maquinaria (ej., radiador, motor) y las áreas de trabajo ",
                    "q10": "Polvo, paja y materiales secos (ej., hojas secas) "
                }
            with st.form("quiz3_form"):
                q8 = st.radio(
                    "8. ¿Qué debes hacer si el extintor del tractor no está presente o el indicador de presión está en rojo? ",
                    ["Ignorarlo y seguir trabajando  ",
                    "Reportarlo inmediatamente al supervisor y reemplazarlo por un extintor nuevo para luego seguir trabajando ",
                    "Guardar el tractor en el establo ",
                    "Esperar al siguiente turno  ",
                    "No sé "],index=None
                )
                q9 = st.radio(
                    "9. ¿Cuál de las siguientes acciones puede ayudar a prevenir incendios en la granja? ",
                    ["Estacionar maquinaria lejos de materiales secos (ej. hojas y paja) ",
                    "Fumar cerca de tractores y materiales secos (ej. hojas y paja)  ",
                    "Mantener limpia la maquinaria (ej., radiador, motor) y las áreas de trabajo ",
                    "Todas las anteriores",
                    "No sé "],index=None
                )
                q10 = st.radio(
                    "10. ¿Qué materiales pueden acumularse en el compartimento del motor y aumentar el riesgo de incendio? ",
                    ["Agua, barro, paja y materiales secos (ej., hojas secas) ",
                    "Polvo, paja y materiales secos (ej., hojas secas) ",
                    "Aceite limpio y herramientas ",
                    "Arena, piedras y polvo ",
                    "No sé "],index=None
                )

                submit = st.form_submit_button("Enviar")

                if submit:
                    #validation vacio
                    if None in [q8, q9, q10]:
                            st.error("Porfavor conteste todas las preguntas antes de continuar.")
                            st.stop()

                    answers = {"q8": q8, "q9": q9, "q10": q10}
                    results = {}
                    score = 0
                    
                    for q in answers:
                                    is_correct = answers[q] == correct_answers[q]
                                    st.session_state["post_answers"][q] = answers[q]
                                    st.session_state["post_results"][q + "_correct"] = is_correct
                    st.session_state["training_step"] = "video4"
                    st.rerun()
# -------- VIDEO 4 --------
        elif step == "video4":
            render_video_module(
                video_id="PpOCbRfQbD8",
                completed_key="video4_completed",
                next_step="quiz4",
                module_title="Módulo 4 – Cuidados que debes tener cuenta sobre incendios en tu hogar"
        )
        # -------- QUIZ 4 --------
        elif step == "quiz4":
            st.header("Quiz 4")
            
            correct_answers = {
                    "q11": "Apagar la estufa/fogón y cubrir el recipiente con una tapa metálica o un trapo grueso ligeramente húmedo",
                    "q12": "Mantener objetos inflamables lejos de fuentes de calor ",
                    "q13": "Verdadero",
                    "q14": "Todas las anteriores",
                    "q16": "Salir de inmediato, avisar a los demás y llamar al 911"
                }

            with st.form("quiz4_form"):
                q11 = st.radio(
                    "11. ¿Qué se debe hacer si ocurre un fuego causado por aceite o grasa mientras se cocina? ",
                    ["Arrojar agua inmediatamente ",
                    "Abrir ventanas y dejar el fuego solo ",
                    "Apagar la estufa/fogón y cubrir el recipiente con una tapa metálica o un trapo grueso ligeramente húmedo",
                    "Mover la sartén rápidamente al fregadero",
                    "No sé "],index=None
                )
                q12 = st.radio(
                    "12. ¿Cuál de las siguientes acciones ayuda a prevenir incendios en el hogar? ",
                    ["Dejar veladoras encendidas durante la noche",
                    "Mantener objetos inflamables lejos de fuentes de calor ",
                    "Usar un solo enchufe eléctrico para conectar varios electrodomésticos a la vez ",
                    "Dejar toallas de cocina cerca de la estufa/fogón mientras esta en funcionamiento  ",
                    "No sé "],index=None
                )
                q13 = st.radio(
                    "13. Responda Verdadero o Falso. Las pilas de estiércol no deben superar más de 5 pies (1.5 metros) y ser movidas constantemente porque puede causar un incendio, cuando la termperatura interta incrementa.",
                    ["Verdadero",
                    "Falso",
                    "No sé "],index=None
                )
                q14 = st.radio(
                    "14. ¿Cómo se sabe que el fuego se sale de control, obligandonos a salir de inmediato y dejar de intentar apagarlo?",
                    ["El fuego es más alto que usted o más grande que un basurero",
                    "El humo está llenando el cuarto y cuesta respirar o ver ",
                    "El fuego está entre usted y la salida",
                    "Todas las anteriores",
                    "No sé "],index=None
                )
                q16 = st.radio(
                    "15. ¿Qué debes hacer si el fuego es grande y no puedes controlarlo con el extintor?",
                    [" Seguir intentando apagarlo tú solo",
                    "Salir de inmediato, avisar a los demás y llamar al 911",
                    "Esconderte dentro del establo",
                    "Buscar tus cosas antes de salir",
                    "No sé "],index=None
                )
                submit = st.form_submit_button("Enviar")

                if submit:
                      #validacion vacio                  
                    if None in [q11, q12, q13, q14, q16]:
                            st.error("Porfavor conteste todas las preguntas antes de continuar.")
                            st.stop()

                    answers = {"q11": q11, "q12": q12, "q13": q13,
                               "q14": q14, "q16": q16}
                    results = {}
                    score = 0
                    
                    for q in answers:
                                    is_correct = answers[q] == correct_answers[q]
                                    st.session_state["post_answers"][q] = answers[q]
                                    st.session_state["post_results"][q + "_correct"] = is_correct
                    st.session_state["training_step"] = "completed"
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
                            **answers,
                            **results,
                            "score": score,
                            "type": "post",
                            "timestamp": str(datetime.now())
                        }
                    
                    #  GUARDAR EN SUPABASE
                    supabase.table("post_test").insert(post_data).execute()                    
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
                        if st.button("Volver al inicio para ver más cursos"):
                            
                            # Reset del flujo
                            st.session_state.pop("training_step", None)
                            st.session_state.pop("course_name", None)
                            st.session_state.pop("selected_training", None)
                            
                            st.session_state["initial_quiz_done"] = False
                            st.session_state["course_started"] = False

                            st.rerun()




        