import streamlit as st
from datetime import datetime
import base64

def get_image_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return data

def home_screen():
    
    img_fire = get_image_base64("assets/fire.png")
    img_bio = get_image_base64("assets/biosecurity.png")

    # Header
    st.markdown("""
    # 🎓 Training Platform
    ### Upgrade your skills with interactive modules
    """)

    st.markdown("---")

    st.subheader("Available Trainings")

    # Layout en columnas
    col1, col2 = st.columns([1,1])
    
    # -------- CARD 1 --------
    with col1:

        st.markdown(f"""
        <div class="card clickable">
            <h3>Fire Safety Training</h3>
            <img src="data:image/png;base64,{img_fire}" />
            <p>Learn how to use extinguishers and prevent fires.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("Start", key="fire", use_container_width=True):
                    st.session_state["selected_training"] = "fire"
                    st.session_state["course_name"] = "Fire Safety Training"
                # GUARDAR HORA DE INICIO
                    st.session_state["training_start_time"] = datetime.now()

                    st.rerun()
                

    # -------- CARD 2 --------
    with col2:

 #       st.markdown(f"""
  #      <div class="card clickable">
   #         <h3>Biosecurity</h3>
    #        <img src="data:image/png;base64,{img_bio}" />
      #      <p>Learn how to biosecurity.</p>
     #   </div>
       # """, unsafe_allow_html=True)
        st.markdown("---")

 #       if st.button("Start", key="bio", use_container_width=True):
  #          st.session_state["selected_training"] = "bio"
   #         st.session_state["course_name"] = "Biosecurity"
        # GUARDAR HORA DE INICIO
    #        st.session_state["training_start_time"] = datetime.now()
            

     #       st.rerun()