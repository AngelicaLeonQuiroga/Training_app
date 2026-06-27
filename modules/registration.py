import streamlit as st
#from utils import save_in_csv
from supabase_client import supabase

def registration_screen():
    st.title("Plataforma de entrenamiento interactivo ")
    st.header("Registro")
    st.markdown("""
            El registro inicial es muy importante, ya que nos permite identificar tu 
                progreso en los videos educativos y ofrecerte retroalimentacion 
                personalizada sobre la información que vayas completando
                """)

    if "user" in st.session_state:
        name = st.session_state["user"]["name"]
        st.success(f"Bienvenido {name}, te has registrado con exito")
        st.write("Haz click acontinuación para comenzar el entrenamiento")

        if st.button("Comenzar"):
            st.session_state["start"] = True
            st.rerun()

    else:
        with st.form("user_registration"):
            name = st.text_input("Nombre completo")
            email = st.text_input("Email")
            education_level = st.selectbox(
                  "Nivel de educación",
                  [
                      "Seleccione una opción...", 
                        "Primaria",
                        "Secundaria",
                        "Tecnico",
                        "Universidad",
                        "Postgrado","No estudie"
                   ],
                )
            position = st.selectbox(
                  "Ocupación",
                  [
                      "Seleccione una opción...", 
                        "Ordeñador",
                        "Encargado general",
                        "Encargado de area",
                        "Veterinario",
                        "Alimentación","Reproducción",
                        "Administrativo",
                        "Maternidad",
                        "Patero",
                        "Salud rebaño","Area becerros",
                        "Mecánico",
                        "Cultivos",
                        "Area de estiercol ",
                        "Otro"
                   ],
                )            
            if position == "Otro":
                position_other = st.text_input("Especifica tu ocupación")
            else:
                position_other = ""
            company = st.text_input("Nombre de la empresa")
            city = st.text_input("Ciudad")
            country = st.text_input("País")
            submitted = st.form_submit_button("Guardar y continuar")

        if submitted:
        # VALIDACIÓN DE "OTRO"
        
             if position == "Seleccione una opción...":
                    st.error("Por favor selecciona una ocupación")
             elif education_level == "Seleccione una opción...":
                    st.error("Por favor selecciona tu nivel de educación")
             elif position == "Otro" and not position_other:
                st.error("Por favor especifica tu ocupación")
             elif not (name and email and position):
                st.error("Por favor complete los campos")
             else:
                  if position == "Otro" and position_other:
                    final_position = position_other
                  else:
                    final_position = position

                  if name and email and position:
                    user = {
                        "name": name,
                        "email": email,
                        "education_level": education_level,
                        "position": final_position,
                        "company": company,
                        "city": city,
                        "country": country,

                    }
                    
                    # 1. VERIFICAR SI YA EXISTE
                    existing_user = supabase.table("users") \
                        .select("*") \
                        .eq("email", email) \
                        .execute()
                    
                    if existing_user.data:
                                # ✅ YA EXISTE → NO INSERTAR
                                st.warning("Este usuario ya esta registrado")

                                # usar el usuario existente
                                st.session_state["user"] = existing_user.data[0]

                    
                    else:
                                # ✅ NO EXISTE → CREAR NUEVO
                                supabase.table("users").insert(user).execute()

                                st.session_state["user"] = user
                                st.success("Usuario registrado con exito")

                    st.rerun()

                    #save_in_csv(user, "users.csv")

                  else:
                    st.error("Por favor complete los campos")
