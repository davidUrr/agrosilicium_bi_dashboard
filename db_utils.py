# db_utils.py
import os
import sqlite3

import gdown
import pandas as pd
import streamlit as st

from config import DB_PATH

# URL de descarga directa de la base de datos de 261 MB
# ⚠️ REEMPLAZA EL ID POR EL TUYO DE GOOGLE DRIVE:
DB_URL = "https://drive.google.com/uc?export=download&id=1MSPlFR_bj-2mQt6tUp9Q_Am4--Q3eK1a"
#https://drive.google.com/file/d/1Mz9O1L0HKwbBWdbOKX5gtL8WZqmMm_fB/view?usp=drive_link
#https://drive.google.com/file/d/1MSPlFR_bj-2mQt6tUp9Q_Am4--Q3eK1a/view?usp=sharing


def asegurar_base_de_datos():
    """
    Verifica si la base de datos SQLite existe localmente.
    Si no existe (ej. en Streamlit Cloud), la descarga automáticamente.
    """
    data_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir, exist_ok=True)
        
    if not os.path.exists(DB_PATH):
        with st.spinner("📦 Descargando base de datos de inteligencia (261 MB)... Esto solo ocurrirá la primera vez."):
            try:
                gdown.download(DB_URL, DB_PATH, quiet=False)
                st.success("✅ Base de datos descargada e indexada correctamente.")
            except Exception as e:
                st.error(f"❌ Error descargando la base de datos: {e}")

@st.cache_data(ttl=3600, show_spinner=False)
def read_from_db(table_name: str) -> pd.DataFrame:
    """
    Lee una tabla desde SQLite aplicando caché de memoria RAM en Streamlit Cloud.
    evita sobrecargar memoria y lecturas repetidas de disco.
    """
    asegurar_base_de_datos()
    
    if not os.path.exists(DB_PATH):
        st.error(f"No se encontró la base de datos en: {DB_PATH}")
        return pd.DataFrame()

    conn = sqlite3.connect(DB_PATH)
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql_query(query, conn)
        return df
    except Exception as e:
        st.error(f"Error al consultar la tabla '{table_name}': {e}")
        return pd.DataFrame()
    finally:
        conn.close()