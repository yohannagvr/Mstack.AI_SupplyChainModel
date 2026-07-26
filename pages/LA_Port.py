import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="LA Port", layout="wide")

st.title(" Los Angeles Port Operations")

st.caption(
    "Analyze emissions generated during cargo handling, unloading, storage, and terminal operations at the Port of Los Angeles."
)

st.divider()

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    containers = st.number_input(
        "Containers Processed (TEU)",
        value=240,
        step=10
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / TEU)",
        value=14.5,
        step=0.5
    )

with right:

    electric_equipment = st.slider(
        "Electric Cargo Equipment (%)",
        0,
        100,
        35
    )

    terminal_efficiency = st.slider(
        "Terminal Efficiency (%)",
        50,
        100,
        82
    )

##############################################################
# CALCULATIONS
##############################################################

base = containers * emission_factor

equipment_reduction = electric_equipment * 0.002

efficiency_reduction = (terminal_efficiency - 50) * 0.003

emissions = base * (
    1
    - equipment_reduction
    - efficiency_reduction
)

TOTAL = 34200

share = emissions / TOTAL * 100

##############################################################
# KPI CARDS
##############################################################

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "Port Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with b:

    st.metric(
        "% of Total",
        f"{share:.1f}%"
    )

with c:

    st.metric(
        "Equipment Electrified",
        f"{electric_equipment}%"
    )

with d:

    st.metric(
        "Efficiency Score",
        f"{terminal_efficiency}%"
    )

st.divider()

##############################################################
# CHARTS
##############################################################

chart = pd.DataFrame({

    "Source":[
        "Cargo Equipment",
        "Container Handling",
        "Terminal Lighting",
        "Buildings"
    ],

    "Emissions":[
        emissions*.45,
        emissions*.30,
        emissions*.15,
        emissions*.10
    ]

})

left, right = st.columns(2)

with left:

    st.subheader("Operational Emissions")

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

        height=430

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Emission Breakdown")

    pie = px.pie(

        chart,

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
# TERMINAL SCORECARD
##############################################################

st.divider()

st.subheader("Terminal Sustainability Score")

score = round(
    (electric_equipment * 0.6)
    + (terminal_efficiency * 0.4)
)

progress_color = "🟢"

if score < 50:
    progress_color = "🔴"

elif score < 75:
    progress_color = "🟡"

st.metric(
    "Overall Sustainability Score",
    f"{score}/100"
)

st.progress(score/100)

st.write(f"{progress_color} Current operational sustainability rating.")

##############################################################
# REDUCTION OPPORTUNITIES
##############################################################

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""

###  Electrify Cargo Equipment

Transition diesel equipment to electric cranes and yard tractors.

Expected Reduction

15–30%

""")

    st.info("""

### Renewable Electricity

Increase renewable energy usage across terminal operations.

Expected Reduction

5–20%

""")

with col2:

    st.info("""

### Reduce Truck Idling

Improve scheduling and appointment systems.

Expected Reduction

5–15%

""")

    st.info("""

### Smart Terminal Automation

Use AI-driven logistics to reduce unnecessary equipment movement.

Expected Reduction

3–10%

""")

##############################################################
# EXECUTIVE SUMMARY
##############################################################

st.divider()

st.subheader("Executive Summary")

st.write(f"""

The Port of Los Angeles currently contributes approximately
**{emissions:,.0f} kg CO₂e**, representing about
**{share:.1f}%** of total supply chain emissions.

The largest contributors are cargo handling equipment and
container movement. Electrification and operational efficiency
offer the greatest opportunities for emissions reduction.

""")