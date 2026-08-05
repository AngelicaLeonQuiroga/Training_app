from supabase_client import supabase
from datetime import datetime
import streamlit as st

def save_progress(
    email,
    course,
    current_step,
    pre_test_completed=False
):

    email = email.strip().lower()

    data = {
        "user_email": email,
        "course": course,
        "current_step": current_step,
        "pre_test_completed": pre_test_completed,
        "updated_at": str(datetime.now())
    }

    existing = (
        supabase.table("training_progress")
        .select("*")
        .eq("user_email", email)
        .eq("course", course)
        .execute()
    )

    if existing.data:

        response = (
            supabase.table("training_progress")
            .update(data)
            .eq("user_email", email)
            .eq("course", course)
            .execute()
        )

    else:

        response = (
            supabase.table("training_progress")
            .insert(data)
            .execute()
        )

    return response

def get_progress(email, course):
    """
    Recupera el progreso guardado de un usuario.
    """
    email = email.strip().lower()
    response = (
        supabase.table("training_progress")
        .select("*")
        .eq("user_email", email)
        .eq("course", course)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None



def mark_completed(email, course):
    """
    Marca el curso como completado.
    No elimina el progreso.
    """

    email = email.strip().lower()

    data = {
        "current_step": "completed",
        "status_test": "completed",
        "pre_test_completed": True,
        "updated_at": str(datetime.now())
    }

    response = (
        supabase.table("training_progress")
        .update(data)
        .eq("user_email", email)
        .eq("course", course)
        .execute()
    )

    return response


def restart_progress(email, course):
    """
    Reinicia el curso desde video1 si el usuario quiere repetir el entrenamiento.
    """

    email = email.strip().lower()

    data = {
        "user_email": email,
        "course": course,
        "current_step": "video1",
        "status_test": "in_progress",
        "pre_test_completed": False,
        "updated_at": str(datetime.now())
    }

    existing = (
        supabase.table("training_progress")
        .select("*")
        .eq("user_email", email)
        .eq("course", course)
        .execute()
    )

    if existing.data:
        response = (
            supabase.table("training_progress")
            .update(data)
            .eq("user_email", email)
            .eq("course", course)
            .execute()
        )
    else:
        response = (
            supabase.table("training_progress")
            .insert(data)
            .execute()
        )

    return response
