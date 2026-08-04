import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Manufacturing", layout="wide")

# ----------------------------------------------------
# Styling
# ----------------------------------------------------

st.markdown("""
<style>

.main{
    background-color:#0f172a;
}

div[data-testid="metric-container"]{
    background:#1e293b;
    border-radius:12px;
    padding:18px;
    border:1px solid #334155;
}

</style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# Header
# ----------------------------------------------------

st.title("Chemical Manufacturing")

st.caption(
"""
Estimate emissions generated during the chemical manufacturing
stage of the Scenario A supply chain.
"""
)

st.divider()

# ----------------------------------------------------
# User Inputs
# ----------------------------------------------------

left, right = st.columns([1, 1])

with left:

    production = st.number_input(
        "Production Volume per Shipment (MT)",
        min_value=0.0,
        value=21.0,
        step=1.0
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / MT)",
        min_value=0.0,
        value=340.0,
        step=1.0
    )

with right:

    scenario = st.selectbox(
        "Scenario",
        ["Scenario A"]
    )

    manufacturing_region = st.selectbox(
        "Manufacturing Region",
        ["SE Asia"]
    )

# ----------------------------------------------------
# Calculation
# ----------------------------------------------------

base_emissions = production * emission_factor

# Scenario A total supply-chain emissions
TOTAL_SUPPLY_CHAIN = 11221

share = (
    base_emissions / TOTAL_SUPPLY_CHAIN * 100
    if TOTAL_SUPPLY_CHAIN > 0
    else 0
)

# ----------------------------------------------------
# KPIs
# ----------------------------------------------------

st.divider()

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Manufacturing Emissions",
        f"{base_emissions:,.0f} kg CO₂e"
    )

with c2:

    st.metric(
        "Share of Total",
        f"{share:.1f}%"
    )

with c3:

    st.metric(
        "Production Volume",
        f"{production:,.0f} MT"
    )

# ----------------------------------------------------
# Emission Factor Information
# ----------------------------------------------------

st.divider()

st.subheader("Emission Factor & Methodology")

st.info("""
### Specialty Chemical Manufacturing — SE Asia

**Emission Factor:** 340 kg CO₂e / MT produced

**Source:** IEA Chemical Sector Analysis 2024 / Ecoinvent

**Application:** Average specialty chemical manufacturing in
Southeast Asia.

The emission factor is applied directly to the quantity of chemical
produced. It represents the manufacturing-stage carbon footprint
before transportation, port handling, and warehousing emissions are
added.
""")

# ----------------------------------------------------
# Gauge
# ----------------------------------------------------

st.subheader("Contribution to Supply Chain")

fig = go.Figure(go.Indicator(

    mode="gauge+number",

    value=share,

    number={"suffix": "%"},

    title={
        "text": "Manufacturing Share of Scenario A"
    },

    gauge={

        "axis": {
            "range": [0, 100]
        },

        "bar": {
            "color": "green"
        },

        "steps": [

            {"range": [0, 20], "color": "#14532d"},
            {"range": [20, 40], "color": "#166534"},
            {"range": [40, 60], "color": "#facc15"},
            {"range": [60, 80], "color": "#f97316"},
            {"range": [80, 100], "color": "#dc2626"}

        ]

    }

))

fig.update_layout(
    paper_bgcolor="#0f172a",
    font_color="white",
    height=350
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ----------------------------------------------------
# Interpretation
# ----------------------------------------------------

st.subheader("Interpretation")

if share > 40:

    st.error(
        f"""
Manufacturing is the **largest emissions source** in Scenario A.

At **{base_emissions:,.0f} kg CO₂e**, manufacturing represents
approximately **{share:.1f}%** of the total supply-chain footprint.

Because manufacturing accounts for more than half of total emissions,
decarbonizing the production process represents one of the largest
potential opportunities for reducing the overall carbon footprint.
"""
    )

elif share > 20:

    st.warning(
        f"""
Manufacturing contributes a significant portion of the total
supply-chain footprint, accounting for approximately **{share:.1f}%**
of emissions.
"""
    )

else:

    st.success(
        f"""
Manufacturing contributes approximately **{share:.1f}%** of the
total Scenario A carbon footprint.
"""
    )

# ----------------------------------------------------
# Emission Context
# ----------------------------------------------------

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
    context["Emissions (kg CO₂e)"] / TOTAL_SUPPLY_CHAIN
)

context = context.sort_values(
    "Emissions",
    ascending=False
)

st.dataframe(
    context,
    use_container_width=True,
    hide_index=True
)

# ----------------------------------------------------
# Reduction Opportunities
# ----------------------------------------------------

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Renewable Energy

Increase renewable electricity and lower-carbon energy sources
used in chemical manufacturing.

**Potential strategy:** Reduce dependence on carbon-intensive
electricity generation and fossil fuels.
""")

    st.info("""
### Process Optimization

Improve production efficiency, equipment utilization, and process
control to reduce energy consumption per metric ton produced.

**Potential strategy:** Lower energy intensity per MT of chemical.
""")

with col2:

    st.info("""
### Lower-Carbon Feedstocks

Evaluate alternative raw materials and feedstocks with lower
embedded carbon emissions.

**Potential strategy:** Reduce upstream emissions associated with
chemical inputs.
""")

    st.info("""
### Waste Heat Recovery

Recover and reuse heat generated during manufacturing processes.

**Potential strategy:** Reduce additional fuel and electricity
requirements for process heating.
""")

# ----------------------------------------------------
# Notes
# ----------------------------------------------------

st.divider()

st.subheader("Analyst Notes")

notes = st.text_area(
    "Add observations or recommendations..."
)

if st.button("Save Notes"):
    st.success("Notes saved (temporary for now).")