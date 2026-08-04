import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Ocean Freight",
    layout="wide"
)

st.title("Ocean Freight")

st.caption(
    "Analyze greenhouse gas emissions from international ocean "
    "transportation under Scenario A."
)

st.divider()

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    cargo = st.number_input(
        "Cargo Weight (MT)",
        min_value=0.0,
        value=21.0,
        step=1.0
    )

    distance = st.number_input(
        "Ocean Distance (km)",
        min_value=0.0,
        value=14200.0,
        step=100.0
    )

with right:

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / tonne-km)",
        min_value=0.0,
        value=0.0117,
        step=0.0001,
        format="%.4f"
    )

    vessel_type = st.selectbox(
        "Vessel / Fuel Methodology",
        [
            "Average Container Vessel — HFO"
        ]
    )

##############################################################
# CALCULATION
##############################################################

emissions = cargo * distance * emission_factor

# Scenario A total supply-chain emissions
TOTAL = 11221

share = emissions / TOTAL * 100

##############################################################
# KPI
##############################################################

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "Ocean Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with b:

    st.metric(
        "% of Total",
        f"{share:.1f}%"
    )

with c:

    st.metric(
        "Ocean Distance",
        f"{distance:,.0f} km"
    )

with d:

    st.metric(
        "Cargo",
        f"{cargo:,.0f} MT"
    )

st.divider()

##############################################################
# EMISSION FACTOR INFORMATION
##############################################################

st.subheader("Emission Factor & Methodology")

st.info("""
### Container Ocean Freight — Average Vessel, HFO

**Emission Factor:** 0.0117 kg CO₂e / tonne-km

**Source:** GLEC Framework v3 / IMO GHG Study 2023

**Methodology:** Well-to-wake

The factor represents average container-vessel emissions and can
vary depending on vessel age, vessel efficiency, and load factor.

Scenario A uses a cargo weight of **21 MT** transported over
**14,200 km**.
""")

##############################################################
# CALCULATION BREAKDOWN
##############################################################

st.subheader("Emission Calculation")

calculation = pd.DataFrame({

    "Input": [
        "Cargo Weight",
        "Ocean Distance",
        "Emission Factor"
    ],

    "Value": [
        f"{cargo:,.0f} MT",
        f"{distance:,.0f} km",
        f"{emission_factor:.4f} kg CO₂e / tonne-km"
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

{cargo:,.0f} MT × {distance:,.0f} km ×
{emission_factor:.4f} kg CO₂e/tonne-km

= **{emissions:,.0f} kg CO₂e per shipment**
"""
)

##############################################################
# CHARTS
##############################################################

left, right = st.columns([1.1, 1])

##############################################################
# CHART 1
##############################################################

with left:

    st.subheader("Ocean Freight Emissions")

    chart = pd.DataFrame({

        "Stage": [
            "Ocean Freight"
        ],

        "Emissions": [
            emissions
        ]

    })

    fig = px.bar(

        chart,

        x="Stage",

        y="Emissions",

        color="Emissions",

        color_continuous_scale="Viridis"

    )

    fig.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font_color="white",

        height=420,

        coloraxis_showscale=False

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

##############################################################
# CHART 2
##############################################################

with right:

    st.subheader("Share of Supply Chain")

    pie_data = pd.DataFrame({

        "Category": [
            "Ocean Freight",
            "All Other Supply Chain Legs"
        ],

        "Emissions": [
            emissions,
            max(TOTAL - emissions, 0)
        ]

    })

    pie = px.pie(

        pie_data,

        values="Emissions",

        names="Category",

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
# CONTRIBUTION
##############################################################

st.divider()

st.subheader("Contribution")

if share > 40:

    st.error(f"""
Ocean freight is the dominant source of emissions in Scenario A,
contributing approximately **{share:.1f}%** of the total footprint.
""")

elif share > 25:

    st.warning(f"""
Ocean freight is a major contributor to the Scenario A carbon
footprint, accounting for approximately **{share:.1f}%** of total
emissions.

Chemical manufacturing remains the larger emissions source at
approximately **63.6%** of the total footprint.
""")

else:

    st.success(f"""
Ocean freight contributes approximately **{share:.1f}%** of the
Scenario A carbon footprint.
""")

##############################################################
# SCENARIO A CONTEXT
##############################################################

st.divider()

st.subheader("Scenario A Emission Context")

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
    / TOTAL
    * 100
)

context["Share (%)"] = context["Share (%)"].round(1)

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

st.subheader("Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### 🌱 Lower-Carbon Marine Fuels

Transition from conventional HFO toward lower-carbon marine fuels,
including sustainable biofuel blends.

**Potential strategy:** Reduce well-to-wake emissions associated
with ocean transportation.
""")

    st.info("""
### 🚢 Improve Vessel Efficiency

Use more efficient vessels and optimize vessel operations,
including routing, speed, and loading.

**Potential strategy:** Reduce fuel consumption per tonne-km.
""")

with col2:

    st.info("""
### 📦 Increase Container Utilization

Improve cargo utilization so available container capacity is used
more efficiently.

**Potential strategy:** Reduce emissions allocated to each unit of
cargo transported.
""")

    st.info("""
### 📍 Optimize Shipping Routes

Evaluate routes, transshipment requirements, and sailing distances
to minimize unnecessary ocean distance.

**Potential strategy:** Reduce total tonne-km traveled.
""")

##############################################################
# EXECUTIVE INSIGHT
##############################################################

st.divider()

st.subheader("Executive Insight")

st.write(f"""
Ocean freight produces approximately **{emissions:,.0f} kg CO₂e per
Scenario A shipment**, based on **{cargo:,.0f} MT** of cargo traveling
**{distance:,.0f} km**.

This represents approximately **{share:.1f}%** of the total
Scenario A supply-chain footprint.

The calculated emissions are based on the **GLEC Framework v3 /
IMO GHG Study 2023** emission factor of **0.0117 kg CO₂e per
tonne-km** for average container ocean freight using HFO.

Ocean freight is the **second-largest emissions source** in
Scenario A after chemical manufacturing. Together, chemical
manufacturing and ocean freight account for approximately
**94.7% of the total calculated footprint**, making these two
stages the highest-priority areas for emissions reduction.
""")