import streamlit as st
import pandas as pd
import datetime
from modules.data_loader import get_route_data, get_accommodation_data, get_ferry_schedule_data, get_island_metadata

# Configuración básica de la página
st.set_page_config(page_title="HellasGo", page_icon="⛴️", layout="wide")

st.title("⛴️ HellasGo: Optimizador de Viaje Inteligente")
st.markdown("**Destinos:** Milos, Halki, Symi, Agistri, Tinos")

# Menú lateral avanzado
st.sidebar.header("Parámetros del Viaje")

origen_seleccionado = st.sidebar.selectbox(
    "✈️ Ciudad de Origen", 
    ["Valencia (VLC)", "Madrid (MAD)", "Ámsterdam (AMS)"]
)
codigo_origen = origen_seleccionado[-4:-1] 

fecha_ida = st.sidebar.date_input(
    "📅 Fecha de Salida",
    value=datetime.date(2027, 5, 2),
    min_value=datetime.date(2027, 4, 20),
    max_value=datetime.date(2027, 5, 20)
)

noches_estancia = st.sidebar.number_input(
    "🌙 Número de noches",
    min_value=1,
    max_value=15,
    value=8,
    step=1
)

fecha_regreso_sugerida = fecha_ida + datetime.timedelta(days=noches_estancia)

fecha_vuelta = st.sidebar.date_input(
    "📅 Fecha de Regreso",
    value=fecha_regreso_sugerida,
    min_value=fecha_ida + datetime.timedelta(days=1),
    max_value=datetime.date(2027, 5, 30)
)

if fecha_vuelta <= fecha_ida:
    st.sidebar.error("⚠️ La fecha de regreso debe ser posterior a la de salida.")
    st.stop()

noches_estancia = (fecha_vuelta - fecha_ida).days

# Filtro por Estilo de Viaje / Vibe
st.sidebar.header("✨ Estilo de Viaje Preferido")
vibe_filtro = st.sidebar.selectbox(
    "Filtrar por Vibe",
    ["Todos", "Playas paradisíacas", "Tranquilidad", "Romántico/Relajado", "Gastronomía", "Pueblos tradicionales"]
)

# Simulador de Presupuesto Máximo
st.sidebar.header("💰 Restricción Presupuestaria")
presupuesto_maximo = st.sidebar.number_input(
    "Presupuesto Máximo Total (€)",
    min_value=300,
    max_value=3000,
    value=1200,
    step=50
)

st.sidebar.header("¿Qué es más importante?")
peso_precio = st.sidebar.slider("Ahorrar dinero", 0.0, 1.0, 0.5)
peso_tiempo = st.sidebar.slider("Llegar rápido", 0.0, 1.0, 0.3)
peso_calidad = st.sidebar.slider("Calidad del alojamiento", 0.0, 1.0, 0.2)

st.sidebar.header("🏨 Explorador de Alojamientos")
isla_seleccionada_hotel = st.sidebar.selectbox(
    "Seleccionar Isla para Hoteles",
    ["Agistri", "Milos", "Tinos", "Symi", "Halki"]
)

# Carga de datos
df_rutas = get_route_data(codigo_origen, str(fecha_ida), str(fecha_vuelta))
df_alojamiento_resumen, df_hoteles_isla = get_accommodation_data(noches_estancia, isla_seleccionada_hotel)
df_ferrys = get_ferry_schedule_data()
df_metadata = get_island_metadata()

# Unir datos maestros
df_master = pd.merge(df_rutas, df_alojamiento_resumen, on="Isla")
df_master = pd.merge(df_master, df_ferrys[["Isla", "Ferry (€)"]], on="Isla", suffixes=("_old", ""))
if "Ferry (€)_old" in df_master.columns:
    df_master = df_master.drop(columns=["Ferry (€)_old"])

df_master = pd.merge(df_master, df_metadata, on="Isla")

# Cálculo del coste total incluyendo gasto diario estimado de vida y ocio
df_master["Gasto Diario Total (€)"] = df_master["Gasto Diario Est. (€/día)"] * noches_estancia
df_master["Costo Total (€)"] = df_master["Vuelo (€)"] + df_master["Ferry (€)"] + df_master["Alojamiento Total (€)"] + df_master["Gasto Diario Total (€)"]

# Bonificación por Vibe
if vibe_filtro != "Todos":
    df_master["Puntuacion_Vibe"] = df_master["Etiquetas"].apply(lambda tags: 15 if vibe_filtro in tags else 0)
else:
    df_master["Puntuacion_Vibe"] = 0

max_precio = df_master["Costo Total (€)"].max()
max_tiempo = df_master["Tiempo Total (h)"].max()

df_master["Puntuación"] = (
    ((1 - (df_master["Costo Total (€)"] / max_precio)) * peso_precio * 100) +
    ((1 - (df_master["Tiempo Total (h)"] / max_tiempo)) * peso_tiempo * 100) +
    ((df_master["Calidad (1-10)"] / 10) * peso_calidad * 100) +
    df_master["Puntuacion_Vibe"]
)
df_master = df_master.sort_values(by="Puntuación", ascending=False).round(1)

# Alerta de presupuesto
df_master["Cumple Presupuesto"] = df_master["Costo Total (€)"] <= presupuesto_maximo

# Pestañas de la aplicación
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Optimizador y Clasificación", 
    "📊 Gráfico de Costes", 
    "🍔 Vida Diaria y Estilo",
    "🏨 Alojamientos (10 por Isla)", 
    "⚓ Horarios y Ferris"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Clasificación de Destinos (Multicriterio)")
        st.markdown(f"Filtro de presupuesto activo: **Máximo €{presupuesto_maximo}**")
        
        df_display = df_master[["Isla", "Tiempo Total (h)", "Costo Total (€)", "Cumple Presupuesto", "Puntuación"]].copy()
        df_display["Asequible"] = df_display["Cumple Presupuesto"].apply(lambda x: "✅ Sí" if x else "❌ Excede")
        st.dataframe(df_display[["Isla", "Tiempo Total (h)", "Costo Total (€)", "Asequible", "Puntuación"]], hide_index=True)
        
    with col2:
        ganador = df_master.iloc[0]
        st.success("🏆 Mejor Opción Actual")
        st.metric(label=f"Destino: {ganador['Isla']}", value=f"{ganador['Puntuación']} pts")
        st.write(f"**Tiempo de viaje:** {ganador['Tiempo Total (h)']} hrs")
        st.write(f"**Gasto total estimado:** €{ganador['Costo Total (€)']}")
        if ganador["Cumple Presupuesto"]:
            st.markdown("✅ **¡Entra dentro de tu presupuesto!**")
        else:
            st.markdown("⚠️ **Supera ligeramente el presupuesto introducido.**")
        st.info(f"📅 Del {fecha_ida} al {fecha_vuelta} ({noches_estancia} noches)")

        # Botón de Exportación a Markdown / Informe descargable (CORREGIDO)
        informe_md = f"""# Informe de Viaje - HellasGo
## Destino Recomendado: {ganador['Isla']}
- **Origen:** {origen_seleccionado}
- **Fechas:** Del {fecha_ida} al {fecha_vuelta} ({noches_estancia} noches)
- **Coste Total Estimado:** €{ganador['Costo Total (€)']}
- Vuelos: €{ganador['Vuelo (€)']}
- Ferris: €{ganador['Ferry (€)']}
- Alojamiento (Medio): €{ganador['Alojamiento Total (€)']}
- Gastos Diarios / Ocio: €{ganador['Gasto Diario Total (€)']}
- **Estilo / Vibe:** {ganador['Vibe Principal']}
"""
        st.download_button(
            label="📥 Descargar Plan de Viaje (Markdown)",
            data=informe_md,
            file_name=f"HellasGo_Plan_{ganador['Isla']}.md",
            mime="text/markdown"
        )

with tab2:
    st.subheader("📊 Desglose Visual de Costes por Destino (Incluyendo Ocio)")
    df_chart = df_master.set_index("Isla")[["Vuelo (€)", "Ferry (€)", "Alojamiento Total (€)", "Gasto Diario Total (€)"]]
    st.bar_chart(df_chart)

with tab3:
    st.subheader("🍔 Coste de Vida Diario y Estilo de cada Isla")
    st.markdown("Estimación del coste diario en comidas, tabernas y transporte local, junto con el ambiente principal de cada destino.")
    st.dataframe(df_metadata[["Isla", "Vibe Principal", "Gasto Diario Est. (€/día)"]], hide_index=True)

with tab4:
    st.subheader(f"🏨 Opciones en {isla_seleccionada_hotel} (Hoteles y Airbnbs)")
    st.markdown(f"Listado con las **10 opciones verificadas** para tu estancia de **{noches_estancia} noches**:")
    
    st.dataframe(df_hoteles_isla[["Nombre", "Tipo", "Precio Noche (€)", "Alojamiento Total (€)", "Calidad (1-10)"]], hide_index=True)
    
    st.markdown("---")
    nombres_alojamientos = df_hoteles_isla["Nombre"].tolist()
    alojamiento_elegido = st.selectbox("📌 Selecciona tu favorito para calcular detalles:", nombres_alojamientos)
    
    detalles_aloj = df_hoteles_isla[df_hoteles_isla["Nombre"] == alojamiento_elegido].iloc[0]
    st.info(f"Has seleccionado **{detalles_aloj['Nombre']}** ({detalles_aloj['Tipo']}). Coste total para {noches_estancia} noches: **€{detalles_aloj['Alojamiento Total (€)']}** (Calidad: {detalles_aloj['Calidad (1-10)']}/10)")

with tab5:
    st.subheader("⚓ Información y Horarios de Conexión en Ferry")
    st.dataframe(df_ferrys, hide_index=True)
