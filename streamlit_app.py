import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="MSTACK.AI",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

#####################################################
# CUSTOM CSS
#####################################################

st.markdown("""
<style>

.main{
    background-color:#0f172a;
}

section[data-testid="stSidebar"]{
    background-color:#111827;
}

.block-container{
    padding-top:1rem;
}

div[data-testid="metric-container"]{
    background:#1e293b;
    border-radius:12px;
    padding:18px;
    border:1px solid #334155;
}

h1,h2,h3,h4{
    color:white;
}

p{
    color:#d1d5db;
}

</style>
""", unsafe_allow_html=True)

#SIDEBAR

with st.sidebar:

    # ===== BRANDING =====
    st.markdown("""
    # 🌎 MSTACK.AI
    # Mobilize Green

    **Supply Chain Carbon Intelligence**
    """)

    st.divider()

    # ===== NAVIGATION BUTTONS =====


    st.page_link("streamlit_app.py", label="Dashboard")

    st.page_link("pages/Manufacturing.py", label="Manufacturing")

    st.page_link("pages/VN_Trucking.py", label="Vietnam Trucking")

    st.page_link("pages/VN_Port.py", label="Vietnam Port")

    st.page_link("pages/Ocean_Freight.py", label="Ocean Freight")

    st.page_link("pages/LA_Port.py", label="LA Port")

    st.page_link("pages/US_Trucking.py", label="U.S. Trucking")

    st.page_link("pages/Warehouse.py", label="Warehouse")

    st.page_link("pages/Sensitivity_Test.py", label="Sensitivity Testing")

#####################################################
# TITLE
#####################################################

st.title("🌎 Supply Chain Carbon Intelligence Dashboard")

st.caption(
"Executive overview of supply chain greenhouse gas emissions."
)

#####################################################
# SCENARIO A DATA
#####################################################

df = pd.DataFrame({

    "Stage": [
        "Chemical Manufacturing",
        "Factory-to-Port Trucking",
        "Origin Port Handling",
        "Ocean Freight",
        "U.S. Port Handling",
        "U.S. Inland Trucking",
        "Warehousing / Storage"
    ],

    "Emissions": [
        7140,
        59,
        12,
        3489,
        19,
        416,
        86
    ]

})

total = df["Emissions"].sum()

#####################################################
# CALCULATE EMISSION SHARES
#####################################################

df["Share"] = (df["Emissions"] / total) * 100

highest = df.loc[df["Emissions"].idxmax(), "Stage"]
highest_value = df["Emissions"].max()
highest_percent = df.loc[df["Emissions"].idxmax(), "Share"]

#####################################################
# KPI CARDS
#####################################################

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "Total Emissions",
        f"{total:,} kg CO₂e"
    )

with c2:

    st.metric(
        "Highest Source",
        highest
    )

with c3:

    st.metric(
        "Supply Chain Legs",
        "7"
    )

with c4:

    st.metric(
        "Average / Leg",
        f"{round(total / 7):,} kg"
    )

st.divider()

#####################################################
# CHARTS
#####################################################

left, right = st.columns([1.1, 1])

with left:

    st.subheader("Emission Hotspots")

    fig = px.bar(
        df.sort_values(
            "Emissions",
            ascending=True
        ),
        x="Emissions",
        y="Stage",
        orientation="h",
        color="Emissions",
        color_continuous_scale="Viridis",
        labels={
            "Emissions": "kg CO₂e",
            "Stage": ""
        }
    )

    fig.update_layout(
        height=430,
        paper_bgcolor="#0f172a",
        plot_bgcolor="#0f172a",
        font_color="white",
        coloraxis_showscale=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

with right:

    st.subheader("Share of Total Emissions")

    pie = px.pie(
        df,
        names="Stage",
        values="Emissions",
        hole=.65
    )

    pie.update_traces(
        textposition="outside",
        textinfo="label+percent"
    )

    pie.update_layout(
        height=430,
        paper_bgcolor="#0f172a",
        font_color="white",
        showlegend=False
    )

    st.plotly_chart(
        pie,
        use_container_width=True
    )

#####################################################
# FLOW
#####################################################

st.divider()

st.subheader("Scenario A Supply Chain Flow")

st.markdown("""

**Chemical Manufacturing — SE Asia**

⬇

**Factory-to-Port Trucking**

⬇

**Origin Port Handling**

⬇

**Ocean Freight**

⬇

**U.S. Port Handling**

⬇

**U.S. Inland Trucking**

⬇

**Warehousing / Storage**

""")

#####################################################
# HOTSPOT SUMMARY
#####################################################

st.divider()

st.subheader("Executive Summary")

# Calculate combined contribution of manufacturing + ocean
top_two = df.nlargest(2, "Emissions")
top_two_total = top_two["Emissions"].sum()
top_two_percent = (top_two_total / total) * 100

st.info(f"""
### Key Findings

• **Total Scenario A emissions are {total:,} kg CO₂e per shipment.**

• **{highest}** is the largest emissions source, producing 
**{highest_value:,} kg CO₂e ({highest_percent:.1f}% of the total footprint).**

• **Ocean Freight** produces **3,489 kg CO₂e**, representing 
**{df.loc[df["Stage"] == "Ocean Freight", "Share"].iloc[0]:.1f}%** of total emissions.

• **Chemical Manufacturing + Ocean Freight account for {top_two_percent:.1f}% 
of the total carbon footprint.**

• The largest opportunities for emissions reduction are therefore concentrated 
in **upstream chemical manufacturing and ocean transportation**, rather than 
port handling or warehousing.

• Use the sidebar to analyze each supply-chain leg individually.
""")