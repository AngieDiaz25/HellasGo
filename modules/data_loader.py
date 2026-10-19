import pandas as pd

def get_route_data():
    """Devuelve un DataFrame con los costos y tiempos de tránsito multimodales."""
    data = [
        {"Isla": "Agistri", "Vuelo (€)": 150, "Ferry (€)": 30, "Tiempo Total (h)": 6.5},
        {"Isla": "Milos", "Vuelo (€)": 150, "Ferry (€)": 75, "Tiempo Total (h)": 8.0},
        {"Isla": "Tinos", "Vuelo (€)": 150, "Ferry (€)": 50, "Tiempo Total (h)": 7.5},
        {"Isla": "Symi", "Vuelo (€)": 220, "Ferry (€)": 25, "Tiempo Total (h)": 9.0},
        {"Isla": "Halki", "Vuelo (€)": 220, "Ferry (€)": 20, "Tiempo Total (h)": 10.5},
    ]
    return pd.DataFrame(data)

def get_accommodation_data():
    """Devuelve un DataFrame con el promedio de alojamientos por isla."""
    data = [
        {"Isla": "Agistri", "Alojamiento Total (€)": 550, "Calidad (1-10)": 8.0},
        {"Isla": "Milos", "Alojamiento Total (€)": 950, "Calidad (1-10)": 9.2},
        {"Isla": "Tinos", "Alojamiento Total (€)": 700, "Calidad (1-10)": 8.8},
        {"Isla": "Symi", "Alojamiento Total (€)": 850, "Calidad (1-10)": 9.0},
        {"Isla": "Halki", "Alojamiento Total (€)": 600, "Calidad (1-10)": 8.5},
    ]
    return pd.DataFrame(data)