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
import openpyxl

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
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Easy Data Entry",
    "🔥 Scope 1: Direct Emissions",
    "💡 Scope 2: Indirect Emissions from Energy",
    "🛵 Scope 3: Other Indirect Emissions",
    "🌳 Carbon Offset Projects",
    "📜 Certification & Audit Contact"
])

# --- Easy Data Entry Tab ---
with tab1:
    st.markdown("""
## 📊 Easy Data Entry Methods
Choose the most convenient way to enter your restaurant's data:
""")
    
    # Method selection
    entry_method = st.radio(
        "Select your preferred data entry method:",
        ["📁 Upload CSV/Excel File", "📋 Quick Entry Form", "📥 Download Template", "📊 View Sample Data"],
        help="Choose the easiest method for you"
    )
    
    if entry_method == "📁 Upload CSV/Excel File":
        st.markdown("### 📁 Upload Your Data File")
        st.info("Upload a CSV or Excel file with your restaurant's data. Use the template below for the correct format.")
        
        uploaded_file = st.file_uploader(
            "Choose a CSV or Excel file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload your data file here"
        )
        
        if uploaded_file is not None:
            try:
                if uploaded_file.name.endswith('.csv'):
                    data = pd.read_csv(uploaded_file)
                else:
                    data = pd.read_excel(uploaded_file)
                
                st.success(f"✅ File uploaded successfully! Found {len(data)} records.")
                st.dataframe(data.head())
                
                # Validate data
                required_columns = [
                    'lpg_used', 'generator_fuel', 'refrigerant_leak', 'owned_vehicle_fuel',
                    'electricity', 'chilled_water', 'rice_kg', 'lentils_kg', 'vegetables_kg',
                    'milk_liters', 'ghee_kg', 'spices_kg', 'oil_liters', 'upstream_transport_km',
                    'food_waste_kg', 'packaging_waste_kg', 'staff_count', 'avg_commute_km',
                    'business_travel_km', 'third_party_deliveries', 'customer_visits', 'takeaway_containers'
                ]
                
                missing_columns = [col for col in required_columns if col not in data.columns]
                if missing_columns:
                    st.warning(f"⚠️ Missing columns: {', '.join(missing_columns)}")
                else:
                    st.success("✅ All required columns found!")
                
                # Process the data
                if st.button("Process Uploaded Data"):
                    # Store in session state for use in other tabs
                    st.session_state.uploaded_data = data.iloc[0].to_dict()  # Use first row
                    st.success("Data processed! You can now view results in other tabs.")
                    
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
    
    elif entry_method == "📋 Quick Entry Form":
        st.markdown("### 📋 Quick Entry Form")
        st.info("Fill out this simplified form for common restaurant scenarios.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔥 Direct Emissions (Scope 1)")
            lpg_quick = st.number_input("LPG used (kg/year)", min_value=0.0, value=500.0, help="Typical: 300-800 kg/year")
            generator_quick = st.number_input("Generator fuel (liters/year)", min_value=0.0, value=100.0, help="Typical: 50-200 liters/year")
            
            st.markdown("#### 💡 Energy (Scope 2)")
            electricity_quick = st.number_input("Electricity (kWh/year)", min_value=0.0, value=12000.0, help="Typical: 8000-20000 kWh/year")
        
        with col2:
            st.markdown("#### 🛵 Key Ingredients (Scope 3)")
            rice_quick = st.number_input("Rice (kg/year)", min_value=0.0, value=2000.0, help="Typical: 1500-3000 kg/year")
            vegetables_quick = st.number_input("Vegetables (kg/year)", min_value=0.0, value=1500.0, help="Typical: 1000-2500 kg/year")
            milk_quick = st.number_input("Milk (liters/year)", min_value=0.0, value=1000.0, help="Typical: 800-1500 liters/year")
            
            st.markdown("#### 👥 Operations")
            staff_quick = st.number_input("Staff count", min_value=0, value=8, step=1, help="Typical: 5-15 people")
            customers_quick = st.number_input("Customer visits/year", min_value=0, value=15000, step=100, help="Typical: 10000-25000 visits")
        
        if st.button("Calculate with Quick Data"):
            # Store quick data in session state
            st.session_state.quick_data = {
                'lpg_used': lpg_quick,
                'generator_fuel': generator_quick,
                'refrigerant_leak': 0.0,
                'owned_vehicle_fuel': 0.0,
                'electricity': electricity_quick,
                'chilled_water': 0.0,
                'rice_kg': rice_quick,
                'lentils_kg': 500.0,
                'vegetables_kg': vegetables_quick,
                'milk_liters': milk_quick,
                'ghee_kg': 200.0,
                'spices_kg': 100.0,
                'oil_liters': 300.0,
                'upstream_transport_km': 5000.0,
                'food_waste_kg': 500.0,
                'packaging_waste_kg': 200.0,
                'staff_count': staff_quick,
                'avg_commute_km': 5.0,
                'business_travel_km': 100.0,
                'third_party_deliveries': 2000,
                'customer_visits': customers_quick,
                'takeaway_containers': 5000
            }
            st.success("Quick data saved! View results in other tabs.")
    
    elif entry_method == "📥 Download Template":
        st.markdown("### 📥 Download Data Template")
        st.info("Download this template to prepare your data in the correct format.")
        
        # Create sample data
        template_data = {
            'lpg_used': [500.0],
            'generator_fuel': [100.0],
            'refrigerant_leak': [0.0],
            'owned_vehicle_fuel': [0.0],
            'electricity': [12000.0],
            'chilled_water': [0.0],
            'rice_kg': [2000.0],
            'lentils_kg': [500.0],
            'vegetables_kg': [1500.0],
            'milk_liters': [1000.0],
            'ghee_kg': [200.0],
            'spices_kg': [100.0],
            'oil_liters': [300.0],
            'upstream_transport_km': [5000.0],
            'food_waste_kg': [500.0],
            'packaging_waste_kg': [200.0],
            'staff_count': [8],
            'avg_commute_km': [5.0],
            'business_travel_km': [100.0],
            'third_party_deliveries': [2000],
            'customer_visits': [15000],
            'takeaway_containers': [5000]
        }
        
        template_df = pd.DataFrame(template_data)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV download
            csv = template_df.to_csv(index=False)
            st.download_button(
                label="📄 Download CSV Template",
                data=csv,
                file_name="restaurant_emissions_template.csv",
                mime="text/csv",
                help="Download as CSV file"
            )
        
        with col2:
            # Excel download
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                template_df.to_excel(writer, sheet_name='Data', index=False)
                # Add instructions sheet
                instructions = pd.DataFrame({
                    'Column': template_df.columns,
                    'Description': [
                        'LPG/Natural Gas used for cooking (kg/year)',
                        'Diesel/Petrol used in generators (liters/year)',
                        'Refrigerant leakage (kg/year)',
                        'Fuel used by company-owned delivery vehicles (liters/year)',
                        'Purchased electricity (kWh/year)',
                        'Purchased chilled water or steam (kWh/year)',
                        'Rice purchased (kg/year)',
                        'Lentils purchased (kg/year)',
                        'Vegetables purchased (kg/year)',
                        'Milk purchased (liters/year)',
                        'Ghee purchased (kg/year)',
                        'Spices purchased (kg/year)',
                        'Cooking oil purchased (liters/year)',
                        'Upstream transport (total km/year)',
                        'Food waste generated (kg/year)',
                        'Packaging waste generated (kg/year)',
                        'Number of staff',
                        'Average staff commute distance (km, one way)',
                        'Business travel (km/year)',
                        'Number of third-party delivery orders/year',
                        'Estimated customer visits/year',
                        'Takeaway containers used/year'
                    ],
                    'Typical Range': [
                        '300-800 kg/year',
                        '50-200 liters/year',
                        '0-10 kg/year',
                        '0-500 liters/year',
                        '8000-20000 kWh/year',
                        '0-1000 kWh/year',
                        '1500-3000 kg/year',
                        '300-800 kg/year',
                        '1000-2500 kg/year',
                        '800-1500 liters/year',
                        '100-300 kg/year',
                        '50-200 kg/year',
                        '200-500 liters/year',
                        '3000-8000 km/year',
                        '300-800 kg/year',
                        '100-400 kg/year',
                        '5-15 people',
                        '3-10 km',
                        '50-200 km/year',
                        '1000-5000 orders/year',
                        '10000-25000 visits/year',
                        '3000-8000 containers/year'
                    ]
                })
                instructions.to_excel(writer, sheet_name='Instructions', index=False)
            
            buffer.seek(0)
            st.download_button(
                label="📊 Download Excel Template",
                data=buffer,
                file_name="restaurant_emissions_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Download as Excel file with instructions"
            )
        
        st.markdown("""
        ### 📋 Instructions:
        1. Download the template file
        2. Fill in your restaurant's data in the first row
        3. Save the file
        4. Upload it back using the "Upload CSV/Excel File" option above
        """)
    
    elif entry_method == "📊 View Sample Data":
        st.markdown("### 📊 Sample Data for Different Restaurant Types")
        
        restaurant_type = st.selectbox(
            "Select restaurant type to view sample data:",
            ["Small Dosa Shop", "Medium Restaurant", "Large Restaurant", "Food Court Stall"]
        )
        
        sample_data = {
            "Small Dosa Shop": {
                'lpg_used': 300.0, 'generator_fuel': 50.0, 'electricity': 8000.0,
                'rice_kg': 1500.0, 'vegetables_kg': 1000.0, 'milk_liters': 800.0,
                'staff_count': 5, 'customer_visits': 10000
            },
            "Medium Restaurant": {
                'lpg_used': 500.0, 'generator_fuel': 100.0, 'electricity': 12000.0,
                'rice_kg': 2000.0, 'vegetables_kg': 1500.0, 'milk_liters': 1000.0,
                'staff_count': 8, 'customer_visits': 15000
            },
            "Large Restaurant": {
                'lpg_used': 800.0, 'generator_fuel': 200.0, 'electricity': 20000.0,
                'rice_kg': 3000.0, 'vegetables_kg': 2500.0, 'milk_liters': 1500.0,
                'staff_count': 15, 'customer_visits': 25000
            },
            "Food Court Stall": {
                'lpg_used': 200.0, 'generator_fuel': 30.0, 'electricity': 5000.0,
                'rice_kg': 800.0, 'vegetables_kg': 600.0, 'milk_liters': 400.0,
                'staff_count': 3, 'customer_visits': 8000
            }
        }
        
        selected_data = sample_data[restaurant_type]
        
        # Display sample data
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### 🔥 Direct Emissions")
            st.write(f"LPG used: {selected_data['lpg_used']} kg/year")
            st.write(f"Generator fuel: {selected_data['generator_fuel']} liters/year")
            
            st.markdown("#### 💡 Energy")
            st.write(f"Electricity: {selected_data['electricity']} kWh/year")
        
        with col2:
            st.markdown("#### 🛵 Key Ingredients")
            st.write(f"Rice: {selected_data['rice_kg']} kg/year")
            st.write(f"Vegetables: {selected_data['vegetables_kg']} kg/year")
            st.write(f"Milk: {selected_data['milk_liters']} liters/year")
            
            st.markdown("#### 👥 Operations")
            st.write(f"Staff: {selected_data['staff_count']} people")
            st.write(f"Customers: {selected_data['customer_visits']} visits/year")
        
        if st.button(f"Use {restaurant_type} Sample Data"):
            # Complete the sample data with default values
            complete_data = {
                'lpg_used': selected_data['lpg_used'],
                'generator_fuel': selected_data['generator_fuel'],
                'refrigerant_leak': 0.0,
                'owned_vehicle_fuel': 0.0,
                'electricity': selected_data['electricity'],
                'chilled_water': 0.0,
                'rice_kg': selected_data['rice_kg'],
                'lentils_kg': selected_data['rice_kg'] * 0.25,  # Estimate
                'vegetables_kg': selected_data['vegetables_kg'],
                'milk_liters': selected_data['milk_liters'],
                'ghee_kg': selected_data['milk_liters'] * 0.2,  # Estimate
                'spices_kg': selected_data['vegetables_kg'] * 0.1,  # Estimate
                'oil_liters': selected_data['vegetables_kg'] * 0.2,  # Estimate
                'upstream_transport_km': selected_data['rice_kg'] * 2,  # Estimate
                'food_waste_kg': selected_data['rice_kg'] * 0.25,  # Estimate
                'packaging_waste_kg': selected_data['customer_visits'] * 0.02,  # Estimate
                'staff_count': selected_data['staff_count'],
                'avg_commute_km': 5.0,
                'business_travel_km': 100.0,
                'third_party_deliveries': selected_data['customer_visits'] * 0.3,  # Estimate
                'customer_visits': selected_data['customer_visits'],
                'takeaway_containers': selected_data['customer_visits'] * 0.4  # Estimate
            }
            st.session_state.sample_data = complete_data
            st.success(f"Sample data for {restaurant_type} loaded! View results in other tabs.")

# --- Scope 1 ---
with tab2:
    st.markdown("""
### 🔥 Scope 1: Direct Emissions
**Direct emissions from sources owned or controlled by the restaurant.**
- *LPG/Natural Gas combustion*: Used for cooking dosa, idli, vada, sambar, etc.
- *Diesel or petrol used in generators*: For backup power in case of electricity cuts.
- *Refrigerant leakage*: From refrigerators, cold storage, and air conditioners.
- *Company-owned delivery vehicles*: Two-wheelers or vans owned by the restaurant for food delivery.
""")
    lpg_used_manual = st.number_input("LPG/Natural Gas used for cooking (kg/year) 🥘", min_value=0.0, help="Total LPG or natural gas used for all cooking in a year.")
    generator_fuel_manual = st.number_input("Diesel/Petrol used in generators (liters/year) ⛽", min_value=0.0, help="Total diesel or petrol used for backup generators in a year.")
    refrigerant_leak_manual = st.number_input("Refrigerant leakage (kg/year) ❄️", min_value=0.0, help="Estimated refrigerant lost from fridges, cold storage, ACs in a year.")
    owned_vehicle_fuel_manual = st.number_input("Fuel used by company-owned delivery vehicles (liters/year) 🚗", min_value=0.0, help="Total petrol/diesel used by restaurant-owned delivery vehicles in a year.")

# --- Scope 2 ---
with tab3:
    st.markdown("""
### 💡 Scope 2: Indirect Emissions from Energy
**Indirect emissions from the generation of purchased energy.**
- *Purchased electricity from the grid*: Used for lighting, fans, rice cookers, mixers/grinders, refrigerators, billing systems.
- *Purchased chilled water or steam*: If the restaurant uses central cooling or solar-heated steam systems (rare).
""")
    electricity_manual = st.number_input("Purchased electricity (kWh/year) 💡", min_value=0.0, help="Total electricity used from the grid in a year.")
    chilled_water_manual = st.number_input("Purchased chilled water or steam (kWh or equivalent/year) 💧", min_value=0.0, help="If applicable. Leave as 0 if not used.")

# --- Scope 3 ---
with tab4:
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
    rice_kg_manual = st.number_input("Rice purchased (kg/year) 🍚", min_value=0.0, help="Total rice purchased in a year.")
    lentils_kg_manual = st.number_input("Lentils purchased (kg/year) 🥣", min_value=0.0)
    vegetables_kg_manual = st.number_input("Vegetables purchased (kg/year) 🥦", min_value=0.0)
    milk_liters_manual = st.number_input("Milk purchased (liters/year) 🥛", min_value=0.0)
    ghee_kg_manual = st.number_input("Ghee purchased (kg/year) 🧈", min_value=0.0)
    spices_kg_manual = st.number_input("Spices purchased (kg/year) 🌶️", min_value=0.0)
    oil_liters_manual = st.number_input("Cooking oil purchased (liters/year) 🛢️", min_value=0.0)
    capital_goods = st.text_input("Major capital goods purchased this year (describe, optional) 🏭")
    upstream_transport_km_manual = st.number_input("Upstream transport (total km/year) 🚚", min_value=0.0, help="Estimated total km for ingredient delivery to your restaurant.")
    food_waste_kg_manual = st.number_input("Food waste generated (kg/year) 🍲", min_value=0.0)
    packaging_waste_kg_manual = st.number_input("Packaging waste generated (kg/year) 📦", min_value=0.0)
    staff_count_manual = st.number_input("Number of staff 👨‍🍳", min_value=0, step=1)
    avg_commute_km_manual = st.number_input("Average staff commute distance (km, one way) 🚌", min_value=0.0)
    business_travel_km_manual = st.number_input("Business travel (km/year) ✈️", min_value=0.0)
    third_party_deliveries_manual = st.number_input("Number of third-party delivery orders/year 🛵", min_value=0, step=1)
    main_delivery_partner = st.text_input("Main delivery partner (e.g., Swiggy, Zomato, etc.) 🛵")
    customer_visits_manual = st.number_input("Estimated customer visits/year 👥", min_value=0, step=1)
    takeaway_containers_manual = st.number_input("Takeaway containers used/year 🥡", min_value=0, step=1)
    franchisee = st.checkbox("Is your restaurant part of a franchise or brand? 🏢")
    leased_space = st.checkbox("Do you operate in a leased space or kitchen? 🏠")

# --- Carbon Offset Projects ---
with tab5:
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
with tab6:
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
    st.markdown("""
    👉 [Go to Certification & Audit Contact tab](#certification--audit-contact)
    """, unsafe_allow_html=True)

# --- Indian Emission Factors (kg CO2e per unit) ---
EMISSION_FACTORS = {
    'lpg_kg': 2.983,         # 1 kg LPG ≈ 2.983 kg CO2e (India GHG Platform)
    'diesel_l': 2.68,       # 1 liter diesel ≈ 2.68 kg CO2e
    'petrol_l': 2.31,       # 1 liter petrol ≈ 2.31 kg CO2e
    'refrigerant_kg': 1300, # R134a GWP ≈ 1300 (example, update as needed)
    'electricity_kwh': 0.82,# 1 kWh grid electricity ≈ 0.82 kg CO2e (India avg)
    'rice_kg': 2.7,         # 1 kg rice ≈ 2.7 kg CO2e (India, incl. methane)
    'lentils_kg': 0.9,      # 1 kg lentils ≈ 0.9 kg CO2e
    'vegetables_kg': 0.5,   # 1 kg vegetables ≈ 0.5 kg CO2e
    'milk_l': 1.4,          # 1 liter milk ≈ 1.4 kg CO2e
    'ghee_kg': 8.0,         # 1 kg ghee ≈ 8.0 kg CO2e
    'spices_kg': 1.5,       # 1 kg spices ≈ 1.5 kg CO2e
    'oil_l': 3.3,           # 1 liter cooking oil ≈ 3.3 kg CO2e
    'food_waste_kg': 1.9,   # 1 kg food waste ≈ 1.9 kg CO2e (landfill, India)
    'packaging_kg': 2.5,    # 1 kg packaging ≈ 2.5 kg CO2e (mixed)
    'km_transport': 0.15,   # 1 km by small truck ≈ 0.15 kg CO2e
    'commute_km': 0.12,     # 1 km by bus ≈ 0.12 kg CO2e
    'business_travel_km': 0.15, # 1 km by taxi ≈ 0.15 kg CO2e
    'delivery_order': 0.3,  # 1 delivery order ≈ 0.3 kg CO2e (bike/scooter)
    'customer_visit': 0.2,  # 1 customer visit ≈ 0.2 kg CO2e (short trip)
    'takeaway_container': 0.05 # 1 container ≈ 0.05 kg CO2e
}

# --- Calculate Emissions ---
# Get data from various sources (manual entry, uploaded file, quick entry, or sample data)
data_source = None
if 'uploaded_data' in st.session_state:
    data_source = st.session_state.uploaded_data
elif 'quick_data' in st.session_state:
    data_source = st.session_state.quick_data
elif 'sample_data' in st.session_state:
    data_source = st.session_state.sample_data

# Initialize variables
lpg_used = 0.0
generator_fuel = 0.0
refrigerant_leak = 0.0
owned_vehicle_fuel = 0.0
electricity = 0.0
chilled_water = 0.0
rice_kg = 0.0
lentils_kg = 0.0
vegetables_kg = 0.0
milk_liters = 0.0
ghee_kg = 0.0
spices_kg = 0.0
oil_liters = 0.0
upstream_transport_km = 0.0
food_waste_kg = 0.0
packaging_waste_kg = 0.0
staff_count = 0
avg_commute_km = 0.0
business_travel_km = 0.0
third_party_deliveries = 0
customer_visits = 0
takeaway_containers = 0

# Use data from easy entry methods if available, otherwise use manual entry
if data_source:
    # Extract values from session state data
    lpg_used = data_source.get('lpg_used', 0.0)
    generator_fuel = data_source.get('generator_fuel', 0.0)
    refrigerant_leak = data_source.get('refrigerant_leak', 0.0)
    owned_vehicle_fuel = data_source.get('owned_vehicle_fuel', 0.0)
    electricity = data_source.get('electricity', 0.0)
    chilled_water = data_source.get('chilled_water', 0.0)
    rice_kg = data_source.get('rice_kg', 0.0)
    lentils_kg = data_source.get('lentils_kg', 0.0)
    vegetables_kg = data_source.get('vegetables_kg', 0.0)
    milk_liters = data_source.get('milk_liters', 0.0)
    ghee_kg = data_source.get('ghee_kg', 0.0)
    spices_kg = data_source.get('spices_kg', 0.0)
    oil_liters = data_source.get('oil_liters', 0.0)
    upstream_transport_km = data_source.get('upstream_transport_km', 0.0)
    food_waste_kg = data_source.get('food_waste_kg', 0.0)
    packaging_waste_kg = data_source.get('packaging_waste_kg', 0.0)
    staff_count = data_source.get('staff_count', 0)
    avg_commute_km = data_source.get('avg_commute_km', 0.0)
    business_travel_km = data_source.get('business_travel_km', 0.0)
    third_party_deliveries = data_source.get('third_party_deliveries', 0)
    customer_visits = data_source.get('customer_visits', 0)
    takeaway_containers = data_source.get('takeaway_containers', 0)
    
    # Show data source indicator
    st.info("📊 Using data from Easy Data Entry tab")
else:
    # Use manually entered data
    lpg_used = lpg_used_manual
    generator_fuel = generator_fuel_manual
    refrigerant_leak = refrigerant_leak_manual
    owned_vehicle_fuel = owned_vehicle_fuel_manual
    electricity = electricity_manual
    chilled_water = chilled_water_manual
    rice_kg = rice_kg_manual
    lentils_kg = lentils_kg_manual
    vegetables_kg = vegetables_kg_manual
    milk_liters = milk_liters_manual
    ghee_kg = ghee_kg_manual
    spices_kg = spices_kg_manual
    oil_liters = oil_liters_manual
    upstream_transport_km = upstream_transport_km_manual
    food_waste_kg = food_waste_kg_manual
    packaging_waste_kg = packaging_waste_kg_manual
    staff_count = staff_count_manual
    avg_commute_km = avg_commute_km_manual
    business_travel_km = business_travel_km_manual
    third_party_deliveries = third_party_deliveries_manual
    customer_visits = customer_visits_manual
    takeaway_containers = takeaway_containers_manual

# Only calculate and display if we're running in Streamlit
if st._is_running_with_streamlit:
    # Calculate emissions
    # Scope 1
    scope1 = (
        lpg_used * EMISSION_FACTORS['lpg_kg'] +
        generator_fuel * EMISSION_FACTORS['diesel_l'] +
        refrigerant_leak * EMISSION_FACTORS['refrigerant_kg'] +
        owned_vehicle_fuel * EMISSION_FACTORS['petrol_l']
    )
    # Scope 2
    scope2 = (
        electricity * EMISSION_FACTORS['electricity_kwh'] +
        chilled_water * EMISSION_FACTORS['electricity_kwh']
    )
    # Scope 3
    scope3 = (
        rice_kg * EMISSION_FACTORS['rice_kg'] +
        lentils_kg * EMISSION_FACTORS['lentils_kg'] +
        vegetables_kg * EMISSION_FACTORS['vegetables_kg'] +
        milk_liters * EMISSION_FACTORS['milk_l'] +
        ghee_kg * EMISSION_FACTORS['ghee_kg'] +
        spices_kg * EMISSION_FACTORS['spices_kg'] +
        oil_liters * EMISSION_FACTORS['oil_l'] +
        upstream_transport_km * EMISSION_FACTORS['km_transport'] +
        food_waste_kg * EMISSION_FACTORS['food_waste_kg'] +
        packaging_waste_kg * EMISSION_FACTORS['packaging_kg'] +
        staff_count * avg_commute_km * 365 * EMISSION_FACTORS['commute_km'] +
        business_travel_km * EMISSION_FACTORS['business_travel_km'] +
        third_party_deliveries * EMISSION_FACTORS['delivery_order'] +
        customer_visits * EMISSION_FACTORS['customer_visit'] +
        takeaway_containers * EMISSION_FACTORS['takeaway_container']
    )
    # Convert to tonnes
    scope1_t = scope1 / 1000
    scope2_t = scope2 / 1000
    scope3_t = scope3 / 1000
    total_t = scope1_t + scope2_t + scope3_t

    # Display results
    st.markdown(f"""
    ---
    ## 🧮 Total GHG Emissions: **{total_t:.2f} tCO₂e/year**
    - 🔥 Scope 1: {scope1_t:.2f} tCO₂e
    - 💡 Scope 2: {scope2_t:.2f} tCO₂e
    - 🛵 Scope 3: {scope3_t:.2f} tCO₂e
    ---
    """)

    # Data export section
    st.markdown("### 📤 Export Your Data")

    # Create data for export
    export_data = {
        'Restaurant Data': {
            'LPG used (kg/year)': lpg_used,
            'Generator fuel (liters/year)': generator_fuel,
            'Refrigerant leakage (kg/year)': refrigerant_leak,
            'Owned vehicle fuel (liters/year)': owned_vehicle_fuel,
            'Electricity (kWh/year)': electricity,
            'Chilled water (kWh/year)': chilled_water,
            'Rice purchased (kg/year)': rice_kg,
            'Lentils purchased (kg/year)': lentils_kg,
            'Vegetables purchased (kg/year)': vegetables_kg,
            'Milk purchased (liters/year)': milk_liters,
            'Ghee purchased (kg/year)': ghee_kg,
            'Spices purchased (kg/year)': spices_kg,
            'Cooking oil purchased (liters/year)': oil_liters,
            'Upstream transport (km/year)': upstream_transport_km,
            'Food waste generated (kg/year)': food_waste_kg,
            'Packaging waste generated (kg/year)': packaging_waste_kg,
            'Number of staff': staff_count,
            'Average staff commute (km)': avg_commute_km,
            'Business travel (km/year)': business_travel_km,
            'Third-party deliveries (orders/year)': third_party_deliveries,
            'Customer visits (visits/year)': customer_visits,
            'Takeaway containers (containers/year)': takeaway_containers
        },
        'Emissions Results': {
            'Scope 1 Emissions (tCO2e/year)': scope1_t,
            'Scope 2 Emissions (tCO2e/year)': scope2_t,
            'Scope 3 Emissions (tCO2e/year)': scope3_t,
            'Total Emissions (tCO2e/year)': total_t
        }
    }

    col1, col2 = st.columns(2)

    with col1:
        # Export as CSV
        export_df = pd.DataFrame(list(export_data['Restaurant Data'].items()), 
                                columns=['Parameter', 'Value'])
        csv_export = export_df.to_csv(index=False)
        st.download_button(
            label="📄 Export Data as CSV",
            data=csv_export,
            file_name=f"restaurant_emissions_data_{datetime.date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )

    with col2:
        # Export as Excel with multiple sheets
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            # Restaurant data sheet
            pd.DataFrame(list(export_data['Restaurant Data'].items()), 
                        columns=['Parameter', 'Value']).to_excel(writer, sheet_name='Restaurant Data', index=False)
            
            # Emissions results sheet
            pd.DataFrame(list(export_data['Emissions Results'].items()), 
                        columns=['Parameter', 'Value']).to_excel(writer, sheet_name='Emissions Results', index=False)
            
            # Summary sheet
            if total_t > 0:
                scope1_pct = scope1_t / total_t * 100
                scope2_pct = scope2_t / total_t * 100
                scope3_pct = scope3_t / total_t * 100
            else:
                scope1_pct = scope2_pct = scope3_pct = 0

            summary_data = {
                'Summary': [
                    f"Total GHG Emissions: {total_t:.2f} tCO₂e/year",
                    f"Scope 1 (Direct): {scope1_t:.2f} tCO₂e ({scope1_pct:.1f}%)",
                    f"Scope 2 (Energy): {scope2_t:.2f} tCO₂e ({scope2_pct:.1f}%)",
                    f"Scope 3 (Value Chain): {scope3_t:.2f} tCO₂e ({scope3_pct:.1f}%)",
                    f"Date: {datetime.date.today().strftime('%B %d, %Y')}",
                    f"Restaurant Type: {'Custom Data' if data_source else 'Manual Entry'}"
                ]
            }
            pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
        
        buffer.seek(0)
        st.download_button(
            label="📊 Export as Excel Report",
            data=buffer,
            file_name=f"restaurant_emissions_report_{datetime.date.today().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    # Clear data option
    if st.button("🗑️ Clear All Data"):
        # Clear session state
        for key in ['uploaded_data', 'quick_data', 'sample_data']:
            if key in st.session_state:
                del st.session_state[key]
        st.success("Data cleared! Refresh the page to start over.")
        st.rerun()

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
