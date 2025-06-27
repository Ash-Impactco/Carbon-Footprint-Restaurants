import streamlit as st
import pandas as pd
import numpy as np
import io
import datetime
import openpyxl

st.set_page_config(layout="wide", page_title="Carbon Calculator", page_icon="./media/favicon.ico")

# --- Banner ---
st.image('./media/background_min.jpg', use_column_width=True)

# --- Simple Header ---
st.markdown("""
# Carbon Calculator for Restaurants
Calculate your restaurant's carbon footprint in minutes.
""")

# Add link to detailed guide
st.markdown("""
<div style='background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin: 10px 0;'>
    <p style='margin: 0;'><strong>📚 Want to learn more?</strong> 
    <a href='https://github.com/Ash-Impactco/Carbon-Footprint-Restaurants/blob/main/blog/restaurant-carbon-footprint-guide.md' target='_blank'>
    Read our complete guide on restaurant carbon footprint calculation, certification, and scope details</a></p>
</div>
""", unsafe_allow_html=True)

# --- Simple Data Entry ---
st.markdown("## Enter Your Data")

# Create two columns for better layout
col1, col2 = st.columns(2)

with col1:
    st.markdown("### Energy & Fuel")
    lpg_used = st.number_input("LPG used (kg/year)", min_value=0.0, value=500.0, help="Total LPG used for cooking")
    generator_fuel = st.number_input("Generator fuel (liters/year)", min_value=0.0, value=100.0, help="Diesel/petrol for backup generators")
    electricity = st.number_input("Electricity (kWh/year)", min_value=0.0, value=12000.0, help="Total electricity from grid")
    
    st.markdown("### Key Ingredients")
    rice_kg = st.number_input("Rice purchased (kg/year)", min_value=0.0, value=2000.0)
    vegetables_kg = st.number_input("Vegetables purchased (kg/year)", min_value=0.0, value=1500.0)
    milk_liters = st.number_input("Milk purchased (liters/year)", min_value=0.0, value=1000.0)

with col2:
    st.markdown("### Operations")
    staff_count = st.number_input("Number of staff", min_value=0, value=8, step=1)
    customer_visits = st.number_input("Customer visits/year", min_value=0, value=15000, step=100)
    third_party_deliveries = st.number_input("Delivery orders/year", min_value=0, value=2000, step=100)
    
    st.markdown("### Other Details")
    food_waste_kg = st.number_input("Food waste (kg/year)", min_value=0.0, value=500.0)
    packaging_waste_kg = st.number_input("Packaging waste (kg/year)", min_value=0.0, value=200.0)
    upstream_transport_km = st.number_input("Transport distance (km/year)", min_value=0.0, value=5000.0, help="Ingredient delivery distance")

# --- Emission Factors ---
EMISSION_FACTORS = {
    'lpg_kg': 2.983,
    'diesel_l': 2.68,
    'electricity_kwh': 0.82,
    'rice_kg': 2.7,
    'vegetables_kg': 0.5,
    'milk_l': 1.4,
    'food_waste_kg': 1.9,
    'packaging_kg': 2.5,
    'km_transport': 0.15,
    'delivery_order': 0.3,
    'customer_visit': 0.2
}

# --- Calculate Emissions ---
if st.button("Calculate Carbon Footprint", type="primary"):
    # Scope 1 (Direct emissions)
    scope1 = (
        lpg_used * EMISSION_FACTORS['lpg_kg'] +
        generator_fuel * EMISSION_FACTORS['diesel_l']
    )
    
    # Scope 2 (Energy)
    scope2 = electricity * EMISSION_FACTORS['electricity_kwh']
    
    # Scope 3 (Value chain)
    scope3 = (
        rice_kg * EMISSION_FACTORS['rice_kg'] +
        vegetables_kg * EMISSION_FACTORS['vegetables_kg'] +
        milk_liters * EMISSION_FACTORS['milk_l'] +
        food_waste_kg * EMISSION_FACTORS['food_waste_kg'] +
        packaging_waste_kg * EMISSION_FACTORS['packaging_kg'] +
        upstream_transport_km * EMISSION_FACTORS['km_transport'] +
        third_party_deliveries * EMISSION_FACTORS['delivery_order'] +
        customer_visits * EMISSION_FACTORS['customer_visit']
    )
    
    # Convert to tonnes
    scope1_t = scope1 / 1000
    scope2_t = scope2 / 1000
    scope3_t = scope3 / 1000
    total_t = scope1_t + scope2_t + scope3_t
    
    # Display results
    st.markdown("---")
    st.markdown("## Your Results")
    
    # Create a nice results display
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Emissions", f"{total_t:.1f} tCO₂e/year")
    
    with col2:
        st.metric("Scope 1 (Direct)", f"{scope1_t:.1f} tCO₂e")
    
    with col3:
        st.metric("Scope 2 (Energy)", f"{scope2_t:.1f} tCO₂e")
    
    with col4:
        st.metric("Scope 3 (Value Chain)", f"{scope3_t:.1f} tCO₂e")
    
    # Progress bar for total emissions
    st.progress(min(total_t / 50, 1.0))  # Assuming 50 tCO2e/year as max for progress bar
    st.caption(f"Progress towards typical restaurant emissions (50 tCO₂e/year)")
    
    # Add link to learn more about certification
    st.markdown("""
    <div style='background-color: #e8f5e8; padding: 10px; border-radius: 5px; margin: 10px 0;'>
        <p style='margin: 0;'><strong>🎯 Next Steps:</strong> 
        <a href='https://github.com/Ash-Impactco/Carbon-Footprint-Restaurants/blob/main/blog/restaurant-carbon-footprint-guide.md' target='_blank'>
        Learn about ISO 14064 certification and how to reduce your emissions</a></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Export option
    st.markdown("### Export Your Results")
    
    # Create export data
    export_data = {
        'Parameter': [
            'LPG used (kg/year)', 'Generator fuel (liters/year)', 'Electricity (kWh/year)',
            'Rice purchased (kg/year)', 'Vegetables purchased (kg/year)', 'Milk purchased (liters/year)',
            'Staff count', 'Customer visits/year', 'Delivery orders/year',
            'Food waste (kg/year)', 'Packaging waste (kg/year)', 'Transport distance (km/year)',
            'Scope 1 Emissions (tCO2e/year)', 'Scope 2 Emissions (tCO2e/year)', 
            'Scope 3 Emissions (tCO2e/year)', 'Total Emissions (tCO2e/year)'
        ],
        'Value': [
            lpg_used, generator_fuel, electricity,
            rice_kg, vegetables_kg, milk_liters,
            staff_count, customer_visits, third_party_deliveries,
            food_waste_kg, packaging_waste_kg, upstream_transport_km,
            scope1_t, scope2_t, scope3_t, total_t
        ]
    }
    
    export_df = pd.DataFrame(export_data)
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = export_df.to_csv(index=False)
        st.download_button(
            label="Download as CSV",
            data=csv,
            file_name=f"carbon_footprint_{datetime.date.today().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    
    with col2:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            export_df.to_excel(writer, sheet_name='Carbon Footprint', index=False)
        buffer.seek(0)
        st.download_button(
            label="Download as Excel",
            data=buffer,
            file_name=f"carbon_footprint_{datetime.date.today().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

# --- Simple Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>Made with ❤️ for sustainable restaurants</p>
    <p><a href='mailto:info@carbonfootprintapp.com'>Contact Us</a> | 
    <a href='https://github.com/Ash-Impactco/Carbon-Footprint-Restaurants'>GitHub</a></p>
</div>
""", unsafe_allow_html=True) 