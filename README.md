# 📈 Sales Dashboard Project

This project contains a synthetic data generator to create realistic 2-year sales data and an interactive web dashboard built with Streamlit to visualize key performance indicators (KPIs).

## Features Included

- **Data Generation:** Creates `SalesData.csv` with randomized but realistic product categories, regions, sales amounts, and profits tracking over two years.
- **Streamlit Web Dashboard:** A responsive Python web app with filters for interactive date ranges, categories, and region selection.
- **KPI Monitoring:** Real-time calculation of total sales, total profit, profit margin, and order count.
- **Top Visuals:** 
  - Time series analysis 
  - Regional mappings/bar charts 
  - Top-performing products 
  - Revenue distribution pies

## 🚀 Setting Up the Streamlit App

1. Ensure you have Python 3.9+ installed.
2. Navigate to the `powerBI-sales-dashboard` directory.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Generate the sample sales data CSV file:
   ```bash
   python generate_data.py
   ```
5. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

Depending on your terminal configuring, it will automatically open the dashboard in your default browser at `http://localhost:8501`.

## 💼 Creating the Power BI Report (.pbix)

Standard Python libraries cannot automatically generate the binary proprietary format of a `.pbix` file. You will need to visually recreate these charts in the Power BI Desktop application using the dataset we generated.

### **Step 1: Import the Data**
1. Open up **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select the `SalesData.csv` file created by the `generate_data.py` script.
4. Click **Load** (or **Transform Data** if you wish to adjust any column data types like Date or Currency).

### **Step 2: Recreate the KPIs & Visuals**

#### Panel 1: Sales Overview (KPIs)
- Select the **Card** visualization from the Visualizations pane.
- Drag `SalesAmount` to the Fields pane to show **Total Sales**.
- Replicate this process using `Profit` for **Total Profit**.
- Replicate this using `ProfitMargin` (Format this as a Percentage).

#### Panel 2: Regional Sales
- For a visual representation: Select **Map** (or **Clustered Bar Chart** if map mapping is restricted).
- Location: Drag in `Region`.
- Tooltips / Bubble Size / Value: Drag in `SalesAmount`.

#### Panel 3: Top-Performing Products
- Select **Stacked Bar Chart**.
- Axis (Y-axis): `Product`.
- Values (X-axis): `SalesAmount`.
- Sort the visualization by Sales Amount in descending order. Top N filtering can be applied via the Filters pane to restrict to the top 10.

#### Panel 4: Time Series Analysis
- Select **Line Chart** or **Area Chart**.
- Axis (X-axis): `Date` (you can drill down to view by Month/Year).
- Values (Y-axis): `SalesAmount`.
- *Bonus*: Drag `Profit` as a secondary line to track the difference.

### **Step 3: Add Slicers/Filters**
To make the dashboard interactive like the Streamlit version:
- Add a **Slicer** visualization.
- Drag `Date` onto the Field to create a date range filter.
- Add additional Slicers for `Product Category` and `Region`.

Once satisfied with the aesthetic arrangement, go to `File` -> `Save As` and name it **Sales Dashboard.pbix**.
# Power-BI-Sales-Dashboard
