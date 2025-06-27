import streamlit as st
import pandas as pd
import numpy as np
from streamlit.components.v1 import html
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
import pickle
import io
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import base64
from functions import *
import datetime
import random

st.set_page_config(layout="wide", page_title="Restaurant GHG Emissions Dashboard", page_icon="./media/favicon.ico")

# --- Banner ---
st.image('./media/background_min.jpg', use_column_width=True)

# --- Show Current Date ---
today = datetime.date.today()
st.markdown(f"**Today is:** {today.strftime('%B %d, %Y')}")

# --- Fun Fact ---
facts = [
    "Did you know? Restaurants can reduce up to 30% of their emissions by switching to renewable energy.",
    "Fun fact: Composting food waste can cut methane emissions by half!",
    "Switching to LED lighting can save up to 80% energy.",
    "Deliveries by bicycle produce zero emissions!",
    "Recycling just one ton of paper saves 17 trees."
]
st.info(random.choice(facts))

# --- Brief Introduction ---
st.markdown("""
# Restaurant GHG Emissions Data Entry

Welcome! This dashboard helps small-scale restaurants track their greenhouse gas (GHG) emissions for ISO 14064 audits and sustainability. Please enter your data for the past year. Each section below covers a different type of emission (Scope 1, 2, 3). If you need certification, please contact us after completing your data entry.
""")

# --- Tabs for Scopes and New Features ---
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔥 Scope 1: Direct Emissions",
    "💡 Scope 2: Indirect Emissions from Energy",
    "🛵 Scope 3: Other Indirect Emissions",
    "🌳 Carbon Offset Projects",
    "📜 Certification & Audit Contact"
])

# --- Scope 1 ---
with tab1:
    st.markdown("""
### 🔥 Scope 1: Direct Emissions
**Direct emissions from sources owned or controlled by the restaurant.**
- *LPG/Natural Gas combustion*: Used for cooking dosa, idli, vada, sambar, etc.
- *Diesel or petrol used in generators*: For backup power in case of electricity cuts.
- *Refrigerant leakage*: From refrigerators, cold storage, and air conditioners.
- *Company-owned delivery vehicles*: Two-wheelers or vans owned by the restaurant for food delivery.
""")
    lpg_used = st.number_input("LPG/Natural Gas used for cooking (kg/year) 🥘", min_value=0.0, help="Total LPG or natural gas used for all cooking in a year.")
    generator_fuel = st.number_input("Diesel/Petrol used in generators (liters/year) ⛽", min_value=0.0, help="Total diesel or petrol used for backup generators in a year.")
    refrigerant_leak = st.number_input("Refrigerant leakage (kg/year) ❄️", min_value=0.0, help="Estimated refrigerant lost from fridges, cold storage, ACs in a year.")
    owned_vehicle_fuel = st.number_input("Fuel used by company-owned delivery vehicles (liters/year) 🚗", min_value=0.0, help="Total petrol/diesel used by restaurant-owned delivery vehicles in a year.")

# --- Scope 2 ---
with tab2:
    st.markdown("""
### 💡 Scope 2: Indirect Emissions from Energy
**Indirect emissions from the generation of purchased energy.**
- *Purchased electricity from the grid*: Used for lighting, fans, rice cookers, mixers/grinders, refrigerators, billing systems.
- *Purchased chilled water or steam*: If the restaurant uses central cooling or solar-heated steam systems (rare).
""")
    electricity = st.number_input("Purchased electricity (kWh/year) 💡", min_value=0.0, help="Total electricity used from the grid in a year.")
    chilled_water = st.number_input("Purchased chilled water or steam (kWh or equivalent/year) 💧", min_value=0.0, help="If applicable. Leave as 0 if not used.")

# --- Scope 3 ---
with tab3:
    st.markdown("""
### 🛵 Scope 3: Other Indirect Emissions
**Other indirect emissions from the value chain (upstream and downstream).**
##### Upstream (before the restaurant):
- *Purchased goods and ingredients*: Emissions from growing and transporting rice, lentils, vegetables, milk, ghee, spices, oil.
- *Capital goods*: Emissions from manufacturing kitchen equipment, gas stoves, furniture.
- *Fuel and energy-related activities*: Emissions from fuel extraction, refining, and transport.
- *Upstream transportation*: Transport of ingredients and goods from suppliers to the restaurant.
- *Waste generated in operations*: Food waste, packaging waste, wastewater disposal.
- *Employee commuting*: Staff traveling to and from the restaurant.
- *Business travel*: Travel to vendor meetings, conferences, training, etc.
- *Upstream leased assets*: If the restaurant rents the space, emissions from the building's operation.
##### Downstream (after the restaurant):
- *Delivery services by third parties*: Swiggy/Zomato delivery bikes/scooters.
- *Customer transportation*: Emissions from customers driving/riding to the restaurant.
- *End-of-life treatment of sold products*: Disposal of takeaway containers, plastic bags, cutlery.
- *Franchisee emissions*: If the restaurant operates under a brand or franchise model.
- *Downstream leased assets*: Use of spaces or kitchens managed by others.
""")
    st.markdown("**Enter only the fields relevant to your restaurant. Leave others as 0 or blank.**")
    rice_kg = st.number_input("Rice purchased (kg/year) 🍚", min_value=0.0, help="Total rice purchased in a year.")
    lentils_kg = st.number_input("Lentils purchased (kg/year) 🥣", min_value=0.0)
    vegetables_kg = st.number_input("Vegetables purchased (kg/year) 🥦", min_value=0.0)
    milk_liters = st.number_input("Milk purchased (liters/year) 🥛", min_value=0.0)
    ghee_kg = st.number_input("Ghee purchased (kg/year) 🧈", min_value=0.0)
    spices_kg = st.number_input("Spices purchased (kg/year) 🌶️", min_value=0.0)
    oil_liters = st.number_input("Cooking oil purchased (liters/year) 🛢️", min_value=0.0)
    capital_goods = st.text_input("Major capital goods purchased this year (describe, optional) 🏭")
    upstream_transport_km = st.number_input("Upstream transport (total km/year) 🚚", min_value=0.0, help="Estimated total km for ingredient delivery to your restaurant.")
    food_waste_kg = st.number_input("Food waste generated (kg/year) 🍲", min_value=0.0)
    packaging_waste_kg = st.number_input("Packaging waste generated (kg/year) 📦", min_value=0.0)
    staff_count = st.number_input("Number of staff 👨‍🍳", min_value=0, step=1)
    avg_commute_km = st.number_input("Average staff commute distance (km, one way) 🚌", min_value=0.0)
    business_travel_km = st.number_input("Business travel (km/year) ✈️", min_value=0.0)
    third_party_deliveries = st.number_input("Number of third-party delivery orders/year 🛵", min_value=0, step=1)
    main_delivery_partner = st.text_input("Main delivery partner (e.g., Swiggy, Zomato, etc.) 🛵")
    customer_visits = st.number_input("Estimated customer visits/year 👥", min_value=0, step=1)
    takeaway_containers = st.number_input("Takeaway containers used/year 🥡", min_value=0, step=1)
    franchisee = st.checkbox("Is your restaurant part of a franchise or brand? 🏢")
    leased_space = st.checkbox("Do you operate in a leased space or kitchen? 🏠")

# --- Carbon Offset Projects ---
with tab4:
    st.markdown("""
## 🌳 Carbon Offset Projects
Support these projects to offset your restaurant's carbon emissions and contribute to sustainability:
""")
    projects = [
        {
            "name": "Reforestation Initiative",
            "desc": "Plant trees to absorb CO2 and restore local ecosystems.",
            "link": "https://www.trees.org/"
        },
        {
            "name": "Renewable Energy Fund",
            "desc": "Support solar and wind projects that replace fossil fuels.",
            "link": "https://www.goldstandard.org/"
        },
        {
            "name": "Clean Cooking Solutions",
            "desc": "Provide clean cookstoves to reduce emissions in communities.",
            "link": "https://www.cleancookingalliance.org/"
        }
    ]
    for p in projects:
        st.markdown(f"**{p['name']}**  ")
        st.markdown(f"{p['desc']}  ")
        st.markdown(f"[Learn more & support]({p['link']})  ")
        st.markdown("---")
    st.markdown("### Express Interest or Pledge Support")
    name = st.text_input("Your Name", key="offset_name")
    email = st.text_input("Your Email", key="offset_email")
    project_choice = st.selectbox("Which project are you interested in?", [p['name'] for p in projects], key="offset_project")
    pledge = st.text_area("How would you like to support or collaborate?")
    if st.button("Submit Interest/Pledge", key="offset_submit"):
        st.balloons()
        st.success("Thank you for your interest! The project team will contact you soon.")

# --- Certification & Audit Contact ---
with tab5:
    st.markdown("""
## 📜 ISO 14064 Certification & Virtual Audit
If you want your GHG emissions data certified, please contact our auditor for a virtual ISO 14064 audit. We will review your data, provide feedback, and issue certification if requirements are met.
""")
    contact_name = st.text_input("Your Name", key="cert_name")
    contact_email = st.text_input("Your Email", key="cert_email")
    contact_message = st.text_area("Message (please describe your request or questions)", key="cert_message")
    if st.button("Contact Auditor", key="cert_submit"):
        st.snow()
        st.success("Thank you! The auditor will contact you soon regarding your certification request.")

# --- Save or Submit Button ---
if st.button("Save/Submit Data"):
    st.balloons()
    st.success("Your data has been saved! If you want your emissions data certified, please contact us for a virtual ISO 14064 audit.")

# --- Colorful Footer ---
st.markdown("""
---
<center>
    <h4>Made with ❤️ for sustainable restaurants</h4>
    <a href='mailto:info@carbonfootprintapp.com'>Contact Us</a> |
    <a href='https://twitter.com/yourprofile'>Twitter</a> |
    <a href='https://linkedin.com/in/yourprofile'>LinkedIn</a>
    <br>
    <span style='color:green;'>Let's make food greener, together!</span>
</center>
""", unsafe_allow_html=True)
