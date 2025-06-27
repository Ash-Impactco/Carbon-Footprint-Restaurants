import streamlit as st

st.set_page_config(page_title="Detailed Information", page_icon="📋")

st.markdown("# 📋 Detailed Information")

st.markdown("""
This page contains detailed information about GHG emissions scopes, certification processes, and advanced features.
""")

# --- Scope Information ---
st.markdown("## 🔥 Scope 1: Direct Emissions")
st.markdown("""
**Direct emissions from sources owned or controlled by the restaurant.**

- **LPG/Natural Gas combustion**: Used for cooking dosa, idli, vada, sambar, etc.
- **Diesel or petrol used in generators**: For backup power in case of electricity cuts.
- **Refrigerant leakage**: From refrigerators, cold storage, and air conditioners.
- **Company-owned delivery vehicles**: Two-wheelers or vans owned by the restaurant for food delivery.
""")

st.markdown("## 💡 Scope 2: Indirect Emissions from Energy")
st.markdown("""
**Indirect emissions from the generation of purchased energy.**

- **Purchased electricity from the grid**: Used for lighting, fans, rice cookers, mixers/grinders, refrigerators, billing systems.
- **Purchased chilled water or steam**: If the restaurant uses central cooling or solar-heated steam systems (rare).
""")

st.markdown("## 🛵 Scope 3: Other Indirect Emissions")
st.markdown("""
**Other indirect emissions from the value chain (upstream and downstream).**

### Upstream (before the restaurant):
- **Purchased goods and ingredients**: Emissions from growing and transporting rice, lentils, vegetables, milk, ghee, spices, oil.
- **Capital goods**: Emissions from manufacturing kitchen equipment, gas stoves, furniture.
- **Fuel and energy-related activities**: Emissions from fuel extraction, refining, and transport.
- **Upstream transportation**: Transport of ingredients and goods from suppliers to the restaurant.
- **Waste generated in operations**: Food waste, packaging waste, wastewater disposal.
- **Employee commuting**: Staff traveling to and from the restaurant.
- **Business travel**: Travel to vendor meetings, conferences, training, etc.
- **Upstream leased assets**: If the restaurant rents the space, emissions from the building's operation.

### Downstream (after the restaurant):
- **Delivery services by third parties**: Swiggy/Zomato delivery bikes/scooters.
- **Customer transportation**: Emissions from customers driving/riding to the restaurant.
- **End-of-life treatment of sold products**: Disposal of takeaway containers, plastic bags, cutlery.
- **Franchisee emissions**: If the restaurant operates under a brand or franchise model.
- **Downstream leased assets**: Use of spaces or kitchens managed by others.
""")

# --- Certification Information ---
st.markdown("## 📜 ISO 14064 Certification & Virtual Audit")
st.markdown("""
If you want your GHG emissions data certified, please contact our auditor for a virtual ISO 14064 audit. We will review your data, provide feedback, and issue certification if requirements are met.

### What is ISO 14064?
ISO 14064 is an international standard for quantifying and reporting greenhouse gas emissions and removals. It provides a framework for organizations to:
- Quantify their GHG emissions
- Develop GHG inventories
- Report GHG emissions
- Validate and verify GHG assertions

### Certification Process:
1. **Data Review**: Our auditors review your emissions data
2. **Virtual Audit**: Conduct a virtual audit session
3. **Feedback**: Provide recommendations for improvement
4. **Certification**: Issue ISO 14064 certification if requirements are met
""")

# Contact form for certification
st.markdown("### Request Certification")
contact_name = st.text_input("Your Name")
contact_email = st.text_input("Your Email")
contact_message = st.text_area("Message (please describe your request or questions)")
if st.button("Contact Auditor"):
    st.success("Thank you! The auditor will contact you soon regarding your certification request.")

# --- Carbon Offset Projects ---
st.markdown("## 🌳 Carbon Offset Projects")
st.markdown("""
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
    st.markdown(f"**{p['name']}**")
    st.markdown(f"{p['desc']}")
    st.markdown(f"[Learn more & support]({p['link']})")
    st.markdown("---")

# --- Emission Factors ---
st.markdown("## 📊 Emission Factors")
st.markdown("""
Our calculations use Indian emission factors (kg CO2e per unit):

| Source | Factor | Unit |
|--------|--------|------|
| LPG | 2.983 | kg CO2e/kg |
| Diesel | 2.68 | kg CO2e/liter |
| Petrol | 2.31 | kg CO2e/liter |
| Electricity | 0.82 | kg CO2e/kWh |
| Rice | 2.7 | kg CO2e/kg |
| Lentils | 0.9 | kg CO2e/kg |
| Vegetables | 0.5 | kg CO2e/kg |
| Milk | 1.4 | kg CO2e/liter |
| Ghee | 8.0 | kg CO2e/kg |
| Spices | 1.5 | kg CO2e/kg |
| Cooking Oil | 3.3 | kg CO2e/liter |
| Food Waste | 1.9 | kg CO2e/kg |
| Packaging | 2.5 | kg CO2e/kg |
| Transport | 0.15 | kg CO2e/km |
| Commute | 0.12 | kg CO2e/km |
| Business Travel | 0.15 | kg CO2e/km |
| Delivery | 0.3 | kg CO2e/order |
| Customer Visit | 0.2 | kg CO2e/visit |
| Takeaway Container | 0.05 | kg CO2e/container |
""")

# --- Advanced Features ---
st.markdown("## 🚀 Advanced Features")
st.markdown("""
### File Upload
- Upload CSV or Excel files with your restaurant's data
- Automatic data validation
- Template download available

### Quick Entry Form
- Simplified form with the most important parameters
- Pre-filled with typical values for medium restaurants
- Perfect for quick estimates or initial assessments

### Sample Data
- Pre-configured data for different restaurant types:
  - Small Dosa Shop
  - Medium Restaurant
  - Large Restaurant
  - Food Court Stall
- Use as-is or modify to match your specific situation

### Data Export
- Download your data and results as CSV or Excel reports
- Comprehensive reports with multiple sheets
- Summary with percentages and recommendations
""")

# --- Footer ---
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>For questions about certification or advanced features, please contact us.</p>
    <p><a href='mailto:info@carbonfootprintapp.com'>Contact Us</a></p>
</div>
""", unsafe_allow_html=True) 