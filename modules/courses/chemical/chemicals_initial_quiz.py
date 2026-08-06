import streamlit as st
from modules.progress import save_progress
from supabase_client import supabase
from datetime import datetime

# Los nuevos cursos deben seguir el modelo de Bioseguridad
# usando las mismas preguntas q4-q18 en pre y post. y q1 a q3 preguntas de percepcion personal 

def initial_quiz_screen():

    st.header("Prueba inicial de conocimientos seguridad y manejo de químicos")
    
    correct_answers = {
    "q4": "Preguntar a su supervisor antes de continuar",
    "q5": "Estar apurado",
    "q6": "Informar primero a su supervisor",
    "q7": "Danger",
    "q8": "No usar el producto y reportarlo al supervisor",

    "q9": "Guantes de goma o nitrilo, protección para los ojos y un mandil resistente a químicos",
    "q10": "Ponerse el EPP adecuado",
    "q11": "Todas las anteriores son derrames mayores",
    "q12": "15 minutos",
    "q13": "Hacer que la persona afectada vomite",

    "q14": "Verdadero",
    "q15": "Agregar siempre el químico al agua y mezclar lentamente",
    "q16": "Limpiar primero y luego desinfectar",
    "q17": "Almacenarlos en envases etiquetados y en un área fresca, seca y ventilada",
    "q18": "Seguir las instrucciones de la etiqueta y llevarlos a una instalación autorizada"
}

    with st.form("initial_quiz"):
        q1 = st.radio(
            "1.  Ha recibido algún tipo de entrenamiento relacionado con seguridad y manejo de químicos en granjas lecheras: ",
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
        #video 1
        q4 = st.radio(
            "4. Si no ha recibido entrenamiento para trabajar con un químico o no está seguro, ¿qué debe hacer?",
            ["Continuar con cuidado usando conocimientos generales de otros químicos", 
             "Preguntar a un compañero que lo haya usado antes",
             "Preguntar a su supervisor antes de continuar", 
             "No sé "],
            index=None
        )
        q5 = st.radio(
            "5. ¿Cuál de las siguientes situaciones aumenta más su riesgo de sufrir una lesión por químicos?",
            ["Trabajar en un área ventilada",
             "Usar guantes de nitrilo",
             "Trabajar cerca de una estación de lavado",
             "Estar apurado",
             "No sé "],
             index=None
        )
        q6 = st.radio(
            "6. Si estás embarazada, crees que podrías estarlo o estás amamantando, ¿qué debes hacer antes de manipular químicos?",
            ["Usar guantes de goma más gruesos",
              "Informar primero a su supervisor",
              "Manipular solo los químicos con la palabra “Warning”",
              "Evitar únicamente los productos que tienen el pictograma de peligro para la salud",
                "No sé "],
                index=None
        )
        q7 = st.radio(
            "7. ¿Qué palabra de señal indica que un químico puede causar lesiones graves, daños permanentes o incluso la muerte?",
            ["Danger",
              "Caution",
              "Dispose",
              "Careful",
              "No sé "],
              index=None
        )
        q8 = st.radio(
            "8. Si la etiqueta de un envase está dañada o no puede leerse, ¿Qué debe hacer?",
            ["Utilizar el químico con precaución",
              "Preguntar a un compañero qué contiene",
              "No usar el producto y reportarlo al supervisor",
              "Cambiar el contenido a otro recipiente",
              "No sé"],
              index=None
        )
        #video 2
        q9 = st.radio(
            "9. Al manejar químicos corrosivos o tóxicos, ¿Qué EPP se requiere normalmente como mínimo?",
            ["Guantes de goma o nitrilo y un mandil resistente a químicos",
              "Solo guantes de goma o nitrilo",
              "Guantes de goma o nitrilo, protección para los ojos y un mandil resistente a químicos",
              "Ninguno de los anteriores",
              "No sé"],
              index=None
        )
        q10 = st.radio(
            "10. Después de avisar a los compañeros cercanos sobre un derrame menor, ¿cuál es la siguiente acción?",
            ["Limpiar inmediatamente el derrame",
              "Llamar al 911",
              "Ponerse el EPP adecuado",
              "Diluirlo con agua",
              "No sé "],index=None
        )
       
        q11 = st.radio(
            "11. ¿Cuál de los siguientes se considera un derrame químico mayor?",
            ["Derrame de un químico inflamable",
              "Derrame de un químico tóxico",
              "Derrame de un químico desconocido",
              "Derrame de un químico que necesita atención médica inmediata",
              "Todas las anteriores son derrames mayores",
              "No sé "],index=None
        )
        q12 = st.radio(
            "12. En caso de exposición a los ojos, ¿durante cuánto tiempo debe enjuagarse?",
            ["Hasta que deje de arder (normalmente 1-2 minutos)",
              "5 minutos",
              "15 minutos",
              "No sé"]
              ,index=None
        )
        q13 = st.radio(
            "13. Si una persona traga un químico, ¿qué debe evitar hacer, a menos que la etiqueta lo indique?",
            ["Enjuagar la boca con agua",
              "Hacer que la persona afectada vomite",
              "Llamar por ayuda",
              "No sé"]
              ,index=None
        )
        #video 3
        q14 = st.radio(
            "14. Responda verdadero o falso. ¿Después de enjuagar los ojos o piel durante 15 minutos tras una exposición química debe buscar atención medica inmediata?",
            ["Verdadero",
              "Falso",
              "No sé"]
              ,index=None
        )
        q15 = st.radio(
            "15. Al mezclar o diluir químicos, ¿cuál es la práctica correcta?",
            ["Agregar agua al químico concentrado",
              "Mezclar para terminar rápido",
              "Adivinar la proporción",
              "Agregar siempre el químico al agua y mezclar lentamente",
              "No sé "],
              index=None
        )
        q16 = st.radio(
            "16. ¿Cuál es el orden correcto para limpiar y desinfectar equipos y superficies?",
            ["Desinfectar y luego limpiar el residuo",
              "Limpiar primero y luego desinfectar",
              "Desinfectar y secar",
              "Limpiar y secar",
              "No sé "],index=None
        )
        q17 = st.radio(
            "17. ¿Cuál de las siguientes practicas es correcta al almacenar químicos?",
            ["Guardarlos en envases de bebidas para ahorrar espacio",
              "Almacenarlos junto con medicamentos veterinario",
              "Almacenarlos en envases etiquetados y en un área fresca, seca y ventilada",
              "Guardarlos cerca de las áreas de contacto con la leche",
              "No sé "],index=None
        )
        q18 = st.radio(
            "18. ¿Qué debe hacerse con los desechos químicos?",
            ["Mezclarlos para reducir espacio",
              "Desecharlos por el desagüe con abundante agua",
              "Seguir las instrucciones de la etiqueta y llevarlos a una instalación autorizada",
              "Enterrarlos en la granja",
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
