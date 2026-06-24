import streamlit as st

def final_screen():
    st.title("Training completed 🎉")
    st.success("Thank you for completing the cybersecurity training.")
    if st.button("Continue"):
            st.session_state["training_step"] = "quiz2"
            st.rerun()