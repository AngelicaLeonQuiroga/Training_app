import streamlit as st
import pandas as pd
import os
import altair as alt
from supabase_client import supabase

#  MAPEO DE PREGUNTAS
FIRE_QUESTION_TEXT = {
    "q4": "¿Qué debo hacer si se inicia un incendio en un basurero?",
    "q5": "¿Cómo verificar que un extintor está listo para usarse?",
    "q6": "¿Hacia dónde se debe apuntar el extintor?",
    "q7": "¿Debo barrer el fuego de lado a lado?",
    "q8": "¿Qué hacer si el extintor del tractor no está disponible?",
    "q9": "¿Qué acción ayuda a prevenir incendios en la granja?",
    "q10": "¿Qué materiales aumentan el riesgo de incendio en motores?",
    "q11": "¿Qué hacer en caso de incendio con grasa o aceite?",
    "q12": "¿Qué ayuda a prevenir incendios en el hogar?",
    "q13": "¿Deben controlarse las pilas de estiércol?",
    "q14": "¿Cuándo dejar de intentar apagar un incendio?",
    "q15": "¿Cómo verificar que un extintor está listo?",
    "q16": "¿Qué hacer si el fuego se sale de control?",
    "q17": "¿Cuándo dejar de intentar apagar un incendio?",
    "q19": "¿Qué hacer si el fuego es grande y no puede controlarse?"
}
# =====================================================
# PLAN DE MEJORA (POST TEST)
# =====================================================

FIRE_POST_QUESTION_TEXT = {
    "q1": "Existen diferentes clases de incendio/fuego según lo que se quema.",
    "q2": "¿Qué tipos de fuego puede apagar un extintor ABC?",
    "q3": "¿Por qué una pila de heno húmedo o estiércol puede incendiarse sola?",
    "q4": "¿Qué debo hacer si se inicia un incendio en un basurero?",

    "q5": "¿Cómo puede saber si un extintor está cargado y listo para usarse?",
    "q6": "¿Hacia dónde debe apuntarse la boquilla del extintor?",
    "q7": "¿Debo barrer la base del fuego moviendo el extintor de lado a lado?",

    "q8": "¿Qué debes hacer si el extintor del tractor no está presente o está en rojo?",
    "q9": "¿Qué acción ayuda a prevenir incendios en la granja?",
    "q10": "¿Qué materiales aumentan el riesgo de incendio en motores?",

    "q11": "¿Qué hacer en caso de incendio con grasa o aceite?",
    "q12": "¿Qué ayuda a prevenir incendios en el hogar?",
    "q13": "¿Deben controlarse las pilas de estiércol?",
    "q14": "¿Cómo identificar que un fuego está fuera de control?",

    "q16": "¿Qué hacer si el fuego es grande y no puedes controlarlo?"
}

FIRE_VIDEO_MAPPING = {
    "📹 Módulo 1 – Tipos de extintores": {
        "questions": ["q1", "q2", "q3", "q4"],
        "recommendation":
        "Revisa nuevamente los conceptos sobre tipos de fuego, extintores ABC y combustión espontánea."
    },

    "📹 Módulo 2 – Cómo usar un extintor": {
        "questions": ["q5", "q6", "q7"],
        "recommendation":
        "Repasa la inspección previa del extintor y el procedimiento correcto para utilizarlo."
    },

    "📹 Módulo 3 – Prevención de riesgos": {
        "questions": ["q8", "q9", "q10"],
        "recommendation":
        "Revisa las medidas preventivas para evitar incendios en maquinaria y áreas de trabajo."
    },

    "📹 Módulo 4 – Seguridad contra incendios en el hogar": {
        "questions": ["q11", "q12", "q13", "q14", "q16"],
        "recommendation":
        "Repasa las medidas de prevención y respuesta ante incendios en el hogar."
    }
}

FIRE_QUESTION_MAPPING = {
        "q4": "q1",
        "q5": "q2",
        "q6": "q3",
        "q7": "q4",
        "q8": "q5",
        "q9": "q6",
        "q10": "q7",
        "q11": "q8",
        "q12": "q9",
        "q13": "q10",
        "q14": "q11",
        "q15": "q12",
        "q16": "q13",
        "q17": "q14",
        "q19": "q16"
    }

BIO_QUESTION_TEXT = {
    "q4": "¿Cuál es el principal objetivo de un plan de bioseguridad en una granja lechera?",
    "q5": "Si una enfermedad ya está presente en la granja, es fácil eliminarla por completo",
    "q6": "¿Cuál de estas acciones es más importante cuando llegan animales nuevos a la granja?",
    "q7": "¿Los vehículos representan un riesgo de bioseguridad?",
    "q8": "¿Cuál de estos animales es un vector de enfermedades?",

    "q9": "¿Cuál es el propósito principal de usar guantes y cubrebotas en la granja?",
    "q10": "Antes de colocarse los guantes, se debe:",
    "q11": "¿Cuándo debe cambiarse un par de guantes desechables?",
    "q12": "¿Qué deben hacer los visitantes antes de ingresar a las áreas de animales?",
    "q13": "Si ocurre un pinchazo accidental con una aguja contaminada, la persona debe:",

    "q14": "¿Cuál es una señal de alerta que puede indicar que un animal está enfermo?",
    "q15": "Si observas un animal con signos de enfermedad, ¿qué debes hacer primero?",
    "q16": "¿Por qué es importante aislar a los animales enfermos?",
    "q17": "¿Qué información debe incluir un reporte efectivo de un animal enfermo?",
    "q18": "¿Qué práctica de bioseguridad debe realizarse antes y después de atender a un animal enfermo?"
}

BIO_POST_QUESTION_TEXT = {
    "q4": "¿Cuál es el principal objetivo de un plan de bioseguridad en una granja lechera?",
    "q5": "Si una enfermedad ya está presente en la granja, es fácil eliminarla por completo",
    "q6": "¿Cuál de estas acciones es más importante cuando llegan animales nuevos a la granja?",
    "q7": "¿Los vehículos representan un riesgo de bioseguridad?",
    "q8": "¿Cuál de estos animales es un vector de enfermedades?",

    "q9": "¿Cuál es el propósito principal de usar guantes y cubrebotas en la granja?",
    "q10": "Antes de colocarse los guantes, se debe:",
    "q11": "¿Cuándo debe cambiarse un par de guantes desechables?",
    "q12": "¿Qué deben hacer los visitantes antes de ingresar a las áreas de animales?",
    "q13": "Si ocurre un pinchazo accidental con una aguja contaminada, la persona debe:",

    "q14": "¿Cuál es una señal de alerta que puede indicar que un animal está enfermo?",
    "q15": "Si observas un animal con signos de enfermedad, ¿qué debes hacer primero?",
    "q16": "¿Por qué es importante aislar a los animales enfermos?",
    "q17": "¿Qué información debe incluir un reporte efectivo de un animal enfermo?",
    "q18": "¿Qué práctica de bioseguridad debe realizarse antes y después de atender a un animal enfermo?"
}

BIO_VIDEO_MAPPING = {

    "📹 Módulo 1 – Qué es la bioseguridad y por qué importa": {
        "questions": ["q4", "q5", "q6", "q7", "q8"],
        "recommendation":
        "Repasa los conceptos básicos de bioseguridad, ingreso de animales y control de vectores."
    },

    "📹 Módulo 2 – Acciones concretas del trabajador": {
        "questions": ["q9", "q10", "q11", "q12", "q13"],
        "recommendation":
        "Revisa el uso correcto de guantes, higiene de manos y protocolos de ingreso."
    },

    "📹 Módulo 3 – Detección y reporte de enfermedades": {
        "questions": ["q14", "q15", "q16", "q17", "q18"],
        "recommendation":
        "Repasa la identificación temprana de enfermedades y los procedimientos de reporte."
    }
}
BIO_QUESTION_MAPPING = {
    "q4": "q4",
    "q5": "q5",
    "q6": "q6",
    "q7": "q7",
    "q8": "q8",
    "q9": "q9",
    "q10": "q10",
    "q11": "q11",
    "q12": "q12",
    "q13": "q13",
    "q14": "q14",
    "q15": "q15",
    "q16": "q16",
    "q17": "q17",
    "q18": "q18"
}


def load_csv(file):
    #path:f"data/{file}"
    if os.path.exists(file):
        return pd.read_csv(file)
    else:
        return pd.DataFrame()
    
def load_dashboard_css():
    with open("styles/dashboard.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def card(title, value):
    st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">{value}</p>
            <p class="metric-title">{title}</p>
        </div>
    """, unsafe_allow_html=True)

def section(title):
    with st.container():
        st.markdown("---")  # separador visual
        st.markdown(f"### {title}")


def classify_performance(score):
    percentage = (score / 15) * 100

    if score <= 9:
        return "Necesita reforzar", round(percentage, 1), \
        "Dominio bajo del tema; se recomienda repetir todo el módulo de videos"

    elif score <= 13:
        return "En progreso", round(percentage, 1), \
        "Buen avance, pero aún no alcanza el estándar de seguridad; repasar temas del modulo"

    else:
        return "Aprobado", round(percentage, 1), \
        "Cumple el estándar de aprobación, Felicitaciones!"
    
def dashboard():
    load_dashboard_css()
    st.title("📊 Panel de control y resultados")
    selected_course = st.selectbox(
        "Seleccione un curso",
        [
            "Seguridad contra incendios",
            "Bioseguridad"
        ],index=None,
        placeholder="Seleccione un curso..."

    )
    if not selected_course:
        st.info("Seleccione un curso para visualizar los resultados.")
        return

    if selected_course == "Seguridad contra incendios":

        question_text = FIRE_QUESTION_TEXT
        post_question_text = FIRE_POST_QUESTION_TEXT
        video_mapping = FIRE_VIDEO_MAPPING
        question_mapping = FIRE_QUESTION_MAPPING

        total_questions = 15

    elif selected_course == "Bioseguridad":
        question_text = BIO_QUESTION_TEXT
        post_question_text = BIO_POST_QUESTION_TEXT
        video_mapping = BIO_VIDEO_MAPPING
        question_mapping = BIO_QUESTION_MAPPING
        total_questions = 15


    user_email = None

    if "user" in st.session_state:
        user_email = str(st.session_state["user"]["email"]).strip().lower()
    else:
        st.info("")

    #st.write(st.session_state)
    response_pre = supabase.table("initial_quiz").select("*").execute()
    response_post = supabase.table("post_test").select("*").execute()

    df_pre = pd.DataFrame(response_pre.data)
    df_post = pd.DataFrame(response_post.data)
    df_pre = df_pre[df_pre["course"] == selected_course]
    df_post = df_post[df_post["course"] == selected_course]
    df_pre_full = df_pre.copy()

    if df_pre.empty or df_post.empty:
        st.warning("No data available yet.")
        return


    # ✅ NORMALIZAR EMAILS AQUÍ
    df_pre["user"] = df_pre["user"].astype(str).str.strip().str.lower()
    df_post["user"] = df_post["user"].astype(str).str.strip().str.lower()


    # ✅ FILTRO
    df_pre = df_pre.dropna(subset=["score"])
    df_post = df_post.dropna(subset=["score"])


    # ✅ ÚLTIMO INTENTO
    df_pre["timestamp"] = pd.to_datetime(df_pre["timestamp"], errors="coerce")
    df_post["timestamp"] = pd.to_datetime(df_post["timestamp"], errors="coerce")

    df_pre = df_pre.sort_values("timestamp").groupby("user").tail(1)
    df_post = df_post.sort_values("timestamp").groupby("user").tail(1)


    # -------- MERGE --------
    merged = df_pre.merge(df_post, on="user", suffixes=("_pre", "_post"))
    if selected_course == "Seguridad contra incendios":

        merged = merged.rename(columns={
            "q17_correct": "q17_correct_pre",
            "q19_correct": "q19_correct_pre",
            "q1_correct": "q1_correct_post",
            "q2_correct": "q2_correct_post",
            "q3_correct": "q3_correct_post"
        })

        merged = merged.drop(
            columns=[
                "q18_correct",
                "q15_correct_post"
            ],
            errors="ignore"
        )
    elif selected_course == "Bioseguridad":

        merged = merged.rename(columns={
            "q1_correct": "q1_correct_post",
            "q2_correct": "q2_correct_post",
            "q3_correct": "q3_correct_post",
            "q17_correct": "q17_correct_pre",
            "q18_correct": "q18_correct_pre"
        })

    if merged.empty:
        st.error("❌ No matching users between pre and post")
        st.write("PRE users:", df_pre["user"].tolist())
        st.write("POST users:", df_post["user"].tolist())
        return
    if user_email:
        user_data = merged[merged["user"] == user_email]
    else:
        user_data = pd.DataFrame()  # vacío

    # -------- SCORES --------
    merged["improvement"] = merged["score_post"] - merged["score_pre"]

    
    # -------- KPIs --------
    with st.container(border=True):
        
        st.markdown("## 👤 Tu rendimiento personal")
        
        if not user_data.empty:
            user_pre = user_data["score_pre"].iloc[0]
            user_post = user_data["score_post"].iloc[0]
            #user_improvement = user_post - user_pre
            # CÁLCULO
            pre_level, pre_pct, _ = classify_performance(user_pre)
            post_level, post_pct, post_msg = classify_performance(user_post)

            improvement_pct = post_pct - pre_pct

            col1, col2, col3 = st.columns(3)
            
            with col1:
                card(
                        "",
                        f"""
                        <span style='font-size:16px'>{pre_pct}%</span><br>
                        {user_pre} preguntas correctas<br>
                        <span style='font-size:13px;color:gray'>Antes del entrenamiento</span>
                        """
                    )

            with col2:                
                card(
                        "",
                        f"""
                        <span style='font-size:16px'>{post_pct}%</span><br>
                        {user_post} preguntas correctas<br>
                        <span style='font-size:13px;color:gray'>Después del entrenamiento</span>
                    """)

            with col3:
                card(
                        "",
                        f"""
                        +{round(improvement_pct,1)}%<br>
                        <span style='font-size:13px;color:gray'>Progreso total</span>
                        """
                    )
            
            st.markdown("---")
            st.markdown("##  🧠 Resultado final")
            # color según nivel
            if post_level == "Aprobado":
                st.success(f"✅ {post_level} ({post_pct}%)")
            elif post_level == "En progreso":
                st.warning(f"🟡 {post_level} ({post_pct}%)")
            else:
                st.error(f"🔴 {post_level} ({post_pct}%)")

            st.markdown(f"""
            **Evaluación:**

            {post_msg}
            """)
            # =====================================================
            # PLAN DE MEJORA PERSONALIZADO
            # =====================================================

            st.markdown("---")
            st.markdown("## 🎯 Plan de mejora personalizado")

            modules_to_review = {}

            for module_name, module_info in video_mapping.items():

                failed_questions = []

                for q in module_info["questions"]:

                    col_name = f"{q}_correct_post"

                    if col_name in user_data.columns:
                        is_correct = user_data[col_name].iloc[0]
                        if not is_correct:

                            failed_questions.append(
                                post_question_text.get(q, q)
                            )

                if failed_questions:

                    modules_to_review[module_name] = {
                        "questions": failed_questions,
                        "recommendation": module_info["recommendation"]
                    }

            if modules_to_review:

                st.info(
                    "Hemos identificado algunos temas que podrían beneficiarse de una revisión adicional."
                )

                for module_name, data in modules_to_review.items():

                    with st.container(border=True):

                        st.markdown(f"### {module_name}")

                        st.markdown("**Preguntas relacionadas:**")

                        for question in data["questions"]:
                            st.markdown(f"- {question}")

                        st.caption(
                            f"💡 Recomendación: {data['recommendation']}"
                        )

            else:

                st.success(
                    "🎉 Excelente trabajo. No se detectaron áreas que requieran refuerzo adicional."
                )


        else:
            st.warning("Inicia sesión y completa el entrenamiento para ver tus resultados personales.")
        st.markdown("---")
        st.markdown("## Resumen general")

        
        pre_avg = merged["score_pre"].mean()
        post_avg = merged["score_post"].mean()

        pre_pct_avg = (pre_avg / total_questions) * 100
        post_pct_avg = (post_avg / total_questions) * 100

        improvement_pct_avg = post_pct_avg - pre_pct_avg
        col1, col2, col3, col4 = st.columns(4)
        total_users = merged["user"].nunique()

        with col1:
            card(
                    "",
                    f"""
                    <span style='font-size:16px'>{round(pre_pct_avg,1)}%</span><br>
                    {round(pre_avg,1)} preguntas correctas<br>
                    <span style='font-size:13px;color:gray'>Promedio antes entrenamiento</span>
                    """
                )
        with col2:
            card(
                    "",
                    f"""
                    <span style='font-size:16px'>{round(post_pct_avg,1)}%</span><br>
                    {round(post_avg,1)} preguntas correctas<br>
                    <span style='font-size:13px;color:gray'>Promedio después entrenamiento</span>
                    """
                )
        with col3:
            card(
                    "",
                    f"""
                    +{round(improvement_pct_avg,1)}%<br>
                    <span style='font-size:13px;color:gray'>Mejora promedio</span>
                    """
                )


        with col4:
            card(
                    "",
                    f"""
                    {round(total_users,1)}<br>
                    <span style='font-size:13px;color:gray'>Total usuarios</span>
                    """
                )

        st.markdown("")
        
    # 📊 SEGMENTACIÓN POR NIVELES
    # =====================================================
    
    with st.container(border=True):

        st.markdown("### 📊 Segmentación por niveles")


        merged[["pre_level", "pre_pct", "pre_msg"]] = merged["score_pre"].apply(
            lambda x: pd.Series(classify_performance(x))
        )
        merged[["post_level", "post_pct", "post_msg"]] = merged["score_post"].apply(
            lambda x: pd.Series(classify_performance(x))
)

        pre_counts = merged["pre_level"].value_counts()
        post_counts = merged["post_level"].value_counts()

        levels_df = pd.DataFrame({
            "Pre": pre_counts,
            "Post": post_counts
        }).fillna(0)

        levels_order = ["Necesita reforzar", "En progreso", "Aprobado"]
        levels_df = levels_df.reindex(levels_order)

        levels_df = levels_df.reset_index().rename(columns={"index": "Level"})

        levels_melted = levels_df.melt(
            id_vars="Level",
            var_name="Type",
            value_name="Count"
        )
        col1, col2= st.columns(2)
        with col1:
            st.markdown("")
            chart_levels = alt.Chart(levels_melted).mark_bar().encode(
            x=alt.X("Level:N", title="Nivel de rendimiento"),
            y=alt.Y("Count:Q", title="Número de usuarios"),
            color=alt.Color("Type:N",
                scale=alt.Scale(domain=["Pre", "Post"], range=["#3498db", "#2ecc71"])
            ),
            xOffset="Type:N",
            tooltip=["Level", "Type", "Count"])
            st.altair_chart(chart_levels, width="stretch")

        with col2:
         # LEVEL INSIGHTS
            low_pre = levels_df.loc[levels_df["Level"] == "Necesita reforzar", "Pre"].values[0]
            low_post = levels_df.loc[levels_df["Level"] == "Necesita reforzar", "Post"].values[0]

            high_pre = levels_df.loc[levels_df["Level"] == "Aprobado", "Pre"].values[0]
            high_post = levels_df.loc[levels_df["Level"] == "Aprobado", "Post"].values[0]
            card(
                    "",
                    f"""
                    <span style='font-size:16px'>Explicación de los niveles de rendimiento</span><p>
                    🔴 Necesita reforzar (0–9 preguntas / ≤60%)</p>
                    <p>🟡 En progreso (10–13 preguntas / 66–86%)    
                    Dominio bajo del tema, buen avance pero requiere refuerzo con los entrenamientos
                    </p>
                    <p>🟢 Aprobado (14–15 preguntas/ ≥93%)  
                    Cumple el estándar de aprobación 
                    </p>"""
                )
    # -------- LEARNING PREFERENCES --------
    # -------- LEARNING INSIGHTS (PRE ONLY) --------
    st.header("🎯 Perspectivas de aprendizaje")

    st.markdown("### 🧠 Formato de aprendizaje preferido")

    # total usuarios
    
    total_pre = df_pre_full["user"].nunique()

    df_q3 = df_pre_full.explode("q3")
    
    # evita duplicados por usuario
    df_q3 = df_q3.drop_duplicates(subset=["user", "q3"])

    total_pre = df_pre_full["user"].nunique()


    # contar respuestas
    pre_counts = df_q3["q3"].value_counts()

    data = []

    for option, count in pre_counts.items():
        data.append({
            "Pregunta": option,
            "# usuarios": int(count),
            "% de usuarios": round((count / total_pre) * 100, 1) if total_pre > 0 else 0
        })

    df_learning = pd.DataFrame(data).sort_values(by="% de usuarios", ascending=False)

    # mostrar tabla
    st.dataframe(df_learning, width="stretch")

    
    # -------- QUESTIONS --------
    # -------- QUESTIONS --------

    data = []

    for pre_q, post_q in question_mapping.items():

        pre_acc = merged[f"{pre_q}_correct_pre"].mean()

        post_acc = merged[f"{post_q}_correct_post"].mean()

        data.append({
            "Question": question_text.get(pre_q, pre_q),
            "Pre": pre_acc,
            "Post": post_acc,
            "Improvement": post_acc - pre_acc
        })

    df_questions = pd.DataFrame(data)

    df_questions_sorted = df_questions.sort_values(by="Improvement", ascending=False) 
    top_question = df_questions_sorted.iloc[0]
    worst_question = df_questions_sorted.iloc[-1]
    st.markdown("### 🧠 Resumen de preguntas")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"""
        🚀 **Más usuarios acertaron**
        
        **{top_question['Question']}**
        
        Puntos de mejora: **{top_question['Improvement']:.2f}**
        """)

    with col2:
        st.error(f"""
        ⚠️ **Menos usuarios acertaron**
        
        **{worst_question['Question']}**
        
        Puntos de mejora: **{worst_question['Improvement']:.2f}**
        """)

# -------- TRAINING EFFECTIVENESS SUMMARY --------
    with st.container(border=True):

        st.markdown("### ✅ Resumen del entrenamiento")

        total = len(merged)
        improved = (merged["improvement"] > 0).sum()
        same = (merged["improvement"] == 0).sum()
        worse = (merged["improvement"] < 0).sum()

        improvement_rate = (improved / total) * 100 if total > 0 else 0
        col1, col2 = st.columns(2)

        # nivel performance shift
        low_pre = (merged["score_pre"] <= 6).sum()
        low_post = (merged["score_post"] <= 6).sum()

        high_pre = (merged["score_pre"] > 10).sum()
        high_post = (merged["score_post"] > 10).sum()
        with col1:
            improvement_pct_avg = ((merged["score_post"].mean() - merged["score_pre"].mean()) / 15) * 100
            st.markdown(f"""
            - 🔻 **{low_pre - low_post} Estudiantes que dejaron de tener un bajo rendimiento**
            - 🚀 **{high_post - high_pre} Estudiantes que alcanzaron alto rendimiento**
            - 📈 **Promedio de mejoramiento:** {merged["improvement"].mean():.2f} preguntas ({improvement_pct_avg:.1f}%)

            """)
            
        with col2:
            
            approved = (merged["score_post"] >= 14).sum()
            effectiveness_score = (approved / total) * 100

            st.metric("🎯 Porcetaje de personas que aprobaron", f"{effectiveness_score:.1f}%")
        
        # evaluación automática
        if improvement_rate >= 90:
                st.success("⭐  La mayoría de los usuarios alcanzó el nivel aprobado. El entrenamiento es altamente eficaz.")
        elif improvement_rate >= 40:
                st.warning("""
                    ⚠️ El entrenamiento muestra eficacia moderada.
                    Muchos usuarios están en progreso, pero aún no alcanzan el estándar de aprobación.
                    """)
        else:  
                st.error("""
                    ❌ La mayoría de los usuarios permanece en nivel bajo.
                    
                    Se recomienda reforzar el contenido del entrenamiento.
                    """)

# =====================================================
# FEEDBACK DE USUARIO
# =====================================================

    with st.container(border=True):

        st.markdown("### 💬 Tu opinión")

        st.markdown("""
        Tu retroalimentación es muy importante para mejorar la plataforma.
        """)

        # rating 1–5
        
        rating_options = {
            "😞 Mala": 1,
            "😐 Regular": 2,
            "🙂 Buena": 3,
            "😃 Muy buena": 4,
            "😎 Excelente": 5
        }

        
        rating_label = st.radio(
            "¿Cómo fue tu experiencia?",
            list(rating_options.keys()),
            horizontal=True
        )

        rating = rating_options[rating_label]



        # comentario
        comment = st.text_area("Comentarios sobre el entrenamiento o que temas mas te gustaria ver (opcional)")

        if st.button("Enviar"):

            if "user" in st.session_state:
                user_email = st.session_state["user"]["email"]
            else:
                user_email = "anonimo"

            try:
                supabase.table("feedback").insert({
                    "user": user_email,
                    "rating": rating,
                    "comment": comment
                }).execute()

                st.success("✅ ¡Gracias por tu opinion!")

            except Exception as e:
                st.error("❌ Error al guardar la opinion")
                st.write(e)


        
