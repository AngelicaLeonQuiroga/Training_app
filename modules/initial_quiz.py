import streamlit as st
#from utils import save_in_csv
from supabase_client import supabase
from datetime import datetime

def initial_quiz_screen():

    st.header("Initial Knowledge Check")
    
    correct_answers = {
        "q4": "Verdadero",
        "q5": "Materiales comunes como madera y papel (A), líquidos inflamables como aceite o gasolina (B) y equipos eléctricos (C) ",
        "q6": "Porque el calor se acumula por dentro y enciende el material (combustión espontánea)",
        "q7": "Usar un extintor ABC",

        "q8": "Revisando el manómetro (medidor de presión): la aguja debe estar en la zona verde",
        "q9": "Hacia la base del fuego ",
        "q10": "Verdadero ",

        "q11": "Reportarlo inmediatamente al supervisor y seguir trabajando ",
        "q12": "Mantener limpia la maquinaria (ej., radiador, motor) y las áreas de trabajo ",
        "q13": "Polvo, paja y materiales secos (ej., hojas secas) ",

        "q14": "Apagar la estufa y cubrir el recipiente con una tapa metálica o un trapo grueso ligeramente húmedo",
        "q15": "Mantener objetos inflamables lejos de fuentes de calor ",
        "q16": "Verdadero",

        "q17": "Todas las anteriores",
        "q18": "Revisando el manómetro (medidor de presión): la aguja debe estar en la zona verde",
        "q19": "Salir de inmediato, avisar a los demás y llamar al 911"
    }

    with st.form("initial_quiz"):
        q1 = st.radio(
            "1.  Ha recibido algún tipo de entrenamiento relacionado con la seguridad contra incendios: ",
            ["En mi trabajo", "El el colegio", "Otro", "Nunca he recibido entrenamientos"],
            index=None
        )

        q2 = st.multiselect(
            "2. Si has recibido un entrenamiento, ¿de quién lo has recibido?",
            ["Compañías externas que vienen al trabajo ", "Programas de extension de la universidad", 
             "Internet","Videos en la granja","Otro","Nunca he recibido entrenamientos"],
        )

        q3 = st.multiselect(
            "3. Indiquenos cual es el formato que mas le gusta aprender?",
            ["Redes sociales como Facebook o tiktok", "Entrenamientos con videos",
             "Cuando los profesores vienen a la granja y nos ensenan", "Ninguno no me gusta aprender cosas nuevas", "Otro",  "No sé "],

        )
        q4 = st.radio(
            "4. Verdadero o Falso: Existen diferentes clases de incendio (A, B, C, D) según lo que se quema, y un mismo extintor no sirve para todas. Por eso se usan los extintores ABC, que cubren las clases más comunes.",
            ["Verdadero", "Falso", "No sé "],
            index=None
        )
        q5 = st.radio(
            "5. ¿Qué tipos de fuego puede apagar un extintor ABC? ",
            ["Materiales comunes como madera y papel (A), líquidos inflamables como aceite o gasolina (B) y equipos eléctricos (C) ",
             "Solo fuegos electricos", "Solo fuegos de papel y madera",
             "Sirve para todos los fuegos, incluidos los de metales",
             "No sé "],
             index=None
        )
        q6 = st.radio(
            "6. ¿Por qué una pila de heno húmedo o de estiércol puede incendiarse sola, sin chispa ni llama?",
            ["Porque el calor se acumula por dentro y enciende el material (combustión espontánea)",
              "Porque el sol la calienta por fuera",
              "Porque el viento la enciende",
              "El heno y el estiércol nunca se incendian solos ",
                "No sé "],
                index=None
        )
        q7 = st.radio(
            "7. En la sala de descanso comienza a incendiarse un papel dentro de un basurero. ¿Qué debo hacer?",
            ["Poner mucha agua hasta apagarlo completamente",
              "Usar un extintor ABC",
              "Cubrir el basurero para que el agua se apague",
              "No usar ningun extintor ",
              "No sé "],
              index=None
        )
        #video 2
        q8 = st.radio(
            "8. ¿Cómo puede saber si un extintor está cargado y listo para usarse?",
            ["Revisando el manómetro (medidor de presión): la aguja debe estar en la zona verde",
              "Agitándolo para escuchar si tiene polvo",
              "Por el color rojo del extintor",
              "No se puede saber hasta que se usa ",
              "No sé "],
              index=None
        )
        q9 = st.radio(
            "9. ¿Hacia dónde debe apuntarse la boquilla del extintor a la hora de apagar un fuego? ",
            ["Hacia la parte más alta de las llamas ",
              "Hacia el humo",
              "Hacia la base del fuego ",
              "Hacia cualquier para del incendio lo importante es actuar ",
              "No sé "],
              index=None
        )
        q10 = st.radio(
            "10. Verdadero o Falso: Debo barrer el fuego moviendo la manguera de lado a lado. ",
            ["Verdadero ",
              "Falso",
              "No sé "],index=None
        )
        #video 3
        q11 = st.radio(
            "11. ¿Qué debes hacer si el extintor del tractor no está presente o el indicador de presión está en rojo? ",
            ["Ignorarlo y seguir trabajando  ",
              "Reportarlo inmediatamente al supervisor y seguir trabajando ",
              "Guardar el tractor en el establo ",
              "Esperar al siguiente turno  ",
              "No sé "],index=None
        )
        q12 = st.radio(
            "12. ¿Cuál de las siguientes acciones puede ayudar a prevenir incendios en la granja? ",
            ["Estacionar maquinaria lejos de materiales secos ",
              "Fumar cerca de tractores y paja ",
              "Mantener limpia la maquinaria (ej., radiador, motor) y las áreas de trabajo ",
              "Todas las anteriores",
              "No sé "]
              ,index=None
        )
        q13 = st.radio(
            "13. ¿Qué materiales pueden acumularse en el compartimento del motor y aumentar el riesgo de incendio? ",
            ["Agua, barro, paja y materiales secos ",
              "Polvo, paja y materiales secos (ej., hojas secas) ",
              "Aceite limpio y herramientas ",
              "Arena, piedras y polvo ",
              "No sé "]
              ,index=None
        )
        #video 4
        q14 = st.radio(
            "14. ¿Qué se debe hacer si ocurre un fuego causado por aceite o grasa mientras se cocina? ",
            ["Arrojar agua inmediatamente ",
              "Abrir ventanas y dejar el fuego solo ",
              "Apagar la estufa y cubrir el recipiente con una tapa metálica o un trapo grueso ligeramente húmedo",
              "Mover la sartén rápidamente al fregadero",
              "No sé "]
              ,index=None
        )
        q15 = st.radio(
            "15. ¿Cuál de las siguientes acciones ayuda a prevenir incendios en el hogar? ",
            ["Dejar veladoras encendidas durante la noche",
              "Mantener objetos inflamables lejos de fuentes de calor ",
              "Usar un solo enchufe eléctrico para conectar varios electrodomésticos a la vez ",
              "Dejar toallas cerca de la estufa mientras se cocina  ",
              "No sé "],
              index=None
        )
        q16 = st.radio(
            "16. Verdadero o Falso. Las pilas de estiércol no deben superar más de 5 pies (1.5 metros) y ser movidas constantemente porque puede causar un incendio.",
            ["Verdadero",
              "Falso",
              "No sé "],index=None
        )
        q17 = st.radio(
            "17. ¿Cómo sabe que el fuego es demasiado peligroso y debe dejar de apagarlo y salir de inmediato?",
            ["El fuego es más alto que usted o más grande que un basurero",
              "El humo está llenando el cuarto y cuesta respirar o ver ",
              "El fuego está entre usted y la salida",
              "Todas las anteriores",
              "No sé "],index=None
        )
        q18 = st.radio(
            "18. ¿Cómo puede saber si un extintor está cargado y listo para usarse?",
            ["Revisando el manómetro (medidor de presión): la aguja debe estar en la zona verde",
              "Agitándolo para escuchar si tiene polvo",
              "Por el color rojo del extintor",
              "No se puede saber hasta que se usa ",
              "No sé "],index=None
        )
        q19 = st.radio(
            "19. ¿Qué debes hacer si el fuego es grande y no puedes controlarlo con el extintor?",
            [" Seguir intentando apagarlo tú solo",
              "Salir de inmediato, avisar a los demás y llamar al 911",
              "Esconderte dentro del establo",
              "Buscar tus cosas antes de salir",
              "No sé "],index=None
        )


        submitted_quiz = st.form_submit_button("Submit answers")

    if submitted_quiz:
        
        # VALIDACIÓN GLOBAL
        if None in [q1, q3, q4, q5, q6, q7, q8, q9, q10,
                    q11, q12, q13, q14, q15, q16, q17, q18, q19] or not q2 or not q3:
            
            st.error(" Please answer all questions before submitting.")
            st.stop()

        
        answers = {
                "q1": q1, "q2": q2, "q3": q3,
                "q4": q4, "q5": q5, "q6": q6, "q7": q7,
                "q8": q8, "q9": q9, "q10": q10,
                "q11": q11, "q12": q12, "q13": q13,
                "q14": q14, "q15": q15, "q16": q16,
                "q17": q17, "q18": q18, "q19": q19,
            }

        results = {}
        score = 0
        
        for q in correct_answers:  # SOLO evalúa q4–q19
                is_correct = answers[q] == correct_answers[q]
                results[q + "_correct"] = is_correct

                if is_correct:
                    score += 1

        quiz_data = {
            "user": st.session_state["user"]["email"],
            "name": st.session_state["user"]["name"],
            "email": st.session_state["user"]["email"],
            **answers,
            **results,
            "score": score,
            "type": "pre",
            "timestamp": str(datetime.now())
        }

        #save_in_csv(quiz_data, "initial_quiz.csv")
        
        #  GUARDAR EN SUPABASE
        supabase.table("initial_quiz").insert(quiz_data).execute()

        st.session_state["initial_quiz_done"] = True
        st.success("Your answers were submitted successfully.")
        st.rerun()
