import streamlit as st
import pandas as pd
import os
import altair as alt
from supabase_client import supabase

#  MAPEO DE PREGUNTAS
question_text = {
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
    "q16": "¿Qué hacer si el fuego se sale de control?"
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
        "Buen avance, pero aún no alcanza el estándar de seguridad; repasar temas el modulo"

    else:
        return "Aprobado", round(percentage, 1), \
        "Cumple el estándar de aprobación, Felicitaciones!"
    
def dashboard():
    load_dashboard_css()
    st.title("📊 Panel de control")
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


        else:
            st.warning("Inicia sesión y completa el entrenamiento para ver tus resultados personales.")
        st.markdown("---")
        st.markdown("## Resumen general")

        

        
        total_questions = 15

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

    
    # -------- DELTA HISTOGRAM --------
    
   # with st.container(border=True):

       # st.markdown("### 📉 Impacto del entrenamiento")


        # Contar valores directamente
       # hist_df = merged["improvement"].value_counts().reset_index()
      #  hist_df.columns = ["Delta", "Count"]

        # Asegurar que es numérico
     #   hist_df["Delta"] = hist_df["Delta"].astype(int)

        # Ordenar correctamente
    #    hist_df = hist_df.sort_values(by="Delta")

        # Opcional: formato bonito (+1, +2, etc.)
   #     hist_df["Delta"] = hist_df["Delta"].apply(lambda x: f"{x:+}")

        # Mostrar gráfico
        
  #      chart = alt.Chart(hist_df).mark_bar().encode(
 #           x=alt.X("Delta:N", title="Puntaje de mejora (Post - Pre)"),
     #       y=alt.Y("Count:Q", title="Numero de estudiantes"),
    #        tooltip=["Delta", "Count"]
   #     )

        #st.altair_chart(chart, use_container_width=True)

       # avg_delta = merged["improvement"].mean()

      #  st.info(f"📊 Promedio de mejora: {avg_delta:.2f} points")

        # -------- QUICK INSIGHTS --------
     #   total = len(merged)

    #    improved = (merged["improvement"] > 0).sum()
   #     same = (merged["improvement"] == 0).sum()
  #      worse = (merged["improvement"] < 0).sum()

 #       st.markdown("### 🔍 Analisis de perspectiva")
#
 #       col1, col2, col3 = st.columns(3)
#        with col1:
       #     card("✅ Mejoro", f"{(improved/total)*100:.1f}%")

      #  with col2:
     #       card("➖ No tuvo cambios", f"{(same/total)*100:.1f}%")

    #    with col3:
        #    card("⚠️ Disminuyo", f"{(improved/total)*100:.1f}%")
       # st.markdown("")
        
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
            st.altair_chart(chart_levels, use_container_width=True)

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
    st.dataframe(df_learning, use_container_width=True)

    
    # -------- QUESTIONS --------
    questions = [f"q{i}" for i in range(4, 17)]

    data = []

    for q in questions:
        pre_acc = merged[q + "_correct_pre"].mean()
        post_acc = merged[q + "_correct_post"].mean()

        data.append({
            "Question": question_text.get(q, q),
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
        🚀 **Mas usuarios acertaron**
        
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


        
