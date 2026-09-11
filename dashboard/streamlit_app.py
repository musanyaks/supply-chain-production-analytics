import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from inventory.eoq import calculate_eoq
from inventory.reorder_point import calculate_reorder_point
from production.production_efficiency import calculate_oee
from procurement.supplier_scorecard import calculate_supplier_scorecard

st.set_page_config(page_title="SCMS Dashboard", layout="wide")
st.title("📊 Supply Chain Analytics Dashboard")

# ==========================================
# READ FROM data/raw/ FOLDER
# ==========================================
@st.cache_data
def load_raw_warehouse_data():
    """Reads actual CSV files from data/raw/ instead of generating dummy data"""
    inv_path = os.path.join('data', 'raw', 'inventory.csv')
    prod_path = os.path.join('data', 'raw', 'products.csv')
    
    # If real files exist, load them
    if os.path.exists(inv_path) and os.path.exists(prod_path):
        df_inv = pd.read_csv(inv_path)
        df_prod = pd.read_csv(prod_path)
        
        # Merge Inventory and Products (assuming they share a product_id)
        if 'product_id' in df_inv.columns and 'id' in df_prod.columns:
            df = pd.merge(df_inv, df_prod, left_on='product_id', right_on='id', how='left')
        else:
            df = df_inv.copy()
            
        # Ensure required columns exist for the dashboard logic
        if 'Remaining_Stock' not in df.columns and 'quantity' in df.columns:
            df.rename(columns={'quantity': 'Remaining_Stock'}, inplace=True)
        if 'Unit_Cost' not in df.columns and 'unit_cost' in df.columns:
            df.rename(columns={'unit_cost': 'Unit_Cost'}, inplace=True)
            
        # Calculate Inventory Value
        df['Inventory_Value'] = df['Remaining_Stock'] * df['Unit_Cost']
        
        # If historical In/Out data isn't in the CSV, we mock just those columns for the chart
        if 'Inbound_Stock' not in df.columns:
            df['Inbound_Stock'] = df['Remaining_Stock'] * 1.2
            df['Outbound_Stock'] = df['Inbound_Stock'] - df['Remaining_Stock']
            
        return df
    else:
        st.error("⚠️ No real data found in `data/raw/`. Please place `inventory.csv` and `products.csv` there.")
        return pd.DataFrame()

# Initialize data in session state
if 'warehouse_df' not in st.session_state:
    df = load_raw_warehouse_data()
    if not df.empty:
        # Add missing columns required by the UI if they aren't in the real CSV
        if 'Safety_Stock' not in df.columns:
            df['Safety_Stock'] = 50 # Default safety stock
        if 'Category' not in df.columns:
            df['Category'] = 'Unknown'
        st.session_state.warehouse_df = df

def simulate_live_movement(df):
    """Simulates automated real-time warehouse movements on real data"""
    n_outbound = np.random.randint(1, 5)
    outbound_indices = np.random.choice(df.index, size=n_outbound, replace=False)
    for idx in outbound_indices:
        qty = np.random.randint(1, 20)
        df.at[idx, 'Outbound_Stock'] += min(qty, df.at[idx, 'Remaining_Stock'])

    n_inbound = np.random.randint(1, 3)
    inbound_indices = np.random.choice(df.index, size=n_inbound, replace=False)
    for idx in inbound_indices:
        qty = np.random.randint(10, 50)
        df.at[idx, 'Inbound_Stock'] += qty

    df['Remaining_Stock'] = (df['Inbound_Stock'] - df['Outbound_Stock']).clip(lower=0)
    df['Inventory_Value'] = df['Remaining_Stock'] * df['Unit_Cost']
    return df

# Sidebar Navigation
menu = st.sidebar.radio("Menu", ["Live Warehouse (Raw Data)", "Inventory Optimization", "Production Efficiency", "Procurement & Suppliers"])

if menu == "Live Warehouse (Raw Data)":
    st.header("🏬 Live Warehouse Overview (Reading from data/raw/)")
    
    if 'warehouse_df' not in st.session_state:
        st.stop()
        
    df = st.session_state.warehouse_df
    
    col_toggle, col_status = st.columns([1, 3])
    with col_toggle: run_sim = st.toggle("▶️ Start Automated Simulation")
    with col_status:
        if run_sim: st.success("Simulation Running: Processing live movements...")
        else: st.info("Simulation Paused.")

    total_inbound = df['Inbound_Stock'].sum()
    total_outbound = df['Outbound_Stock'].sum()
    total_remaining = df['Remaining_Stock'].sum()
    total_value = df['Inventory_Value'].sum()
    critical_stock_count = len(df[df['Remaining_Stock'] < df['Safety_Stock']])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="⬇️ Total Inbound", value=f"{total_inbound:,}")
    with col2: st.metric(label="⬆️ Total Outbound", value=f"{total_outbound:,}")
    with col3: st.metric(label="📦 Total Remaining", value=f"{total_remaining:,}")
    with col4: st.metric(label="💵 Total Value", value=f"${total_value:,.2f}")
        
    st.divider()
    if critical_stock_count > 0:
        st.warning(f"⚠️ **Action Required:** {critical_stock_count} SKUs are below Safety Stock.")
    
    st.subheader("Inbound vs Outbound vs Remaining by Category")
    chart_data = df.groupby('Category')[['Inbound_Stock', 'Outbound_Stock', 'Remaining_Stock']].sum()
    st.bar_chart(chart_data)
    
    st.divider()
    st.subheader("Raw Data Table")
    st.dataframe(df, use_container_width=True, height=400)
    
    if run_sim:
        st.session_state.warehouse_df = simulate_live_movement(df)
        time.sleep(3)
        st.rerun()

elif menu == "Inventory Optimization":
    st.header("Inventory Optimization Calculators")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Economic Order Quantity (EOQ)")
        demand = st.number_input("Annual Demand (Units)", min_value=1, value=10000, key="eoq_d")
        order_c = st.number_input("Ordering Cost ($)", min_value=0.1, value=50.0, key="eoq_oc")
        hold_c = st.number_input("Holding Cost per Unit ($)", min_value=0.1, value=2.5, key="eoq_hc")
        if st.button("Calculate EOQ"):
            st.success(f"Optimal Order Quantity: {calculate_eoq(demand, order_c, hold_c)['eoq']} units")
    with col2:
        st.subheader("Reorder Point (ROP)")
        daily_d = st.number_input("Avg Daily Demand", min_value=0.0, value=30.0, key="rop_dd")
        lead_t = st.number_input("Lead Time (Days)", min_value=0, value=7, key="rop_lt")
        safety_s = st.number_input("Safety Stock", min_value=0, value=50, key="rop_ss")
        if st.button("Calculate ROP"):
            st.warning(f"Trigger Purchase Order at: {calculate_reorder_point(daily_d, lead_t, safety_s)['reorder_point']} units")

elif menu == "Production Efficiency":
    st.header("Overall Equipment Effectiveness (OEE)")
    col1, col2, col3 = st.columns(3)
    with col1: avail = st.slider("Availability", 0.0, 1.0, 0.85)
    with col2: perf = st.slider("Performance", 0.0, 1.0, 0.90)
    with col3: qual = st.slider("Quality", 0.0, 1.0, 0.95)
    if st.button("Calculate OEE"):
        res = calculate_oee(avail, perf, qual)
        st.metric(label="OEE Score", value=f"{res['oee_percentage']}%")

elif menu == "Procurement & Suppliers":
    st.header("Supplier Scorecard")
    otd = st.slider("On-Time Delivery (%)", 0, 100, 85)
    qa = st.slider("Quality Acceptance (%)", 0, 100, 95)
    cc = st.slider("Cost Competitiveness (%)", 0, 100, 80)
    if st.button("Evaluate Supplier"):
        res = calculate_supplier_scorecard(otd, qa, cc)
        st.metric(label="Total Score", value=f"{res['total_score']} / 100")
        st.success(f"Supplier Tier: {res['tier']}")
