import streamlit as st
import pandas as pd
import requests

try:
    RAPIDAPI_KEY = st.secrets["api_keys"]["rapidapi"]
except KeyError:
    RAPIDAPI_KEY = "NOT_CONFIGURED"

@st.cache_data(ttl=3600)
def get_route_data(origin="VLC", departure_date="2027-05-02", return_date="2027-05-10"):
    data = [
        {"Island": "Agistri", "Hub": "Athens", "Flight (€)": 150, "Ferry (€)": 30, "Total Time (h)": 6.5},
        {"Island": "Milos", "Hub": "Athens", "Flight (€)": 150, "Ferry (€)": 75, "Total Time (h)": 8.0},
        {"Island": "Tinos", "Hub": "Athens", "Flight (€)": 150, "Ferry (€)": 50, "Total Time (h)": 7.5},
        {"Island": "Symi", "Hub": "Rhodes", "Flight (€)": 220, "Ferry (€)": 25, "Total Time (h)": 9.0},
        {"Island": "Halki", "Hub": "Rhodes", "Flight (€)": 220, "Ferry (€)": 20, "Total Time (h)": 10.5},
    ]
    df = pd.DataFrame(data)

    if RAPIDAPI_KEY == "NOT_CONFIGURED":
        return df

    url = "https://sky-scrapper.p.rapidapi.com/api/v1/flights/searchFlights"
    querystring = {
        "originSkyId": origin, 
        "destinationSkyId": "ATH", 
        "date": departure_date, 
        "returnDate": return_date, 
        "adults": "2", 
        "currency": "EUR"
    }
    headers = {"x-rapidapi-key": RAPIDAPI_KEY, "x-rapidapi-host": "sky-scrapper.p.rapidapi.com"}

    try:
        response = requests.get(url, headers=headers, params=querystring)
        if response.status_code == 200:
            flights = response.json()
            itineraries = flights.get("data", {}).get("itineraries", [])
            if itineraries:
                real_price = itineraries[0]["price"]["raw"]
                df.loc[df["Hub"] == "Athens", "Flight (€)"] = real_price
    except Exception:
        pass

    return df

@st.cache_data(ttl=3600)
def get_island_metadata():
    data = [
        {
            "Island": "Agistri", 
            "Est. Daily Cost (€/day)": 55, 
            "Main Vibe": "Peace and Cycling",
            "Tags": ["Pristine Beaches", "Quiet", "Close to Athens"]
        },
        {
            "Island": "Milos", 
            "Est. Daily Cost (€/day)": 80, 
            "Main Vibe": "Dreamy Beaches and Geology",
            "Tags": ["Paradise Beaches", "Hiking", "Photography"]
        },
        {
            "Island": "Tinos", 
            "Est. Daily Cost (€/day)": 65, 
            "Main Vibe": "Gastronomy and Marble Villages",
            "Tags": ["Gastronomy", "Traditional Villages", "Art"]
        },
        {
            "Island": "Symi", 
            "Est. Daily Cost (€/day)": 75, 
            "Main Vibe": "Neoclassical Architecture & Romantic",
            "Tags": ["Romantic/Relaxed", "Traditional Villages", "Photography"]
        },
        {
            "Island": "Halki", 
            "Est. Daily Cost (€/day)": 50, 
            "Main Vibe": "Total Unplugging and Peace",
            "Tags": ["Quiet", "Pristine Beaches", "Romantic/Relaxed"]
        }
    ]
    return pd.DataFrame(data)

@st.cache_data(ttl=3600)
def get_accommodation_data(nights=8, destination="Agistri"):
    catalog_accommodation = [
        # --- AGISTRI (10 options) ---
        {"Island": "Agistri", "Name": "Aegistri Hotel (Boutique)", "Type": "Hotel", "Price Night (€)": 75, "Quality (1-10)": 8.2},
        {"Island": "Agistri", "Name": "Skliri Stone Villa", "Type": "Airbnb", "Price Night (€)": 90, "Quality (1-10)": 8.8},
        {"Island": "Agistri", "Name": "DrogkOU Studios", "Type": "Airbnb", "Price Night (€)": 60, "Quality (1-10)": 7.9},
        {"Island": "Agistri", "Name": "Megalochori Pine Suites", "Type": "Hotel", "Price Night (€)": 105, "Quality (1-10)": 9.0},
        {"Island": "Agistri", "Name": "Checkpoint Seaview Loft", "Type": "Airbnb", "Price Night (€)": 70, "Quality (1-10)": 8.3},
        {"Island": "Agistri", "Name": "Scala Beachfront Room", "Type": "Airbnb", "Price Night (€)": 65, "Quality (1-10)": 8.0},
        {"Island": "Agistri", "Name": "Drenia Oasis Bungalows", "Type": "Hotel", "Price Night (€)": 120, "Quality (1-10)": 9.2},
        {"Island": "Agistri", "Name": "Aponissos Sunset Retreat", "Type": "Airbnb", "Price Night (€)": 95, "Quality (1-10)": 8.9},
        {"Island": "Agistri", "Name": "Limenaria Traditional House", "Type": "Airbnb", "Price Night (€)": 55, "Quality (1-10)": 7.7},
        {"Island": "Agistri", "Name": "Agistri Blue Hotel", "Type": "Hotel", "Price Night (€)": 85, "Quality (1-10)": 8.4},
        
        # --- MILOS (10 options) ---
        {"Island": "Milos", "Name": "Milos Cove Luxury Suites", "Type": "Hotel", "Price Night (€)": 160, "Quality (1-10)": 9.6},
        {"Island": "Milos", "Name": "Pollonia Sunset Cave House", "Type": "Airbnb", "Price Night (€)": 110, "Quality (1-10)": 9.2},
        {"Island": "Milos", "Name": "Captain's Quarter Plaka", "Type": "Airbnb", "Price Night (€)": 85, "Quality (1-10)": 8.7},
        {"Island": "Milos", "Name": "Porto Millos Hotel", "Type": "Hotel", "Price Night (€)": 95, "Quality (1-10)": 8.5},
        {"Island": "Milos", "Name": "Sarakiniko White Cliff Villa", "Type": "Airbnb", "Price Night (€)": 130, "Quality (1-10)": 9.4},
        {"Island": "Milos", "Name": "Adamas Harbor Cozy Studio", "Type": "Airbnb", "Price Night (€)": 70, "Quality (1-10)": 8.1},
        {"Island": "Milos", "Name": "Skinopi Lodge Minimal", "Type": "Hotel", "Price Night (€)": 180, "Quality (1-10)": 9.8},
        {"Island": "Milos", "Name": "Klima Fishing Village House", "Type": "Airbnb", "Price Night (€)": 125, "Quality (1-10)": 9.5},
        {"Island": "Milos", "Name": "Paliochori Beach Resort", "Type": "Hotel", "Price Night (€)": 140, "Quality (1-10)": 9.1},
        {"Island": "Milos", "Name": "Triovasalos Cycladic Home", "Type": "Airbnb", "Price Night (€)": 75, "Quality (1-10)": 8.3},

        # --- TINOS (10 options) ---
        {"Island": "Tinos", "Name": "Tinos Beach Resort & Spa", "Type": "Hotel", "Price Night (€)": 115, "Quality (1-10)": 9.0},
        {"Island": "Tinos", "Name": "Volax Traditional Cycladic Home", "Type": "Airbnb", "Price Night (€)": 80, "Quality (1-10)": 9.0},
        {"Island": "Tinos", "Name": "Panormos Sea View Apartment", "Type": "Airbnb", "Price Night (€)": 70, "Quality (1-10)": 8.4},
        {"Island": "Tinos", "Name": "Mr & Mrs White Tinos", "Type": "Hotel", "Price Night (€)": 135, "Quality (1-10)": 9.3},
        {"Island": "Tinos", "Name": "Kardiani Cliff Stone House", "Type": "Airbnb", "Price Night (€)": 95, "Quality (1-10)": 8.9},
        {"Island": "Tinos", "Name": "Agios Fokas Budget Studio", "Type": "Airbnb", "Price Night (€)": 60, "Quality (1-10)": 7.8},
        {"Island": "Tinos", "Name": "Xala Boutique Hotel Tinos", "Type": "Hotel", "Price Night (€)": 150, "Quality (1-10)": 9.5},
        {"Island": "Tinos", "Name": "Ysternia Sunset Balcony", "Type": "Airbnb", "Price Night (€)": 90, "Quality (1-10)": 8.8},
        {"Island": "Tinos", "Name": "Tinos Port Suites", "Type": "Hotel", "Price Night (€)": 105, "Quality (1-10)": 8.6},
        {"Island": "Tinos", "Name": "Pyrgos Marble Village Loft", "Type": "Airbnb", "Price Night (€)": 72, "Quality (1-10)": 8.5},

        # --- SYMI (10 options) ---
        {"Island": "Symi", "Name": "Symi Residence & Spa", "Type": "Hotel", "Price Night (€)": 130, "Quality (1-10)": 9.2},
        {"Island": "Symi", "Name": "Neo Classical Harbor House", "Type": "Airbnb", "Price Night (€)": 95, "Quality (1-10)": 9.3},
        {"Island": "Symi", "Name": "Yanos Sunset Studio", "Type": "Airbnb", "Price Night (€)": 75, "Quality (1-10)": 8.6},
        {"Island": "Symi", "Name": "Althea Boutique Hotel", "Type": "Hotel", "Price Night (€)": 110, "Quality (1-10)": 8.8},
        {"Island": "Symi", "Name": "Nos Beach Traditional Loft", "Type": "Airbnb", "Price Night (€)": 88, "Quality (1-10)": 8.9},
        {"Island": "Symi", "Name": "Chorio Panoramic View House", "Type": "Airbnb", "Price Night (€)": 82, "Quality (1-10)": 8.7},
        {"Island": "Symi", "Name": "Ianos Hotel Symi", "Type": "Hotel", "Price Night (€)": 140, "Quality (1-10)": 9.4},
        {"Island": "Symi", "Name": "Pedi Bay Sea House", "Type": "Airbnb", "Price Night (€)": 100, "Quality (1-10)": 9.0},
        {"Island": "Symi", "Name": "Nimborio Quiet Retreat", "Type": "Airbnb", "Price Night (€)": 70, "Quality (1-10)": 8.4},
        {"Island": "Symi", "Name": "Harbor View Suites Symi", "Type": "Hotel", "Price Night (€)": 125, "Quality (1-10)": 9.1},

        # --- HALKI (10 options) ---
        {"Island": "Halki", "Name": "Halki Port Apartments", "Type": "Hotel", "Price Night (€)": 80, "Quality (1-10)": 8.6},
        {"Island": "Halki", "Name": "Emborios Captain House", "Type": "Airbnb", "Price Night (€)": 85, "Quality (1-10)": 8.9},
        {"Island": "Halki", "Name": "Pefkos Cozy Retreat", "Type": "Airbnb", "Price Night (€)": 65, "Quality (1-10)": 8.2},
        {"Island": "Halki", "Name": "Foutalis Hotel & Studios", "Type": "Hotel", "Price Night (€)": 90, "Quality (1-10)": 8.7},
        {"Island": "Halki", "Name": "Nick's Traditional Sea House", "Type": "Airbnb", "Price Night (€)": 78, "Quality (1-10)": 8.5},
        {"Island": "Halki", "Name": "Nimborio Sunset Balcony", "Type": "Airbnb", "Price Night (€)": 72, "Quality (1-10)": 8.3},
        {"Island": "Halki", "Name": "Asti Hotel Halki", "Type": "Hotel", "Price Night (€)": 100, "Quality (1-10)": 9.0},
        {"Island": "Halki", "Name": "Pontimus Cliff Villa", "Type": "Airbnb", "Price Night (€)": 110, "Quality (1-10)": 9.2},
        {"Island": "Halki", "Name": "Chorio Old Town Stone Cottage", "Type": "Airbnb", "Price Night (€)": 60, "Quality (1-10)": 7.9},
        {"Island": "Halki", "Name": "Halki Palace Studios", "Type": "Hotel", "Price Night (€)": 95, "Quality (1-10)": 8.8}
    ]

    df_all = pd.DataFrame(catalog_accommodation)
    df_all["Total Accommodation (€)"] = df_all["Price Night (€)"] * nights

    summary_data = []
    for island in df_all["Island"].unique():
        subset = df_all[df_all["Island"] == island]
        summary_data.append({
            "Island": island,
            "Total Accommodation (€)": subset["Total Accommodation (€)"].mean(),
            "Quality (1-10)": subset["Quality (1-10)"].mean()
        })
    df_resumen = pd.DataFrame(summary_data)
    df_hotels_island = df_all[df_all["Island"] == destination]

    return df_resumen, df_hotels_island

@st.cache_data(ttl=3600)
def get_ferry_schedule_data():
    data = [
        {"Island": "Agistri", "Departure Port": "Piraeus", "Ferry Duration": "1h 15m", "Frequency": "Daily (Every 2h)", "Ferry (€)": 30},
        {"Island": "Milos", "Departure Port": "Piraeus", "Ferry Duration": "3h 30m (Fast)", "Frequency": "2 per day", "Ferry (€)": 75},
        {"Island": "Tinos", "Departure Port": "Piraeus", "Ferry Duration": "4h 00m", "Frequency": "3 per day", "Ferry (€)": 50},
        {"Island": "Symi", "Departure Port": "Rhodes", "Ferry Duration": "1h 00m", "Frequency": "Daily", "Ferry (€)": 25},
        {"Island": "Halki", "Departure Port": "Rhodes", "Ferry Duration": "1h 30m", "Frequency": "4 per week", "Ferry (€)": 20},
    ]
    return pd.DataFrame(data)
