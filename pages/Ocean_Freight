import streamlit as st
import plotly.express as px
import pandas as pd

st.set_page_config(page_title="Ocean Freight", layout="wide")

st.title("🚢 Ocean Freight")

st.caption(
    "Analyze greenhouse gas emissions from international ocean transportation."
)

st.divider()

##############################################################
# INPUTS
##############################################################

left,right = st.columns(2)

with left:

    vessel = st.selectbox(
        "Vessel Type",
        [
            "Conventional Container Ship",
            "Panamax",
            "New Panamax"
        ]
    )

    distance = st.number_input(
        "Distance (km)",
        value=13300
    )

with right:

    containers = st.number_input(
        "Containers (TEU)",
        value=240
    )

    load = st.slider(
        "Container Fill (%)",
        50,
        100,
        80
    )

##############################################################
# EMISSION FACTORS
##############################################################

if vessel=="Conventional Container Ship":
    factor=.090

elif vessel=="Panamax":
    factor=.075

else:
    factor=.060

##############################################################
# CALCULATION
##############################################################

tonnes_per_container = 20

cargo = containers * tonnes_per_container

emissions = cargo * distance * factor

emissions *= (100-load+80)/100

TOTAL = 34200

share = emissions/TOTAL*100

##############################################################
# KPI
##############################################################

a,b,c,d = st.columns(4)

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
        "Distance",
        f"{distance:,} km"
    )

with d:

    st.metric(
        "Vessel",
        vessel
    )

st.divider()

##############################################################
# CHARTS
##############################################################

left,right=st.columns([1.1,1])

##############################################################

with left:

    st.subheader("Emission Breakdown")

    chart=pd.DataFrame({

        "Category":[

            "Fuel",
            "Engine",
            "Auxiliary",
            "Refrigeration"

        ],

        "Emissions":[

            emissions*.74,
            emissions*.13,
            emissions*.08,
            emissions*.05

        ]

    })

    fig=px.bar(

        chart,

        x="Category",

        y="Emissions",

        color="Emissions",

        color_continuous_scale="Viridis"

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

##############################################################

with right:

    st.subheader("Emission Sources")

    pie=px.pie(

        chart,

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
# SUMMARY
##############################################################

st.divider()

st.subheader("Contribution")

if share>45:

    st.error("""

Ocean Freight is currently the dominant
source of emissions across the supply chain.

Reducing emissions in this stage will have
the largest impact.

""")

elif share>25:

    st.warning("""

Ocean Freight is a major contributor
to the company's carbon footprint.

""")

else:

    st.success("""

Ocean Freight emissions are relatively
low compared to the total supply chain.

""")

##############################################################
# REDUCTIONS
##############################################################

st.divider()

st.subheader("Reduction Opportunities")

col1,col2=st.columns(2)

with col1:

    st.info("""

### 🚢 Upgrade Vessel

Using newer ships can reduce fuel
consumption significantly.

Estimated Reduction

15-30%

""")

    st.info("""

### 📦 Improve Container Fill

Increase utilization from 80%
to 95%.

Estimated Reduction

8-18%

""")

with col2:

    st.info("""

### 🌱 Sustainable Marine Fuel

Transition toward biofuels or
green methanol.

Estimated Reduction

25-60%

""")

    st.info("""

### 📅 Reduce Shipping Frequency

Ship larger loads less often.

Estimated Reduction

5-15%

""")

##############################################################
# QUICK FACTS
##############################################################

st.divider()

st.subheader("Executive Insight")

st.write(f"""

Ocean freight currently emits approximately
**{emissions:,.0f} kg CO₂e**.

This represents **{share:.1f}%** of total
supply chain emissions.

For international supply chains,
ocean transportation is commonly the
largest emissions hotspot, making it
the highest priority for sustainability
initiatives.

""")