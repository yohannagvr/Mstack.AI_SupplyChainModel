import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Scenario Analysis",
    layout="wide"
)

st.title("Sensitivity Testing & Scenario Analysis")

st.caption(
    "Evaluate how changes in supply-chain activity and emission factors "
    "affect the Scenario A carbon footprint."
)

st.divider()

#############################################################
# BASELINE SCENARIO A
#############################################################

BASELINE = 11221

#############################################################
# BASELINE EMISSION FACTORS
#############################################################

MANUFACTURING_EF = 340.0
ORIGIN_TRUCK_EF = 0.062
ORIGIN_PORT_EF = 12.4
OCEAN_EF = 0.0117
US_PORT_EF = 18.7
US_TRUCK_EF = 0.062
WAREHOUSE_EF = 8.2

#############################################################
# BASELINE ACTIVITY DATA
#############################################################

MANUFACTURING_MT = 21
ORIGIN_TRUCK_DISTANCE = 45
ORIGIN_TEUS = 1
OCEAN_DISTANCE = 14200
US_PORT_TEUS = 1
US_TRUCK_DISTANCE = 320
WAREHOUSE_MONTHS = 0.5

#############################################################
# INPUTS
#############################################################

st.subheader("Sensitivity Inputs")

left, right = st.columns(2)

with left:

    st.markdown("### Manufacturing")

    manufacturing_factor = st.number_input(
        "Manufacturing Emission Factor (kg CO₂e / MT)",
        min_value=0.0,
        value=MANUFACTURING_EF,
        step=5.0
    )

    st.markdown("### Ocean Freight")

    ocean_distance = st.number_input(
        "Ocean Distance (km)",
        min_value=0.0,
        value=float(OCEAN_DISTANCE),
        step=100.0
    )

    ocean_factor = st.number_input(
        "Ocean Emission Factor (kg CO₂e / tonne-km)",
        min_value=0.0,
        value=OCEAN_EF,
        step=0.0001,
        format="%.4f"
    )

with right:

    st.markdown("### U.S. Inland Trucking")

    us_truck_distance = st.number_input(
        "U.S. Truck Distance (km)",
        min_value=0.0,
        value=float(US_TRUCK_DISTANCE),
        step=10.0
    )

    st.markdown("### Warehousing")

    warehouse_months = st.number_input(
        "Average Warehouse Dwell Time (months)",
        min_value=0.0,
        value=WAREHOUSE_MONTHS,
        step=0.25
    )

#############################################################
# BASELINE CALCULATIONS
#############################################################

baseline_manufacturing = (
    MANUFACTURING_MT * MANUFACTURING_EF
)

baseline_origin_truck = (
    MANUFACTURING_MT
    * ORIGIN_TRUCK_DISTANCE
    * ORIGIN_TRUCK_EF
)

baseline_origin_port = (
    ORIGIN_TEUS * ORIGIN_PORT_EF
)

baseline_ocean = (
    MANUFACTURING_MT
    * OCEAN_DISTANCE
    * OCEAN_EF
)

baseline_us_port = (
    US_PORT_TEUS * US_PORT_EF
)

baseline_us_truck = (
    MANUFACTURING_MT
    * US_TRUCK_DISTANCE
    * US_TRUCK_EF
)

baseline_warehouse = (
    MANUFACTURING_MT
    * WAREHOUSE_MONTHS
    * WAREHOUSE_EF
)

calculated_baseline = (
    baseline_manufacturing
    + baseline_origin_truck
    + baseline_origin_port
    + baseline_ocean
    + baseline_us_port
    + baseline_us_truck
    + baseline_warehouse
)

#############################################################
# SCENARIO CALCULATIONS
#############################################################

scenario_manufacturing = (
    MANUFACTURING_MT
    * manufacturing_factor
)

scenario_origin_truck = baseline_origin_truck

scenario_origin_port = baseline_origin_port

scenario_ocean = (
    MANUFACTURING_MT
    * ocean_distance
    * ocean_factor
)

scenario_us_port = baseline_us_port

scenario_us_truck = (
    MANUFACTURING_MT
    * us_truck_distance
    * US_TRUCK_EF
)

scenario_warehouse = (
    MANUFACTURING_MT
    * warehouse_months
    * WAREHOUSE_EF
)

scenario = (
    scenario_manufacturing
    + scenario_origin_truck
    + scenario_origin_port
    + scenario_ocean
    + scenario_us_port
    + scenario_us_truck
    + scenario_warehouse
)

reduction = BASELINE - scenario

percent = (
    reduction / BASELINE * 100
)

#############################################################
# KPI CARDS
#############################################################

a, b, c, d = st.columns(4)

with a:

    st.metric(
        "Scenario A Baseline",
        f"{BASELINE:,.0f} kg CO₂e"
    )

with b:

    st.metric(
        "Sensitivity Scenario",
        f"{scenario:,.0f} kg CO₂e",
        delta=f"{scenario - BASELINE:,.0f} kg"
    )

with c:

    st.metric(
        "Change",
        f"{abs(reduction):,.0f} kg CO₂e"
    )

with d:

    st.metric(
        "Change %",
        f"{percent:+.1f}%"
    )

st.divider()

#############################################################
# BASELINE VS SCENARIO
#############################################################

compare = pd.DataFrame({

    "Scenario": [
        "Scenario A Baseline",
        "Sensitivity Scenario"
    ],

    "Emissions": [
        BASELINE,
        scenario
    ]

})

left, right = st.columns(2)

with left:

    st.subheader("Baseline vs Sensitivity Scenario")

    fig = px.bar(
        compare,
        x="Scenario",
        y="Emissions",
        color="Scenario",
        text="Emissions"
    )

    fig.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="white",
        height=430,
        yaxis_title="kg CO₂e / shipment",
        xaxis_title=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

#############################################################
# WATERFALL
#############################################################

with right:

    st.subheader("Change in Emissions")

    change = scenario - BASELINE

    waterfall = go.Figure(
        go.Waterfall(

            orientation="v",

            measure=[
                "absolute",
                "relative",
                "relative"
            ],

            x=[
                "Baseline",
                "Input Changes",
                "Scenario"
            ],

            y=[
                BASELINE,
                change,
                0
            ],

            connector={
                "line": {
                    "color": "gray"
                }
            }

        )
    )

    waterfall.update_layout(
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="white",
        height=430,
        yaxis_title="kg CO₂e"
    )

    st.plotly_chart(
        waterfall,
        use_container_width=True
    )

#############################################################
# GAUGE
#############################################################

st.divider()

st.subheader("Overall Emissions Change")

gauge_value = max(min(abs(percent), 100), 0)

gauge = go.Figure(
    go.Indicator(

        mode="gauge+number",

        value=gauge_value,

        number={
            "suffix": "%"
        },

        title={
            "text": "Percentage Change from Baseline"
        },

        gauge={

            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "color": "green"
            }

        }

    )
)

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
# LEG-BY-LEG COMPARISON
#############################################################

st.divider()

st.subheader("Leg-by-Leg Sensitivity Results")

leg_comparison = pd.DataFrame({

    "Supply Chain Leg": [

        "Chemical Manufacturing",
        "Factory-to-Port Trucking",
        "Origin Port Handling",
        "Ocean Freight",
        "U.S. Port Handling",
        "U.S. Inland Trucking",
        "Warehousing / Storage"

    ],

    "Baseline (kg CO₂e)": [

        baseline_manufacturing,
        baseline_origin_truck,
        baseline_origin_port,
        baseline_ocean,
        baseline_us_port,
        baseline_us_truck,
        baseline_warehouse

    ],

    "Sensitivity (kg CO₂e)": [

        scenario_manufacturing,
        scenario_origin_truck,
        scenario_origin_port,
        scenario_ocean,
        scenario_us_port,
        scenario_us_truck,
        scenario_warehouse

    ]

})

leg_comparison["Change (kg CO₂e)"] = (
    leg_comparison["Sensitivity (kg CO₂e)"]
    - leg_comparison["Baseline (kg CO₂e)"]
)

leg_comparison["Change (%)"] = (

    leg_comparison["Change (kg CO₂e)"]
    / leg_comparison["Baseline (kg CO₂e)"]
    * 100

)

leg_comparison["Baseline (kg CO₂e)"] = (
    leg_comparison["Baseline (kg CO₂e)"].round(1)
)

leg_comparison["Sensitivity (kg CO₂e)"] = (
    leg_comparison["Sensitivity (kg CO₂e)"].round(1)
)

leg_comparison["Change (kg CO₂e)"] = (
    leg_comparison["Change (kg CO₂e)"].round(1)
)

leg_comparison["Change (%)"] = (
    leg_comparison["Change (%)"].round(1)
)

st.dataframe(
    leg_comparison,
    use_container_width=True,
    hide_index=True
)

#############################################################
# EXECUTIVE RECOMMENDATION
#############################################################

st.divider()

st.subheader("Executive Recommendation")

if reduction > 0:

    st.success(
        f"""
The selected sensitivity assumptions reduce the estimated
Scenario A footprint from **{BASELINE:,.0f} kg CO₂e** to
**{scenario:,.0f} kg CO₂e per shipment**.

This represents a reduction of approximately
**{reduction:,.0f} kg CO₂e ({percent:.1f}%)**.

The model indicates that changes to manufacturing emissions,
ocean freight distance/emission intensity, and U.S. trucking
distance can materially affect the overall supply-chain footprint.
"""
    )

elif reduction < 0:

    st.warning(
        f"""
The selected assumptions increase the estimated carbon footprint
by approximately **{abs(reduction):,.0f} kg CO₂e ({abs(percent):.1f}%)**
compared with the Scenario A baseline.

This demonstrates how increases in transportation distance,
warehouse dwell time, or emission intensity can increase total
supply-chain emissions.
"""
    )

else:

    st.info(
        """
The selected assumptions produce the same emissions as the
Scenario A baseline.
"""
    )

#############################################################
# SCENARIO SUMMARY
#############################################################

st.divider()

st.subheader("Sensitivity Scenario Summary")

summary = pd.DataFrame({

    "Variable": [

        "Manufacturing Emission Factor",
        "Ocean Distance",
        "Ocean Emission Factor",
        "U.S. Truck Distance",
        "Warehouse Dwell Time"

    ],

    "Baseline": [

        f"{MANUFACTURING_EF:.0f} kg CO₂e/MT",
        f"{OCEAN_DISTANCE:,.0f} km",
        f"{OCEAN_EF:.4f} kg CO₂e/tonne-km",
        f"{US_TRUCK_DISTANCE:,.0f} km",
        f"{WAREHOUSE_MONTHS:.2f} months"

    ],

    "Sensitivity": [

        f"{manufacturing_factor:.0f} kg CO₂e/MT",
        f"{ocean_distance:,.0f} km",
        f"{ocean_factor:.4f} kg CO₂e/tonne-km",
        f"{us_truck_distance:,.0f} km",
        f"{warehouse_months:.2f} months"

    ]

})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)