import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Excel verisini oku
df = pd.read_excel("harita_datası_temizlendi_tel_eklendi.xlsx", engine="openpyxl")

# Geçerli koordinatları filtrele
valid_df = df[
    df["latitude"].between(40.9, 41.1) &
    df["longitude"].between(28.9, 29.2)
]

# Renk eşlemesi
color_map = {
    "Premium-Potansiyel Musteriler": "red",
    "Orta-Potansiyel Musteriler": "green",
    "Düşük-Potansiyel Musteriler": "orange"
}

# Harita merkezi
map_center = [valid_df["latitude"].mean(), valid_df["longitude"].mean()]
m = folium.Map(location=map_center, zoom_start=13)

# Katmanlar
risk_layers = {}
for group in valid_df["premium_risk_group"].dropna().unique():
    risk_layers[group] = folium.FeatureGroup(name=f"Risk: {group}", show=True)

type_layers = {}
for tipi in valid_df["isletme_tipi"].dropna().unique():
    type_layers[tipi] = folium.FeatureGroup(name=f"Tip: {tipi}", show=False)

# Markerlar
for _, row in valid_df.iterrows():
    group = row["premium_risk_group"]
    tipi = row["isletme_tipi"]

    popup_text = f"""
    <b>Name:</b> {row['name']}<br>
    <b>Mahalle:</b> {row['mahalle']}<br>
    <b>Premium_Skor:</b> {row['score']}<br>
    <b>Puan:</b> {row['overall_rating']}<br>
    <b>Puanlama_Sayısı:</b> {row['user_ratings_total']}<br>
    <b>Adres:</b> {row['address']}<br>
    <b>Telefon:</b> {row['phone']}<br>
    <b>Segment:</b> {group}<br>
    <b>İşletme Tipi:</b> {tipi}<br>
    <a href="https://www.google.com/maps/dir/?api=1&destination={row['latitude']},{row['longitude']}" target="_blank">
    📍 Google Maps ile Yol Tarifi
    </a>
    """

    if group in risk_layers:
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color_map.get(group, "blue"))
        ).add_to(risk_layers[group])

    if tipi in type_layers:
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_text, max_width=300),
            icon=folium.Icon(color=color_map.get(group, "blue"))
        ).add_to(type_layers[tipi])

# Katmanları ekle
for layer in risk_layers.values():
    m.add_child(layer)
for layer in type_layers.values():
    m.add_child(layer)

folium.LayerControl(collapsed=False).add_to(m)

# Streamlit içinde göster
st.title("📍 Premium Müşteri Haritası")
st_folium(m, width=800, height=600)