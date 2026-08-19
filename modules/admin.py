import streamlit as st
import pandas as pd
from supabase_client import supabase

ADMIN_EMAIL = "dairyfarmtraining@gmail.com"


def admin_panel():

    st.title("🔒 Panel de Administrador")

    st.info("Authorized administrator access")

    tables = [
        "users",
        "initial_quiz",
        "post_test",
        "training_sessions",
        "training_progress",
        "feedback"
    ]

    for table_name in tables:

        try:

            response = (
                supabase
                .table(table_name)
                .select("*")
                .execute()
            )

            df = pd.DataFrame(response.data)

            st.subheader(table_name)

            st.write(f"Records: {len(df)}")

            st.download_button(
                label=f"📥 Download {table_name}.csv",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name=f"{table_name}.csv",
                mime="text/csv",
                key=table_name
            )

        except Exception as e:

            st.error(f"Error loading {table_name}")
            st.write(e)