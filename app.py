import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import sqlalchemy as sal
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Sales Analytics Dashboard", page_icon="📦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0a0e1a; color: #e0e0e0; }
    .stApp { background-color: #0a0e1a; }
    section[data-testid="stSidebar"] { background-color: #0d1424; border-right: 1px solid #1e2d40; }

    .kpi-card {
        background: linear-gradient(135deg, #0d1424 0%, #112240 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 22px 20px;
        text-align: center;
    }
    .kpi-value { font-size: 36px; font-weight: 700; color: #ffffff; letter-spacing: -1px; }
    .kpi-label { font-size: 11px; color: #5a7a9a; margin-top: 5px; text-transform: uppercase; letter-spacing: 1px; font-weight: 500; }
    .kpi-sub { font-size: 12px; color: #3fb950; margin-top: 4px; font-weight: 500; }

    .page-title { font-size: 26px; font-weight: 700; color: #ffffff; margin-bottom: 2px; letter-spacing: -0.5px; }
    .page-subtitle { font-size: 13px; color: #5a7a9a; margin-bottom: 20px; }
    .section-title { font-size: 13px; font-weight: 600; color: #8ba3be; margin-bottom: 8px; letter-spacing: 0.3px; }

    .table-card {
        background: linear-gradient(135deg, #0d1424 0%, #112240 100%);
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 16px;
    }

    div[data-baseweb="select"] > div { background-color: #112240 !important; border: 1px solid #1e3a5f !important; border-radius: 8px !important; color: #ffffff !important; }
    div[data-baseweb="select"] span { color: #c9d1d9 !important; }
    li[role="option"] { background-color: #0d1424 !important; color: #c9d1d9 !important; }
    li[role="option"]:hover { background-color: #112240 !important; color: #ffffff !important; }

    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .block-container { padding-top: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# ── DB ──
#@st.cache_resource
#def get_engine():
#    user     = os.getenv('RAILWAY_MYSQL_USER', 'root')
#    password = os.getenv('RAILWAY_MYSQL_PASSWORD', '')
#    host     = os.getenv('RAILWAY_MYSQL_HOST', 'localhost')
#    port     = os.getenv('RAILWAY_MYSQL_PORT', '3306')
#    database = os.getenv('RAILWAY_MYSQL_DATABASE', 'railway')
#    return sal.create_engine(
#       f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
#        pool_pre_ping=True,
#        pool_recycle=1800
#   )

@st.cache_data(ttl=3600)
def load_data():
    try:
        user     = os.getenv('RAILWAY_MYSQL_USER', 'root')
        password = os.getenv('RAILWAY_MYSQL_PASSWORD', '')
        host     = os.getenv('RAILWAY_MYSQL_HOST', 'localhost')
        port     = os.getenv('RAILWAY_MYSQL_PORT', '3306')
        database = os.getenv('RAILWAY_MYSQL_DATABASE', 'railway')
        engine = sal.create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}",
            pool_pre_ping=True,
            pool_recycle=1800
        )
        df = pd.read_sql("SELECT * FROM df_orders", engine)
        df.columns = [c.lower().strip() for c in df.columns]
        df['order_date'] = pd.to_datetime(df['order_date'])
        df['month'] = df['order_date'].dt.month
        df['month_name'] = df['order_date'].dt.strftime('%B')
        df['year'] = df['order_date'].dt.year
        return df
    except Exception as e:
        st.error(f"Database error: {e}")
        return pd.DataFrame()

PLOTLY_THEME = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(13,20,36,0.8)',
    font_color='#5a7a9a',
    font_family='Inter',
    xaxis=dict(gridcolor='#1e2d40', linecolor='#1e3a5f', tickfont=dict(color='#5a7a9a', size=10)),
    yaxis=dict(gridcolor='#1e2d40', linecolor='#1e3a5f', tickfont=dict(color='#8ba3be', size=10)),
)
COLORS = ['#c9d1d9', '#8ba3be', '#5a7a9a', '#3a5a7a']
LINE_COLOR = '#c9d1d9'

MONTHS = ['January','February','March','April','May','June','July','August','September','October','November','December']

# ── LOAD ──
df_full = load_data()
if df_full.empty:
    st.stop()

# ── SIDEBAR ──
with st.sidebar:
    st.markdown("### 📦 Sales Dashboard")
    st.markdown("<div style='font-size:11px;color:#5a7a9a;margin-bottom:16px'>Superstore Analytics</div>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("", ["📊 Dashboard", "📈 Sales Report", "💰 Profit Report", "🗺️ Regional Report"], label_visibility="collapsed")
    st.markdown("---")

    years = sorted(df_full['year'].unique().tolist())
    st.markdown("<div style='font-size:12px;color:#5a7a9a;margin-bottom:6px;font-weight:500'>FILTER BY YEAR</div>", unsafe_allow_html=True)
    year_cols = st.columns(len(years))
    selected_years = []
    for i, yr in enumerate(years):
        with year_cols[i]:
            if st.button(str(yr), key=f"yr_{yr}", use_container_width=True):
                if yr not in st.session_state.get('sel_years', years):
                    st.session_state.sel_years = years.copy()
                else:
                    st.session_state.sel_years = [yr]
    selected_years = st.session_state.get('sel_years', years)

    st.markdown("<div style='font-size:12px;color:#5a7a9a;margin-top:12px;margin-bottom:6px;font-weight:500'>FILTER BY CATEGORY</div>", unsafe_allow_html=True)
    cats = sorted(df_full['category'].unique().tolist())
    selected_cat = st.selectbox("Category", ["All Categories"] + cats, label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f"<div style='font-size:11px;color:#3a5a7a'>📋 {len(df_full):,} orders</div>", unsafe_allow_html=True)

# ── FILTER ──
df = df_full[df_full['year'].isin(selected_years)] if selected_years else df_full
if selected_cat != "All Categories":
    df = df[df['category'] == selected_cat]

# ── SHARED CALCS ──
total_sales   = df['sale_price'].sum()
total_profit  = df['profit'].sum()
total_orders  = df['order_id'].nunique()
total_qty     = df['quantity'].sum()
profit_margin = (total_profit / total_sales * 100) if total_sales > 0 else 0

def fmt(val):
    if val >= 1_000_000: return f"${val/1_000_000:.2f}M"
    if val >= 1_000: return f"${val/1_000:.1f}K"
    return f"${val:.0f}"

monthly = df.groupby(['month', 'month_name']).agg(
    sales=('sale_price', 'sum'),
    profit=('profit', 'sum'),
    orders=('order_id', 'nunique')
).reset_index().sort_values('month')

cat_sales  = df.groupby('category')['sale_price'].sum().reset_index()
cat_profit = df.groupby('category')['profit'].sum().reset_index()
region_sales  = df.groupby('region')['sale_price'].sum().reset_index()

# ── PAGE 1: DASHBOARD ──
if page == "📊 Dashboard":
    st.markdown('<div class="page-title">Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Overall sales performance overview</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{fmt(total_sales)}</div><div class="kpi-label">Total Sales</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{fmt(total_profit)}</div><div class="kpi-label">Total Profit</div><div class="kpi-sub">{profit_margin:.1f}% margin</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_orders:,}</div><div class="kpi-label">Total Orders</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_qty:,}</div><div class="kpi-label">Sum of Quantity</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.markdown('<div class="section-title">Monthly Sales Trend</div>', unsafe_allow_html=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['sales'], name='Sales',
            line=dict(color='#c9d1d9', width=2), mode='lines+markers+text',
            text=[f"{v/1000:.0f}K" for v in monthly['sales']], textposition='top center',
            textfont=dict(size=9, color='#c9d1d9'), marker=dict(size=5)))
        fig.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['profit'], name='Profit',
            line=dict(color='#5a7a9a', width=2), mode='lines+markers+text',
            text=[f"{v/1000:.0f}K" for v in monthly['profit']], textposition='bottom center',
            textfont=dict(size=9, color='#5a7a9a'), marker=dict(size=5)))
        fig.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['orders'], name='Orders',
            line=dict(color='#3a5a7a', width=1.5, dash='dot'), mode='lines+markers',
            marker=dict(size=4)))
        fig.update_layout(**PLOTLY_THEME, height=320, margin=dict(l=10,r=10,t=20,b=60),
            legend=dict(font=dict(color='#8ba3be', size=10), orientation='h', yanchor='bottom', y=1.02))
        fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Total Sales by Category (Region)</div>', unsafe_allow_html=True)
        region_cat = df.groupby('region')['sale_price'].sum().reset_index()
        fig2 = go.Figure(go.Pie(
            labels=region_cat['region'], values=region_cat['sale_price'],
            hole=0.45, marker_colors=COLORS,
            textfont=dict(color='#ffffff', size=11), textinfo='percent',
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<extra></extra>'
        ))
        fig2.update_layout(**PLOTLY_THEME, height=320, margin=dict(l=10,r=10,t=20,b=10),
            legend=dict(font=dict(color='#8ba3be', size=10)))
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Profit by Category & State (Top 10 States)</div>', unsafe_allow_html=True)
        top_states = df.groupby('state')['profit'].sum().nlargest(8).index
        state_cat = df[df['state'].isin(top_states)].groupby(['state','category'])['profit'].sum().reset_index()
        fig3 = go.Figure()
        for i, cat in enumerate(df['category'].unique()):
            d = state_cat[state_cat['category'] == cat]
            fig3.add_trace(go.Bar(name=cat, x=d['state'], y=d['profit'],
                marker_color=COLORS[i], text=[f"{v/1000:.0f}K" for v in d['profit']],
                textposition='outside', textfont=dict(size=8)))
        fig3.update_layout(**PLOTLY_THEME, barmode='group', height=300,
            margin=dict(l=10,r=10,t=10,b=60), showlegend=True,
            legend=dict(font=dict(color='#8ba3be', size=9), orientation='h', yanchor='bottom', y=1.02))
        fig3.update_xaxes(tickangle=-30, tickfont=dict(size=9))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Top 10 States by Sales</div>', unsafe_allow_html=True)
        state_sales = df.groupby('state')['sale_price'].sum().nlargest(10).sort_values(ascending=True)
        fig4 = go.Figure(go.Bar(
            x=state_sales.values, y=state_sales.index, orientation='h',
            marker_color=['#c9d1d9' if i == len(state_sales)-1 else '#3a5a7a' for i in range(len(state_sales))],
            text=[f"${v/1000:.1f}K" for v in state_sales.values], textposition='outside',
            textfont=dict(color='#8ba3be', size=9)))
        fig4.update_layout(**PLOTLY_THEME, height=300, margin=dict(l=10,r=60,t=10,b=30), showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

# ── PAGE 2: SALES REPORT ──
elif page == "📈 Sales Report":
    st.markdown('<div class="page-title">Sales Performance Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Detailed sales analysis by category, region and time</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="section-title">Sales by Category</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=cat_sales['category'], y=cat_sales['sale_price'],
            marker_color=COLORS[:3],
            text=[f"{v/1000:.2f}K" if v < 1e6 else f"{v/1e6:.2f}M" for v in cat_sales['sale_price']],
            textposition='outside', textfont=dict(color='#8ba3be', size=11)))
        fig.update_layout(**PLOTLY_THEME, height=350, margin=dict(l=10,r=10,t=10,b=30), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        top_cat = cat_sales.loc[cat_sales['sale_price'].idxmax(), 'category']
        top_val = cat_sales['sale_price'].max()
        st.markdown(f"<div style='font-size:11px;color:#5a7a9a;text-align:center'>{top_cat} leads with {fmt(top_val)}</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-title">Monthly Sales Trend</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['sales'],
            line=dict(color=LINE_COLOR, width=2), mode='lines+markers+text',
            fill='tozeroy', fillcolor='rgba(58,90,122,0.2)',
            text=[f"{v/1000:.0f}K" for v in monthly['sales']], textposition='top center',
            textfont=dict(size=9, color='#c9d1d9'), marker=dict(color=LINE_COLOR, size=5)))
        fig2.update_layout(**PLOTLY_THEME, height=350, margin=dict(l=10,r=10,t=10,b=60),
            showlegend=False)
        fig2.update_xaxes(tickangle=-45, tickfont=dict(size=9))
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown('<div class="section-title">Sales by Category & Region</div>', unsafe_allow_html=True)
        pivot = df.groupby(['category','region'])['sale_price'].sum().reset_index()
        pivot_agg = df.groupby('category')['sale_price'].sum().reset_index()
        pivot_qty = df.groupby('category')['quantity'].sum().reset_index()
        summary = pivot_agg.merge(pivot_qty, on='category')
        summary.columns = ['Category', 'Total Sales', 'Qty']
        summary['Total Sales'] = summary['Total Sales'].apply(lambda x: f"${x:,.2f}")

        # Regional breakdown per category
        cat_region = df.groupby(['category','region']).agg(
            sales=('sale_price','sum'), qty=('quantity','sum')).reset_index()

        st.dataframe(cat_region.style.set_properties(**{
            'background-color': '#0d1424', 'color': '#8ba3be',
            'font-size': '11px', 'border': '1px solid #1e2d40'
        }).set_table_styles([
            {'selector': 'thead th', 'props': [('background-color','#112240'),('color','#c9d1d9'),('font-size','11px')]}
        ]), use_container_width=True, height=320, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Total Sales by Category (Donut)</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=cat_sales['category'], values=cat_sales['sale_price'],
            hole=0.55, marker_colors=COLORS[:3],
            textfont=dict(color='#ffffff', size=11),
            textinfo='value+percent',
            hovertemplate='<b>%{label}</b><br>$%{value:,.2f} (%{percent})<extra></extra>'
        ))
        fig3.update_layout(**PLOTLY_THEME, height=280, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(color='#8ba3be', size=10), orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Total Sales KPI</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d1424,#112240);border:1px solid #1e3a5f;border-radius:12px;padding:40px;text-align:center;margin-top:10px">
            <div style="font-size:48px;font-weight:700;color:#ffffff">{fmt(cat_sales['sale_price'].max())}</div>
            <div style="font-size:13px;color:#5a7a9a;margin-top:8px">{cat_sales.loc[cat_sales['sale_price'].idxmax(),'category']} — Top Category</div>
            <div style="font-size:13px;color:#5a7a9a;margin-top:4px">Total: {fmt(total_sales)}</div>
        </div>""", unsafe_allow_html=True)

# ── PAGE 3: PROFIT REPORT ──
elif page == "💰 Profit Report":
    st.markdown('<div class="page-title">Profit Performance Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Detailed profit analysis by category, region and time</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="section-title">Profit by Category</div>', unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=cat_profit['category'], y=cat_profit['profit'],
            marker_color=COLORS[:3],
            text=[f"{v/1000:.1f}K" for v in cat_profit['profit']],
            textposition='outside', textfont=dict(color='#8ba3be', size=11)))
        fig.update_layout(**PLOTLY_THEME, height=350, margin=dict(l=10,r=10,t=10,b=30), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Monthly Profit Trend</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=monthly['month_name'], y=monthly['profit'],
            line=dict(color=LINE_COLOR, width=2), mode='lines+markers+text',
            fill='tozeroy', fillcolor='rgba(58,90,122,0.2)',
            text=[f"{v/1000:.1f}K" for v in monthly['profit']], textposition='top center',
            textfont=dict(size=9, color='#c9d1d9'), marker=dict(color=LINE_COLOR, size=5)))
        fig2.update_layout(**PLOTLY_THEME, height=350, margin=dict(l=10,r=10,t=10,b=60),
            showlegend=False)
        fig2.update_xaxes(tickangle=-45, tickfont=dict(size=9))
        st.plotly_chart(fig2, use_container_width=True)

    with col3:
        st.markdown('<div class="section-title">Profit by Category & Region</div>', unsafe_allow_html=True)
        cat_region_profit = df.groupby(['category','region']).agg(
            profit=('profit','sum'), qty=('quantity','sum')).reset_index()
        cat_region_profit['profit'] = cat_region_profit['profit'].round(2)
        st.dataframe(cat_region_profit.style.set_properties(**{
            'background-color': '#0d1424', 'color': '#8ba3be', 'font-size': '11px'
        }).set_table_styles([
            {'selector': 'thead th', 'props': [('background-color','#112240'),('color','#c9d1d9'),('font-size','11px')]}
        ]), use_container_width=True, height=320, hide_index=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="section-title">Total Profit by Category (Donut)</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=cat_profit['category'], values=cat_profit['profit'],
            hole=0.55, marker_colors=COLORS[:3],
            textfont=dict(color='#ffffff', size=11),
            textinfo='value+percent',
            hovertemplate='<b>%{label}</b><br>$%{value:,.2f} (%{percent})<extra></extra>'
        ))
        fig3.update_layout(**PLOTLY_THEME, height=280, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(color='#8ba3be', size=10), orientation='h', yanchor='bottom', y=1.02))
        st.plotly_chart(fig3, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-title">Total Profit KPI</div>', unsafe_allow_html=True)
        top_profit_cat = cat_profit.loc[cat_profit['profit'].idxmax(), 'category']
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0d1424,#112240);border:1px solid #1e3a5f;border-radius:12px;padding:40px;text-align:center;margin-top:10px">
            <div style="font-size:48px;font-weight:700;color:#ffffff">{fmt(total_profit)}</div>
            <div style="font-size:13px;color:#5a7a9a;margin-top:8px">Total Profit</div>
            <div style="font-size:13px;color:#3fb950;margin-top:4px">{profit_margin:.1f}% overall margin</div>
            <div style="font-size:13px;color:#5a7a9a;margin-top:4px">{top_profit_cat} leads profit</div>
        </div>""", unsafe_allow_html=True)

# ── PAGE 4: REGIONAL REPORT ──
elif page == "🗺️ Regional Report":
    st.markdown('<div class="page-title">Regional Report</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Sales and profit performance by region and state</div>', unsafe_allow_html=True)

    # KPIs
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{fmt(total_sales)}</div><div class="kpi-label">Total Sales</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_orders:,}</div><div class="kpi-label">Total Orders</div></div>', unsafe_allow_html=True)
    with c3: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{total_qty:,}</div><div class="kpi-label">Sum of Quantity</div></div>', unsafe_allow_html=True)
    with c4: st.markdown(f'<div class="kpi-card"><div class="kpi-value">{fmt(total_profit)}</div><div class="kpi-label">Total Profit</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Sales by State (Top 15)</div>', unsafe_allow_html=True)
        state_s = df.groupby('state')['sale_price'].sum().nlargest(15).sort_values(ascending=True)
        fig = go.Figure(go.Bar(
            x=state_s.values, y=state_s.index, orientation='h',
            marker_color=['#c9d1d9' if i == len(state_s)-1 else '#3a5a7a' for i in range(len(state_s))],
            text=[f"${v/1000:.1f}K" for v in state_s.values], textposition='outside',
            textfont=dict(color='#8ba3be', size=9)))
        fig.update_layout(**PLOTLY_THEME, height=420, margin=dict(l=10,r=70,t=10,b=30), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Profit by State (Top 15)</div>', unsafe_allow_html=True)
        state_p = df.groupby('state')['profit'].sum().nlargest(15).sort_values(ascending=True)
        fig2 = go.Figure(go.Bar(
            x=state_p.values, y=state_p.index, orientation='h',
            marker_color=['#3fb950' if i == len(state_p)-1 else '#1e3a5f' for i in range(len(state_p))],
            text=[f"${v/1000:.1f}K" for v in state_p.values], textposition='outside',
            textfont=dict(color='#8ba3be', size=9)))
        fig2.update_layout(**PLOTLY_THEME, height=420, margin=dict(l=10,r=70,t=10,b=30), showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col3, col4 = st.columns(2)

    with col3:
        st.markdown('<div class="section-title">Sales by Region</div>', unsafe_allow_html=True)
        fig3 = go.Figure(go.Pie(
            labels=region_sales['region'], values=region_sales['sale_price'],
            hole=0.55, marker_colors=COLORS,
            textfont=dict(color='#ffffff', size=11), textinfo='label+percent',
            hovertemplate='<b>%{label}</b><br>$%{value:,.0f}<extra></extra>'
        ))
        fig3.update_layout(**PLOTLY_THEME, height=280, margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(font=dict(color='#8ba3be', size=10)))
        st.plotly_chart(fig3, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Region Performance Summary</div>', unsafe_allow_html=True)
        region_summary = df.groupby('region').agg(
            Sales=('sale_price','sum'),
            Profit=('profit','sum'),
            Orders=('order_id','nunique'),
            Qty=('quantity','sum')
        ).reset_index().dropna()
        region_summary['Margin'] = (region_summary['Profit'] / region_summary['Sales'] * 100).round(1).astype(str) + '%'
        region_summary['Sales'] = region_summary['Sales'].apply(fmt)
        region_summary['Profit'] = region_summary['Profit'].apply(fmt)
        st.dataframe(region_summary.style.set_properties(**{
            'background-color': '#0d1424', 'color': '#8ba3be', 'font-size': '12px'
        }).set_table_styles([
            {'selector': 'thead th', 'props': [('background-color','#112240'),('color','#c9d1d9'),('font-size','12px'),('padding','8px')]}
        ]), use_container_width=True, height=250, hide_index=True)

