import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import time

# Add root directory to path to import local modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from inventory.eoq import calculate_eoq
from inventory.reorder_point import calculate_reorder_point
from production.production_efficiency import calculate_oee
from procurement.supplier_scorecard import calculate_supplier_scorecard

st.set_page_config(page_title="SCMS Dashboard", layout="wide")
st.title("📊 Supply Chain Analytics Dashboard")

# ==========================================
# DATA INITIALIZATION & STATE MANAGEMENT
# ==========================================
def generate_warehouse_data():
    """Generates initial massive warehouse dataset"""
    np.random.seed(42)
    n_rows = 10000
    df = pd.DataFrame({
        'SKU': [f'SKU-{i:05d}' for i in range(n_rows)],
        'Product_Name': np.random.choice(['Steel Widget', 'Cog', 'Sprocket', 'Gadget', 'Screw', 'Bolt', 'Router', 'Cable'], n_rows),
        'Category': np.random.choice(['Raw Material', 'Finished Good', 'Spare Part'], n_rows),
        'Unit_Cost': np.round(np.random.uniform(0.5, 150.0, n_rows), 2),
        'Safety_Stock': np.random.randint(50, 500, n_rows),
        'Lead_Time_Days': np.random.randint(1, 30, n_rows)
    })
    df['Inbound_Stock'] = np.random.randint(1000, 10000, n_rows)
    df['Outbound_Stock'] = np.random.randint(500, 9500, n_rows)
    df['Remaining_Stock'] = (df['Inbound_Stock'] - df['Outbound_Stock']).clip(lower=0)
    df['Inventory_Value'] = df['Remaining_Stock'] * df['Unit_Cost']
    return df

# Initialize data in session state
if 'warehouse_df' not in st.session_state:
    data_path = 'data/processed/warehouse_movements.csv'
    if os.path.exists(data_path):
        st.session_state.warehouse_df = pd.read_csv(data_path)
    else:
        os.makedirs('data/processed', exist_ok=True)
        df = generate_warehouse_data()
        df.to_csv(data_path, index=False)
        st.session_state.warehouse_df = df

def simulate_live_movement(df):
    """Simulates automated real-time warehouse movements"""
    # 1. Simulate Customer Orders (Pick Stock Out)
    n_outbound = np.random.randint(5, 20)
    outbound_indices = np.random.choice(df.index, size=n_outbound, replace=False)
    for idx in outbound_indices:
        qty = np.random.randint(10, 100)
        # Ensure we don't pick more than remaining
        df.at[idx, 'Outbound_Stock'] += min(qty, df.at[idx, 'Remaining_Stock'])

    # 2. Simulate Supplier Deliveries (Add Stock In)
    n_inbound = np.random.randint(2, 10)
    inbound_indices = np.random.choice(df.index, size=n_inbound, replace=False)
    for idx in inbound_indices:
        qty = np.random.randint(50, 500)
        df.at[idx, 'Inbound_Stock'] += qty

    # 3. Recalculate
    df['Remaining_Stock'] = (df['Inbound_Stock'] - df['Outbound_Stock']).clip(lower=0)
    df['Inventory_Value'] = df['Remaining_Stock'] * df['Unit_Cost']
    return df

# Sidebar Navigation
menu = st.sidebar.radio("Menu", ["Live Warehouse Simulation", "Stock Movements (Manual)", "Inventory Optimization", "Production Efficiency", "Procurement & Suppliers"])

# ==========================================
# PAGE 1: LIVE WAREHOUSE AUTOMATION
# ==========================================
if menu == "Live Warehouse Simulation":
    st.header("🏬 Automated Live Warehouse Overview")
    st.write("Turn on the simulation to watch the 10,000 SKUs automatically process inbound and outbound movements in real-time.")
    
    # Simulation Toggle
    col_toggle, col_status = st.columns([1, 3])
    with col_toggle:
        run_sim = st.toggle("▶️ Start Automated Simulation")
    with col_status:
        if run_sim:
            st.success("Simulation Running: Processing live movements...")
        else:
            st.info("Simulation Paused.")

    # Load Data
    df = st.session_state.warehouse_df
    
    # Calculate KPIs
    total_inbound = df['Inbound_Stock'].sum()
    total_outbound = df['Outbound_Stock'].sum()
    total_remaining = df['Remaining_Stock'].sum()
    total_value = df['Inventory_Value'].sum()
    critical_stock_count = len(df[df['Remaining_Stock'] < df['Safety_Stock']])
    
    # Display KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric(label="⬇️ Total Inbound", value=f"{total_inbound:,}")
    with col2: st.metric(label="⬆️ Total Outbound", value=f"{total_outbound:,}")
    with col3: st.metric(label="📦 Total Remaining", value=f"{total_remaining:,}")
    with col4: st.metric(label="💵 Total Value", value=f"${total_value:,.2f}")
        
    st.divider()
    
    # Alert Banner
    if critical_stock_count > 0:
        st.warning(f"⚠️ **Action Required:** {critical_stock_count:,} SKUs have dropped below their Safety Stock level.")
    
    # Chart
    st.subheader("Inbound vs Outbound vs Remaining by Category")
    chart_data = df.groupby('Category')[['Inbound_Stock', 'Outbound_Stock', 'Remaining_Stock']].sum()
    st.bar_chart(chart_data)
    
    st.divider()
    st.subheader("Top 15 Critical Items (Lowest Stock)")
    # Show the most critical items dynamically updating
    critical_df = df.sort_values('Remaining_Stock').head(15)
    st.dataframe(critical_df[['SKU', 'Product_Name', 'Remaining_Stock', 'Safety_Stock']], use_container_width=True)
    
    # If simulation is running, update data and rerun
    if run_sim:
        # Process automated movements
        st.session_state.warehouse_df = simulate_live_movement(df)
        
        # Save to CSV
        st.session_state.warehouse_df.to_csv('data/processed/warehouse_movements.csv', index=False)
        
        # Wait 3 seconds and refresh the UI
        time.sleep(3)
        st.rerun()

# ==========================================
# PAGE 2: MANUAL STOCK MOVEMENTS
# ==========================================
elif menu == "Stock Movements (Manual)":
    st.header("🔄 Manual Warehouse Stock Movements")
    st.write("Select an SKU to manually Add new stock (Inbound) or Pick existing stock (Outbound).")
    
    df = st.session_state.warehouse_df
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Select Item & Action")
        sku_list = df['SKU'].tolist()
        selected_sku = st.selectbox("Search/Select SKU:", sku_list)
        
        item = df[df['SKU'] == selected_sku].iloc[0]
        st.write(f"**Product Name:** {item['Product_Name']}")
        
        action = st.radio("Action:", ["Add Stock (Inbound)", "Pick Stock (Outbound)"])
        qty = st.number_input("Quantity to move:", min_value=1, value=100, step=10)
        
        if st.button("Execute Movement", type="primary"):
            idx = df.index[df['SKU'] == selected_sku][0]
            if action == "Add Stock (Inbound)":
                df.at[idx, 'Inbound_Stock'] += qty
                st.success(f"✅ Added {qty} units to {selected_sku}.")
            else:
                if qty > df.at[idx, 'Remaining_Stock']:
                    st.error(f"❌ Cannot pick {qty} units. Only {df.at[idx, 'Remaining_Stock']} remaining!")
                else:
                    df.at[idx, 'Outbound_Stock'] += qty
                    st.success(f"✅ Picked {qty} units from {selected_sku}.")
            
            df['Remaining_Stock'] = (df['Inbound_Stock'] - df['Outbound_Stock']).clip(lower=0)
            df['Inventory_Value'] = df['Remaining_Stock'] * df['Unit_Cost']
            st.session_state.warehouse_df = df
            df.to_csv('data/processed/warehouse_movements.csv', index=False)
            st.rerun()

    with col2:
        st.subheader("Current Item Status")
        item_updated = df[df['SKU'] == selected_sku].iloc[0]
        m1, m2 = st.columns(2)
        with m1:
            st.metric(label="Total Inbound", value=f"{int(item_updated['Inbound_Stock']):,}")
            st.metric(label="Remaining Stock", value=f"{int(item_updated['Remaining_Stock']):,}")
        with m2:
            st.metric(label="Total Outbound", value=f"{int(item_updated['Outbound_Stock']):,}")
            st.metric(label="Current Value", value=f"${item_updated['Inventory_Value']:,.2f}")

# ==========================================
# PAGE 3: INVENTORY OPTIMIZATION
# ==========================================
elif menu == "Inventory Optimization":
    st.header("Inventory Optimization Calculators")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Economic Order Quantity (EOQ)")
        demand = st.number_input("Annual Demand (Units)", min_value=1, value=10000, key="eoq_d")
        order_c = st.number_input("Ordering Cost ($)", min_value=0.1, value=50.0, key="eoq_oc")
        hold_c = st.number_input("Holding Cost per Unit ($)", min_value=0.1, value=2.5, key="eoq_hc")
        if st.button("Calculate EOQ"):
            res = calculate_eoq(demand, order_c, hold_c)
            st.success(f"Optimal Order Quantity: {res['eoq']} units")

    with col2:
        st.subheader("Reorder Point (ROP)")
        daily_d = st.number_input("Avg Daily Demand", min_value=0.0, value=30.0, key="rop_dd")
        lead_t = st.number_input("Lead Time (Days)", min_value=0, value=7, key="rop_lt")
        safety_s = st.number_input("Safety Stock", min_value=0, value=50, key="rop_ss")
        if st.button("Calculate ROP"):
            res = calculate_reorder_point(daily_d, lead_t, safety_s)
            st.warning(f"Trigger Purchase Order at: {res['reorder_point']} units")

# ==========================================
# PAGE 4: PRODUCTION EFFICIENCY
# ==========================================
elif menu == "Production Efficiency":
    st.header("Overall Equipment Effectiveness (OEE)")
    col1, col2, col3 = st.columns(3)
    with col1: avail = st.slider("Availability", 0.0, 1.0, 0.85)
    with col2: perf = st.slider("Performance", 0.0, 1.0, 0.90)
    with col3: qual = st.slider("Quality", 0.0, 1.0, 0.95)
        
    if st.button("Calculate OEE"):
        res = calculate_oee(avail, perf, qual)
        st.metric(label="OEE Score", value=f"{res['oee_percentage']}%")
        st.write(f"Availability Loss: {res['availability_loss']}%")

# ==========================================
# PAGE 5: PROCUREMENT & SUPPLIERS
# ==========================================
elif menu == "Procurement & Suppliers":
    st.header("Supplier Scorecard")
    otd = st.slider("On-Time Delivery (%)", 0, 100, 85)
    qa = st.slider("Quality Acceptance (%)", 0, 100, 95)
    cc = st.slider("Cost Competitiveness (%)", 0, 100, 80)
    
    if st.button("Evaluate Supplier"):
        res = calculate_supplier_scorecard(otd, qa, cc)
        st.metric(label="Total Score", value=f"{res['total_score']} / 100")
        st.success(f"Supplier Tier: {res['tier']}")
