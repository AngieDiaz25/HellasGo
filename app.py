import streamlit as st
import pandas as pd
from modules.data_loader import get_route_data, get_accommodation_data

# Configuración básica de la página
st.set_page_config(page_title="HellasGo", page_icon="⛴️", layout="wide")

st.title("⛴️ HellasGo: Optimizador de Viaje")
st.markdown("**Destinos:** Milos, Halki, Symi, Agistri, Tinos | **Fechas:** 02 - 10 Mayo 2027")

# Cargar datos desde nuestro módulo
df_rutas = get_route_data()
df_alojamiento = get_accommodation_data()

# Unir los datos por la columna 'Isla'
df_master = pd.merge(df_rutas, df_alojamiento, on="Isla")
df_master["Costo Total (€)"] = df_master["Vuelo (€)"] + df_master["Ferry (€)"] + df_master["Alojamiento Total (€)"]

# Menú lateral para ajustar preferencias
st.sidebar.header("¿Qué es más importante?")
peso_precio = st.sidebar.slider("Ahorrar dinero", 0.0, 1.0, 0.5)
peso_tiempo = st.sidebar.slider("Llegar rápido", 0.0, 1.0, 0.3)
peso_calidad = st.sidebar.slider("Calidad del alojamiento", 0.0, 1.0, 0.2)

# Fórmula matemática para decidir la mejor isla
max_precio = df_master["Costo Total (€)"].max()
max_tiempo = df_master["Tiempo Total (h)"].max()

df_master["Puntuación"] = (
    ((1 - (df_master["Costo Total (€)"] / max_precio)) * peso_precio * 100) +
    ((1 - (df_master["Tiempo Total (h)"] / max_tiempo)) * peso_tiempo * 100) +
    ((df_master["Calidad (1-10)"] / 10) * peso_calidad * 100)
)
df_master = df_master.sort_values(by="Puntuación", ascending=False).round(1)

# Mostrar resultados en la pantalla
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Clasificación de Destinos")
    st.dataframe(df_master[["Isla", "Tiempo Total (h)", "Costo Total (€)", "Puntuación"]], hide_index=True)

with col2:
    ganador = df_master.iloc[0]
    st.success("🏆 Mejor Opción Actual")
    st.metric(label=f"Destino: {ganador['Isla']}", value=f"{ganador['Puntuación']} pts")
    st.write(f"**Tiempo de viaje:** {ganador['Tiempo Total (h)']} hrs")
    st.write(f"**Gasto total estimado:** €{ganador['Costo Total (€)']}")