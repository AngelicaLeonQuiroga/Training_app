import streamlit as st
from modules.progress import save_progress
from supabase_client import supabase
from datetime import datetime

# Los nuevos cursos deben seguir el modelo de Bioseguridad
# usando las mismas preguntas q4-q18 en pre y post. y q1 a q3 preguntas de percepcion personal 

def initial_quiz_screen():

    st.header("Prueba inicial de conocimientos bioseguridad")
    
    correct_answers = {
    "q4": "Minimizar la entrada y propagación de gérmenes para proteger animales y trabajadores",
    "q5": "Falso",
    "q6": "Conocer su origen y observarlos antes de juntarlos",
    "q7": "Sí, pueden llegar con estiércol o bacterias pegadas en ruedas y equipo",
    "q8": "Todas las anteriores",

    "q9": "Prevenir la propagación de enfermedades y microorganismos",
    "q10": "Lavarse las manos durante al menos 20 segundos",
    "q11": "Cuando se cambie de tarea o exista riesgo de contaminación cruzada",
    "q12": "Lavarse las manos y seguir el protocolo de bioseguridad de la granja",
    "q13": "Lavar inmediatamente la herida, informar al supervisor y buscar atención médica",

    "q14": "Fiebre o temperatura corporal elevada",
    "q15": "Reportarlo inmediatamente al supervisor o veterinario",
    "q16": "Para evitar la propagación de enfermedades al resto del hato",
    "q17": "La identificación, ubicación, síntomas observados y cuándo comenzaron los cambios",
    "q18": "Lavarse las manos y seguir los procedimientos de higiene establecidos"
}

    with st.form("initial_quiz"):
        q1 = st.radio(
            "1.  Ha recibido algún tipo de entrenamiento relacionado con Bioseguridad en granjas lecheras: ",
            ["Sí, en el trabajo", "Sí, en el colegio", "Sí, en otro sitio", "No, nunca he recibido entrenamientos"],
            index=None
        )

        q2 = st.multiselect(
            "2. Si has recibido un entrenamiento, ¿de quién lo has recibido?",
            ["Compañías externas que vienen al trabajo ", "Programas de extensión de la universidad", 
             "Internet","Videos en la granja","Nunca he recibido entrenamientos","Otro"],
        )

        q3 = st.multiselect(
            "3. Indiquenos cual es el formato que más le gusta aprender?",
            ["Facebook","Tiktok", "Instagram","Otras redes sociales" ,"Entrenamientos con videos, flyers o charlas que ofrece la granja",
             "Cuando el personal externo viene a la granja a dar información", "Material impreso", "Otro",  "No sé "],

        )
        q4 = st.radio(
            "4. ¿Cuál es el principal objetivo de un plan de bioseguridad en una granja lechera?",
            ["Evitar que los trabajadores se enfermen", 
             "Reducir la cantidad de medicamentos que se usan en los animales",
             "Minimizar la entrada y propagación de gérmenes para proteger animales y trabajadores", 
             "No sé "],
            index=None
        )
        q5 = st.radio(
            "5. Si una enfermedad ya está presente en la granja, es fácil eliminarla por completo",
            ["Verdadero",
             "Falso",
             "No sé "],
             index=None
        )
        q6 = st.radio(
            "6. ¿Cuál de estas acciones es más importante cuando llegan animales nuevos a la granja?",
            ["Mezclarlos de inmediato con el resto para que se adapten",
              "Conocer su origen y observarlos antes de juntarlos",
              "Darles alimento y agua limpia",
                "No sé "],
                index=None
        )
        q7 = st.radio(
            "7. ¿Los vehículos representan un riesgo de bioseguridad?",
            ["Sí, el ruido estresa a las vacas",
              "Sí, pero solo cuando transportan animales",
              "Sí, pueden llegar con estiércol o bacterias pegadas en ruedas y equipo",
              "No, los vehículos no representan un riesgo",
              "No sé "],
              index=None
        )
        q8 = st.radio(
            "8. ¿Cuál de estos animales es un vector de enfermedades?",
            ["Insectos",
              "Roedores y aves",
              "Mascotas",
              "Fauna silvestre",
              "Todas las anteriores",
              "No sé"],
              index=None
        )
        #video 2
        q9 = st.radio(
            "9. ¿Cuál es el propósito principal de usar guantes y cubrebotas en la granja?",
            ["Mantener la ropa limpia",
              "Prevenir la propagación de enfermedades y microorganismos",
              "Trabajar más rápido y que no se resbalen los implementos",
              "Evitar mojarse las manos",
              "No sé"],
              index=None
        )
        q10 = st.radio(
            "10. Antes de colocarse los guantes, se debe:",
            ["Lavarse las manos durante al menos 20 segundos",
              "Limpiar los guantes con agua",
              "Usar desinfectante únicamente",
              "Ninguna de las anteriores",
              "No sé "],index=None
        )
       
        q11 = st.radio(
            "11. ¿Cuándo debe cambiarse un par de guantes desechables?",
            ["Solo cuando estén rotos",
              "Al final de la semana",
              "Cuando se cambie de tarea o exista riesgo de contaminación cruzada",
              "Nunca es necesario cambiarlos",
              "No sé "],index=None
        )
        q12 = st.radio(
            "12. ¿Qué deben hacer los visitantes antes de ingresar a las áreas de animales?",
            ["Entrar directamente si tienen experiencia",
              "Lavarse las manos y seguir el protocolo de bioseguridad de la granja",
              "Solo usar botas limpias",
              "Firmar un registro únicamente",
              "No sé"]
              ,index=None
        )
        q13 = st.radio(
            "13. Si ocurre un pinchazo accidental con una aguja contaminada, la persona debe:",
            ["Continuar trabajando normalmente",
              "Tirar la aguja a la basura regular",
              "Aplicar desinfectante y regresar al trabajo",
              "Lavar inmediatamente la herida, informar al supervisor y buscar atención médica",
              "No sé"]
              ,index=None
        )
        #video 3
        q14 = st.radio(
            "14. ¿Cuál de las siguientes es una señal de alerta que puede indicar que un animal está enfermo?",
            ["Mayor consumo de alimento",
              "Fiebre o temperatura corporal elevada",
              "Aumento de actividad física",
              "Mayor producción de leche",
              "No sé"]
              ,index=None
        )
        q15 = st.radio(
            "15. Si observas un animal con signos de enfermedad, ¿qué debes hacer primero?",
            ["Esperar varios días para confirmar que está enfermo",
              "Administrarle medicamentos por tu cuenta",
              "Reportarlo inmediatamente al supervisor o veterinario",
              "Moverlo a otra área sin autorización",
              "No sé "],
              index=None
        )
        q16 = st.radio(
            "16. ¿Por qué es importante aislar a los animales enfermos?",
            ["Para facilitar la alimentación del animal",
              "Para aumentar su producción de leche",
              "Para evitar la propagación de enfermedades al resto del hato",
              "Para reducir el trabajo del personal",
              "No sé "],index=None
        )
        q17 = st.radio(
            "17. ¿Qué información debe incluir un reporte efectivo de un animal enfermo?",
            ["La identificación, ubicación, síntomas observados y cuándo comenzaron los cambios",
              "Solo la identificación del animal",
              "Únicamente los síntomas observados que es lo más importante",
              "Solamente la ubicación del animal",
              "No sé "],index=None
        )
        q18 = st.radio(
            "18. ¿Qué práctica de bioseguridad debe realizarse antes y después de atender a un animal enfermo?",
            [" Cambiar de corral al animal",
              "Registrar el peso y estado del animal",
              "Lavarse las manos y seguir los procedimientos de higiene establecidos",
              "Alimentar a otros animales primero",
              "No sé "],index=None
        )


        submitted_quiz = st.form_submit_button("Enviar respuestas")

    if submitted_quiz:
        
        # VALIDACIÓN GLOBAL
        if None in [q1, q3, q4, q5, q6, q7, q8, q9, q10,
                    q11, q12, q13, q14, q15, q16, q17, q18] or not q2 or not q3:
            
            st.error(" Por favor conteste todas la preguntas antes de enviarlas")
            st.stop()

        
        answers = {
                "q1": q1, "q2": q2, "q3": q3,
                "q4": q4, "q5": q5, "q6": q6, "q7": q7,
                "q8": q8, "q9": q9, "q10": q10,
                "q11": q11, "q12": q12, "q13": q13,
                "q14": q14, "q15": q15, "q16": q16,
                "q17": q17, "q18": q18,
            }

        results = {}
        score = 0
        
        for q in correct_answers:  # SOLO evalúa q4–q18
                is_correct = answers[q] == correct_answers[q]
                results[q + "_correct"] = is_correct

                if is_correct:
                    score += 1

        quiz_data = {
            "user": st.session_state["user"]["email"],
            "name": st.session_state["user"]["name"],
            "email": st.session_state["user"]["email"],
            "course": st.session_state["course_name"],
            **answers,
            **results,
            "score": score,
            "type": "pre",
            "timestamp": str(datetime.now())
        }
        
        #  GUARDAR EN SUPABASE
        supabase.table("initial_quiz").insert(quiz_data).execute()
        save_progress(
            st.session_state["user"]["email"],
            st.session_state["course_name"],
            "video1",
            pre_test_completed=True
        )
        st.session_state["initial_quiz_done"] = True
        st.success("Tus respuestas se subieron exitosamente.")
        st.rerun()
