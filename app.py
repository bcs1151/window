# app.py
import streamlit as st
import datetime
from decimal import Decimal, ROUND_HALF_UP

st.set_page_config(page_title="UPVC Proposal (visual)", layout="wide")
st.title("UPVC Price Proposal — Visual Output")

# Helper
def fmt(x):
    try:
        return f"{float(x):,.2f}"
    except:
        return x

def round2(x):
    return float(Decimal(x).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

# Form for inputs
with st.form("proposal_form"):
    st.header("Input (proposal fields)")
    c1, c2, c3 = st.columns([1,1,2])
    with c1:
        proposal_no = st.text_input("Proposal No.", value="208")
        proposal_date = st.date_input("Date", value=datetime.date(2025,8,13))
    with c2:
        site_address = st.text_input("Site Address", value="C-90 Kavi Nagar, Ghaziabad")
        contact_no = st.text_input("Contact No.", value="")
    with c3:
        architect = st.text_input("Architect", value="")
        email = st.text_input("Email ID", value="")

    st.subheader("Window / Pricing")
    w1, w2, w3, w4 = st.columns(4)
    with w1:
        window_design = st.text_input("Window Design", value="SLIMLINE INTERNAL SLIDING FOLDING PARTITION (0+5)")
    with w2:
        width_mm = st.number_input("Width (mm)", min_value=0, value=3900)
    with w3:
        height_mm = st.number_input("Height (mm)", min_value=0, value=3000)
    with w4:
        qty = st.number_input("Qty", min_value=1, value=1)

    r1, r2, r3 = st.columns(3)
    with r1:
        rate = st.number_input("Rate (INR / Sqft)", min_value=0.0, value=2765.0, step=1.0)
    with r2:
        glass = st.text_input("Glass (thickness / type)", value="8MM CLIT")
    with r3:
        profile_colour = st.text_input("Profile Colour", value="MATT BLACK")

    st.subheader("Other charges & tax")
    i1, i2, i3 = st.columns(3)
    with i1:
        installation = st.number_input("Installation / Loading / Unloading (₹)", value=25000.0, min_value=0.0)
    with i2:
        freight = st.number_input("Freight Charge (₹)", value=4000.0, min_value=0.0)
    with i3:
        gst_rate = st.number_input("GST (%)", min_value=0.0, max_value=100.0, value=18.0)

    submitted = st.form_submit_button("Generate Proposal")

# If form not submitted, still offer a quick generate (so user can see preview)
if not submitted:
    if st.button("Quick Generate (use current inputs)"):
        submitted = True

if submitted:
    # Calculations
    # 1 sqft = 92903.04 mm² (i.e., 304.8mm * 304.8mm)
    area_sqft_each = (width_mm * height_mm) / 92903.04 if width_mm and height_mm else 0
    total_area = area_sqft_each * qty
    total_material_value = total_area * rate
    total_value = total_material_value + installation + freight
    gst_amount = total_value * (gst_rate / 100.0)
    net_payable = total_value + gst_amount

    # Round numbers
    area_sqft_each = round2(area_sqft_each)
    total_area = round2(total_area)
    total_material_value = round2(total_material_value)
    total_value = round2(total_value)
    gst_amount = round2(gst_amount)
    net_payable = round2(net_payable)

    # Build HTML that matches the styling of your image (table-like, colored rows)
    html = f"""
    <html>
    <head>
    <style>
      body {{ font-family: Arial, Helvetica, sans-serif; color: #111; }}
      .proposal {{ width: 100%; max-width: 1100px; margin: 10px auto; border: 1px solid #333; padding: 10px; }}
      .header-box {{ border: 1px solid #999; padding: 8px; font-size: 14px; }}
      .title {{ text-align: center; font-weight: bold; margin-top: 6px; margin-bottom: 6px; font-size: 16px; }}
      table.quote {{ border-collapse: collapse; width: 100%; font-size: 13px; }}
      table.quote th, table.quote td {{
          border: 1px solid #333;
          padding: 6px;
          vertical-align: middle;
      }}
      table.quote th {{ background: #f2f2f2; text-align: left; font-weight:600; }}
      .center {{ text-align:center; }}
      .small {{ font-size:12px; color:#222; }}
      .yellow {{ background: #fff39e; font-weight:700; }}
      .green {{ background: #b9f3c9; font-weight:700; }}
      .right {{ text-align:right; }}
      .no-border {{ border: none; }}
      .meta-row td {{ border: none; padding: 3px 6px; }}
      .img-cell {{ width:120px; text-align:center; }}
      .product-img {{ width:100px; height:70px; background:#e9f6ff; display:inline-block; border:1px solid #ccc; }}
    </style>
    </head>
    <body>
      <div class="proposal">
        <table style="width:100%; border-collapse:collapse;">
          <tr>
            <td style="width:65%;">
              <div class="header-box">
                <div><strong>Proposal No:</strong> {proposal_no}</div>
                <div><strong>Dated:</strong> {proposal_date}</div>
                <div><strong>Kind Attention:</strong> </div>
                <div><strong>Site Address:</strong> {site_address}</div>
                <div><strong>Contact No:</strong> {contact_no}</div>
                <div><strong>Architect:</strong> {architect}</div>
                <div><strong>Email ID:</strong> {email}</div>
              </div>
            </td>
            <td style="width:35%; text-align:center;">
              <div style="border:1px solid #999; padding:6px;">
                <div style="font-weight:700;">PRICE PROPOSAL FOR SLIMLINE INTERNAL SLIDING FOLDING PARTITION</div>
              </div>
            </td>
          </tr>
        </table>

        <br/>

        <table class="quote">
          <tr>
            <th style="width:3%;">S.No</th>
            <th style="width:18%;">Window Design</th>
            <th style="width:10%;">Location</th>
            <th style="width:20%;">Window code as per coupler</th>
            <th style="width:20%;">Dimension (mm) <br/><span class='small'>(Width × Height)</span></th>
            <th style="width:6%;">Area in Sft</th>
            <th style="width:6%;">Qty</th>
            <th style="width:8%;">Total Area (in Sft)</th>
            <th style="width:8%;">Total Price (in INR)</th>
          </tr>

          <tr>
            <td class="center">1</td>
            <td>{window_design}</td>
            <td class="center">-</td>
            <td class="center">SLIMLINE INTERNAL SLIDING FOLDING PARTITION (0+5)</td>
            <td class="center">{width_mm} × {height_mm}</td>
            <td class="center">{fmt(area_sqft_each)}</td>
            <td class="center">{int(qty)}</td>
            <td class="right">{fmt(total_area)}</td>
            <td class="right">{fmt(total_material_value)}</td>
          </tr>

          <!-- summary rows -->
          <tr>
            <td colspan="8" class="right"><strong>Total Number of windows</strong></td>
            <td class="center"><strong>{int(qty)}</strong></td>
          </tr>
          <tr>
            <td colspan="8" class="right">Total Area In Sqft</td>
            <td class="right">{fmt(total_area)}</td>
          </tr>
          <tr>
            <td colspan="8" class="right">Total Material value</td>
            <td class="right">{fmt(total_material_value)}</td>
          </tr>
          <tr>
            <td colspan="8" class="right">Total Glass value</td>
            <td class="right">0.00</td>
          </tr>
          <tr>
            <td colspan="8" class="right">Installation Charges/Loading/Unloading charges</td>
            <td class="right">{fmt(installation)}</td>
          </tr>
          <tr>
            <td colspan="8" class="right">Freight Charge</td>
            <td class="right">{fmt(freight)}</td>
          </tr>

          <tr class="yellow">
            <td colspan="8" class="right"><strong>Total Value</strong></td>
            <td class="right"><strong>{fmt(total_value)}</strong></td>
          </tr>

          <tr>
            <td colspan="8" class="right">GST Tax @ {gst_rate:.0f}%</td>
            <td class="right">{fmt(gst_amount)}</td>
          </tr>

          <tr class="green">
            <td colspan="8" class="right"><strong>Net Payable Amount</strong></td>
            <td class="right"><strong>{fmt(net_payable)}</strong></td>
          </tr>
        </table>

        <br/>
        <div class="small">Note: This proposal layout is visually produced from the input fields. You can copy / screenshot or extend to PDF export if required.</div>
      </div>
    </body>
    </html>
    """

    # Render HTML in Streamlit (allow scripts disabled)
    st.components.v1.html(html, height=820, scrolling=True)
    st.success("Proposal generated — copy, screenshot or extend to PDF export as needed.")
