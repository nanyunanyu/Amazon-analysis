import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="Amazon 电商数据分析系统",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# 加载数据
@st.cache_data
def load_data():
    df = pd.read_csv("ecommerce_dataset_Amazon.csv")
    df['scraped_at'] = pd.to_datetime(df['scraped_at'])
    # 填充缺失值
    df['price_original'] = df['price_original'].fillna(df['price_current'])
    df['discount_pct'] = df['discount_pct'].fillna(0)
    return df

try:
    df = load_data()

    # --- 侧边栏 ---
    st.sidebar.title("🔍 筛选中心")
    
    # 类别多选
    categories = sorted(df['category'].unique())
    selected_cats = st.sidebar.multiselect("商品类别", categories, default=categories)

    # 品牌多选
    brands = sorted(df['brand'].dropna().unique())
    selected_brands = st.sidebar.multiselect("品牌", brands, default=brands[:10] if len(brands) > 10 else brands)

    # 价格区间
    min_p, max_p = float(df['price_current'].min()), float(df['price_current'].max())
    price_range = st.sidebar.slider("价格范围 (USD)", min_p, max_p, (min_p, max_p))

    # 评分筛选
    min_rating = st.sidebar.number_input("最低评分", 0.0, 5.0, 0.0, 0.5)

    # 数据过滤
    mask = (
        df['category'].isin(selected_cats) &
        df['brand'].isin(selected_brands) &
        (df['price_current'] >= price_range[0]) &
        (df['price_current'] <= price_range[1]) &
        (df['rating_score'] >= min_rating)
    )
    f_df = df.loc[mask]

    # --- 主界面 ---
    st.image("https://s1.chu0.com/src/img/png/07/074a65e2f7504570befac5c0bd281a1e.png?e=2051020800&token=1srnZGLKZ0Aqlz6dk7yF4SkiYf4eP-YrEOdM1sob:s1q-6EM6O-BIOd4yxBa2_hqdA8I=")
    st.title(" Amazon 电商数据洞察 Dashboard")
    
    # KPI 指标
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.metric("商品总数", f"{len(f_df):,}")
    with c2:
        st.metric("平均价格", f"${f_df['price_current'].mean():.2f}")
    with c3:
        st.metric("平均评分", f"{f_df['rating_score'].mean():.1f} ⭐")
    with c4:
        st.metric("总评论数", f"{f_df['reviews_count'].sum():,}")

    st.markdown("---")

    # 图表展示
    t1, t2, t3 = st.tabs(["💰 价格与折扣", "🏷️ 品牌与类别", "⭐ 评分分析"])

    with t1:
        col_a, col_b = st.columns(2)
        with col_a:
            fig_price = px.histogram(f_df, x="price_current", nbins=30, title="价格分布直方图", 
                                    labels={'price_current': '当前价格'}, color_discrete_sequence=['#FF9900'])
            st.plotly_chart(fig_price, use_container_width=True)
        with col_b:
            fig_disc = px.scatter(f_df, x="price_current", y="discount_pct", color="category",
                                 size="reviews_count", hover_name="title", title="价格 vs 折扣率 (气泡大小=评论数)")
            st.plotly_chart(fig_disc, use_container_width=True)

    with t2:
        col_c, col_d = st.columns(2)
        with col_c:
            brand_counts = f_df['brand'].value_counts().head(15).reset_index()
            fig_brand = px.bar(brand_counts, x='count', y='brand', orientation='h', title="Top 15 品牌商品数量")
            st.plotly_chart(fig_brand, use_container_width=True)
        with col_d:
            cat_price = f_df.groupby('category')['price_current'].mean().reset_index()
            fig_cat = px.pie(cat_price, values='price_current', names='category', hole=0.4, title="各类别平均价格占比")
            st.plotly_chart(fig_cat, use_container_width=True)

    with t3:
        fig_rating = px.box(f_df, x="category", y="rating_score", points="all", title="各类别评分分布 (箱线图)")
        st.plotly_chart(fig_rating, use_container_width=True)

    # 详情数据
    st.markdown("---")
    st.subheader("📦 商品详情列表")
    st.dataframe(f_df[['title', 'brand', 'category', 'price_current', 'rating_score', 'reviews_count', 'availability']], use_container_width=True)

except Exception as e:
    st.error(f"加载分析时出错: {e}")
