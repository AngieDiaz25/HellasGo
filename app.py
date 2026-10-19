import streamlit as st
import pandas as pd
import datetime
from modules.data_loader import get_route_data, get_accommodation_data, get_ferry_schedule_data, get_island_metadata

st.set_page_config(page_title="HellasGo", page_icon="⛴️", layout="wide")

st.title("⛴️ HellasGo: Smart Trip Optimizer")
st.markdown("**Destinations:** Milos, Halki, Symi, Agistri, Tinos")

st.sidebar.header("Trip Parameters")

origin_selected = st.sidebar.selectbox(
    "✈️ Origin City", 
    ["Valencia (VLC)", "Madrid (MAD)", "Amsterdam (AMS)"]
)
origin_code = origin_selected[-4:-1] 

departure_date = st.sidebar.date_input(
    "📅 Departure Date",
    value=datetime.date(2027, 5, 2),
    min_value=datetime.date(2027, 4, 20),
    max_value=datetime.date(2027, 5, 20)
)

stay_nights = st.sidebar.number_input(
    "🌙 Number of Nights",
    min_value=1,
    max_value=15,
    value=8,
    step=1
)

suggested_return_date = departure_date + datetime.timedelta(days=stay_nights)

return_date = st.sidebar.date_input(
    "📅 Return Date",
    value=suggested_return_date,
    min_value=departure_date + datetime.timedelta(days=1),
    max_value=datetime.date(2027, 5, 30)
)

if return_date <= departure_date:
    st.sidebar.error("⚠️ The return date must be after the departure date.")
    st.stop()

stay_nights = (return_date - departure_date).days

st.sidebar.header("✨ Preferred Travel Vibe")
vibe_filter = st.sidebar.selectbox(
    "Filter by Vibe",
    ["All", "Paradise Beaches", "Quiet", "Romantic/Relaxed", "Gastronomy", "Traditional Villages"]
)

st.sidebar.header("💰 Budget Restriction")
max_budget = st.sidebar.number_input(
    "Maximum Total Budget (€)",
    min_value=300,
    max_value=3000,
    value=1200,
    step=50
)

st.sidebar.header("What matters most to you?")
weight_price = st.sidebar.slider("Save money", 0.0, 1.0, 0.5)
weight_time = st.sidebar.slider("Arrive quickly", 0.0, 1.0, 0.3)
weight_quality = st.sidebar.slider("Accommodation quality", 0.0, 1.0, 0.2)

st.sidebar.header("🏨 Accommodation Explorer")
island_selected_hotel = st.sidebar.selectbox(
    "Select Island for Hotels",
    ["Agistri", "Milos", "Tinos", "Symi", "Halki"]
)

df_routes = get_route_data(origin_code, str(departure_date), str(return_date))
df_accommodation_summary, df_hotels_island = get_accommodation_data(stay_nights, island_selected_hotel)
df_ferries = get_ferry_schedule_data()
df_metadata = get_island_metadata()

df_master = pd.merge(df_routes, df_accommodation_summary, on="Island")
df_master = pd.merge(df_master, df_ferries[["Island", "Ferry (€)"]], on="Island", suffixes=("_old", ""))
if "Ferry (€)_old" in df_master.columns:
    df_master = df_master.drop(columns=["Ferry (€)_old"])

df_master = pd.merge(df_master, df_metadata, on="Island")

df_master["Total Daily Cost (€)"] = df_master["Est. Daily Cost (€/day)"] * stay_nights
df_master["Total Cost (€)"] = df_master["Flight (€)"] + df_master["Ferry (€)"] + df_master["Total Accommodation (€)"] + df_master["Total Daily Cost (€)"]

if vibe_filter != "All":
    df_master["Vibe_Score"] = df_master["Tags"].apply(lambda tags: 15 if vibe_filter in tags else 0)
else:
    df_master["Vibe_Score"] = 0

max_price = df_master["Total Cost (€)"].max()
max_time = df_master["Total Time (h)"].max()

df_master["Score"] = (
    ((1 - (df_master["Total Cost (€)"] / max_price)) * weight_price * 100) +
    ((1 - (df_master["Total Time (h)"] / max_time)) * weight_time * 100) +
    ((df_master["Quality (1-10)"] / 10) * weight_quality * 100) +
    df_master["Vibe_Score"]
)
df_master = df_master.sort_values(by="Score", ascending=False).round(1)

df_master["Meets Budget"] = df_master["Total Cost (€)"] <= max_budget

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏆 Optimizer & Ranking", 
    "📊 Cost Breakdown Chart", 
    "🍔 Daily Life & Vibe",
    "🏨 Accommodations (10 per Island)", 
    "⚓ Ferries & Schedules"
])

with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Destination Ranking (Multi-criteria)")
        st.markdown(f"Active budget filter: **Maximum €{max_budget}**")

        df_display = df_master[["Island", "Total Time (h)", "Total Cost (€)", "Meets Budget", "Score"]].copy()
        df_display["Affordable"] = df_display["Meets Budget"].apply(lambda x: "✅ Yes" if x else "❌ Exceeds")
        st.dataframe(df_display[["Island", "Total Time (h)", "Total Cost (€)", "Affordable", "Score"]], hide_index=True)

    with col2:
        winner = df_master.iloc[0]
        st.success("🏆 Best Current Option")
        st.metric(label=f"Destination: {winner['Island']}", value=f"{winner['Score']} pts")
        st.write(f"**Travel time:** {winner['Total Time (h)']} hrs")
        st.write(f"**Estimated total spend:** €{winner['Total Cost (€)']}")
        if winner["Meets Budget"]:
            st.markdown("✅ **Fits within your budget!**")
        else:
            st.markdown("⚠️ **Slightly exceeds the entered budget.**")
        st.info(f"📅 From {departure_date} to {return_date} ({stay_nights} nights)")

        report_md = f"""# Travel Report - HellasGo
## Recommended Destination: {winner['Island']}
- **Origin:** {origin_selected}
- **Dates:** From {departure_date} to {return_date} ({stay_nights} nights)
- **Estimated Total Cost:** €{winner['Total Cost (€)']}
  - Flights: €{winner['Flight (€)']}
  - Ferries: €{winner['Ferry (€)']}
  - Accommodation (Average): €{winner['Total Accommodation (€)']}
  - Daily Expenses / Leisure: €{winner['Total Daily Cost (€)']}
- **Style / Vibe:** {winner['Main Vibe']}
"""
        st.download_button(
            label="📥 Download Travel Plan (Markdown)",
            data=report_md,
            file_name=f"HellasGo_Plan_{winner['Island']}.md",
            mime="text/markdown"
        )

with tab2:
    st.subheader("📊 Visual Cost Breakdown by Destination (Including Leisure)")
    df_chart = df_master.set_index("Island")[["Flight (€)", "Ferry (€)", "Total Accommodation (€)", "Total Daily Cost (€)"]]
    st.bar_chart(df_chart)

with tab3:
    st.subheader("🍔 Daily Living Cost & Vibe per Island")
    st.markdown("Estimated daily costs for meals, tavernas, and local transport, along with the core atmosphere of each destination.")
    st.dataframe(df_metadata[["Island", "Main Vibe", "Est. Daily Cost (€/day)"]], hide_index=True)

with tab4:
    st.subheader(f"🏨 Options in {island_selected_hotel} (Hotels and Airbnbs)")
    st.markdown(f"List of **10 verified options** for your stay of **{stay_nights} nights**:")

    st.dataframe(df_hotels_island[["Name", "Type", "Price Night (€)", "Total Accommodation (€)", "Quality (1-10)"]], hide_index=True)

    st.markdown("---")
    accommodation_names = df_hotels_island["Name"].tolist()
    chosen_accommodation = st.selectbox("📌 Select your favorite to calculate details:", accommodation_names)

    details_accommod = df_hotels_island[df_hotels_island["Name"] == chosen_accommodation].iloc[0]
    st.info(f"You selected **{details_accommod['Name']}** ({details_accommod['Type']}). Total cost for {stay_nights} nights: **€{details_accommod['Total Accommodation (€)']}** (Quality: {details_accommod['Quality (1-10)']}/10)")

with tab5:
    st.subheader("⚓ Ferry Connection Information & Schedules")
    st.dataframe(df_ferries, hide_index=True)
