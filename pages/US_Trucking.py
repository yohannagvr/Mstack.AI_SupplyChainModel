import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="US Trucking",
    layout="wide"
)

st.title("🚛 U.S. Inland Trucking")

st.caption(
    "Analyze emissions generated while transporting products "
    "from the Port of Los Angeles to the distribution facility "
    "under Scenario A."
)

st.divider()

##############################################################
# SCENARIO A DATA
##############################################################

CARGO_WEIGHT = 21.0
DISTANCE = 320.0
EMISSION_FACTOR = 0.062

TOTAL_SUPPLY_CHAIN = 11221

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    cargo_weight = st.number_input(
        "Cargo Weight (MT)",
        min_value=0.0,
        value=CARGO_WEIGHT,
        step=1.0
    )

    distance = st.number_input(
        "Transportation Distance (km)",
        min_value=0.0,
        value=DISTANCE,
        step=10.0
    )

with right:

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / tonne-km)",
        min_value=0.0,
        value=EMISSION_FACTOR,
        step=0.001,
        format="%.3f"
    )

    truck_type = st.selectbox(
        "Vehicle Type",
        [
            "Diesel HGV (>26 tonnes)"
        ]
    )

##############################################################
# CALCULATION
##############################################################

emissions = (
    cargo_weight
    * distance
    * emission_factor
)

share = (
    emissions
    / TOTAL_SUPPLY_CHAIN
    * 100
)

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
        "Distance",
        f"{distance:,.0f} km"
    )

with d:

    st.metric(
        "Cargo",
        f"{cargo_weight:,.0f} MT"
    )

st.divider()

##############################################################
# EMISSION FACTOR INFORMATION
##############################################################

st.subheader("Emission Factor & Methodology")

st.info("""
### Diesel Heavy Goods Vehicle (>26 tonnes)

**Emission Factor:** 0.062 kg CO₂e / tonne-km

**Sources:** EPA MOVES / GLEC Framework

The factor represents laden heavy-goods vehicle transportation.
Unladen travel can have a higher emissions intensity per
tonne-kilometer.
""")

##############################################################
# CALCULATION BREAKDOWN
##############################################################

st.subheader("Emission Calculation")

calculation = pd.DataFrame({

    "Input": [
        "Cargo Weight",
        "Transportation Distance",
        "Emission Factor"
    ],

    "Value": [
        f"{cargo_weight:,.0f} MT",
        f"{distance:,.0f} km",
        f"{emission_factor:.3f} kg CO₂e / tonne-km"
    ]

})

st.dataframe(
    calculation,
    use_container_width=True,
    hide_index=True
)

st.success(
    f"""
**Calculation:**

{cargo_weight:,.0f} MT × {distance:,.0f} km ×
{emission_factor:.3f} kg CO₂e/tonne-km

= **{emissions:,.0f} kg CO₂e per shipment**
"""
)

##############################################################
# CHARTS
##############################################################

left, right = st.columns(2)

##############################################################
# EMISSION INTENSITY
##############################################################

with left:

    st.subheader("Transportation Emission Factor")

    comparison = pd.DataFrame({

        "Transportation Mode": [
            "Diesel HGV (>26 tonnes)"
        ],

        "Emission Factor": [
            emission_factor
        ]

    })

    fig = px.bar(

        comparison,

        x="Transportation Mode",

        y="Emission Factor",

        color="Emission Factor",

        color_continuous_scale="Viridis"

    )

    fig.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font_color="white",

        height=420,

        coloraxis_showscale=False,

        yaxis_title="kg CO₂e / tonne-km",

        xaxis_title=""

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

##############################################################
# SUPPLY CHAIN SHARE
##############################################################

with right:

    st.subheader("Share of Scenario A Footprint")

    other_emissions = max(
        TOTAL_SUPPLY_CHAIN - emissions,
        0
    )

    share_data = pd.DataFrame({

        "Category": [
            "U.S. Inland Trucking",
            "Other Supply Chain Legs"
        ],

        "Emissions": [
            emissions,
            other_emissions
        ]

    })

    pie = px.pie(

        share_data,

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
# CARBON INTENSITY
##############################################################

st.divider()

st.subheader("Carbon Intensity")

intensity = emissions / cargo_weight

a, b = st.columns(2)

with a:

    st.metric(
        "Carbon Intensity",
        f"{intensity:.2f} kg CO₂e / MT"
    )

with b:

    st.metric(
        "Emission Factor",
        f"{emission_factor:.3f} kg CO₂e / tonne-km"
    )

##############################################################
# SCENARIO A CONTEXT
##############################################################

st.divider()

st.subheader("Scenario A Supply Chain Context")

context = pd.DataFrame({

    "Supply Chain Leg": [

        "Chemical Manufacturing",
        "Ocean Freight",
        "U.S. Inland Trucking",
        "Warehousing / Storage",
        "Factory-to-Port Trucking",
        "U.S. Port Handling",
        "Origin Port Handling"

    ],

    "Emissions (kg CO₂e)": [

        7140,
        3489,
        416,
        86,
        59,
        19,
        12

    ]

})

context["Share (%)"] = (

    context["Emissions (kg CO₂e)"]
    / TOTAL_SUPPLY_CHAIN
    * 100

)

context["Share (%)"] = (
    context["Share (%)"].round(1)
)

context = context.sort_values(
    "Emissions (kg CO₂e)",
    ascending=False
)

st.dataframe(
    context,
    use_container_width=True,
    hide_index=True
)

##############################################################
# REDUCTION OPPORTUNITIES
##############################################################

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Route Optimization

Reduce unnecessary transportation distance through
route planning and distribution-network optimization.

**Primary lever:** Reduce tonne-km traveled.
""")

    st.info("""
### Increase Truck Utilization

Improve shipment consolidation and truck utilization
to avoid unnecessary trips.

**Primary lever:** Move more cargo per trip.
""")

with col2:

    st.info("""
### Lower-Carbon Trucking

Evaluate lower-carbon trucking technologies and fuels
as they become available for the required route.

**Primary lever:** Reduce kg CO₂e per tonne-km.
""")

    st.info("""
### Reduce Empty Miles

Coordinate inbound and outbound transportation to
reduce unnecessary empty vehicle movements.

**Primary lever:** Improve overall vehicle utilization.
""")

##############################################################
# EXECUTIVE SUMMARY
##############################################################

st.divider()

st.subheader("Executive Summary")

st.write(f"""
U.S. inland trucking contributes approximately
**{emissions:,.0f} kg CO₂e per Scenario A shipment**.

Based on the current model, this represents approximately
**{share:.1f}%** of the total Scenario A supply-chain footprint
of **{TOTAL_SUPPLY_CHAIN:,.0f} kg CO₂e**.

The Scenario A trucking leg consists of **{cargo_weight:,.0f} MT**
of cargo transported approximately **{distance:,.0f} km** using a
diesel heavy goods vehicle with an emission factor of
**{emission_factor:.3f} kg CO₂e per tonne-km**.

Compared with chemical manufacturing and ocean freight, U.S.
inland trucking is a smaller contributor to the overall footprint.
However, reducing transportation distance, improving truck
utilization, and transitioning to lower-carbon freight
technologies can still reduce emissions.
""")