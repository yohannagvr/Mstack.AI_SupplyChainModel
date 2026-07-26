import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="US Trucking", layout="wide")

st.title("🚛 U.S. Inland Trucking")

st.caption(
    "Estimate emissions generated while transporting products from the Port of Los Angeles to warehouses and distribution centers."
)

st.divider()

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    truck_type = st.selectbox(
        "Truck Type",
        [
            "Diesel",
            "Hybrid",
            "Electric"
        ]
    )

    distance = st.number_input(
        "Transportation Distance (km)",
        value=1850,
        step=50
    )

with right:

    cargo_weight = st.number_input(
        "Cargo Weight (tons)",
        value=4800,
        step=100
    )

    load_factor = st.slider(
        "Truck Load Factor (%)",
        50,
        100,
        85
    )

##############################################################
# EMISSION FACTORS
##############################################################

if truck_type == "Diesel":
    emission_factor = 0.18

elif truck_type == "Hybrid":
    emission_factor = 0.11

else:
    emission_factor = 0.04

##############################################################
# CALCULATIONS
##############################################################

base = cargo_weight * distance * emission_factor

load_reduction = (load_factor - 50) * 0.004

emissions = base * (1 - load_reduction)

TOTAL = 34200

share = emissions / TOTAL * 100

##############################################################
# KPI CARDS
##############################################################

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "Truck Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with b:

    st.metric(
        "% of Total",
        f"{share:.1f}%"
    )

with c:

    st.metric(
        "Truck Type",
        truck_type
    )

with d:

    st.metric(
        "Load Factor",
        f"{load_factor}%"
    )

st.divider()

##############################################################
# CHARTS
##############################################################

comparison = pd.DataFrame({

    "Truck":[
        "Diesel",
        "Hybrid",
        "Electric"
    ],

    "Emission Factor":[
        0.18,
        0.11,
        0.04
    ]

})

left, right = st.columns(2)

with left:

    st.subheader("Truck Type Comparison")

    fig = px.bar(

        comparison,

        x="Truck",

        y="Emission Factor",

        color="Truck"

    )

    fig.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font_color="white",

        height=420

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Current Logistics Metrics")

    metrics = pd.DataFrame({

        "Category":[
            "Driving",
            "Fuel",
            "Idle Time",
            "Loading"
        ],

        "Emissions":[
            emissions*0.62,
            emissions*0.18,
            emissions*0.10,
            emissions*0.10
        ]

    })

    pie = px.pie(

        metrics,

        names="Category",

        values="Emissions",

        hole=.60

    )

    pie.update_layout(

        paper_bgcolor="#0f172a",

        font_color="white",

        height=420

    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

##############################################################
# PERFORMANCE SCORE
##############################################################

st.divider()

st.subheader("Fleet Performance")

score = round(

    load_factor * 0.55 +

    (100 - emission_factor * 300) * 0.45

)

score = max(0, min(score,100))

st.metric(
    "Fleet Sustainability Score",
    f"{score}/100"
)

st.progress(score/100)

##############################################################
# CARBON INTENSITY
##############################################################

intensity = emissions / cargo_weight

st.metric(

    "Carbon Intensity",

    f"{intensity:.2f} kg CO₂e / ton"

)

##############################################################
# RECOMMENDATIONS
##############################################################

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""

### ⚡ Electrify Fleet

Transition diesel trucks to electric vehicles.

Expected Reduction

40–75%

""")

    st.info("""

### 📦 Increase Load Factor

Ship fuller loads to reduce trips.

Expected Reduction

5–15%

""")

with col2:

    st.info("""

### 🛣 Route Optimization

Reduce unnecessary mileage.

Expected Reduction

5–12%

""")

    st.info("""

### 🚦 Reduce Idle Time

Improve scheduling and loading efficiency.

Expected Reduction

2–8%

""")

##############################################################
# EXECUTIVE SUMMARY
##############################################################

st.divider()

st.subheader("Executive Summary")

st.write(f"""

Current inland trucking emissions are approximately
**{emissions:,.0f} kg CO₂e**.

This transportation stage contributes about
**{share:.1f}%** of the supply chain's total
greenhouse gas emissions.

Selecting lower-carbon vehicles and improving
truck utilization provides the greatest opportunity
for reducing emissions during inland distribution.

""")