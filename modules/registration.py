import streamlit as st
#from utils import save_in_csv
from supabase_client import supabase

def registration_screen():
    st.title("Plataforma de entrenamiento interactivo")
    st.header("Registro inicial")

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
            position = st.text_input("Posición")
            company = st.text_input("Nombre de la empresa")
            submitted = st.form_submit_button("Guardar y continuar")

        if submitted:
            if name and email and position:
                user = {
                    "name": name,
                    "email": email,
                    "position": position,
                    "company": company,
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
