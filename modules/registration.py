import streamlit as st
#from utils import save_in_csv
from supabase_client import supabase

def registration_screen():
    st.title("interactive training platform")
    st.header("Initial registration")

    if "user" in st.session_state:
        name = st.session_state["user"]["name"]
        st.success(f"Welcome {name}, your registration was successful.")
        st.write("Click below to begin training.")

        if st.button("Begin training"):
            st.session_state["start"] = True
            st.rerun()

    else:
        with st.form("user_registration"):
            name = st.text_input("Full name")
            email = st.text_input("Email")
            position = st.text_input("Position")
            company = st.text_input("Company")
            submitted = st.form_submit_button("Save and continue")

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
                            st.warning("This user is already registered")

                            # usar el usuario existente
                            st.session_state["user"] = existing_user.data[0]

                
                else:
                            # ✅ NO EXISTE → CREAR NUEVO
                            supabase.table("users").insert(user).execute()

                            st.session_state["user"] = user
                            st.success("User registered successfully")

                st.rerun()

                #save_in_csv(user, "users.csv")

            else:
                st.error("Please complete all required fields.")
