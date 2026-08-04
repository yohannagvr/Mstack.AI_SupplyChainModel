import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Vietnam Port",
    layout="wide"
)

st.title("Vietnam Port Operations")

st.caption(
    "Analyze emissions generated during cargo handling and "
    "terminal operations at the origin port under Scenario A."
)

st.divider()

# ------------------------------------------------
# SCENARIO A DATA
# ------------------------------------------------

TEU_EQUIVALENT = 1
EMISSION_FACTOR = 12.4

# Official Scenario A total from supplied model
TOTAL_SUPPLY_CHAIN = 11221

# Official Scenario A value from supplied table
BASELINE_PORT_EMISSIONS = 12

# ------------------------------------------------
# INPUTS
# ------------------------------------------------

left, right = st.columns(2)

with left:

    containers = st.number_input(
        "Containers Handled (TEU)",
        min_value=0.0,
        value=1.0,
        step=1.0
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / TEU)",
        min_value=0.0,
        value=EMISSION_FACTOR,
        step=0.1
    )

with right:

    scenario_mode = st.selectbox(
        "Modeling Basis",
        [
            "Scenario A — Baseline",
            "Custom Sensitivity"
        ]
    )

    if scenario_mode == "Scenario A — Baseline":

        st.info(
            """
            Scenario A uses 1 TEU equivalent and the
            Clean Cargo Working Group emission factor
            of 12.4 kg CO₂e / TEU.
            """
        )

    else:

        st.info(
            """
            Custom sensitivity allows the number of TEUs
            and emission factor to be adjusted.
            """
        )

# ------------------------------------------------
# CALCULATIONS
# ------------------------------------------------

calculated_emissions = (
    containers
    * emission_factor
)

# Use supplied Scenario A value when baseline is selected
if scenario_mode == "Scenario A — Baseline":

    emissions = BASELINE_PORT_EMISSIONS

else:

    emissions = calculated_emissions

share = (
    emissions
    / TOTAL_SUPPLY_CHAIN
    * 100
)

# ------------------------------------------------
# KPI CARDS
# ------------------------------------------------

st.divider()

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Port Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with c2:

    st.metric(
        "Share of Scenario A",
        f"{share:.1f}%"
    )

with c3:

    st.metric(
        "TEU Equivalent",
        f"{containers:,.0f}"
    )

with c4:

    st.metric(
        "Emission Factor",
        f"{emission_factor:.1f} kg/TEU"
    )

# ------------------------------------------------
# METHODOLOGY
# ------------------------------------------------

st.divider()

st.subheader("Emission Factor & Methodology")

st.info("""
### Origin Port Terminal Handling

**Emission Factor:** 12.4 kg CO₂e / TEU

**Source:** Clean Cargo Working Group

**Scope:** Diesel crane and yard operations.

Scenario A uses **1 TEU equivalent** for the origin-port
handling leg.

The supplied Scenario A model reports approximately
**12 kg CO₂e per shipment** for this stage.
""")

# ------------------------------------------------
# CALCULATION
# ------------------------------------------------

st.subheader("Emission Calculation")

calculation = pd.DataFrame({

    "Input": [
        "Container Volume",
        "Emission Factor",
        "Scenario A Reported Emissions"
    ],

    "Value": [
        f"{containers:,.0f} TEU",
        f"{emission_factor:.1f} kg CO₂e / TEU",
        f"{emissions:,.0f} kg CO₂e"
    ]

})

st.dataframe(
    calculation,
    use_container_width=True,
    hide_index=True
)

# ------------------------------------------------
# GAUGE
# ------------------------------------------------

st.subheader("Contribution to Scenario A")

fig = go.Figure(
    go.Indicator(

        mode="gauge+number",

        value=share,

        number={
            "suffix": "%"
        },

        title={
            "text": "Share of Total Supply Chain Emissions"
        },

        gauge={

            "axis": {
                "range": [0, 10]
            },

            "bar": {
                "color": "green"
            },

            "steps": [

                {
                    "range": [0, 1],
                    "color": "#14532d"
                },

                {
                    "range": [1, 3],
                    "color": "#166534"
                },

                {
                    "range": [3, 5],
                    "color": "#facc15"
                },

                {
                    "range": [5, 10],
                    "color": "#f97316"
                }

            ]

        }

    )
)

fig.update_layout(
    paper_bgcolor="#0f172a",
    font_color="white",
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ------------------------------------------------
# SUPPLY CHAIN CONTEXT
# ------------------------------------------------

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

# ------------------------------------------------
# INTERPRETATION
# ------------------------------------------------

st.divider()

st.subheader("Interpretation")

if share > 10:

    st.warning(
        f"""
Vietnam port operations contribute approximately
**{share:.1f}%** of Scenario A emissions.

Although this is a measurable source, it is not one
of the primary emissions hotspots in the current model.
"""
    )

elif share > 1:

    st.info(
        f"""
Vietnam port operations contribute approximately
**{share:.1f}%** of Scenario A emissions.

The impact is relatively small compared with
manufacturing and ocean transportation.
"""
    )

else:

    st.success(
        f"""
Vietnam port operations contribute approximately
**{share:.1f}%** of Scenario A emissions.

At approximately **{share:.1f}%**, this is one of the
smallest contributors in the current supply-chain model.
"""
    )

# ------------------------------------------------
# REDUCTION STRATEGIES
# ------------------------------------------------

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Electrify Cargo Equipment

Replace diesel cranes and yard equipment with
electric alternatives where feasible.

**Primary lever:** Reduce diesel fuel consumption
during cargo handling.
""")

    st.info("""
### Renewable Electricity

Increase renewable electricity usage for terminal
operations.

**Primary lever:** Reduce electricity-related
emissions.
""")

with col2:

    st.info("""
### Reduce Equipment Idle Time

Improve scheduling and terminal coordination to
reduce unnecessary equipment operation.

**Primary lever:** Reduce operating hours.
""")

    st.info("""
### Terminal Optimization

Improve cargo movement and yard planning to reduce
unnecessary equipment movements.

**Primary lever:** Improve operational efficiency.
""")

# ------------------------------------------------
# EXECUTIVE SUMMARY
# ------------------------------------------------

st.divider()

st.subheader("Executive Summary")

st.write(f"""
Vietnam origin-port operations contribute approximately
**{emissions:,.0f} kg CO₂e per Scenario A shipment**.

This represents approximately **{share:.1f}%** of the
**{TOTAL_SUPPLY_CHAIN:,.0f} kg CO₂e** Scenario A supply-chain
footprint.

The emission factor used is **{emission_factor:.1f} kg CO₂e per TEU**,
based on the Clean Cargo Working Group methodology for diesel
crane and yard operations.

Compared with chemical manufacturing and ocean freight, Vietnam
port handling is a relatively minor contributor. Therefore,
electrification and terminal efficiency improvements are useful
secondary initiatives, while the largest reduction opportunities
remain concentrated in manufacturing and ocean transportation.
""")