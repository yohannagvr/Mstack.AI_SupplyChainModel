import streamlit as st
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(
    page_title="Vietnam Trucking",
    layout="wide"
)

st.title("🚚 Vietnam Trucking")

st.caption(
    "Analyze factory-to-port trucking emissions in Vietnam "
    "under Scenario A."
)

st.divider()

# ------------------------------------------------
# SCENARIO A DATA
# ------------------------------------------------

CARGO_WEIGHT = 21.0
DISTANCE = 45.0
EMISSION_FACTOR = 0.062

TOTAL_SUPPLY_CHAIN = 11221

# Supplied Scenario A value
BASELINE_EMISSIONS = 59

# ------------------------------------------------
# INPUTS
# ------------------------------------------------

left, right = st.columns(2)

with left:

    distance = st.number_input(
        "Distance (km)",
        min_value=0.0,
        value=DISTANCE,
        step=5.0
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / tonne-km)",
        min_value=0.0,
        value=EMISSION_FACTOR,
        step=0.001,
        format="%.3f"
    )

with right:

    cargo_weight = st.number_input(
        "Cargo Weight (MT)",
        min_value=0.0,
        value=CARGO_WEIGHT,
        step=1.0
    )

    truck_type = st.selectbox(
        "Truck Type",
        [
            "Diesel HGV (>26 tonnes)"
        ]
    )

# ------------------------------------------------
# CALCULATION
# ------------------------------------------------

calculated_emissions = (
    distance
    * cargo_weight
    * emission_factor
)

# Use official supplied Scenario A value
# when the baseline inputs are selected.
if (
    distance == DISTANCE
    and cargo_weight == CARGO_WEIGHT
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

# ------------------------------------------------
# METRICS
# ------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "VN Truck Emissions",
        f"{emissions:,.0f} kg CO₂e"
    )

with c2:

    st.metric(
        "Share of Scenario A",
        f"{share:.1f}%"
    )

with c3:

    st.metric(
        "Distance",
        f"{distance:,.0f} km"
    )

with c4:

    st.metric(
        "Cargo",
        f"{cargo_weight:,.0f} MT"
    )

st.divider()

# ------------------------------------------------
# METHODOLOGY
# ------------------------------------------------

st.subheader("Emission Factor & Methodology")

st.info("""
### Factory-to-Port Diesel Trucking

**Emission Factor:** 0.062 kg CO₂e / tonne-km

**Sources:** EPA MOVES / GLEC Framework

The emission factor represents laden heavy goods vehicle
transportation.

Scenario A uses **21 MT** transported approximately
**45 km** from the manufacturing facility to the origin port.
""")

# ------------------------------------------------
# CALCULATION
# ------------------------------------------------

st.subheader("Emission Calculation")

calculation = pd.DataFrame({

    "Input": [
        "Cargo Weight",
        "Distance",
        "Emission Factor"
    ],

    "Value": [
        f"{cargo_weight:,.0f} MT",
        f"{distance:,.0f} km",
        f"{emission_factor:.3f} kg CO₂e / tonne-km"
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

{cargo_weight:,.0f} MT × {distance:,.0f} km ×
{emission_factor:.3f} kg CO₂e/tonne-km

Calculated result:
**{calculated_emissions:,.2f} kg CO₂e**

Official Scenario A model value:
**{emissions:,.0f} kg CO₂e**
"""
)

st.caption(
    "Note: The supplied Scenario A table reports 59 kg CO₂e. "
    "Using the rounded emission factor and activity data produces "
    f"{calculated_emissions:,.2f} kg CO₂e."
)

# ------------------------------------------------
# GAUGE
# ------------------------------------------------

st.divider()

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

st.subheader("Scenario A Supply Chain Context")

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

    st.error(
        f"""
Vietnam trucking contributes approximately
**{share:.1f}%** of Scenario A emissions and would
be considered a major emissions source.
"""
    )

elif share > 3:

    st.warning(
        f"""
Vietnam trucking contributes approximately
**{share:.1f}%** of Scenario A emissions and represents
a moderate transportation emissions source.
"""
    )

else:

    st.success(
        f"""
Vietnam trucking contributes approximately
**{share:.1f}%** of Scenario A emissions.

This is a relatively small contributor compared with
chemical manufacturing and ocean freight.
"""
    )

# ------------------------------------------------
# REDUCTION OPPORTUNITIES
# ------------------------------------------------

st.divider()

st.subheader("Emission Reduction Opportunities")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### 🛣 Route Optimization

Reduce unnecessary transportation distance through
route planning and facility-to-port optimization.

**Primary lever:** Reduce tonne-km traveled.
""")

    st.info("""
### 📦 Improve Truck Utilization

Consolidate shipments where operationally feasible
to reduce unnecessary truck movements.

**Primary lever:** Increase cargo moved per trip.
""")

with col2:

    st.info("""
### ⚡ Lower-Carbon Trucking

Evaluate lower-carbon fuels and vehicle technologies
for future freight operations.

**Primary lever:** Reduce kg CO₂e per tonne-km.
""")

    st.info("""
### 🚦 Reduce Empty Miles

Coordinate inbound and outbound transportation to
minimize unnecessary empty vehicle movements.

**Primary lever:** Improve overall fleet utilization.
""")

# ------------------------------------------------
# EXECUTIVE SUMMARY
# ------------------------------------------------

st.divider()

st.subheader("Executive Summary")

st.write(f"""
Vietnam factory-to-port trucking contributes approximately
**{emissions:,.0f} kg CO₂e per Scenario A shipment**.

This represents approximately **{share:.1f}%** of the
**{TOTAL_SUPPLY_CHAIN:,.0f} kg CO₂e** Scenario A footprint.

The leg consists of **{cargo_weight:,.0f} MT** transported
approximately **{distance:,.0f} km** using a diesel HGV with
an emission factor of **{emission_factor:.3f} kg CO₂e per
tonne-km**.

Vietnam trucking is a relatively minor contributor to the
overall footprint. The largest reduction opportunities remain
chemical manufacturing and ocean freight, which together
account for the overwhelming majority of Scenario A emissions.
""")