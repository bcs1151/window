import streamlit as st
import datetime
import pandas as pd

st.set_page_config(page_title="UPVC Price Proposal", layout="wide")

st.title("🪟 UPVC Price Proposal Generator")
st.write("Auto-calculate material value, GST, and net payable amount based on your inputs.")

# --- Proposal Details ---
st.header("📄 Proposal Details")
col1, col2, col3 = st.columns(3)
with col1:
    proposal_no = st.text_input("Proposal No.", "208")
with col2:
    proposal_date = st.date_input("Date", datetime.date.today())
with col3:
    site_address = st.text_input("Site Address", "C-90 Kavi Nagar, Ghaziabad")

col4, col5 = st.columns(2)
with col4:
    contact_no = st.text_input("Contact No.", "")
with col5:
    architect = st.text_input("Architect", "")

# --- Product / Window Details ---
st.header("🧱 Product Details")
colA, colB, colC = st.columns(3)
with colA:
    window_design = st.text_input("Window Design", "Slimline Internal Sliding Folding Partition (0+5)")
with colB:
    width = st.number_input("Width (mm)", 0, value=3900)
with colC:
    height = st.number_input("Height (mm)", 0, value=3000)

colD, colE, colF = st.columns(3)
with colD:
    qty = st.number_input("Quantity", 1, value=1)
with colE:
    rate = st.number_input("Rate (INR per Sqft)", 0.0, value=2765.0)
with colF:
    glass_thickness = st.text_input("Glass Thickness", "8MM CLIT")

profile_color = st.text_input("Profile Colour", "MATT BLACK")

# --- Calculations ---
st.header("📊 Calculation Summary")

# Convert mm → sqft
area_sqft = (width * height) / 92903.04  # 1 sqft = 92903.04 mm²
total_area = area_sqft * qty
total_material_value = total_area * rate

install_charge = st.number_input("Installation / Loading / Unloading (₹)", 0.0, value=25000.0)
freight_charge = st.number_input("Freight Charge (₹)", 0.0, value=4000.0)
gst_rate = st.number_input("GST (%)", 0.0, 100.0, value=18.0)

# Computations
total_value = total_material_value + install_charge + freight_charge
gst_amount = total_value * gst_rate / 100
net_payable = total_value + gst_amount

# --- Display Results ---
st.subheader("💰 Price Summary")

st.markdown(f"""
| Description | Amount (₹) |
|--------------|------------:|
| **Total Area (Sqft)** | {total_area:,.2f} |
| **Total Material Value** | {total_material_value:,.2f} |
| **Installation / Loading / Unloading** | {install_charge:,.2f} |
| **Freight Charge** | {freight_charge:,.2f} |
| <span style="background-color:yellow; font-weight:bold;">Total Value</span> | <span style="background-color:yellow; font-weight:bold;">{total_value:,.2f}</span> |
| **GST @ {gst_rate:.0f}%** | {gst_amount:,.2f} |
| <span style="background-color:lightgreen; font-weight:bold;">Net Payable Amount</span> | <span style="background-color:lightgreen; font-weight:bold;">{net_payable:,.2f}</span> |
""", unsafe_allow_html=True)

# --- Optional PDF Export ---
st.write("### 📤 Download Proposal as PDF")

df = pd.DataFrame({
    "Field": ["Proposal No", "Date", "Window Design", "Width", "Height", "Qty", "Rate", "Total Value", "GST", "Net Payable"],
    "Value": [proposal_no, str(proposal_date), window_design, width, height, qty, rate, total_value, gst_amount, net_payable]
})

csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download as CSV",
    data=csv,
    file_name=f"UPVC_Proposal_{proposal_no}.csv",
    mime="text/csv"
)

st.info("💡 Tip: You can export this data as CSV and convert to PDF using Excel or integrate FPDF later.")
