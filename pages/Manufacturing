import streamlit as st
import plotly.graph_objects as go

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

st.title("🏭 Chemical Manufacturing")

st.caption(
"""
Estimate emissions generated during the manufacturing
stage of the supply chain.
"""
)

st.divider()

# ----------------------------------------------------
# User Inputs
# ----------------------------------------------------

left,right = st.columns([1,1])

with left:

    production = st.number_input(
        "Annual Production Volume (tons)",
        min_value=0.0,
        value=5000.0,
        step=100.0
    )

    emission_factor = st.number_input(
        "Emission Factor (kg CO₂e / ton)",
        min_value=0.0,
        value=1.64,
        step=0.01
    )

with right:

    renewable_share = st.slider(
        "Renewable Energy Usage (%)",
        0,
        100,
        25
    )

    efficiency = st.slider(
        "Manufacturing Efficiency (%)",
        50,
        100,
        80
    )

# ----------------------------------------------------
# Calculation
# ----------------------------------------------------

base_emissions = production * emission_factor

renewable_reduction = renewable_share * 0.002

efficiency_reduction = (efficiency - 50) * 0.003

adjusted = base_emissions * (
    1
    - renewable_reduction
    - efficiency_reduction
)

adjusted = max(adjusted,0)

TOTAL_SUPPLY_CHAIN = 34200

share = adjusted / TOTAL_SUPPLY_CHAIN * 100

# ----------------------------------------------------
# KPIs
# ----------------------------------------------------

st.divider()

c1,c2,c3 = st.columns(3)

with c1:

    st.metric(
        "Manufacturing Emissions",
        f"{adjusted:,.0f} kg CO₂e"
    )

with c2:

    st.metric(
        "Share of Total",
        f"{share:.1f}%"
    )

with c3:

    st.metric(
        "Renewable Usage",
        f"{renewable_share}%"
    )

# ----------------------------------------------------
# Gauge
# ----------------------------------------------------

st.subheader("Contribution to Supply Chain")

fig = go.Figure(go.Indicator(

    mode="gauge+number",

    value=share,

    number={"suffix":"%"},

    gauge={

        "axis":{"range":[0,100]},

        "bar":{"color":"green"},

        "steps":[

            {"range":[0,20],"color":"#14532d"},
            {"range":[20,40],"color":"#166534"},
            {"range":[40,60],"color":"#facc15"},
            {"range":[60,80],"color":"#f97316"},
            {"range":[80,100],"color":"#dc2626"}

        ]

    }

))

fig.update_layout(
    paper_bgcolor="#0f172a",
    font_color="white",
    height=350
)

st.plotly_chart(fig,use_container_width=True)

# ----------------------------------------------------
# Explanation
# ----------------------------------------------------

st.subheader("Interpretation")

if share > 40:

    st.error(
        """
Manufacturing is currently one of the
largest contributors to overall emissions.
Reducing emissions here could significantly
lower the company's carbon footprint.
"""
    )

elif share > 20:

    st.warning(
        """
Manufacturing contributes a moderate
portion of total emissions.
Efficiency improvements may provide
meaningful reductions.
"""
    )

else:

    st.success(
        """
Manufacturing is not currently
the dominant emission source.
"""
    )

# ----------------------------------------------------
# Reduction Opportunities
# ----------------------------------------------------

st.divider()

st.subheader("Emission Reduction Opportunities")

col1,col2 = st.columns(2)

with col1:

    st.info("""
###  Renewable Electricity

Increase renewable electricity purchases.

Expected reduction:

**10–35%**
""")

    st.info("""
###  Process Optimization

Improve equipment efficiency.

Expected reduction:

**5–15%**
""")

with col2:

    st.info("""
###  Sustainable Raw Materials

Source lower-carbon feedstocks.

Expected reduction:

**5–20%**
""")

    st.info("""
### Waste Heat Recovery

Recover heat from manufacturing processes.

Expected reduction:

**3–10%**
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