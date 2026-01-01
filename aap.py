import streamlit as st
import pandas as pd
from automated_report import get_data, generate_ai_summary

st.set_page_config(page_title="Interactive AI Dashboard", layout="wide")

st.title("📊 Production Support AI Dashboard")

# 1. Fetch the data
df_raw = get_data()

# --- THE FIX: Force headers to uppercase so SERVICE_NAME always works ---
df_raw.columns = [c.strip().upper() for c in df_raw.columns]
# -----------------------------------------------------------------------

# 2. Sidebar Filters
st.sidebar.header("Filter Controls")
all_services = df_raw['SERVICE_NAME'].unique() # This will no longer crash!
selected_services = st.sidebar.multiselect("Select Services", options=all_services, default=all_services)

# 3. Filter the dataframe
df_filtered = df_raw[df_raw['SERVICE_NAME'].isin(selected_services)]

# 4. Display Metrics
st.write("### Data Table")
st.dataframe(df_filtered)

# 5. AI Analysis
if st.button("Generate AI Analysis"):
    with st.spinner("Analyzing..."):
        summary = generate_ai_summary(df_filtered)
        st.info(summary)
# --- 6. The Visual Impact ---
st.write("### Performance Visualization")

# Create a chart that updates as you change the filters
st.bar_chart(data=df_filtered, x="SERVICE_NAME", y="SUCCESS_RATE")

# --- 7. The "Automated Alert" ---
# This automatically scans the data and flags failures for the manager
failed_services = df_filtered[df_filtered['SUCCESS_RATE'] < 95]['SERVICE_NAME'].tolist()

if failed_services:
    st.error(f"⚠️ SLA BREACH: The following services are below 95%: {', '.join(failed_services)}")
else:
    st.success("✅ All selected services are meeting SLA targets.")

from fpdf import FPDF
import datetime

def create_pdf(df, summary):
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Mainframe Performance Executive Report", ln=True, align='C')
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt=f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
    
    # Data Table
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Service Metrics:", ln=True)
    pdf.set_font("Arial", size=10)
    for index, row in df.iterrows():
        pdf.cell(200, 10, txt=f"- {row['SERVICE_NAME']}: {row['SUCCESS_RATE']}%", ln=True)
    
    # AI Summary
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="AI Analysis & Mainframe Root Cause:", ln=True)
    pdf.set_font("Arial", size=10)
    pdf.multi_cell(0, 10, txt=summary)
    
    return pdf.output(dest='S').encode('latin-1')

# --- Add the Download Button to the Sidebar ---
if 'summary' in locals(): # Only show if AI has run
    pdf_data = create_pdf(df_filtered, summary)
    st.sidebar.download_button(
        label="📥 Download PDF Report",
        data=pdf_data,
        file_name="Production_Report.pdf",
        mime="application/pdf"
    )