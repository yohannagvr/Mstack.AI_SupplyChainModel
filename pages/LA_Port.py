import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="LA Port", layout="wide")

st.title("US Los Angeles Port — Terminal Operations")

st.write("""
This leg represents container handling and terminal operations at the
U.S. port. Emissions include diesel crane and yard operations associated
with handling the shipment.
""")

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    containers = st.number_input(
        "Containers Processed (TEU)",
        min_value=1,
        value=1,
        step=1
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / TEU)",
        min_value=0.0,
        value=18.7,
        step=0.1
    )

with right:

    scenario = st.selectbox(
        "Scenario",
        ["Scenario A"]
    )

    terminal_type = st.selectbox(
        "Terminal Operations",
        ["Diesel crane + yard operations"]
    )

##############################################################
# CALCULATIONS
##############################################################

emissions = containers * emission_factor

# Scenario A total supply-chain emissions
TOTAL = 11221

share = emissions / TOTAL * 100

##############################################################
# KPI CARDS
##############################################################

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "Port Emissions",
        f"{emissions:,.1f} kg CO₂e"
    )

with b:

    st.metric(
        "% of Total",
        f"{share:.2f}%"
    )

with c:

    st.metric(
        "Containers",
        f"{containers} TEU"
    )

with d:

    st.metric(
        "Emission Factor",
        f"{emission_factor:.1f} kg/TEU"
    )

st.divider()

##############################################################
# EMISSION FACTOR INFORMATION
##############################################################

st.subheader("Emission Factor")

st.info("""
### U.S. Port Terminal Handling

**Emission Factor:** 18.7 kg CO₂e / TEU

**Methodology:** Clean Cargo Working Group

**Scope:** Diesel crane and yard operations

The U.S. port factor is higher than the origin-port factor used
in Scenario A because U.S. terminal operations have a higher
reported emissions intensity.
""")

##############################################################
# CHARTS
##############################################################

chart = pd.DataFrame({

    "Source": [
        "U.S. Port Terminal Handling"
    ],

    "Emissions": [
        emissions
    ]

})

left, right = st.columns(2)

with left:

    st.subheader("Port Emissions")

    fig = px.bar(

        chart,

        x="Source",

        y="Emissions",

        color="Emissions",

        color_continuous_scale="Viridis"

    )

    fig.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font_color="white",

        height=430,

        coloraxis_showscale=False

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Port Share of Supply Chain")

    pie_data = pd.DataFrame({

        "Category": [
            "U.S. Port Handling",
            "All Other Supply Chain Legs"
        ],

        "Emissions": [
            emissions,
            TOTAL - emissions
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

        height=430

    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

##############################################################
# SUPPLY CHAIN CONTEXT
##############################################################

st.divider()

st.subheader("Supply Chain Context")

st.write("""
The U.S. port is one of the smallest contributors to the Scenario A
carbon footprint. While terminal operations are necessary for transferring
the container from ocean transportation to inland transportation, the
associated emissions are relatively small compared with chemical
manufacturing and ocean freight.
""")

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

    "Emissions": [
        7140,
        3489,
        416,
        86,
        59,
        19,
        12
    ]

})

# Calculate each leg's percentage of total emissions
context["Share (%)"] = (
    context["Emissions"] / TOTAL * 100
)

# Rename the emissions column only for display
context_display = context.rename(
    columns={
        "Emissions": "Emissions (kg CO₂e)"
    }
)

st.dataframe(
    context_display,
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
### Electrify Cargo Equipment

Replace diesel-powered cranes, yard tractors, and other terminal
equipment with electric alternatives where infrastructure allows.

Potential benefit:
Lower direct fuel-related emissions from terminal operations.
""")

    st.info("""
### Renewable Electricity

Increase the use of renewable electricity for electrically powered
terminal equipment and facility operations.

Potential benefit:
Further reduction in the emissions intensity of terminal activities.
""")

with col2:

    st.info("""
### Reduce Truck Idling

Improve truck appointment scheduling and terminal coordination to
reduce unnecessary waiting and idling around the port.

Potential benefit:
Lower emissions associated with port-related truck activity.
""")

    st.info("""
### Improve Terminal Efficiency

Optimize container movement, equipment utilization, and yard
organization to reduce unnecessary equipment activity.

Potential benefit:
Lower energy use per container handled.
""")

##############################################################
# EXECUTIVE SUMMARY
##############################################################

st.divider()

st.subheader("Executive Summary")

st.write(f"""
### Key Findings

The U.S. port handling leg contributes approximately
**{emissions:,.1f} kg CO₂e per Scenario A shipment**.

This represents approximately **{share:.2f}%** of the total
Scenario A supply-chain footprint of **{TOTAL:,} kg CO₂e**.

The port emission factor is **18.7 kg CO₂e per TEU**, based on
Clean Cargo Working Group data for U.S. terminal operations.

Compared with the major emissions sources in the supply chain,
U.S. port handling is a relatively minor contributor. Chemical
manufacturing and ocean freight together account for the majority
of the overall footprint.

Therefore, port electrification and efficiency improvements are
useful secondary reduction strategies, but the largest overall
carbon reductions are expected to come from addressing the
manufacturing and ocean-freight legs.
""")