import streamlit as st

def final_screen():
    st.title("Entrenamiento completado!")
    st.success("Gracias por completar nuestro entrenamiento.")
    if st.button("Continuar"):
            st.session_state["training_step"] = "quiz2"
            st.rerun()