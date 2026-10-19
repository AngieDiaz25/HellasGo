import streamlit as st
import pandas as pd
import requests

try:
    RAPIDAPI_KEY = st.secrets["api_keys"]["rapidapi"]
except KeyError:
    RAPIDAPI_KEY = "NO_CONFIGURADA"

@st.cache_data(ttl=3600)
def get_route_data(origen="VLC", fecha_ida="2027-05-02", fecha_vuelta="2027-05-10"):
    """Busca vuelos de ida y vuelta desde el origen seleccionado hacia Atenas en las fechas indicadas."""
    data = [
        {"Isla": "Agistri", "Hub": "Atenas", "Vuelo (€)": 150, "Ferry (€)": 30, "Tiempo Total (h)": 6.5},
        {"Isla": "Milos", "Hub": "Atenas", "Vuelo (€)": 150, "Ferry (€)": 75, "Tiempo Total (h)": 8.0},
        {"Isla": "Tinos", "Hub": "Atenas", "Vuelo (€)": 150, "Ferry (€)": 50, "Tiempo Total (h)": 7.5},
        {"Isla": "Symi", "Hub": "Rodas", "Vuelo (€)": 220, "Ferry (€)": 25, "Tiempo Total (h)": 9.0},
        {"Isla": "Halki", "Hub": "Rodas", "Vuelo (€)": 220, "Ferry (€)": 20, "Tiempo Total (h)": 10.5},
    ]
    df = pd.DataFrame(data)

    if RAPIDAPI_KEY == "NO_CONFIGURADA":
        return df

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"
    querystring = {
        "originSkyId": origen, 
        "destinationSkyId": "ATH", 
        "date": fecha_ida, 
        "returnDate": fecha_vuelta, 
        "adults": "2", 
        "currency": "EUR"
    }
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            vuelos = response.json()
            itinerarios = vuelos.get("data", {}).get("itineraries", [])
            if itinerarios:
                precio_real = itinerarios[0]["price"]["raw"]
                df.loc[df["Hub"] == "Atenas", "Vuelo (€)"] = precio_real
    except Exception:
        pass

    return df

@st.cache_data(ttl=3600)
def get_island_metadata():
    """Devuelve información complementaria: coste diario estimado y etiquetas de estilo (vibe)."""
    data = [
        {
            "Isla": "Agistri", 
            "Gasto Diario Est. (€/día)": 55, 
            "Vibe Principal": "Tranquilidad y Ciclismo",
            "Etiquetas": ["Playas vírgenes", "Tranquilidad", "Cerca de Atenas"]
        },
        {
            "Isla": "Milos", 
            "Gasto Diario Est. (€/día)": 80, 
            "Vibe Principal": "Playas de Ensueño y Geología",
            "Etiquetas": ["Playas paradisíacas", "Senderismo", "Fotografía"]
        },
        {
            "Isla": "Tinos", 
            "Gasto Diario Est. (€/día)": 65, 
            "Vibe Principal": "Gastronomía y Pueblos de Mármol",
            "Etiquetas": ["Gastronomía", "Pueblos tradicionales", "Arte"]
        },
        {
            "Isla": "Symi", 
            "Gasto Diario Est. (€/día)": 75, 
            "Vibe Principal": "Arquitectura Neoclásica y Romántico",
            "Etiquetas": ["Romántico/Relajado", "Pueblos tradicionales", "Fotografía"]
        },
        {
            "Isla": "Halki", 
            "Gasto Diario Est. (€/día)": 50, 
            "Vibe Principal": "Desconexión Total y Paz",
            "Etiquetas": ["Tranquilidad", "Playas vírgenes", "Romántico/Relajado"]
        }
    ]
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def get_accommodation_data(noches=8, destino="Agistri"):
    """Devuelve las 10 opciones variadas por isla y el resumen medio global."""
    catalogo_alojamientos = [
        # --- AGISTRI (10 opciones) ---
        {"Isla": "Agistri", "Nombre": "Aegistri Hotel (Boutique)", "Tipo": "Hotel", "Precio Noche (€)": 75, "Calidad (1-10)": 8.2},
        {"Isla": "Agistri", "Nombre": "Skliri Stone Villa", "Tipo": "Airbnb", "Precio Noche (€)": 90, "Calidad (1-10)": 8.8},
        {"Isla": "Agistri", "Nombre": "DrogkOU Studios", "Tipo": "Airbnb", "Precio Noche (€)": 60, "Calidad (1-10)": 7.9},
        {"Isla": "Agistri", "Nombre": "Megalochori Pine Suites", "Tipo": "Hotel", "Precio Noche (€)": 105, "Calidad (1-10)": 9.0},
        {"Isla": "Agistri", "Nombre": "Checkpoint Seaview Loft", "Tipo": "Airbnb", "Precio Noche (€)": 70, "Calidad (1-10)": 8.3},
        {"Isla": "Agistri", "Nombre": "Scala Beachfront Room", "Tipo": "Airbnb", "Precio Noche (€)": 65, "Calidad (1-10)": 8.0},
        {"Isla": "Agistri", "Nombre": "Drenia Oasis Bungalows", "Tipo": "Hotel", "Precio Noche (€)": 120, "Calidad (1-10)": 9.2},
        {"Isla": "Agistri", "Nombre": "Aponissos Sunset Retreat", "Tipo": "Airbnb", "Precio Noche (€)": 95, "Calidad (1-10)": 8.9},
        {"Isla": "Agistri", "Nombre": "Limenaria Traditional House", "Tipo": "Airbnb", "Precio Noche (€)": 55, "Calidad (1-10)": 7.7},
        {"Isla": "Agistri", "Nombre": "Agistri Blue Hotel", "Tipo": "Hotel", "Precio Noche (€)": 85, "Calidad (1-10)": 8.4},
        
        # --- MILOS (10 opciones) ---
        {"Isla": "Milos", "Nombre": "Milos Cove Luxury Suites", "Tipo": "Hotel", "Precio Noche (€)": 160, "Calidad (1-10)": 9.6},
        {"Isla": "Milos", "Nombre": "Pollonia Sunset Cave House", "Tipo": "Airbnb", "Precio Noche (€)": 110, "Calidad (1-10)": 9.2},
        {"Isla": "Milos", "Nombre": "Captain's Quarter Plaka", "Tipo": "Airbnb", "Precio Noche (€)": 85, "Calidad (1-10)": 8.7},
        {"Isla": "Milos", "Nombre": "Porto Millos Hotel", "Tipo": "Hotel", "Precio Noche (€)": 95, "Calidad (1-10)": 8.5},
        {"Isla": "Milos", "Nombre": "Sarakiniko White Cliff Villa", "Tipo": "Airbnb", "Precio Noche (€)": 130, "Calidad (1-10)": 9.4},
        {"Isla": "Milos", "Nombre": "Adamas Harbor Cozy Studio", "Tipo": "Airbnb", "Precio Noche (€)": 70, "Calidad (1-10)": 8.1},
        {"Isla": "Milos", "Nombre": "Skinopi Lodge Minimal", "Tipo": "Hotel", "Precio Noche (€)": 180, "Calidad (1-10)": 9.8},
        {"Isla": "Milos", "Nombre": "Klima Fishing Village House", "Tipo": "Airbnb", "Precio Noche (€)": 125, "Calidad (1-10)": 9.5},
        {"Isla": "Milos", "Nombre": "Paliochori Beach Resort", "Tipo": "Hotel", "Precio Noche (€)": 140, "Calidad (1-10)": 9.1},
        {"Isla": "Milos", "Nombre": "Triovasalos Cycladic Home", "Tipo": "Airbnb", "Precio Noche (€)": 75, "Calidad (1-10)": 8.3},

        # --- TINOS (10 opciones) ---
        {"Isla": "Tinos", "Nombre": "Tinos Beach Resort & Spa", "Tipo": "Hotel", "Precio Noche (€)": 115, "Calidad (1-10)": 9.0},
        {"Isla": "Tinos", "Nombre": "Volax Traditional Cycladic Home", "Tipo": "Airbnb", "Precio Noche (€)": 80, "Calidad (1-10)": 9.0},
        {"Isla": "Tinos", "Nombre": "Panormos Sea View Apartment", "Tipo": "Airbnb", "Precio Noche (€)": 70, "Calidad (1-10)": 8.4},
        {"Isla": "Tinos", "Nombre": "Mr & Mrs White Tinos", "Tipo": "Hotel", "Precio Noche (€)": 135, "Calidad (1-10)": 9.3},
        {"Isla": "Tinos", "Nombre": "Kardiani Cliff Stone House", "Tipo": "Airbnb", "Precio Noche (€)": 95, "Calidad (1-10)": 8.9},
        {"Isla": "Tinos", "Nombre": "Agios Fokas Budget Studio", "Tipo": "Airbnb", "Precio Noche (€)": 60, "Calidad (1-10)": 7.8},
        {"Isla": "Tinos", "Nombre": "Xala Boutique Hotel Tinos", "Tipo": "Hotel", "Precio Noche (€)": 150, "Calidad (1-10)": 9.5},
        {"Isla": "Tinos", "Nombre": "Ysternia Sunset Balcony", "Tipo": "Airbnb", "Precio Noche (€)": 90, "Calidad (1-10)": 8.8},
        {"Isla": "Tinos", "Nombre": "Tinos Port Suites", "Tipo": "Hotel", "Precio Noche (€)": 105, "Calidad (1-10)": 8.6},
        {"Isla": "Tinos", "Nombre": "Pyrgos Marble Village Loft", "Tipo": "Airbnb", "Precio Noche (€)": 72, "Calidad (1-10)": 8.5},

        # --- SYMI (10 opciones) ---
        {"Isla": "Symi", "Nombre": "Symi Residence & Spa", "Tipo": "Hotel", "Precio Noche (€)": 130, "Calidad (1-10)": 9.2},
        {"Isla": "Symi", "Nombre": "Neo Classical Harbor House", "Tipo": "Airbnb", "Precio Noche (€)": 95, "Calidad (1-10)": 9.3},
        {"Isla": "Symi", "Nombre": "Yanos Sunset Studio", "Tipo": "Airbnb", "Precio Noche (€)": 75, "Calidad (1-10)": 8.6},
        {"Isla": "Symi", "Nombre": "Althea Boutique Hotel", "Tipo": "Hotel", "Precio Noche (€)": 110, "Calidad (1-10)": 8.8},
        {"Isla": "Symi", "Nombre": "Nos Beach Traditional Loft", "Tipo": "Airbnb", "Precio Noche (€)": 88, "Calidad (1-10)": 8.9},
        {"Isla": "Symi", "Nombre": "Chorio Panoramic View House", "Tipo": "Airbnb", "Precio Noche (€)": 82, "Calidad (1-10)": 8.7},
        {"Isla": "Symi", "Nombre": "Ianos Hotel Symi", "Tipo": "Hotel", "Precio Noche (€)": 140, "Calidad (1-10)": 9.4},
        {"Isla": "Symi", "Nombre": "Pedi Bay Sea House", "Tipo": "Airbnb", "Precio Noche (€)": 100, "Calidad (1-10)": 9.0},
        {"Isla": "Symi", "Nombre": "Nimborio Quiet Retreat", "Tipo": "Airbnb", "Precio Noche (€)": 70, "Calidad (1-10)": 8.4},
        {"Isla": "Symi", "Nombre": "Harbor View Suites Symi", "Tipo": "Hotel", "Precio Noche (€)": 125, "Calidad (1-10)": 9.1},

        # --- HALKI (10 opciones) ---
        {"Isla": "Halki", "Nombre": "Halki Port Apartments", "Tipo": "Hotel", "Precio Noche (€)": 80, "Calidad (1-10)": 8.6},
        {"Isla": "Halki", "Nombre": "Emborios Captain House", "Tipo": "Airbnb", "Precio Noche (€)": 85, "Calidad (1-10)": 8.9},
        {"Isla": "Halki", "Nombre": "Pefkos Cozy Retreat", "Tipo": "Airbnb", "Precio Noche (€)": 65, "Calidad (1-10)": 8.2},
        {"Isla": "Halki", "Nombre": "Foutalis Hotel & Studios", "Tipo": "Hotel", "Precio Noche (€)": 90, "Calidad (1-10)": 8.7},
        {"Isla": "Halki", "Nombre": "Nick's Traditional Sea House", "Tipo": "Airbnb", "Precio Noche (€)": 78, "Calidad (1-10)": 8.5},
        {"Isla": "Halki", "Nombre": "Nimborio Sunset Balcony", "Tipo": "Airbnb", "Precio Noche (€)": 72, "Calidad (1-10)": 8.3},
        {"Isla": "Halki", "Nombre": "Asti Hotel Halki", "Tipo": "Hotel", "Precio Noche (€)": 100, "Calidad (1-10)": 9.0},
        {"Isla": "Halki", "Nombre": "Pontimus Cliff Villa", "Tipo": "Airbnb", "Precio Noche (€)": 110, "Calidad (1-10)": 9.2},
        {"Isla": "Halki", "Nombre": "Chorio Old Town Stone Cottage", "Tipo": "Airbnb", "Precio Noche (€)": 60, "Calidad (1-10)": 7.9},
        {"Isla": "Halki", "Nombre": "Halki Palace Studios", "Tipo": "Hotel", "Precio Noche (€)": 95, "Calidad (1-10)": 8.8}
    ]

    df_all = pd.DataFrame(catalogo_alojamientos)
    df_all["Alojamiento Total (€)"] = df_all["Precio Noche (€)"] * noches

    resumen_data = []
    for isla in df_all["Isla"].unique():
        subset = df_all[df_all["Isla"] == isla]
        resumen_data.append({
            "Isla": isla,
            "Alojamiento Total (€)": subset["Alojamiento Total (€)"].mean(),
            "Calidad (1-10)": subset["Calidad (1-10)"].mean()
        })
    df_resumen = pd.DataFrame(resumen_data)
    df_hotels_isla = df_all[df_all["Isla"] == destino]

    return df_resumen, df_hotels_isla

@st.cache_data(ttl=3600)
def get_ferry_schedule_data():
    """Devuelve los horarios y costes de los ferris."""
    data = [
        {"Isla": "Agistri", "Puerto Salida": "El Pireo", "Duración Ferry": "1h 15m", "Frecuencia": "Diaria (Cada 2h)", "Ferry (€)": 30},
        {"Isla": "Milos", "Puerto Salida": "El Pireo", "Duración Ferry": "3h 30m (Rápido)", "Frecuencia": "2 al día", "Ferry (€)": 75},
        {"Isla": "Tinos", "Puerto Salida": "El Pireo", "Duración Ferry": "4h 00m", "Frecuencia": "3 al día", "Ferry (€)": 50},
        {"Isla": "Symi", "Puerto Salida": "Rodas", "Duración Ferry": "1h 00m", "Frecuencia": "Diaria", "Ferry (€)": 25},
        {"Isla": "Halki", "Puerto Salida": "Rodas", "Duración Ferry": "1h 30m", "Frecuencia": "4 por semana", "Ferry (€)": 20},
    ]
    return pd.DataFrame(data)
