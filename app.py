import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load data with caching for performance
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('SalesData.csv')
        # Ensure Date column is datetime
        df['Date'] = pd.to_datetime(df['Date'])
        # Sort values by Date
        df.sort_values(by='Date', inplace=True)
        return df
    except FileNotFoundError:
        st.error("SalesData.csv not found. Please run `python generate_data.py` first.")
        st.stop()

# Basic CSS to style KPI boxes
st.markdown("""
<style>
div[data-testid="stMetricValue"] {
    font-size: 2rem;
}
</style>
""", unsafe_allow_html=True)

def main():
    # Application Title
    st.title("📈 Executive Sales Dashboard")
    st.markdown("Interactive overview of our global sales performance, product trends, and regional breakdown.")

    # Load Data
    df = load_data()

    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Data Filters")
    
    # Date Range Filter
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Ensure they selected start and end
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date
        
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # Product Category Filter
    st.sidebar.subheader("Product Category")
    all_categories = df['Product Category'].unique()
    selected_categories = st.sidebar.multiselect("Select Categories", all_categories, default=all_categories)
    
    # Region Filter
    st.sidebar.subheader("Region")
    all_regions = df['Region'].unique()
    selected_regions = st.sidebar.multiselect("Select Regions", all_regions, default=all_regions)
    
    # Apply Filters
    filtered_df = df[
        (df['Date'] >= start_date) & 
        (df['Date'] <= end_date) &
        (df['Product Category'].isin(selected_categories)) &
        (df['Region'].isin(selected_regions))
    ]
    
    if filtered_df.empty:
        st.warning("No data matches the selected filters. Try broadening your criteria.")
        st.stop()

    # --- KPI SECTION ---
    st.markdown("### 🏆 Key Performance Indicators")
    
    # Calculate KPIs
    total_sales = filtered_df['SalesAmount'].sum()
    total_profit = filtered_df['Profit'].sum()
    avg_profit_margin = total_profit / total_sales if total_sales > 0 else 0
    total_orders = len(filtered_df)
    
    # Assuming "Previous Period" is same length of time exactly before start_date
    period_length = end_date - start_date
    prev_start_date = start_date - period_length
    prev_end_date = start_date - pd.Timedelta(days=1)
    
    prev_df = df[
        (df['Date'] >= prev_start_date) & 
        (df['Date'] <= prev_end_date) &
        (df['Product Category'].isin(selected_categories)) &
        (df['Region'].isin(selected_regions))
    ]
    
    prev_sales = prev_df['SalesAmount'].sum() if not prev_df.empty else 0
    sales_growth = ((total_sales - prev_sales) / prev_sales * 100) if prev_sales > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    
    col1.metric("Total Sales", f"${total_sales:,.0f}", f"{sales_growth:.1f}%")
    col2.metric("Total Profit", f"${total_profit:,.0f}")
    col3.metric("Avg Profit Margin", f"{avg_profit_margin:.1%}")
    col4.metric("Total Orders", f"{total_orders:,}")

    st.markdown("---")

    # --- MAIN CHARTS ---
    col1, col2 = st.columns(2)

    # 1. Time Series Analysis (Sales Trend)
    with col1:
        st.subheader("Time Series Analysis: Sales Trends")
        # Group by Month-Year for cleaner visualization
        time_df = filtered_df.copy()
        time_df['MonthYear'] = time_df['Date'].dt.to_period('M').astype(str)
        monthly_sales = time_df.groupby('MonthYear')[['SalesAmount', 'Profit']].sum().reset_index()
        
        fig_time = px.area(
            monthly_sales, 
            x='MonthYear', 
            y=['SalesAmount', 'Profit'], 
            title="Monthly Sales and Profit Overlay",
            labels={"value": "Amount ($)", "variable": "Metric", "MonthYear": "Month"}
        )
        st.plotly_chart(fig_time, use_container_width=True)

    # 2. Regional Sales
    with col2:
        st.subheader("Regional Sales Performance")
        regional_sales = filtered_df.groupby('Region')['SalesAmount'].sum().reset_index()
        fig_region = px.bar(
            regional_sales, 
            y='Region', 
            x='SalesAmount', 
            orientation='h', 
            title="Total Sales by Region",
            color='SalesAmount',
            color_continuous_scale="Viridis",
            labels={"SalesAmount": "Total Sales ($)"}
        )
        fig_region.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_region, use_container_width=True)

    # --- SECOND ROW OF CHARTS ---
    col3, col4 = st.columns(2)
    
    # 3. Top-Performing Products
    with col3:
        st.subheader("Top-Performing Products")
        product_sales = filtered_df.groupby('Product')['SalesAmount'].sum().reset_index()
        top_products = product_sales.sort_values(by='SalesAmount', ascending=False).head(10)
        
        fig_products = px.bar(
            top_products, 
            x='SalesAmount', 
            y='Product', 
            orientation='h', 
            title="Top 10 Products by Sales",
            color='SalesAmount',
            color_continuous_scale="Blues_r",
            labels={"SalesAmount": "Total Sales ($)"}
        )
        fig_products.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_products, use_container_width=True)

    # 4. Sales by Category (Pie chart)
    with col4:
        st.subheader("Sales by Product Category")
        category_sales = filtered_df.groupby('Product Category')['SalesAmount'].sum().reset_index()
        fig_pie = px.pie(
            category_sales, 
            values='SalesAmount', 
            names='Product Category',
            title="Revenue Distribution by Category",
            hole=0.4 # Donut chart style
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- RAW DATA EXPANDER ---
    with st.expander("View Raw Data"):
        st.dataframe(filtered_df, use_container_width=True)
        # Give an option to download the filtered data
        csv = filtered_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name='filtered_sales_data.csv',
            mime='text/csv',
        )

if __name__ == "__main__":
    main()
