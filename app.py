import streamlit as st
import pandas as pd

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="SmartStock",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------------
# SAMPLE DATA
# ---------------------------------------------------------

inventory_data = {
    "Medicine": [
        "Paracetamol",
        "Amoxicillin",
        "Ibuprofen",
        "Azithromycin",
        "Cefixime"
    ],
    "Current Stock": [120, 45, 80, 25, 60],
    "Reorder Level": [50, 50, 40, 30, 40],
    "Status": [
        "Normal",
        "Low Stock",
        "Normal",
        "Low Stock",
        "Normal"
    ]
}

inventory_df = pd.DataFrame(inventory_data)

# ---------------------------------------------------------
# CUSTOM DESIGN
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* ---------- GLOBAL ---------- */

    .stApp {
        background-color: #f7f6f2;
        color: #171717;
    }

    .main .block-container {
        max-width: 1400px;
        padding-top: 2.5rem;
        padding-bottom: 4rem;
    }

    /* Hide Streamlit default chrome */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* ---------- TYPOGRAPHY ---------- */

    h1, h2, h3 {
        font-family: Georgia, "Times New Roman", serif !important;
        font-weight: 400 !important;
        color: #171717 !important;
    }

    p, div, span, label {
        font-family: Arial, Helvetica, sans-serif;
    }

    /* ---------- TOP BRAND ---------- */

    .brand-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-bottom: 1.4rem;
        border-bottom: 1px solid #d7d5ce;
        margin-bottom: 3.5rem;
    }

    .brand {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 5rem;
        letter-spacing: 0.12em;
        color: #171717;
    }

    .brand-subtitle {
        font-size: 0.72rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #77746d;
    }

    /* ---------- HERO ---------- */

    .hero-label {
        font-size: 0.72rem;
        letter-spacing: 0.22em;
        text-transform: uppercase;
        color: #77746d;
        margin-bot tom: 1rem;
    }

    .hero-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 3.4rem;
        line-height: 1.05;
        font-weight: 400;
        letter-spacing: -0.04em;
        color: #171717;
        max-width: 850px;
        margin-bottom: 1.5rem;
    }

    .hero-description {
        max-width: 680px;
        font-size: 1rem;
        line-height: 1.7;
        color: #66635d;
        margin-bottom: 3rem;
    }

    /* ---------- SECTION ---------- */

    .section-label {
        font-size: 0.7rem;
        letter-spacing: 0.2em;
        text-transform: uppercase;
        color: #77746d;
        margin-top: 3rem;
        margin-bottom: 1rem;
    }

    .section-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2.2rem;
        font-weight: 400;
        color: #171717;
        margin-bottom: 2rem;
    }

    /* ---------- KPI CARDS ---------- */

    .kpi {
        border-top: 1px solid #171717;
        padding-top: 1.2rem;
        padding-bottom: 2rem;
    }

    .kpi-number {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 3.2rem;
        line-height: 1;
        color: #171717;
        margin-bottom: 0.6rem;
    }

    .kpi-label {
        font-size: 0.68rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: #77746d;
    }

    /* ---------- INFO PANEL ---------- */

    .info-panel {
        background: #171717;
        color: #f7f6f2;
        padding: 2.5rem;
        min-height: 220px;
    }

    .info-panel-label {
        font-size: 0.68rem;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: #aaa79f;
        margin-bottom: 1rem;
    }

    .info-panel-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 2rem;
        line-height: 1.2;
        margin-bottom: 1rem;
    }

    .info-panel-text {
        color: #c7c4bd;
        line-height: 1.6;
        font-size: 0.9rem;
    }

    /* ---------- TABLE ---------- */

    .table-heading {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 1.8rem;
        color: #171717;
        margin-bottom: 1rem;
    }

    /* ---------- FOOTER ---------- */

    .footer {
        border-top: 1px solid #d7d5ce;
        margin-top: 5rem;
        padding-top: 1.5rem;
        display: flex;
        justify-content: space-between;
        color: #77746d;
        font-size: 0.72rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# BRAND HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="brand-row">
        <div>
            <div class="brand">SMARTSTOCK</div>
            <div class="brand-subtitle">Intelligent Medicine Operations</div>
        </div>
        <div class="brand-subtitle">Hospital Inventory · 2026</div>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

st.markdown(
    """
    <div class="hero-label">Medicine Intelligence Platform</div>

    <div class="hero-title">
        Smarter inventory.<br>
        Better preparedness.
    </div>

    <div class="hero-description">
        SmartStock brings medicine inventory, demand forecasting,
        risk analysis and procurement intelligence together in one
        streamlined hospital operations platform.
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# KPI SECTION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">At a glance</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-number">40</div>
            <div class="kpi-label">Total Medicines</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-number">02</div>
            <div class="kpi-label">Low Stock</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-number">00</div>
            <div class="kpi-label">High Risk</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        """
        <div class="kpi">
            <div class="kpi-number">00</div>
            <div class="kpi-label">Expiring Soon</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# NAVIGATION
# ---------------------------------------------------------

st.markdown(
    '<div class="section-label">Workspace</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "Overview",
        "Inventory",
        "Forecast & Risk",
        "Procurement"
    ]
)

# ---------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------

with tab1:

    st.markdown(
        """
        <div class="section-title">
            Inventory intelligence
        </div>
        """,
        unsafe_allow_html=True
    )

    left, right = st.columns([1.15, 1])

    with left:
        st.markdown(
            """<div class="info-panel">
<div class="info-panel-label">
SmartStock Insight
</div>

<div class="info-panel-title">
From stock monitoring<br>
to intelligent action.
</div>

<div class="info-panel-text">
Monitor medicine availability, identify shortage
risks and support timely procurement decisions
using forecasting and risk-aware recommendations.
</div>
</div>""",
        unsafe_allow_html=True
    )

    with right:
        st.markdown(
            """<div style="
border-top:1px solid #171717;
padding-top:1.2rem;
">
<div class="section-label">
System Status
</div>

<p style="
font-family:Georgia,serif;
font-size:1.6rem;
margin-top:1rem;
">
Operational
</p>

<p style="
color:#77746d;
line-height:1.6;
">
Frontend prototype is connected locally.<br>
Backend and machine-learning services will
be integrated in the next stage.
</p>
</div>""",
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# INVENTORY
# ---------------------------------------------------------

with tab2:

    st.markdown(
        """
        <div class="section-title">
            Medicine Inventory
        </div>
        """,
        unsafe_allow_html=True
    )

    st.dataframe(
        inventory_df,
        use_container_width=True,
        hide_index=True
    )

# ---------------------------------------------------------
# FORECAST & RISK
# ---------------------------------------------------------

with tab3:

    st.markdown(
        """
        <div class="section-title">
            Forecast & Risk
        </div>

        <p style="color:#77746d; line-height:1.7;">
            Demand forecasting, shortage risk, expiry risk and
            reorder recommendations will appear here after
            integration with the SmartStock ML service.
        </p>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# PROCUREMENT
# ---------------------------------------------------------

with tab4:

    st.markdown(
        """
        <div class="section-title">
            Procurement
        </div>

        <p style="color:#77746d; line-height:1.7;">
            Supplier information, reorder recommendations and
            controlled procurement workflows will appear here
            after MCP integration.
        </p>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        <span>SmartStock</span>
        <span>Medicine Intelligence · Inventory · Procurement</span>
    </div>
    """,
    unsafe_allow_html=True
)