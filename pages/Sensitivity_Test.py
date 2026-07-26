import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Scenario Analysis",
    layout="wide"
)

st.title("🧪 Sensitivity Testing & Scenario Analysis")

st.caption(
    "Evaluate how operational decisions affect total supply chain emissions."
)

st.divider()

#############################################################
# BASELINE
#############################################################

BASELINE = 34200

#############################################################
# INPUTS
#############################################################

left,right = st.columns(2)

with left:

    vessel = st.selectbox(

        "Vessel Type",

        [
            "Conventional",
            "Panamax",
            "New Panamax"
        ]

    )

    shipments = st.selectbox(

        "Shipping Frequency",

        [
            "24 Shipments / Year",
            "12 Shipments / Year"
        ]

    )

with right:

    load = st.selectbox(

        "Container Fill",

        [
            "80%",
            "95%"
        ]

    )

    grid = st.selectbox(

        "Manufacturing Grid",

        [
            "Coal Heavy",
            "Partial Renewable"
        ]

    )

#############################################################
# CALCULATE REDUCTIONS
#############################################################

scenario = BASELINE

if vessel=="Panamax":
    scenario *= .92

elif vessel=="New Panamax":
    scenario *= .84

if shipments=="12 Shipments / Year":
    scenario *= .93

if load=="95%":
    scenario *= .90

if grid=="Partial Renewable":
    scenario *= .82

reduction = BASELINE-scenario

percent = reduction/BASELINE*100

#############################################################
# KPI CARDS
#############################################################

a,b,c,d = st.columns(4)

with a:

    st.metric(

        "Baseline",

        f"{BASELINE:,.0f} kg"

    )

with b:

    st.metric(

        "Scenario",

        f"{scenario:,.0f} kg"

    )

with c:

    st.metric(

        "Reduction",

        f"{reduction:,.0f} kg"

    )

with d:

    st.metric(

        "% Improvement",

        f"{percent:.1f}%"

    )

st.divider()

#############################################################
# BAR CHART
#############################################################

compare = pd.DataFrame({

    "Scenario":[

        "Baseline",

        "Optimized"

    ],

    "Emissions":[

        BASELINE,

        scenario

    ]

})

left,right = st.columns(2)

with left:

    st.subheader("Baseline vs Optimized")

    fig = px.bar(

        compare,

        x="Scenario",

        y="Emissions",

        color="Scenario",

        text="Emissions"

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

#############################################################
# WATERFALL STYLE
#############################################################

with right:

    st.subheader("Improvement")

    waterfall = go.Figure(go.Waterfall(

        orientation="v",

        measure=["absolute","relative"],

        x=["Baseline","Reduction"],

        y=[BASELINE,-reduction]

    ))

    waterfall.update_layout(

        paper_bgcolor="#0f172a",

        font_color="white",

        height=430

    )

    st.plotly_chart(

        waterfall,

        use_container_width=True

    )

#############################################################
# GAUGE
#############################################################

st.divider()

st.subheader("Overall Reduction")

gauge = go.Figure(go.Indicator(

    mode="gauge+number",

    value=percent,

    number={"suffix":"%"},

    gauge={

        "axis":{"range":[0,50]},

        "bar":{"color":"green"}

    }

))

gauge.update_layout(

    paper_bgcolor="#0f172a",

    font_color="white",

    height=350

)

st.plotly_chart(

    gauge,

    use_container_width=True

)

#############################################################
# EXECUTIVE RECOMMENDATION
#############################################################

st.divider()

st.subheader("Executive Recommendation")

if percent>25:

    st.success("""

Excellent scenario.

The selected operational changes provide
a significant reduction in greenhouse
gas emissions and should be considered
for implementation.

""")

elif percent>15:

    st.warning("""

Moderate improvement.

Additional optimization opportunities
remain throughout the supply chain.

""")

else:

    st.error("""

Minimal improvement.

Consider changing vessel type,
increasing load factor,
or using renewable manufacturing energy.

""")

#############################################################
# SUMMARY TABLE
#############################################################

st.divider()

summary = pd.DataFrame({

    "Decision":[

        "Vessel",

        "Shipments",

        "Container Fill",

        "Manufacturing Grid"

    ],

    "Selection":[

        vessel,

        shipments,

        load,

        grid

    ]

})

st.subheader("Scenario Summary")

st.dataframe(

    summary,

    use_container_width=True,

    hide_index=True

)