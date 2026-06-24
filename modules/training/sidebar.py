import streamlit as st

def render_sidebar(step, course_steps):

    with st.sidebar:

        # -------- USER --------
        if "user" in st.session_state:
            st.success(f"👤 {st.session_state['user']['name']}")

        st.markdown("---")

        # -------- NAVIGATION --------
        st.markdown("### Navigation")
        
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        st.markdown("---")
        menu = st.radio(
            "Navigation",
            ["🏠 Home", "📚 Training", "📊 Dashboard"],
            label_visibility="collapsed"
        )
        if menu == "🏠 Home":
            st.session_state["selected_training"] = None
        
        elif menu == "📊 Dashboard":
            st.session_state["selected_training"] = "dashboard"

        st.markdown("---")

        # -------- COURSE (solo si NO estás en dashboard) --------
        if (
            "course_name" in st.session_state and
            st.session_state.get("selected_training") != "dashboard"
        ):

            st.markdown(f"## 📚 {st.session_state['course_name']}")
            st.markdown("### Course Progress")

            step_keys = [s[0] for s in course_steps]

            for key, label in course_steps:
                if key == step:
                    st.markdown(f"👉 **{label}**")
                elif key in step_keys and step in step_keys and step_keys.index(key) < step_keys.index(step):
                    st.markdown(f"✅ {label}")
                else:
                    st.markdown(f"⬜ {label}")
