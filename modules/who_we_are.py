import streamlit as st
import base64


def get_image_base64(path):
    with open(path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    return data

def who_we_are():
    
    # (opcional) cargar imágenes
    img_user = get_image_base64("assets/user.png")
    img_sponsor = get_image_base64("assets/sponsor.png")
    st.title("👥 Quiénes somos")

    st.markdown("---")

    # -------- SECCIÓN 1: EL PROYECTO --------
    st.markdown("""
    ## 📚 Sobre la plataforma
Esta plataforma de entrenamiento ha sido diseñada como una herramienta integral de aprendizaje orientada al fortalecimiento de competencias en materia de seguridad dentro del sector agropecuario.

A través de una estructura basada en módulos interactivos, evaluaciones diagnósticas y análisis del desempeño, el sistema permite no solo la adquisición de conocimientos, sino también la medición objetiva del progreso del usuario a lo largo del proceso formativo.

El enfoque pedagógico de la plataforma está centrado en el aprendizaje autónomo, facilitando que cada usuario avance a su propio ritmo, identifique áreas de mejora y consolide conceptos clave mediante la práctica continua. De esta manera, se promueve una formación más efectiva, aplicable y alineada con los estándares de seguridad requeridos en entornos reales de trabajo.
    """)

    # -------- SECCIÓN 2: DESARROLLADOR --------
    st.markdown("## 👨‍💻 Desarrollo")

    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown(f"""
        <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_user}" style="width:150px;" />
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""**Maristela Rovai, DVM, PhD**""")
        st.markdown("""Professor Dairy and Food Science Department""")
        st.markdown("""South Dakota State University""")
        st.markdown("""maristela.rovai@sdstate.edu""")

    st.markdown("---")

    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown(f"""        
            <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_user}" style="width:150px;" />
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(""" 
        **Noelia Silva del Rio, DVM, PhD**          
        """)
        st.markdown("""Population Health & Reproduction, School of Veterinary Medicine""")
        st.markdown("""Veterinary Medicine Teaching & Research Center""")
        st.markdown("""University of California, Davis, California""")
        st.markdown("""nsilvadelrio@ucdavis.edu""")

    st.markdown("---")

    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown(f"""
         <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_user}" style="width:150px;" />
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""**Ludy Angelica Leon Quiroga, Electronic Eng**""")
        st.markdown("""Master's student - Dairy and Food Science Department""")
        st.markdown("""South Dakota State University""")
        st.markdown("""ludy.leonquiroga@sdstate.edu""")
        st.markdown("""angelicaleonquiroga@gmail.com""")
        st.markdown("""Participó en el desarrollo de esta plataforma, incluyendo el diseño, 
                    implementación y análisis de datos del sistema de entrenamiento
                    
        Tecnologías utilizadas:
        - Python
        - Streamlit
        - Supabase
        - Pandas & visualización de datos
        """)

    st.markdown("---")

    # -------- SECCIÓN 3: PATROCINADOR --------
    st.markdown("## 🤝 Patrocinio")

    col1, col2 = st.columns([1,2])

    with col1:
        st.markdown(f"""
        <div style="display: flex; justify-content: center;">
                <img src="data:image/png;base64,{img_sponsor}" />
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        Esta plataforma de capacitación cuenta con el apoyo de una subvención otorgada por la Fundación de Extensión, 
        financiada a través de la Iniciativa de Investigación Agrícola y Alimentaria (AFRI) - Centro Nacional de Intercambio de Información para la Industria 
        y la Fuerza Laboral, proyecto n.° 2023-67037-40533, del Instituto Nacional de Alimentación y Agricultura del Departamento de Agricultura de los Estados Unidos. 
        Las opiniones, hallazgos, conclusiones o recomendaciones expresadas en esta plataforma de capacitación y en el apoyo consultivo son responsabilidad de sus 
        autores y no reflejan necesariamente la opinión del Departamento de Agricultura de los Estados Unidos ni de la Fundación de Extensión.
        Su apoyo ha permitido el desarrollo de los videos de seguridad para mejorar 
                la capacitación de los usuarios.
                Tambien formaron parte South Dakota State University y University of California, Davis.
        """)

    st.markdown("---")

    # -------- SECCIÓN 4: MISIÓN --------
    st.markdown("""
    ##
    """)

    # -------- SECCIÓN 5: VISIÓN --------
    st.markdown("""
    """)