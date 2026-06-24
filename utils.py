import pandas as pd
import os

def save_in_csv(data: dict, file: str):
    """Guarda un diccionario en un CSV dentro de /data/."""
    path = f"data/{file}"
    os.makedirs("data", exist_ok=True)


 # ✅ si NO existe o está vacío
    if not os.path.exists(path) or os.stat(path).st_size == 0:
        df_new = pd.DataFrame([data])

    else:
        try:
            df = pd.read_csv(path)
            df_new = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        except pd.errors.EmptyDataError:
            # ✅ archivo corrupto o vacío
            df_new = pd.DataFrame([data])

    df_new.to_csv(path, index=False)

