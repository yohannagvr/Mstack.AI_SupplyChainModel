import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Warehouse",
    layout="wide"
)

st.title("Warehousing & Distribution")

st.caption(
    "Analyze emissions generated while products are stored "
    "and handled within the U.S. warehouse and distribution network."
)

st.divider()

##############################################################
# SCENARIO A DATA
##############################################################

CARGO_WEIGHT = 21.0
DWELL_TIME = 0.5
EMISSION_FACTOR = 8.2

TOTAL_SUPPLY_CHAIN = 11221

# Official Scenario A value from supplied model
BASELINE_EMISSIONS = 86

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    cargo_weight = st.number_input(
        "Material Stored (MT)",
        min_value=0.0,
        value=CARGO_WEIGHT,
        step=1.0
    )

    dwell_time = st.number_input(
        "Average Warehouse Dwell Time (months)",
        min_value=0.0,
        value=DWELL_TIME,
        step=0.25
    )

with right:

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / MT / month)",
        min_value=0.0,
        value=EMISSION_FACTOR,
        step=0.1
    )

    scenario = st.selectbox(
        "Modeling Basis",
        [
            "Scenario A — Baseline",
            "Custom Sensitivity"
        ]
    )

##############################################################
# CALCULATIONS
##############################################################

calculated_emissions = (
    cargo_weight
    * dwell_time
    * emission_factor
)

# Use official Scenario A value when baseline inputs are selected
if (
    scenario == "Scenario A — Baseline"
    and cargo_weight == CARGO_WEIGHT
    and dwell_time == DWELL_TIME
    and emission_factor == EMISSION_FACTOR
):

    emissions = BASELINE_EMISSIONS

else:

    emissions = calculated_emissions

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
        "Warehouse Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with b:

    st.metric(
        "Share of Scenario A",
        f"{share:.1f}%"
    )

with c:

    st.metric(
        "Material Stored",
        f"{cargo_weight:,.0f} MT"
    )

with d:

    st.metric(
        "Average Dwell",
        f"{dwell_time:.2f} months"
    )

st.divider()

##############################################################
# METHODOLOGY
##############################################################

st.subheader("Emission Factor & Methodology")

st.info("""
### U.S. Warehouse Storage

**Emission Factor:** 8.2 kg CO₂e / MT / month

**Source:** GHG Protocol Scope 3 / EPA eGRID

The factor represents emissions associated with warehouse
storage based on material quantity and average dwell time.

Scenario A assumes **21 MT** of material with an average
warehouse dwell time of **0.5 months**.
""")

##############################################################
# CALCULATION
##############################################################

st.subheader("Emission Calculation")

calculation = pd.DataFrame({

    "Input": [
        "Material Stored",
        "Average Dwell Time",
        "Emission Factor"
    ],

    "Value": [
        f"{cargo_weight:,.0f} MT",
        f"{dwell_time:.2f} months",
        f"{emission_factor:.1f} kg CO₂e / MT / month"
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

{cargo_weight:,.0f} MT × {dwell_time:.2f} months ×
{emission_factor:.1f} kg CO₂e/MT/month

Calculated result:
**{calculated_emissions:,.2f} kg CO₂e**

Scenario A reported value:
**{emissions:,.0f} kg CO₂e**
"""
)

##############################################################
# EMISSION BREAKDOWN
##############################################################

st.divider()

st.subheader("Warehouse Emission Sources")

# Operational breakdown used for visualization only.
# The total remains tied to the documented warehouse
# emission factor calculation above.

breakdown = pd.DataFrame({

    "Source": [
        "Lighting",
        "HVAC",
        "Material Handling",
        "Building Systems",
        "Other Operations"
    ],

    "Emissions": [
        emissions * 0.20,
        emissions * 0.35,
        emissions * 0.22,
        emissions * 0.15,
        emissions * 0.08
    ]

})

left, right = st.columns(2)

with left:

    st.subheader("Operational Emissions")

    fig = px.bar(

        breakdown,

        x="Source",

        y="Emissions",

        color="Emissions",

        color_continuous_scale="Viridis"

    )

    fig.update_layout(

        paper_bgcolor="#0f172a",

        plot_bgcolor="#0f172a",

        font_color="white",

        height=430

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Emission Share")

    pie = px.pie(

        breakdown,

        values="Emissions",

        names="Source",

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
# SCENARIO A SUPPLY CHAIN CONTEXT
##############################################################

st.divider()

st.subheader("Scenario A Supply Chain Context")

context = pd.DataFrame({

    "Supply Chain Leg": [

        "Chemical Manufacturing",
        "Ocean Freight",
        "U.S. Inland Trucking",
        "Warehousing / Distribution",
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
# INTERPRETATION
##############################################################

st.divider()

st.subheader("Interpretation")

if share > 10:

    st.error(
        f"""
Warehousing contributes approximately **{share:.1f}%**
of Scenario A emissions and represents a significant
supply-chain emissions source.
"""
    )

elif share > 3:

    st.warning(
        f"""
Warehousing contributes approximately **{share:.1f}%**
of Scenario A emissions and represents a moderate
emissions source.
"""
    )

else:

    st.success(
        f"""
Warehousing contributes approximately **{share:.1f}%**
of Scenario A emissions.

This is a relatively small contributor compared with
chemical manufacturing, ocean freight, and U.S. inland
trucking.
"""
    )

##############################################################
# REDUCTION OPPORTUNITIES
##############################################################

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Renewable Electricity

Increase renewable electricity usage within warehouse
operations.

**Primary lever:** Reduce electricity-related emissions.
""")

    st.info("""
### Electrify Material Handling

Replace fossil-fuel-powered forklifts and handling
equipment with electric alternatives.

**Primary lever:** Reduce operational fuel emissions.
""")

with col2:

    st.info("""
### Energy-Efficient Lighting

Use LED lighting and automated controls to reduce
warehouse electricity demand.

**Primary lever:** Reduce building energy consumption.
""")

    st.info("""
### HVAC Optimization

Improve temperature controls, insulation, and HVAC
efficiency.

**Primary lever:** Reduce heating and cooling energy use.
""")

##############################################################
# EXECUTIVE SUMMARY
##############################################################

st.divider()

st.subheader("Executive Summary")

st.write(f"""
U.S. warehousing and distribution contributes approximately
**{emissions:,.0f} kg CO₂e per Scenario A shipment**.

This represents approximately **{share:.1f}%** of the
**{TOTAL_SUPPLY_CHAIN:,.0f} kg CO₂e** Scenario A supply-chain
footprint.

The calculation is based on **{cargo_weight:,.0f} MT** of material,
an average dwell time of **{dwell_time:.2f} months**, and an emission
factor of **{emission_factor:.1f} kg CO₂e per MT per month**.

Warehousing is a relatively small contributor in the current
Scenario A model. While energy efficiency, renewable electricity,
and electrification can reduce warehouse emissions, the largest
decarbonization opportunities remain concentrated in chemical
manufacturing and ocean freight.
""")