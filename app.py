import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Retail Sales Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Premium dark theme ----------
st.markdown(
    """
    <style>
    #MainMenu, header, footer {visibility: hidden;}

    .stApp {
        background: linear-gradient(135deg, #060816 0%, #0b1024 45%, #0a0f1f 100%);
        color: #f3f4f6;
    }

    .block-container {
        padding-top: 0.8rem;
        padding-bottom: 1.2rem;
        max-width: 100%;
        width: 100%;
    }

    h1, h2, h3, h4 {
        color: #f9fafb !important;
        font-weight: 700 !important;
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #070b1f 0%, #0a1030 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    section[data-testid="stSidebar"] * {
        color: #f3f4f6 !important;
    }

    section[data-testid="stSidebar"] .stSelectbox > div > div,
    section[data-testid="stSidebar"] .stTextInput > div > div > input,
    section[data-testid="stSidebar"] .stDateInput > div > div,
    section[data-testid="stSidebar"] .stMultiSelect > div > div,
    section[data-testid="stSidebar"] .stNumberInput > div > div > input {
        background: #111933 !important;
        color: #f9fafb !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
    }

    .stSelectbox div[data-baseweb="select"] > div {
        background: #111933 !important;
        color: #f9fafb !important;
    }

    div[data-baseweb="popover"],
    div[data-baseweb="popover"] ul {
        background: #111933 !important;
        color: #f9fafb !important;
        border-radius: 12px !important;
    }

    section[data-testid="stSidebar"] svg {
        fill: #f9fafb !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] {
        background: #111933 !important;
        border: 1px dashed rgba(167,139,250,0.55) !important;
        border-radius: 14px !important;
    }

    section[data-testid="stSidebar"] [data-testid="stFileUploaderDropzone"] * {
        color: #cbd5e1 !important;
    }

    /* ---------- Main inputs ---------- */
    .stTextInput > div > div > input {
        background: #111933 !important;
        color: #f9fafb !important;
        border: 1px solid rgba(255,255,255,0.10) !important;
        border-radius: 12px !important;
        height: 44px !important;
    }

    /* ---------- Reusable cards ---------- */
    .hero {
        background: radial-gradient(circle at top right, rgba(88, 101, 242, 0.22), transparent 30%),
                    linear-gradient(135deg, rgba(18,27,62,0.98), rgba(7,10,24,0.98));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 22px 24px;
        box-shadow: 0 14px 34px rgba(0,0,0,0.28);
        margin-bottom: 16px;
        overflow: hidden;
    }

    .panel {
        background: linear-gradient(180deg, rgba(16,22,49,0.92) 0%, rgba(10,15,35,0.96) 100%);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 16px 18px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.28);
        margin-bottom: 18px;
        overflow: hidden;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(15,19,42,0.96), rgba(9,12,27,0.98));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 16px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.26);
        min-height: 110px;
    }

    .metric-title {
        font-size: 0.9rem;
        color: #d1d5db;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .metric-value {
        font-size: clamp(1.35rem, 2.1vw, 1.95rem);
        font-weight: 800;
        color: #f9fafb;
        line-height: 1.15;
    }

    .metric-sub {
        color: #9ca3af;
        margin-top: 6px;
        font-size: 0.82rem;
    }

    .section-label {
        font-size: 0.76rem;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #a78bfa;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .small-muted {
        color: #94a3b8;
        font-size: 0.9rem;
    }

    .insight-box {
        background: linear-gradient(180deg, rgba(16,22,49,0.95), rgba(8,12,27,0.98));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 18px;
        padding: 18px;
        min-height: 260px;
        box-shadow: 0 10px 24px rgba(0,0,0,0.28);
        margin-top: 18px;
        overflow: hidden;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 14px;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,0.08);
    }

    .stDownloadButton > button {
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.08);
        background: linear-gradient(180deg, #111933, #0a1023);
        color: white;
        height: 44px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Helpers ----------
def find_col(df: pd.DataFrame, names: list[str]):
    lower = {c.lower().strip(): c for c in df.columns}
    for name in names:
        if name.lower() in lower:
            return lower[name.lower()]
    return None


def load_data(uploaded_file) -> pd.DataFrame:
    if uploaded_file.name.lower().endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)
    df.columns = [str(c).strip() for c in df.columns]
    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    col_map = {
        "bill_no": find_col(df, ["Bill_No", "Bill No", "BillNo"]),
        "date": find_col(df, ["Date"]),
        "item_name": find_col(df, ["Item_Name", "Item Name"]),
        "item_category": find_col(df, ["Item_Category", "Item Category"]),
        "salesman_name": find_col(df, ["Salesman_Name", "Salesman Name"]),
        "sales_type": find_col(df, ["Sales_Type", "Sales Type"]),
        "final_sales": find_col(df, ["Final_Sales", "Final Sales", "Amt With Tax"]),
    }

    required = ["date", "item_name", "item_category", "salesman_name", "sales_type", "final_sales"]
    missing = [k for k in required if col_map[k] is None]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    work = pd.DataFrame()
    for key, col in col_map.items():
        if col:
            work[key] = df[col]

    work["date"] = pd.to_datetime(work["date"], errors="coerce")
    work = work.dropna(subset=["date"]).copy()
    work["final_sales"] = pd.to_numeric(work["final_sales"], errors="coerce").fillna(0)
    work["item_name"] = work["item_name"].astype(str).str.strip()
    work["item_category"] = work["item_category"].astype(str).str.strip()
    work["salesman_name"] = work["salesman_name"].astype(str).str.strip()
    work["sales_type"] = work["sales_type"].astype(str).str.strip().str.title()
    work["net_sales"] = work.apply(
        lambda r: -abs(r["final_sales"]) if r["sales_type"] == "Return" else abs(r["final_sales"]),
        axis=1,
    )
    work["month_name"] = work["date"].dt.strftime("%b")
    work["year_month"] = work["date"].dt.to_period("M").astype(str)
    return work


def inr(value: float) -> str:
    return f"₹ {value:,.0f}"


def kpi_card(title: str, value: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plot_config():
    return {"displayModeBar": False, "scrollZoom": False, "responsive": True}


# ---------- Sidebar ----------
st.sidebar.markdown("## Retail Sales Analytics")
st.sidebar.markdown("Upload a CSV or Excel file and explore sales insights.")
uploaded_file = st.sidebar.file_uploader("Upload sales file", type=["csv", "xlsx", "xls"])

if uploaded_file is None:
    st.markdown(
        """
        <div class="hero">
            <div class="section-label">Upload data</div>
            <h1 style="margin:0; font-size:2.2rem;">Sales Performance Analyzer</h1>
            <p class="small-muted">Upload your sales file to generate a premium analytics dashboard with KPIs, trends, top products, and automated insights.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.info("Upload your sales file from the left sidebar to begin.")
    st.stop()

try:
    raw_df = load_data(uploaded_file)
    df = prepare_data(raw_df)
except Exception as e:
    st.error(f"Could not process file: {e}")
    st.stop()

st.sidebar.markdown("---")
st.sidebar.markdown("## Filters")
category_options = ["All"] + sorted(df["item_category"].dropna().unique().tolist())
salesman_options = ["All"] + sorted(df["salesman_name"].dropna().unique().tolist())
month_options = ["All"] + sorted(df["month_name"].dropna().unique().tolist())
sales_type_options = ["All"] + sorted(df["sales_type"].dropna().unique().tolist())

selected_category = st.sidebar.selectbox("Item Category", category_options)
selected_salesman = st.sidebar.selectbox("Salesman", salesman_options)
selected_month = st.sidebar.selectbox("Month", month_options)
selected_sales_type = st.sidebar.selectbox("Sales Type", sales_type_options)

filtered = df.copy()
if selected_category != "All":
    filtered = filtered[filtered["item_category"] == selected_category]
if selected_salesman != "All":
    filtered = filtered[filtered["salesman_name"] == selected_salesman]
if selected_month != "All":
    filtered = filtered[filtered["month_name"] == selected_month]
if selected_sales_type != "All":
    filtered = filtered[filtered["sales_type"] == selected_sales_type]

# ---------- Header ----------
st.markdown(
    f"""
    <div class="hero">
        <div class="section-label">Retail analytics web app</div>
        <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:16px; flex-wrap:wrap;">
            <div>
                <h1 style="margin:0; font-size:2.2rem;">Sales Performance Analyzer</h1>
                <p class="small-muted" style="max-width:720px;">Explore revenue, orders, monthly trends, category contribution, top products, and product-level detail using your uploaded sales data.</p>
            </div>
            <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); border-radius:16px; min-width:240px; padding:14px 16px;">
                <div class="small-muted">Loaded file</div>
                <div style="font-weight:700; font-size:1rem; color:#f9fafb; word-break:break-word;">{uploaded_file.name}</div>
                <div class="small-muted">Rows: {len(filtered):,}</div>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- KPIs ----------
total_revenue = filtered[filtered["sales_type"] == "Sales"]["final_sales"].sum()
total_returns = filtered[filtered["sales_type"] == "Return"]["final_sales"].sum()
net_revenue = filtered["net_sales"].sum()
total_orders = filtered["bill_no"].nunique() if "bill_no" in filtered.columns else len(filtered)
avg_order_value = net_revenue / total_orders if total_orders else 0

c1, c2, c3, c4 = st.columns(4)
with c1:
    kpi_card("💰 Total Revenue", inr(total_revenue), "Gross sales value")
with c2:
    kpi_card("🧾 Net Revenue", inr(net_revenue), "Sales adjusted for returns")
with c3:
    kpi_card("📦 Total Orders", f"{total_orders:,}", "Unique bill count")
with c4:
    kpi_card("📊 Avg Order Value", inr(avg_order_value), "Average revenue per order")

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ---------- Main charts ----------
col1, col2 = st.columns(2)
with col1:
    st.markdown('<div class="panel"><div class="section-label">Category contribution</div><h3 style="margin-top:0;">Revenue by Category</h3>', unsafe_allow_html=True)
    cat = filtered.groupby("item_category", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False)
    if not cat.empty:
        fig = px.pie(
            cat,
            values="net_sales",
            names="item_category",
            hole=0.72,
            color_discrete_sequence=["#7c3aed", "#2563eb", "#06b6d4", "#f59e0b", "#10b981", "#ef4444", "#a855f7"],
        )
        fig.update_traces(textinfo="percent", textfont_size=12)
        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f9fafb"),
            margin=dict(l=10, r=10, t=10, b=10),
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=0.88, font=dict(size=11)),
            annotations=[dict(text=inr(net_revenue), x=0.5, y=0.5, showarrow=False, font=dict(size=18, color="#f9fafb"))],
        )
        st.plotly_chart(fig, use_container_width=True, config=plot_config())
    else:
        st.write("No data available.")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<div class="panel"><div class="section-label">Track performance over time</div><h3 style="margin-top:0;">Monthly Revenue Trend</h3>', unsafe_allow_html=True)
    monthly = filtered.groupby("year_month", as_index=False)["net_sales"].sum().sort_values("year_month")
    if not monthly.empty:
        fig = px.line(monthly, x="year_month", y="net_sales", markers=True)
        fig.update_traces(line=dict(color="#8b5cf6", width=4), marker=dict(size=8, color="#a78bfa"))
        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f9fafb"),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Month",
            yaxis_title="Revenue",
            autosize=True,
        )
        st.plotly_chart(fig, use_container_width=True, config=plot_config())
    else:
        st.write("No data available.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)
with col3:
    st.markdown('<div class="panel"><div class="section-label">Top performers</div><h3 style="margin-top:0;">Salesman Performance</h3>', unsafe_allow_html=True)
    salesmen = filtered.groupby("salesman_name", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False).head(8)
    if not salesmen.empty:
        fig = px.bar(
            salesmen,
            x="salesman_name",
            y="net_sales",
            color="net_sales",
            color_continuous_scale=["#2563eb", "#7c3aed", "#14b8a6"],
        )
        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f9fafb"),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Salesman",
            yaxis_title="Net Sales",
            coloraxis_showscale=False,
            autosize=True,
        )
        fig.update_xaxes(tickangle=-25)
        st.plotly_chart(fig, use_container_width=True, config=plot_config())
    else:
        st.write("No data available.")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown('<div class="panel"><div class="section-label">By revenue</div><h3 style="margin-top:0;">Top Products</h3>', unsafe_allow_html=True)
    products = filtered.groupby("item_name", as_index=False)["net_sales"].sum().sort_values("net_sales", ascending=False).head(10)
    if not products.empty:
        fig = px.bar(
            products,
            x="net_sales",
            y="item_name",
            orientation="h",
            color="net_sales",
            color_continuous_scale=["#0ea5e9", "#7c3aed", "#f59e0b"],
        )
        fig.update_layout(
            height=360,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#f9fafb"),
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_title="Revenue",
            yaxis_title="",
            coloraxis_showscale=False,
            yaxis=dict(autorange="reversed", automargin=True),
            autosize=True,
        )
        st.plotly_chart(fig, use_container_width=True, config=plot_config())
    else:
        st.write("No data available.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ---------- Search and insights ----------
left, right = st.columns(2)
with left:
    st.markdown('<div class="panel"><div class="section-label">Search</div><h3 style="margin-top:0;">Product Details</h3>', unsafe_allow_html=True)
    query = st.text_input("Enter product name", placeholder="Search product...")
    if query:
        product_df = filtered[filtered["item_name"].str.contains(query, case=False, na=False)]
        if product_df.empty:
            st.warning("No matching product found.")
        else:
            product_summary = (
                product_df.groupby(["item_name", "item_category", "salesman_name"], as_index=False)["net_sales"]
                .sum()
                .sort_values("net_sales", ascending=False)
            )
            st.dataframe(product_summary, use_container_width=True, hide_index=True)
    else:
        st.markdown('<div class="small-muted">Try searching: Kurta, Shirt, Pant, Koti, Blazer</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="insight-box">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Auto insights</div>', unsafe_allow_html=True)
    st.markdown('<h3 style="margin-top:0;">Generated from your data</h3>', unsafe_allow_html=True)
    if filtered.empty:
        st.write("No data available.")
    else:
        category_top = filtered.groupby("item_category")["net_sales"].sum().sort_values(ascending=False)
        salesman_top = filtered.groupby("salesman_name")["net_sales"].sum().sort_values(ascending=False)
        product_top = filtered.groupby("item_name")["net_sales"].sum().sort_values(ascending=False)
        returns_value = filtered[filtered["sales_type"] == "Return"]["final_sales"].sum()
        gross_sales = filtered[filtered["sales_type"] == "Sales"]["final_sales"].sum()
        return_rate = (returns_value / gross_sales * 100) if gross_sales else 0

        if not category_top.empty:
            st.write(f"- **{category_top.index[0]}** is the top category with {inr(category_top.iloc[0])} in net sales.")
        if not salesman_top.empty:
            st.write(f"- **{salesman_top.index[0]}** is the best-performing salesman with {inr(salesman_top.iloc[0])}.")
        if not product_top.empty:
            st.write(f"- **{product_top.index[0]}** is the highest-selling product with {inr(product_top.iloc[0])}.")
        st.write(f"- Return rate by value is **{return_rate:.2f}%** for the selected filters.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)

# ---------- Preview and downloads ----------
st.markdown('<div class="panel"><div class="section-label">Review the selected dataset</div><h3 style="margin-top:0;">Filtered Data Preview</h3>', unsafe_allow_html=True)
st.dataframe(filtered, use_container_width=True, hide_index=True)
dl1, dl2 = st.columns(2)
with dl1:
    st.download_button(
        "Download Filtered Data (CSV)",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="filtered_sales_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
with dl2:
    summary_df = pd.DataFrame(
        {
            "metric": ["Total Revenue", "Net Revenue", "Total Orders", "Avg Order Value", "Total Returns"],
            "value": [total_revenue, net_revenue, total_orders, avg_order_value, total_returns],
        }
    )
    st.download_button(
        "Download KPI Summary",
        data=summary_df.to_csv(index=False).encode("utf-8"),
        file_name="sales_kpi_summary.csv",
        mime="text/csv",
        use_container_width=True,
    )
st.markdown("</div>", unsafe_allow_html=True)
