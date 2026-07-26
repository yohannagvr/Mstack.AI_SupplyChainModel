import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Warehouse",
    layout="wide"
)

st.title("🏢 Warehousing & Distribution")

st.caption(
    "Estimate emissions generated during warehouse operations and distribution activities."
)

st.divider()

##############################################################
# INPUTS
##############################################################

left, right = st.columns(2)

with left:

    warehouse_area = st.number_input(
        "Warehouse Size (m²)",
        value=25000,
        step=1000
    )

    electricity = st.number_input(
        "Annual Electricity Usage (kWh)",
        value=1250000,
        step=50000
    )

with right:

    renewable = st.slider(
        "Renewable Electricity (%)",
        0,
        100,
        30
    )

    electric_forklifts = st.slider(
        "Electric Forklifts (%)",
        0,
        100,
        60
    )

##############################################################
# CALCULATIONS
##############################################################

grid_factor = 0.40

base = electricity * grid_factor

renewable_reduction = renewable * 0.003

forklift_reduction = electric_forklifts * 0.002

emissions = base * (
    1
    - renewable_reduction
    - forklift_reduction
)

TOTAL = 34200

share = emissions / TOTAL * 100

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
        "% of Total",
        f"{share:.1f}%"
    )

with c:

    st.metric(
        "Warehouse Size",
        f"{warehouse_area:,} m²"
    )

with d:

    st.metric(
        "Renewable Energy",
        f"{renewable}%"
    )

st.divider()

##############################################################
# BREAKDOWN
##############################################################

breakdown = pd.DataFrame({

    "Source":[
        "Lighting",
        "HVAC",
        "Forklifts",
        "Equipment",
        "Office"
    ],

    "Emissions":[
        emissions*.20,
        emissions*.35,
        emissions*.22,
        emissions*.15,
        emissions*.08
    ]

})

left, right = st.columns(2)

with left:

    st.subheader("Warehouse Emissions")

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
# SUSTAINABILITY SCORE
##############################################################

st.divider()

st.subheader("Warehouse Sustainability Score")

score = round(
    renewable * 0.6 +
    electric_forklifts * 0.4
)

st.metric(
    "Overall Score",
    f"{score}/100"
)

st.progress(score/100)

##############################################################
# RECOMMENDATIONS
##############################################################

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""

### ☀ Install Solar Panels

Reduce grid electricity dependence.

Expected Reduction

15–40%

""")

    st.info("""

### ⚡ Electrify Equipment

Replace propane equipment with electric alternatives.

Expected Reduction

10–25%

""")

with col2:

    st.info("""

### 💡 LED Lighting

Upgrade warehouse lighting systems.

Expected Reduction

5–12%

""")

    st.info("""

### ❄ HVAC Optimization

Use smart climate control systems.

Expected Reduction

8–18%

""")

##############################################################
# EXECUTIVE SUMMARY
##############################################################

st.divider()

st.subheader("Executive Summary")

st.write(f"""

Current warehouse emissions are estimated at
**{emissions:,.0f} kg CO₂e**.

This stage contributes approximately
**{share:.1f}%** of total supply chain emissions.

Increasing renewable electricity usage,
electrifying forklifts,
and improving HVAC efficiency represent the
largest opportunities for reducing emissions
within warehouse operations.

""")