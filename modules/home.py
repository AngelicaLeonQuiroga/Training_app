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
    learning = get_image_base64("assets/learning.png")
    farmer = get_image_base64("assets/farmer.png")
    check = get_image_base64("assets/check.png")

    # Header

    
    st.markdown(f"""
        <div class="banner">
            <h1>Aprende a tu ritmo <img src="data:image/png;base64,{learning}"  style="width:80px; margin:10px 0;"/>
            </h1>
        <div class="banner-text">
        <p>Mejora tus habilidades con módulos interactivos y evaluaciones prácticas.
            </p>
            <p class="banner-text p"><img src="data:image/png;base64,{check}"  style="width:20px; margin:10px 0;"/> Elige un tema</p>
            <p class="banner-text p"><img src="data:image/png;base64,{check}"  style="width:20px; margin:10px 0;"/> Realiza la evaluación inicial</p>
            <p class="banner-text p"><img src="data:image/png;base64,{check}"  style="width:20px; margin:10px 0;"/> Completa el entrenamiento</p>
            <p class="banner-text p"><img src="data:image/png;base64,{check}"  style="width:20px; margin:10px 0;"/> Consulta tus resultados</p>
        </div>
           </div>""", unsafe_allow_html=True)       
    st.info("Selecciona un curso abajo 👇")
    
    st.markdown("---")

    st.subheader("Entrenamientos disponibles")

    # Layout en columnas
    col1, col2 = st.columns([1,1])
    
    # -------- CARD 1 --------
    with col1:

        st.markdown(f"""
        <div class="card clickable">
            <h3>Seguridad contra incendios</h3>
            <img src="data:image/png;base64,{img_fire}" />
            <p>Aprende a prevenir incendios y usar extintores.</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("Comenzar", key="fire", width="stretch"):
                    st.session_state["selected_training"] = "fire"
                    st.session_state["course_name"] = "Seguridad contra incendios"
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
