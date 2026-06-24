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


# ✅ FUNCIÓN DE NIVELES
def get_level(score):
    if score <= 6:
        return "Low"
    elif score <= 10:
        return "Medium"
    else:
        return "High"

def dashboard():
    load_dashboard_css()
    st.title("📊 Training Dashboard")

    # -------- LOAD DATA --------
    #df_pre = load_csv("data/initial_quiz.csv")
    #df_post = load_csv("data/post_test.csv")

    
    response_pre = supabase.table("initial_quiz").select("*").execute()
    response_post = supabase.table("post_test").select("*").execute()

    df_pre = pd.DataFrame(response_pre.data)
    df_post = pd.DataFrame(response_post.data)

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


    # -------- SCORES --------
    merged["improvement"] = merged["score_post"] - merged["score_pre"]

    
    # -------- KPIs --------
    with st.container(border=True):
        
        st.markdown("## Overview")

        col1, col2, col3, col4 = st.columns(4)

        pre_avg = round(merged["score_pre"].mean(), 2)
        post_avg = round(merged["score_post"].mean(), 2)
        improvement = round(merged["improvement"].mean(), 2)
        total_users = merged["user"].nunique()

        with col1:
            card("📊 Pre Avg", pre_avg)

        with col2:
            card("📈 Post Avg", post_avg)

        with col3:
            card("🚀 Improvement", improvement)

        with col4:
            card("👥 Total Users", total_users)

        st.markdown("")

    
    # -------- DELTA HISTOGRAM --------
    
    with st.container(border=True):

        st.markdown("### 📉 Improvement Distribution (Delta)")


        # Contar valores directamente
        hist_df = merged["improvement"].value_counts().reset_index()
        hist_df.columns = ["Delta", "Count"]

        # Asegurar que es numérico
        hist_df["Delta"] = hist_df["Delta"].astype(int)

        # Ordenar correctamente
        hist_df = hist_df.sort_values(by="Delta")

        # Opcional: formato bonito (+1, +2, etc.)
        hist_df["Delta"] = hist_df["Delta"].apply(lambda x: f"{x:+}")

        # Mostrar gráfico
        
        chart = alt.Chart(hist_df).mark_bar().encode(
            x=alt.X("Delta:N", title="Score Improvement (Post - Pre)"),
            y=alt.Y("Count:Q", title="Number of Students"),
            tooltip=["Delta", "Count"]
        )

        st.altair_chart(chart, use_container_width=True)

        avg_delta = merged["improvement"].mean()

        st.info(f"📊 Average improvement: {avg_delta:.2f} points")

        # -------- QUICK INSIGHTS --------
        total = len(merged)

        improved = (merged["improvement"] > 0).sum()
        same = (merged["improvement"] == 0).sum()
        worse = (merged["improvement"] < 0).sum()

        st.markdown("### 🔍 Insights")

        col1, col2, col3 = st.columns(3)
        with col1:
            card("✅ Improved", f"{(improved/total)*100:.1f}%")

        with col2:
            card("➖ No Change", f"{(same/total)*100:.1f}%")

        with col3:
            card("⚠️ Decreased", f"{(improved/total)*100:.1f}%")
        st.markdown("")
        
    # 📊 SEGMENTACIÓN POR NIVELES
    # =====================================================
    
    with st.container(border=True):

        st.markdown("### 📊 Performance by Level")


        merged["pre_level"] = merged["score_pre"].apply(get_level)
        merged["post_level"] = merged["score_post"].apply(get_level)

        pre_counts = merged["pre_level"].value_counts()
        post_counts = merged["post_level"].value_counts()

        levels_df = pd.DataFrame({
            "Pre": pre_counts,
            "Post": post_counts
        }).fillna(0)

        levels_order = ["Low", "Medium", "High"]
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
            x=alt.X("Level:N", title="Performance Level"),
            y=alt.Y("Count:Q", title="Number of Students"),
            color=alt.Color("Type:N",
                scale=alt.Scale(domain=["Pre", "Post"], range=["#3498db", "#2ecc71"])
            ),
            xOffset="Type:N",
            tooltip=["Level", "Type", "Count"])
            st.altair_chart(chart_levels, use_container_width=True)

        with col2:
         # LEVEL INSIGHTS
            low_pre = levels_df.loc[levels_df["Level"] == "Low", "Pre"].values[0]
            low_post = levels_df.loc[levels_df["Level"] == "Low", "Post"].values[0]

            high_pre = levels_df.loc[levels_df["Level"] == "High", "Pre"].values[0]
            high_post = levels_df.loc[levels_df["Level"] == "High", "Post"].values[0]
            card("🔻 Low Reduction", int(low_pre - low_post))
            st.markdown("")
            card("🚀 High Increase", int(high_post - high_pre))
            st.markdown("")
            with st.expander("📘 What do these levels mean?"):
                
                st.markdown("""
            ### Performance Levels Explained

            - 🔴 **Low (0–6)**  
            Learners have limited understanding and may struggle with key concepts.

            - 🟡 **Medium (7–10)**  
            Learners understand the basics but still have room to improve.

            - 🟢 **High (11–16)**  
            Learners demonstrate strong knowledge and are ready to apply what they learned.

            ---

            🎯 **Training Goal:**  
            Increase the number of students in *High* and reduce *Low*.
            """)

    # -------- LEARNING PREFERENCES --------
    # -------- LEARNING INSIGHTS (PRE ONLY) --------
    st.header("🎯 Learning Insights")

    st.markdown("### 🧠 Preferred Learning Format")

    # total usuarios
    total_pre = df_pre.shape[0]

    # contar respuestas
    pre_counts = df_pre["q3"].value_counts()

    data = []

    for option, count in pre_counts.items():
        data.append({
            "Answer": option,
            "Users": int(count),
            "% of Users": round((count / total_pre) * 100, 1) if total_pre > 0 else 0
        })

    df_learning = pd.DataFrame(data).sort_values(by="% of Users", ascending=False)

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
    st.markdown("### 🧠 Key Insights by Question")

    col1, col2 = st.columns(2)

    with col1:
        st.success(f"""
        🚀 **Top Improvement**
        
        **{top_question['Question']}**
        
        Improvement: **{top_question['Improvement']:.2f}**
        """)

    with col2:
        st.error(f"""
        ⚠️ **Needs Attention**
        
        **{worst_question['Question']}**
        
        Improvement: **{worst_question['Improvement']:.2f}**
        """)

# -------- TRAINING EFFECTIVENESS SUMMARY --------
    with st.container(border=True):

        st.markdown("### ✅ Training Summary")

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
            st.markdown(f"""
            - 🔻 **{low_pre - low_post} students moved out of low performance**
            - 🚀 **{high_post - high_pre} students reached high performance**
            - 📈 **Average improvement:** {merged["improvement"].mean():.2f} points

            """)
            
        with col2:
            
            effectiveness_score = (improved / total) * 100

            st.metric("🎯 Training Effectiveness Score", f"{effectiveness_score:.1f}%")
        
        # evaluación automática
        if improvement_rate > 70:
                st.success("✅ Training is highly effective")
        elif improvement_rate > 40:
                st.warning("⚠️ Training shows moderate effectiveness")
        else:
                st.error("❌ Training effectiveness is low")

        
