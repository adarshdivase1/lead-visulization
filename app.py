import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Enterprise Lead Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Advanced Professional CSS with Light/Dark Mode Support
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Root variables for theming */
    :root {
        --primary-color: #3b82f6;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --info-color: #06b6d4;
    }
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }
    
    /* Main container */
    .main > div {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Metric cards - Light mode */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px rgba(102, 126, 234, 0.3);
    }
    
    [data-testid="stMetric"] label {
        color: rgba(255, 255, 255, 0.95) !important;
        font-weight: 600;
        font-size: 0.875rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricValue"] {
        color: white !important;
        font-size: 2.25rem;
        font-weight: 700;
    }
    
    [data-testid="stMetric"] [data-testid="stMetricDelta"] {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    /* Headers - Light mode */
    h1 {
        color: #1e293b;
        font-weight: 800;
        padding-bottom: 1rem;
        border-bottom: 4px solid #667eea;
        margin-bottom: 1.5rem;
        letter-spacing: -0.5px;
    }
    
    h2 {
        color: #334155;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        letter-spacing: -0.3px;
    }
    
    h3 {
        color: #475569;
        font-weight: 600;
        margin-bottom: 0.75rem;
    }
    
    /* Insight boxes */
    .insight-box {
        background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
        border-left: 5px solid #3b82f6;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 12px;
        color: #0f172a;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.1);
    }
    
    .insight-box b {
        color: #1e40af;
        font-weight: 700;
    }
    
    /* Success box */
    .success-box {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 12px;
        color: #0f172a;
        box-shadow: 0 4px 6px rgba(16, 185, 129, 0.1);
    }
    
    /* Warning box */
    .warning-box {
        background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 5px solid #f59e0b;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-radius: 12px;
        color: #0f172a;
        box-shadow: 0 4px 6px rgba(245, 158, 11, 0.1);
    }
    
    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #f8fafc;
        border: 2px solid #e2e8f0;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    [data-testid="stExpander"]:hover {
        border-color: #cbd5e1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        padding: 0px 24px;
        background-color: transparent;
        border-radius: 8px;
        color: #64748b;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: white;
        color: #334155;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: white !important;
        color: #3b82f6 !important;
        box-shadow: 0 2px 8px rgba(59, 130, 246, 0.15);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #1e293b;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.2);
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.3);
        transform: translateY(-2px);
    }
    
    /* Download buttons */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg, #059669 0%, #047857 100%);
        transform: translateY(-2px);
    }
    
    /* Dataframe styling */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
        border: 2px dashed #cbd5e1;
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #3b82f6;
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
    }
    
    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        /* Main background */
        .main {
            background-color: #0f172a;
        }
        
        /* Headers - Dark mode */
        h1 {
            color: #f1f5f9;
            border-bottom-color: #8b5cf6;
        }
        
        h2 {
            color: #e2e8f0;
        }
        
        h3 {
            color: #cbd5e1;
        }
        
        /* Text */
        p, span, div {
            color: #e2e8f0;
        }
        
        /* Insight boxes - Dark mode */
        .insight-box {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-left-color: #60a5fa;
            color: #e2e8f0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        .insight-box b {
            color: #93c5fd;
        }
        
        .success-box {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-left-color: #34d399;
            color: #e2e8f0;
        }
        
        .warning-box {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-left-color: #fbbf24;
            color: #e2e8f0;
        }
        
        /* Expanders - Dark mode */
        [data-testid="stExpander"] {
            background-color: #1e293b;
            border-color: #334155;
        }
        
        [data-testid="stExpander"]:hover {
            border-color: #475569;
        }
        
        /* Tabs - Dark mode */
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1e293b;
        }
        
        .stTabs [data-baseweb="tab"] {
            color: #94a3b8;
        }
        
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #334155;
            color: #e2e8f0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #334155 !important;
            color: #60a5fa !important;
        }
        
        /* Sidebar - Dark mode */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        }
        
        [data-testid="stSidebar"] h1, 
        [data-testid="stSidebar"] h2, 
        [data-testid="stSidebar"] h3 {
            color: #f1f5f9;
        }
        
        /* File uploader - Dark mode */
        [data-testid="stFileUploader"] {
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            border-color: #475569;
        }
        
        [data-testid="stFileUploader"]:hover {
            border-color: #60a5fa;
            background: linear-gradient(135deg, #1e3a5f 0%, #1e40af 100%);
        }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main > div > div {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Enterprise Lead Analytics Dashboard")
st.markdown("*AI-Powered Sales Intelligence & Performance Tracking*")

def extract_leads_from_excel(df_raw):
    """Extract lead data from hierarchical Excel structure"""
    try:
        data_rows = df_raw.values.tolist()
        leads_data = []
        current_month = None
        current_status = None
        current_owner = None
        
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']
        statuses = ['New', 'Contacted', 'Pre-Qualified', 'Pre Qualified', 
                   'Lost Lead', 'Postpone', 'Attempted to Contact', 
                   'Not Qualified', 'Cold Call', 'Qualified', 'Converted']
        owners = ['Onkar', 'Balasubramanian', 'Samyuktha', 'Pravesh', 
                 'Devangi', 'Gauri', 'Saphinangi', 'Sneha', 'Nishant', 
                 'Asmita', 'Tirath', 'Nivedita', 'Selvam', 'social Inv']
        
        for row in data_rows:
            row = [str(cell).strip() if pd.notna(cell) else "" for cell in row]
            
            if all(cell == "" or cell == "nan" for cell in row):
                continue
            
            if len(row) > 0 and any(month in row[0] for month in months):
                current_month = row[0].split('(')[0].strip()
                continue
            
            if len(row) > 1 and any(status.lower() in row[1].lower() for status in statuses):
                current_status = row[1].split('(')[0].strip()
                continue
            
            if len(row) > 2 and any(owner.lower() in row[2].lower() for owner in owners):
                current_owner = row[2].split('(')[0].strip()
                continue
            
            lead_name = row[3] if len(row) > 3 else ""
            
            if (lead_name and 
                lead_name not in ["", "nan", "None", ".", "-"] and 
                len(lead_name) > 1 and
                current_month and 
                current_status and 
                current_owner):
                
                lead_record = {
                    'Month': current_month,
                    'Status': current_status,
                    'Sales_Person': current_owner,
                    'Lead_Name': lead_name,
                    'Source': row[4] if len(row) > 4 else '',
                    'Company': row[5] if len(row) > 5 else ''
                }
                leads_data.append(lead_record)
        
        if not leads_data:
            return None
        
        df_clean = pd.DataFrame(leads_data)
        df_clean['Month'] = df_clean['Month'].str.replace(r'\s*\(\d+\)', '', regex=True).str.strip()
        df_clean['Status'] = df_clean['Status'].str.replace(r'\s*\(\d+\)', '', regex=True).str.strip()
        df_clean['Sales_Person'] = df_clean['Sales_Person'].str.replace(r'\s*\(\d+\)', '', regex=True).str.strip()
        df_clean['Company'] = df_clean['Company'].str.strip()
        df_clean['Source'] = df_clean['Source'].str.strip()
        
        status_mapping = {
            'Pre Qualified': 'Pre-Qualified',
            'Postpone': 'Postponed',
        }
        df_clean['Status'] = df_clean['Status'].replace(status_mapping)
        
        # More conservative duplicate removal - only if ALL fields match
        df_clean = df_clean.drop_duplicates(subset=['Lead_Name', 'Month', 'Sales_Person', 'Company', 'Source'], keep='first')
        
        # Debug: Show how many duplicates were removed
        duplicates_removed = len(leads_data) - len(df_clean)
        if duplicates_removed > 0:
            st.info(f"ℹ️ Removed {duplicates_removed} exact duplicate entries")
        
        return df_clean
        
    except Exception as e:
        st.error(f"Error extracting data: {str(e)}")
        return None

def load_data(uploaded_file):
    """Load and validate data from uploaded file"""
    try:
        file_extension = uploaded_file.name.split('.')[-1].lower()
        
        # DEBUG: Show file info
        st.info(f"📂 File: {uploaded_file.name} | Size: {uploaded_file.size} bytes | Type: {file_extension}")
        
        if file_extension == 'csv':
            df = pd.read_csv(uploaded_file)
            st.info(f"🔍 CSV RAW: Loaded {len(df)} rows initially")
            
            if 'Month' not in df.columns:
                st.info("📄 Detecting hierarchical format...")
                df_raw = pd.read_csv(uploaded_file, header=None)
                st.warning(f"🔍 RAW DATA: {len(df_raw)} rows in hierarchical format")
                df = extract_leads_from_excel(df_raw)
                if df is not None:
                    st.success(f"✅ PARSED: Extracted {len(df)} leads from hierarchical format")
                if df is None:
                    return None
        
        elif file_extension in ['xlsx', 'xls']:
            df_test = pd.read_excel(uploaded_file, nrows=5)
            if 'Month' in df_test.columns:
                st.info("🔍 Standard format detected. Loading directly.")
                df = pd.read_excel(uploaded_file)
                st.info(f"🔍 Excel RAW: Loaded {len(df)} rows initially")
            else:
                st.info("📄 Detecting hierarchical format...")
                df_raw = pd.read_excel(uploaded_file, header=None)
                st.warning(f"🔍 RAW DATA: {len(df_raw)} rows in hierarchical format")
                df = extract_leads_from_excel(df_raw)
                if df is not None:
                    st.success(f"✅ PARSED: Extracted {len(df)} leads from hierarchical format")
                if df is None:
                    return None
        else:
            st.error(f"Unsupported file format: {file_extension}")
            return None
        
        if df is None or df.empty:
            st.error("Empty file")
            return None
        
        required_cols = ['Month', 'Status', 'Sales_Person', 'Lead_Name', 'Source', 'Company']
        missing_cols = [col for col in required_cols if col not in df.columns]
        
        if missing_cols:
            st.error(f"❌ Missing columns: {', '.join(missing_cols)}")
            return None
        
        df['Month_Date'] = pd.to_datetime(df['Month'], format='%B %Y', errors='coerce')
        
        if df['Month_Date'].isna().all():
            df['Month_Date'] = pd.to_datetime(df['Month'], errors='coerce')
        
        df = df.dropna(subset=['Month_Date'])
        
        if df.empty:
            st.error("No valid dates found")
            return None
        
        df = df.sort_values('Month_Date')
        
        for col in ['Status', 'Sales_Person', 'Source', 'Company']:
            if col in df.columns:
                df[col] = df[col].fillna('').astype(str).str.strip()
        
        # EXTREMELY CONSERVATIVE filtering - only remove exact matches
        test_entries_before = len(df)
        
        # Only remove if Lead_Name is EXACTLY these values (case-insensitive)
        exact_test_names = ['test', 'testt', 'abc']
        df = df[~df['Lead_Name'].str.strip().str.lower().isin(exact_test_names)]
        
        # Only remove if Company is EXACTLY these values
        exact_test_companies = ['testing compny001', 'testing company001', 'test company']
        df = df[~df['Company'].str.strip().str.lower().isin(exact_test_companies)]
        
        test_entries_removed = test_entries_before - len(df)
        
        # DETAILED DEBUG INFO
        if test_entries_removed > 0:
            st.warning(f"⚠️ Removed {test_entries_removed} test entries")
        
        # Show what was actually removed
        with st.expander("🔍 DEBUG: What was filtered out?"):
            st.write(f"**Before filtering:** {test_entries_before} records")
            st.write(f"**After filtering:** {len(df)} records")
            st.write(f"**Removed:** {test_entries_removed} records")
            
            if test_entries_removed > 0:
                st.write("**Filter criteria used:**")
                st.write("- Exact Lead Names removed:", exact_test_names)
                st.write("- Exact Company Names removed:", exact_test_companies)
        
        st.success(f"✅ Successfully loaded {len(df)} leads!")
        
        # COMPREHENSIVE data validation summary
        with st.expander("📊 DETAILED Data Validation Summary - OPEN THIS!", expanded=True):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("📊 Total Records", len(df))
            with col2:
                st.metric("📅 Date Range", f"{df['Month_Date'].min().strftime('%b %Y')} - {df['Month_Date'].max().strftime('%b %Y')}")
            with col3:
                st.metric("👥 Unique Salespeople", df['Sales_Person'].nunique())
            with col4:
                st.metric("🏢 Unique Companies", df['Company'].nunique())
            
            st.markdown("---")
            st.markdown("### 📋 Status Distribution:")
            status_counts = df['Status'].value_counts().to_dict()
            status_df = pd.DataFrame({
                'Status': status_counts.keys(),
                'Count': status_counts.values()
            })
            status_df['Percentage'] = (status_df['Count'] / len(df) * 100).round(2)
            st.dataframe(status_df, use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### 👥 Top 10 Salespeople by Volume:")
            top_sales = df['Sales_Person'].value_counts().head(10)
            st.dataframe(pd.DataFrame({
                'Salesperson': top_sales.index,
                'Lead Count': top_sales.values
            }), use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### 📅 Monthly Distribution:")
            monthly_dist = df.groupby('Month').size().reset_index(name='Count')
            monthly_dist = monthly_dist.merge(df[['Month', 'Month_Date']].drop_duplicates(), on='Month')
            monthly_dist = monthly_dist.sort_values('Month_Date')
            st.dataframe(monthly_dist[['Month', 'Count']], use_container_width=True, hide_index=True)
            
            st.markdown("---")
            st.markdown("### ⚠️ Data Quality Checks:")
            
            quality_checks = []
            
            # Check for missing lead names
            missing_names = df['Lead_Name'].isna().sum()
            quality_checks.append(f"✅ Missing lead names: {missing_names}")
            
            # Check for missing companies
            missing_companies = (df['Company'] == '').sum()
            quality_checks.append(f"ℹ️ Blank companies: {missing_companies}")
            
            # Check for missing sources
            missing_sources = (df['Source'] == '').sum()
            quality_checks.append(f"ℹ️ Blank sources: {missing_sources}")
            
            # Check date range
            date_span = (df['Month_Date'].max() - df['Month_Date'].min()).days
            quality_checks.append(f"✅ Date span: {date_span} days ({date_span/30:.1f} months)")
            
            for check in quality_checks:
                st.write(check)
            
            st.markdown("---")
            st.markdown("### 🔍 Sample of First 10 Records:")
            st.dataframe(df[['Month', 'Lead_Name', 'Company', 'Status', 'Sales_Person', 'Source']].head(10), 
                        use_container_width=True, hide_index=True)
        
        return df
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None

def calculate_metrics(df):
    """Calculate comprehensive KPIs with correct conversion definition"""
    total_leads = len(df)
    
    # CORRECTED: Only "Converted" status counts as conversion
    converted = len(df[df['Status'] == 'Converted'])
    pre_qualified = len(df[df['Status'] == 'Pre-Qualified'])
    
    contacted = len(df[df['Status'] == 'Contacted'])
    new_leads = len(df[df['Status'] == 'New'])
    lost_leads = len(df[df['Status'] == 'Lost Lead'])
    
    # CORRECTED: Conversion rate based only on "Converted" status
    conversion_rate = (converted / total_leads * 100) if total_leads > 0 else 0
    contact_rate = (contacted / total_leads * 100) if total_leads > 0 else 0
    loss_rate = (lost_leads / total_leads * 100) if total_leads > 0 else 0
    
    current_month = df['Month_Date'].max()
    last_month = current_month - pd.DateOffset(months=1)
    
    current_month_leads = len(df[df['Month_Date'] == current_month])
    last_month_leads = len(df[df['Month_Date'] == last_month])
    
    month_growth = ((current_month_leads - last_month_leads) / last_month_leads * 100) if last_month_leads > 0 else 0
    avg_leads_per_person = df.groupby('Sales_Person').size().mean()
    
    return {
        'total_leads': total_leads,
        'conversion_rate': conversion_rate,
        'contact_rate': contact_rate,
        'loss_rate': loss_rate,
        'new_leads': new_leads,
        'month_growth': month_growth,
        'avg_leads_per_person': avg_leads_per_person,
        'current_month_leads': current_month_leads,
        'active_salespeople': df['Sales_Person'].nunique(),
        'converted_leads': converted,  # Only Converted
        'lost_leads': lost_leads,
        'pre_qualified': pre_qualified,  # Separate tracking
        'active_leads': total_leads - converted - lost_leads
    }

def display_kpi_dashboard(metrics):
    """Executive KPI Dashboard with enhanced metrics"""
    st.subheader("📈 Executive Dashboard - Key Performance Indicators")
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Total Leads", f"{metrics['total_leads']:,}", 
                 help="Total leads in system")
    
    with col2:
        # CORRECTED: Benchmark changed to 3% (realistic for B2B)
        delta_color = "normal" if metrics['conversion_rate'] >= 3 else "inverse"
        st.metric("Conversion Rate", f"{metrics['conversion_rate']:.1f}%",
                 delta=f"{metrics['conversion_rate'] - 3:.1f}%",
                 help="Only 'Converted' status (Pre-Qualified shown separately)")
    
    with col3:
        st.metric("Contact Rate", f"{metrics['contact_rate']:.1f}%",
                 help="Successfully contacted leads")
    
    with col4:
        st.metric("Monthly Growth", f"{metrics['month_growth']:+.1f}%",
                 delta=f"{metrics['month_growth']:.1f}%",
                 help="MoM growth rate")
    
    with col5:
        st.metric("Active Sales Team", f"{metrics['active_salespeople']}",
                 help="Number of active salespeople")
    
    with col6:
        st.metric("Loss Rate", f"{metrics['loss_rate']:.1f}%",
                 delta=f"-{metrics['loss_rate']:.1f}%",
                 delta_color="inverse",
                 help="Lost lead percentage")

def create_monthly_trends_advanced(df):
    """Advanced monthly trends with comprehensive analytics"""
    st.subheader("📅 Monthly Lead Generation Trends & Analytics")
    
    monthly_data = df.groupby('Month').agg({
        'Lead_Name': 'count',
        'Month_Date': 'first'
    }).reset_index()
    monthly_data.columns = ['Month', 'Lead_Count', 'Date']
    monthly_data = monthly_data.sort_values('Date')
    
    monthly_data['MA_3'] = monthly_data['Lead_Count'].rolling(window=3, min_periods=1).mean()
    monthly_data['Growth_Rate'] = monthly_data['Lead_Count'].pct_change() * 100
    monthly_data['Cumulative'] = monthly_data['Lead_Count'].cumsum()
    
    fig = make_subplots(
        rows=3, cols=1,
        subplot_titles=('Lead Volume & Moving Average', 'Month-over-Month Growth Rate', 'Cumulative Lead Generation'),
        vertical_spacing=0.12,
        row_heights=[0.4, 0.3, 0.3]
    )
    
    # Lead volume bars
    fig.add_trace(
        go.Bar(
            x=monthly_data['Month'],
            y=monthly_data['Lead_Count'],
            name='Monthly Leads',
            marker=dict(
                color=monthly_data['Lead_Count'],
                colorscale='Blues',
                showscale=False,
                line=dict(color='rgba(255,255,255,0.5)', width=1)
            ),
            text=monthly_data['Lead_Count'].astype(int),
            textposition='outside',
            textfont=dict(size=11, color='#1e293b'),
            hovertemplate='<b>%{x}</b><br>Leads: %{y}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Moving average
    fig.add_trace(
        go.Scatter(
            x=monthly_data['Month'],
            y=monthly_data['MA_3'],
            name='3-Month Moving Avg',
            mode='lines+markers',
            line=dict(color='#ef4444', width=3),
            marker=dict(size=8, color='#ef4444', symbol='diamond'),
            hovertemplate='<b>%{x}</b><br>3-Month Avg: %{y:.1f}<extra></extra>'
        ),
        row=1, col=1
    )
    
    # Growth rate
    colors = ['#10b981' if x >= 0 else '#ef4444' for x in monthly_data['Growth_Rate'].fillna(0)]
    fig.add_trace(
        go.Bar(
            x=monthly_data['Month'],
            y=monthly_data['Growth_Rate'].fillna(0),
            name='Growth %',
            marker_color=colors,
            text=[f"{x:+.1f}%" for x in monthly_data['Growth_Rate'].fillna(0)],
            textposition='outside',
            textfont=dict(size=10),
            hovertemplate='<b>%{x}</b><br>Growth: %{y:.1f}%<extra></extra>'
        ),
        row=2, col=1
    )
    
    # Cumulative
    fig.add_trace(
        go.Scatter(
            x=monthly_data['Month'],
            y=monthly_data['Cumulative'],
            name='Cumulative Leads',
            mode='lines+markers',
            fill='tozeroy',
            line=dict(color='#8b5cf6', width=3),
            marker=dict(size=8, color='#8b5cf6'),
            hovertemplate='<b>%{x}</b><br>Total: %{y}<extra></extra>'
        ),
        row=3, col=1
    )
    
    fig.update_xaxes(title_text="Month", row=1, col=1, tickangle=-45)
    fig.update_yaxes(title_text="Lead Count", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=2, col=1, tickangle=-45)
    fig.update_yaxes(title_text="Growth %", row=2, col=1)
    fig.update_xaxes(title_text="Month", row=3, col=1, tickangle=-45)
    fig.update_yaxes(title_text="Cumulative", row=3, col=1)
    
    fig.update_layout(
        height=900,
        showlegend=True,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Insights
    latest_growth = monthly_data['Growth_Rate'].iloc[-1] if len(monthly_data) > 0 else 0
    avg_monthly = monthly_data['Lead_Count'].mean()
    best_month = monthly_data.loc[monthly_data['Lead_Count'].idxmax(), 'Month']
    best_count = monthly_data['Lead_Count'].max()
    
    st.markdown(f"""
    <div class="insight-box">
    <b>📊 Key Insights:</b><br>
    • Current month growth: <b style="color: {'#10b981' if latest_growth > 0 else '#ef4444'}">{latest_growth:+.1f}%</b><br>
    • Average monthly leads: <b>{avg_monthly:.0f}</b><br>
    • Best performing month: <b>{best_month}</b> with <b>{int(best_count)}</b> leads<br>
    • Total cumulative leads: <b>{monthly_data['Cumulative'].iloc[-1]}</b>
    </div>
    """, unsafe_allow_html=True)

def create_team_performance_comprehensive(df):
    """Comprehensive team performance analytics"""
    st.subheader("👥 Team Performance & Productivity Analysis")
    
    # Calculate comprehensive metrics per salesperson
    team_metrics = df.groupby('Sales_Person').agg({
        'Lead_Name': 'count',
        'Month_Date': lambda x: x.max()
    }).reset_index()
    
    team_metrics.columns = ['Sales_Person', 'Total_Leads', 'Last_Activity']
    
    # Calculate conversions properly - only "Converted" status
    converted_status = df[df['Status'] == 'Converted']
    converted_counts = converted_status.groupby('Sales_Person').size()
    team_metrics['Converted'] = team_metrics['Sales_Person'].map(converted_counts).fillna(0).astype(int)
    
    # Calculate pre-qualified separately
    preq_status = df[df['Status'] == 'Pre-Qualified']
    preq_counts = preq_status.groupby('Sales_Person').size()
    team_metrics['Pre_Qualified'] = team_metrics['Sales_Person'].map(preq_counts).fillna(0).astype(int)
    
    # Calculate contacted leads
    contacted_status = df[df['Status'] == 'Contacted']
    contacted_counts = contacted_status.groupby('Sales_Person').size()
    team_metrics['Contacted'] = team_metrics['Sales_Person'].map(contacted_counts).fillna(0).astype(int)
    
    # Calculate new leads
    new_status = df[df['Status'] == 'New']
    new_counts = new_status.groupby('Sales_Person').size()
    team_metrics['New'] = team_metrics['Sales_Person'].map(new_counts).fillna(0).astype(int)
    
    # Calculate lost leads
    lost_status = df[df['Status'] == 'Lost Lead']
    lost_counts = lost_status.groupby('Sales_Person').size()
    team_metrics['Lost'] = team_metrics['Sales_Person'].map(lost_counts).fillna(0).astype(int)
    
    # Calculate rates
    team_metrics['Conversion_Rate'] = (team_metrics['Converted'] / team_metrics['Total_Leads'] * 100).round(1)
    team_metrics['Active'] = team_metrics['Total_Leads'] - team_metrics['Converted'] - team_metrics['Lost']
    
    # Add a debug expander at the top
    with st.expander("🔍 Debug: Conversion Status Breakdown by Salesperson"):
        status_by_person = df.groupby(['Sales_Person', 'Status']).size().reset_index(name='Count')
        status_pivot = status_by_person.pivot(index='Sales_Person', columns='Status', values='Count').fillna(0).astype(int)
        # Sort by total leads
        status_pivot['Total'] = status_pivot.sum(axis=1)
        status_pivot = status_pivot.sort_values('Total', ascending=False)
        st.dataframe(status_pivot, use_container_width=True)
        
        st.info("💡 Converted = 'Converted' status only | Pre-Qualified tracked separately")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Performance scatter - sorted by total leads for clarity
        team_sorted = team_metrics.sort_values('Total_Leads', ascending=False).head(15)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=team_sorted['Total_Leads'],
            y=team_sorted['Conversion_Rate'],
            mode='markers+text',
            marker=dict(
                size=team_sorted['Total_Leads'] * 1.5 + 10,
                color=team_sorted['Conversion_Rate'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Conv %"),
                line=dict(width=2, color='white'),
                cmin=0,
                cmax=max(30, team_sorted['Conversion_Rate'].max())
            ),
            text=team_sorted['Sales_Person'].str.split().str[0],
            textposition='middle center',
            textfont=dict(size=9, color='white', family='Arial Black'),
            customdata=team_sorted[['Sales_Person', 'Converted']],
            hovertemplate='<b>%{customdata[0]}</b><br>Total Leads: %{x}<br>Conversion Rate: %{y:.1f}%<br>Converted: %{customdata[1]}<extra></extra>',
            name='Performance'
        ))
        
        fig.update_layout(
            title='Team Performance Matrix (Top 15)',
            xaxis_title="Total Leads Managed",
            yaxis_title="Conversion Rate (%)",
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Lead distribution by salesperson - top 10
        top_10 = team_metrics.nlargest(10, 'Total_Leads').sort_values('Total_Leads', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_10['Sales_Person'],
            x=top_10['Total_Leads'],
            orientation='h',
            marker=dict(
                color=top_10['Total_Leads'],
                colorscale='Viridis',
                showscale=False,
                line=dict(color='rgba(255,255,255,0.3)', width=1)
            ),
            text=top_10['Total_Leads'].astype(int),
            textposition='outside',
            customdata=top_10[['Converted', 'Conversion_Rate']],
            hovertemplate='<b>%{y}</b><br>Total: %{x}<br>Converted: %{customdata[0]}<br>Rate: %{customdata[1]:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Top 10 Sales Leaders by Volume',
            xaxis_title="Total Leads",
            yaxis_title="",
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed breakdown
    st.markdown("### 📊 Detailed Team Breakdown")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Stacked bar chart showing actual breakdown
        top_performers = team_metrics.nlargest(8, 'Total_Leads').sort_values('Total_Leads', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            name='Converted',
            y=top_performers['Sales_Person'],
            x=top_performers['Converted'],
            orientation='h',
            marker_color='#10b981',
            text=top_performers['Converted'].astype(int),
            textposition='inside',
            textfont=dict(color='white')
        ))
        
        fig.add_trace(go.Bar(
            name='Contacted',
            y=top_performers['Sales_Person'],
            x=top_performers['Contacted'],
            orientation='h',
            marker_color='#3b82f6',
            text=top_performers['Contacted'].astype(int),
            textposition='inside',
            textfont=dict(color='white')
        ))
        
        fig.add_trace(go.Bar(
            name='Pre-Qualified',
            y=top_performers['Sales_Person'],
            x=top_performers['Pre_Qualified'],
            orientation='h',
            marker_color='#06b6d4',
            text=top_performers['Pre_Qualified'].astype(int),
            textposition='inside',
            textfont=dict(color='white')
        ))
        
        fig.add_trace(go.Bar(
            name='New',
            y=top_performers['Sales_Person'],
            x=top_performers['New'],
            orientation='h',
            marker_color='#f59e0b',
            text=top_performers['New'].astype(int),
            textposition='inside',
            textfont=dict(color='white')
        ))
        
        fig.add_trace(go.Bar(
            name='Lost',
            y=top_performers['Sales_Person'],
            x=top_performers['Lost'],
            orientation='h',
            marker_color='#ef4444',
            text=top_performers['Lost'].astype(int),
            textposition='inside',
            textfont=dict(color='white')
        ))
        
        fig.update_layout(
            title='Lead Status Distribution (Top 8)',
            barmode='stack',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Number of Leads"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Conversion rate comparison - only those with conversions
        team_with_conversions = team_metrics[team_metrics['Converted'] > 0].copy()
        
        if len(team_with_conversions) > 0:
            top_conv = team_with_conversions.nlargest(8, 'Conversion_Rate').sort_values('Conversion_Rate', ascending=True)
            
            fig = go.Figure()
            
            colors = ['#10b981' if x >= 3 else '#f59e0b' if x >= 1 else '#ef4444' 
                     for x in top_conv['Conversion_Rate']]
            
            fig.add_trace(go.Bar(
                y=top_conv['Sales_Person'],
                x=top_conv['Conversion_Rate'],
                orientation='h',
                marker_color=colors,
                text=[f"{x:.1f}%" for x in top_conv['Conversion_Rate']],
                textposition='outside',
                customdata=top_conv['Converted'],
                hovertemplate='<b>%{y}</b><br>Rate: %{x:.1f}%<br>Converted: %{customdata}<extra></extra>'
            ))
            
            fig.update_layout(
                title='Top Conversion Rates',
                xaxis_title="Conversion Rate (%)",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No conversions recorded yet")
    
    with col3:
        # Performance tiers based on conversion rate
        if len(team_metrics) > 0:
            # CORRECTED: Realistic B2B thresholds
            high_performers = len(team_metrics[team_metrics['Conversion_Rate'] >= 3])
            medium_performers = len(team_metrics[(team_metrics['Conversion_Rate'] >= 1) & 
                                                 (team_metrics['Conversion_Rate'] < 3)])
            low_performers = len(team_metrics[team_metrics['Conversion_Rate'] < 1])
            
            fig = go.Figure()
            
            fig.add_trace(go.Pie(
                labels=['High (≥3%)', 'Medium (1-3%)', 'Low (<1%)'],
                values=[high_performers, medium_performers, low_performers],
                hole=0.5,
                marker=dict(colors=['#10b981', '#f59e0b', '#ef4444']),
                textposition='auto',
                textinfo='label+value+percent',
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
            ))
            
            fig.update_layout(
                title='Performance Tier Distribution',
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No performance data available")
    
    # Performance table
    with st.expander("📋 Complete Team Performance Table"):
        display_df = team_metrics.sort_values('Total_Leads', ascending=False).copy()
        
        # Format for display
        display_df_formatted = display_df.copy()
        display_df_formatted['Conversion_Rate'] = display_df_formatted['Conversion_Rate'].apply(lambda x: f"{x:.1f}%")
        display_df_formatted['Last_Activity'] = display_df_formatted['Last_Activity'].dt.strftime('%B %Y')
        
        # Reorder columns for better readability
        display_df_formatted = display_df_formatted[['Sales_Person', 'Total_Leads', 'Converted', 'Pre_Qualified', 'Contacted', 'New', 'Lost', 'Active', 'Conversion_Rate', 'Last_Activity']]
        
        st.dataframe(display_df_formatted, use_container_width=True, hide_index=True)
        
        # Add summary stats
        total_converted = display_df['Converted'].sum()
        avg_conv_rate = display_df['Conversion_Rate'].mean()
        
        if total_converted > 0:
            top_converter = display_df.nlargest(1, 'Converted')['Sales_Person'].values[0]
            top_conversions = display_df['Converted'].max()
            
            st.markdown(f"""
            <div class="insight-box">
            <b>📊 Team Summary:</b><br>
            • Total Converted Leads: <b>{int(total_converted)}</b><br>
            • Average Conversion Rate: <b>{avg_conv_rate:.1f}%</b><br>
            • Top Converter: <b>{top_converter}</b> with <b>{int(top_conversions)}</b> conversions<br>
            • Team Members with Conversions: <b>{len(display_df[display_df['Converted'] > 0])}</b> out of <b>{len(display_df)}</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="warning-box">
            <b>⚠️ No conversions recorded yet.</b> Focus on moving leads through the pipeline!
            </div>
            """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)

def create_advanced_funnel(df):
    """Multi-dimensional conversion funnel"""
    st.subheader("🔄 Advanced Conversion Funnel Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Define comprehensive funnel
        funnel_stages = {
            'All Leads': len(df),
            'New': len(df[df['Status'] == 'New']),
            'Attempted Contact': len(df[df['Status'] == 'Attempted to Contact']),
            'Contacted': len(df[df['Status'] == 'Contacted']),
            'Pre-Qualified': len(df[df['Status'] == 'Pre-Qualified']),
            'Converted': len(df[df['Status'] == 'Converted'])
        }
        
        # Remove empty stages
        funnel_stages = {k: v for k, v in funnel_stages.items() if v > 0}
        
        if len(funnel_stages) >= 2:
            stages = list(funnel_stages.keys())
            values = list(funnel_stages.values())
            
            fig = go.Figure()
            
            fig.add_trace(go.Funnel(
                y=stages,
                x=values,
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(
                    color=['#8b5cf6', '#6366f1', '#3b82f6', '#06b6d4', '#10b981', '#059669'],
                    line=dict(width=3, color='white')
                ),
                connector=dict(
                    line=dict(color='#64748b', width=4, dash='dot')
                ),
                hovertemplate='<b>%{y}</b><br>Leads: %{x}<br>%{percentInitial}<extra></extra>'
            ))
            
            fig.update_layout(
                title='Complete Lead Conversion Funnel',
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 📉 Drop-off Analysis")
        
        if len(funnel_stages) >= 2:
            stages_list = list(funnel_stages.keys())
            values_list = list(funnel_stages.values())
            
            for i in range(len(stages_list) - 1):
                drop_off = values_list[i] - values_list[i+1]
                drop_off_pct = (drop_off / values_list[i] * 100) if values_list[i] > 0 else 0
                retention = 100 - drop_off_pct
                
                st.metric(
                    f"{stages_list[i]} → {stages_list[i+1]}",
                    f"{drop_off} lost",
                    f"-{drop_off_pct:.1f}%",
                    delta_color="inverse"
                )
                st.progress(retention / 100)
                st.caption(f"Retention: {retention:.1f}%")
                st.markdown("---")
    
    # Status breakdown over time
    st.markdown("### 📈 Status Evolution Timeline")
    
    status_timeline = df.groupby(['Month', 'Status']).size().reset_index(name='Count')
    status_timeline = status_timeline.merge(
        df[['Month', 'Month_Date']].drop_duplicates(),
        on='Month'
    ).sort_values('Month_Date')
    
    fig = px.area(
        status_timeline,
        x='Month',
        y='Count',
        color='Status',
        title='Lead Status Distribution Over Time',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_layout(
        height=400,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)

def create_source_intelligence(df):
    """Advanced lead source intelligence"""
    st.subheader("📞 Lead Source Intelligence & ROI Analysis")
    
    df_sources = df[df['Source'].str.len() > 0].copy()
    
    if len(df_sources) == 0:
        st.info("No source data available")
        return
    
    source_data = df_sources.groupby('Source').agg({
        'Lead_Name': 'count',
        'Status': lambda x: (x == 'Converted').sum()
    }).reset_index()
    source_data.columns = ['Source', 'Total_Leads', 'Converted']
    source_data['Conversion_Rate'] = (source_data['Converted'] / source_data['Total_Leads'] * 100).round(1)
    source_data['Lost'] = df_sources.groupby('Source')['Status'].apply(lambda x: (x == 'Lost Lead').sum()).values
    source_data['Loss_Rate'] = (source_data['Lost'] / source_data['Total_Leads'] * 100).round(1)
    source_data = source_data.sort_values('Total_Leads', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Top sources with conversion
        top_sources = source_data.head(15).sort_values('Total_Leads', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_sources['Source'],
            x=top_sources['Total_Leads'],
            orientation='h',
            name='Total Leads',
            marker=dict(
                color=top_sources['Conversion_Rate'],
                colorscale='RdYlGn',
                showscale=True,
                colorbar=dict(title="Conv %"),
                line=dict(color='white', width=1)
            ),
            text=top_sources['Total_Leads'].astype(int),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Leads: %{x}<br>Conv: %{marker.color:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Top 15 Lead Sources (Color = Conversion Rate)',
            xaxis_title="Number of Leads",
            height=600,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🏆 Source Performance")
        
        # Best sources
        best_by_volume = source_data.nlargest(5, 'Total_Leads')
        best_by_conversion = source_data[source_data['Total_Leads'] >= 5].nlargest(5, 'Conversion_Rate')
        
        st.markdown("**📊 Highest Volume:**")
        for idx, row in best_by_volume.iterrows():
            st.metric(
                row['Source'][:30],
                f"{row['Total_Leads']} leads",
                f"{row['Conversion_Rate']:.1f}% conv"
            )
        
        st.markdown("---")
        st.markdown("**🎯 Best Conversion:**")
        for idx, row in best_by_conversion.iterrows():
            st.metric(
                row['Source'][:30],
                f"{row['Conversion_Rate']:.1f}%",
                f"{row['Total_Leads']} leads"
            )
    
    # Source comparison matrix
    st.markdown("### 📊 Source Performance Matrix")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Volume vs conversion scatter
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=source_data['Total_Leads'],
            y=source_data['Conversion_Rate'],
            mode='markers',
            marker=dict(
                size=source_data['Total_Leads'],
                color=source_data['Conversion_Rate'],
                colorscale='Viridis',
                showscale=True,
                sizemode='area',
                sizeref=2.*max(source_data['Total_Leads'])/(40.**2),
                line=dict(width=1, color='white')
            ),
            text=source_data['Source'],
            hovertemplate='<b>%{text}</b><br>Leads: %{x}<br>Conv: %{y:.1f}%<extra></extra>'
        ))
        
        fig.update_layout(
            title='Volume vs Quality',
            xaxis_title="Total Leads",
            yaxis_title="Conversion Rate (%)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top sources pie
        top_5 = source_data.head(5)
        others = pd.DataFrame({
            'Source': ['Others'],
            'Total_Leads': [source_data.iloc[5:]['Total_Leads'].sum()]
        })
        pie_data = pd.concat([top_5[['Source', 'Total_Leads']], others])
        
        fig = go.Figure()
        
        fig.add_trace(go.Pie(
            labels=pie_data['Source'],
            values=pie_data['Total_Leads'],
            hole=0.4,
            marker=dict(
                colors=px.colors.qualitative.Set2,
                line=dict(color='white', width=2)
            ),
            textposition='auto',
            textinfo='label+percent'
        ))
        
        fig.update_layout(
            title='Source Distribution',
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Loss rate comparison
        top_loss = source_data.nlargest(8, 'Total_Leads')
        
        fig = go.Figure()
        
        colors = ['#ef4444' if x > 20 else '#f59e0b' if x > 10 else '#10b981' 
                 for x in top_loss['Loss_Rate']]
        
        fig.add_trace(go.Bar(
            y=top_loss['Source'],
            x=top_loss['Loss_Rate'],
            orientation='h',
            marker_color=colors,
            text=[f"{x:.1f}%" for x in top_loss['Loss_Rate']],
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Loss Rate by Source',
            xaxis_title="Loss Rate (%)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_company_analysis(df):
    """Deep company intelligence"""
    st.subheader("🏢 Company Intelligence & Account Analysis")
    
    df_companies = df[df['Company'].str.len() > 0].copy()
    
    if len(df_companies) == 0:
        st.info("No company data available")
        return
    
    company_data = df_companies.groupby('Company').agg({
        'Lead_Name': 'count',
        'Status': lambda x: list(x.unique()),
        'Sales_Person': lambda x: list(x.unique()),
        'Month_Date': ['min', 'max']
    }).reset_index()
    
    company_data.columns = ['Company', 'Total_Leads', 'Statuses', 'Sales_Team', 'First_Contact', 'Last_Contact']
    company_data['Days_Active'] = (company_data['Last_Contact'] - company_data['First_Contact']).dt.days
    company_data['Status_Count'] = company_data['Statuses'].apply(len)
    company_data['Team_Size'] = company_data['Sales_Team'].apply(len)
    company_data = company_data.sort_values('Total_Leads', ascending=False)
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        # Top companies
        top_20 = company_data.head(20).sort_values('Total_Leads', ascending=True)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=top_20['Company'],
            x=top_20['Total_Leads'],
            orientation='h',
            marker=dict(
                color=top_20['Days_Active'],
                colorscale='Plasma',
                showscale=True,
                colorbar=dict(title="Days Active"),
                line=dict(color='white', width=1)
            ),
            text=top_20['Total_Leads'].astype(int),
            textposition='outside',
            hovertemplate='<b>%{y}</b><br>Leads: %{x}<br>Active: %{marker.color} days<extra></extra>'
        ))
        
        fig.update_layout(
            title='Top 20 Companies by Lead Volume',
            xaxis_title="Number of Leads",
            height=700,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Key Accounts")
        
        top_accounts = company_data.head(8)
        
        for idx, row in top_accounts.iterrows():
            with st.container():
                st.markdown(f"**{row['Company'][:40]}**")
                
                col_a, col_b, col_c = st.columns(3)
                with col_a:
                    st.metric("Leads", row['Total_Leads'])
                with col_b:
                    st.metric("Team", row['Team_Size'])
                with col_c:
                    st.metric("Days", row['Days_Active'])
                
                st.markdown("---")
    
    # Additional analytics
    st.markdown("### 📊 Company Engagement Analytics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Engagement duration
        fig = go.Figure()
        
        max_days = company_data['Days_Active'].max()
        
        # Create dynamic bins based on max days
        if max_days <= 30:
            bins = [0, 10, 20, 30, max_days + 1]
            labels = ['0-10', '11-20', '21-30', '30+']
        elif max_days <= 90:
            bins = [0, 30, 60, 90, max_days + 1]
            labels = ['0-30', '31-60', '61-90', '90+']
        elif max_days <= 180:
            bins = [0, 30, 60, 90, 180, max_days + 1]
            labels = ['0-30', '31-60', '61-90', '91-180', '180+']
        elif max_days <= 365:
            bins = [0, 30, 60, 90, 180, 365, max_days + 1]
            labels = ['0-30', '31-60', '61-90', '91-180', '181-365', '365+']
        else:
            bins = [0, 30, 60, 90, 180, 365, max_days + 1]
            labels = ['0-30', '31-60', '61-90', '91-180', '181-365', '365+']
        
        # Remove duplicate bins
        bins = sorted(list(set(bins)))
        # Adjust labels to match bins
        if len(bins) != len(labels) + 1:
            # Create simple labels based on actual bins
            labels = [f"{int(bins[i])}-{int(bins[i+1]-1)}" for i in range(len(bins)-1)]
        
        company_data['Duration_Bin'] = pd.cut(company_data['Days_Active'], bins=bins, labels=labels[:len(bins)-1], include_lowest=True)
        duration_counts = company_data['Duration_Bin'].value_counts().sort_index()
        
        fig.add_trace(go.Bar(
            x=duration_counts.index.astype(str),
            y=duration_counts.values,
            marker=dict(
                color=duration_counts.values,
                colorscale='Greens',
                showscale=False
            ),
            text=duration_counts.values,
            textposition='outside'
        ))
        
        fig.update_layout(
            title='Engagement Duration (Days)',
            xaxis_title="Duration Range",
            yaxis_title="Companies",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Team coverage
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=company_data['Team_Size'],
            nbinsx=10,
            marker=dict(
                color='#3b82f6',
                line=dict(color='white', width=1)
            )
        ))
        
        fig.update_layout(
            title='Sales Team Coverage',
            xaxis_title="Team Members per Company",
            yaxis_title="Number of Companies",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        # Lead concentration
        fig = go.Figure()
        
        fig.add_trace(go.Histogram(
            x=company_data['Total_Leads'],
            nbinsx=15,
            marker=dict(
                color='#8b5cf6',
                line=dict(color='white', width=1)
            )
        ))
        
        fig.update_layout(
            title='Lead Concentration',
            xaxis_title="Leads per Company",
            yaxis_title="Frequency",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)

def create_heatmap_analysis(df):
    """Advanced heatmap analysis"""
    st.subheader("🔥 Lead Activity Heatmap & Patterns")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Status x Month heatmap
        heatmap_data = df.groupby(['Month', 'Status']).size().reset_index(name='Count')
        
        if not heatmap_data.empty:
            heatmap_pivot = heatmap_data.pivot(index='Status', columns='Month', values='Count').fillna(0)
            
            if 'Month_Date' in df.columns:
                month_order = df.groupby('Month')['Month_Date'].first().sort_values().index
                month_order = [m for m in month_order if m in heatmap_pivot.columns]
                if month_order:
                    heatmap_pivot = heatmap_pivot[month_order]
            
            fig = go.Figure(data=go.Heatmap(
                z=heatmap_pivot.values,
                x=heatmap_pivot.columns,
                y=heatmap_pivot.index,
                colorscale='YlOrRd',
                text=heatmap_pivot.values.astype(int),
                texttemplate='%{text}',
                textfont={"size": 11, "color": "white"},
                hovertemplate='<b>%{y}</b><br>%{x}<br>Leads: %{z}<extra></extra>',
                colorbar=dict(title="Leads")
            ))
            
            fig.update_layout(
                title='Status × Month Heatmap',
                height=450,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for Status × Month heatmap")
    
    with col2:
        # Salesperson x Status heatmap
        sp_status = df.groupby(['Sales_Person', 'Status']).size().reset_index(name='Count')
        
        if not sp_status.empty:
            top_sp = df.groupby('Sales_Person').size().nlargest(10).index
            sp_status_filtered = sp_status[sp_status['Sales_Person'].isin(top_sp)]
            
            if len(sp_status_filtered) > 0:
                sp_pivot = sp_status_filtered.pivot(index='Sales_Person', columns='Status', values='Count').fillna(0)
                
                fig = go.Figure(data=go.Heatmap(
                    z=sp_pivot.values,
                    x=sp_pivot.columns,
                    y=sp_pivot.index,
                    colorscale='Blues',
                    text=sp_pivot.values.astype(int),
                    texttemplate='%{text}',
                    textfont={"size": 10, "color": "white"},
                    hovertemplate='<b>%{y}</b><br>%{x}<br>Count: %{z}<extra></extra>',
                    colorbar=dict(title="Count")
                ))
                
                fig.update_layout(
                    title='Top 10 Salespeople × Status',
                    height=450,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Not enough data for Salesperson × Status heatmap")
        else:
            st.info("No data available for Salesperson × Status heatmap")
    
    # Insights
    if not heatmap_data.empty and 'heatmap_pivot' in locals() and len(heatmap_pivot) > 0:
        max_cell = heatmap_pivot.max().max()
        if max_cell > 0:
            max_location = heatmap_pivot.stack().idxmax()
            
            st.markdown(f"""
            <div class="insight-box">
            <b>🔥 Heatmap Insights:</b><br>
            • Highest activity: <b>{max_location[0]}</b> status in <b>{max_location[1]}</b> with <b>{int(max_cell)}</b> leads<br>
            • Total status categories tracked: <b>{len(heatmap_pivot)}</b><br>
            • Months analyzed: <b>{len(heatmap_pivot.columns)}</b>
            </div>
            """, unsafe_allow_html=True)

def create_forecast_analysis(df):
    """Time series forecasting"""
    st.subheader("🔮 Predictive Analytics & Forecasting")
    
    monthly_data = df.groupby('Month_Date').size().reset_index(name='Leads')
    monthly_data = monthly_data.sort_values('Month_Date')
    
    if len(monthly_data) < 3:
        st.warning("Need at least 3 months of data for forecasting")
        return
    
    X = np.arange(len(monthly_data))
    y = monthly_data['Leads'].values
    
    n = len(X)
    x_mean = X.mean()
    y_mean = y.mean()
    
    numerator = np.sum((X - x_mean) * (y - y_mean))
    denominator = np.sum((X - x_mean) ** 2)
    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean
    
    trend_line = slope * X + intercept
    
    # Forecast next 6 months
    future_X = np.arange(len(monthly_data), len(monthly_data) + 6)
    forecast = slope * future_X + intercept
    forecast = np.maximum(forecast, 0)
    
    # Calculate confidence intervals (simple method)
    residuals = y - trend_line
    std_error = np.std(residuals)
    forecast_upper = forecast + 1.96 * std_error
    forecast_lower = np.maximum(forecast - 1.96 * std_error, 0)
    
    last_date = monthly_data['Month_Date'].max()
    future_dates = pd.date_range(start=last_date + pd.DateOffset(months=1), periods=6, freq='MS')
    
    fig = go.Figure()
    
    # Historical data
    fig.add_trace(go.Scatter(
        x=monthly_data['Month_Date'],
        y=monthly_data['Leads'],
        mode='lines+markers',
        name='Actual',
        line=dict(color='#3b82f6', width=3),
        marker=dict(size=10, symbol='circle')
    ))
    
    # Trend line
    fig.add_trace(go.Scatter(
        x=monthly_data['Month_Date'],
        y=trend_line,
        mode='lines',
        name='Trend',
        line=dict(color='#ef4444', width=2, dash='dash')
    ))
    
    # Forecast
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=forecast,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='#10b981', width=3, dash='dot'),
        marker=dict(size=10, symbol='diamond')
    ))
    
    # Confidence interval
    fig.add_trace(go.Scatter(
        x=list(future_dates) + list(future_dates[::-1]),
        y=list(forecast_upper) + list(forecast_lower[::-1]),
        fill='toself',
        fillcolor='rgba(16, 185, 129, 0.2)',
        line=dict(color='rgba(255,255,255,0)'),
        name='95% Confidence',
        showlegend=True
    ))
    
    fig.update_layout(
        title='6-Month Lead Generation Forecast',
        xaxis_title="Date",
        yaxis_title="Number of Leads",
        height=500,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Forecast summary
    col1, col2, col3 = st.columns(3)
    
    trend_direction = "📈 Growing" if slope > 0 else "📉 Declining" if slope < 0 else "➡️ Stable"
    trend_color = "#10b981" if slope > 0 else "#ef4444" if slope < 0 else "#f59e0b"
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
        <b>🔮 Next Month Prediction:</b><br>
        Expected leads: <b>{forecast[0]:.0f}</b><br>
        Range: <b>{forecast_lower[0]:.0f} - {forecast_upper[0]:.0f}</b><br>
        Confidence: <b>95%</b>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="success-box">
        <b>📊 6-Month Outlook:</b><br>
        Average: <b>{forecast.mean():.0f}</b> leads/month<br>
        Total expected: <b>{forecast.sum():.0f}</b> leads<br>
        Trend: <b style="color: {trend_color}">{trend_direction}</b>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="warning-box">
        <b>⚡ Growth Rate:</b><br>
        Monthly change: <b>{abs(slope):.2f}</b> leads<br>
        Rate: <b>{(slope/y_mean*100):+.2f}%</b> per month<br>
        Trajectory: <b>{trend_direction}</b>
        </div>
        """, unsafe_allow_html=True)

def create_advanced_filters(df):
    """Enhanced filtering system"""
    st.sidebar.header("🎛️ Advanced Filters")
    
    # Date range
    st.sidebar.subheader("📅 Date Range")
    min_date = df['Month_Date'].min()
    max_date = df['Month_Date'].max()
    
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    # Status filter
    st.sidebar.subheader("🔍 Filter Criteria")
    all_statuses = ['All'] + sorted(df['Status'].unique().tolist())
    selected_statuses = st.sidebar.multiselect(
        "Status",
        all_statuses,
        default=['All']
    )
    
    # Salesperson filter
    all_sales = ['All'] + sorted(df['Sales_Person'].unique().tolist())
    selected_sales = st.sidebar.multiselect(
        "Salesperson",
        all_sales,
        default=['All']
    )
    
    # Source filter
    all_sources = ['All'] + sorted([s for s in df['Source'].unique() if s])
    selected_sources = st.sidebar.multiselect(
        "Source",
        all_sources,
        default=['All']
    )
    
    # Apply filters
    df_filtered = df.copy()
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        df_filtered = df_filtered[
            (df_filtered['Month_Date'] >= pd.Timestamp(start_date)) &
            (df_filtered['Month_Date'] <= pd.Timestamp(end_date))
        ]
    
    if 'All' not in selected_statuses and selected_statuses:
        df_filtered = df_filtered[df_filtered['Status'].isin(selected_statuses)]
    
    if 'All' not in selected_sales and selected_sales:
        df_filtered = df_filtered[df_filtered['Sales_Person'].isin(selected_sales)]
    
    if 'All' not in selected_sources and selected_sources:
        df_filtered = df_filtered[df_filtered['Source'].isin(selected_sources)]
    
    if len(df_filtered) < len(df):
        st.sidebar.success(f"✅ Showing {len(df_filtered)} of {len(df)} leads")
    
    return df_filtered

def create_detailed_data_explorer(df):
    """Advanced data explorer"""
    st.subheader("📋 Detailed Lead Records Explorer")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_term = st.text_input("🔍 Search leads (name, company, source):", "")
    
    with col2:
        sort_by = st.selectbox("Sort by:", ['Month', 'Lead_Name', 'Company', 'Status', 'Sales_Person'])
    
    display_df = df.copy()
    
    if search_term:
        mask = (
            display_df['Lead_Name'].str.contains(search_term, case=False, na=False) |
            display_df['Company'].str.contains(search_term, case=False, na=False) |
            display_df['Source'].str.contains(search_term, case=False, na=False)
        )
        display_df = display_df[mask]
    
    display_cols = ['Month', 'Lead_Name', 'Company', 'Status', 'Sales_Person', 'Source']
    display_df = display_df[display_cols].sort_values(sort_by, ascending=False)
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=500
    )
    
    st.caption(f"📊 Showing {len(display_df)} of {len(df)} records")

def export_reports(df, metrics):
    """Enhanced export functionality"""
    st.subheader("📥 Export Reports & Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        csv = df.to_csv(index=False)
        st.download_button(
            label="📊 Full Dataset",
            data=csv,
            file_name=f"leads_complete_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col2:
        summary_data = pd.DataFrame({
            'Metric': list(metrics.keys()),
            'Value': list(metrics.values())
        })
        csv_summary = summary_data.to_csv(index=False)
        st.download_button(
            label="📋 Summary Report",
            data=csv_summary,
            file_name=f"summary_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col3:
        team_data = df.groupby('Sales_Person').agg({
            'Lead_Name': 'count',
            'Status': lambda x: (x == 'Converted').sum()
        }).reset_index()
        team_data.columns = ['Sales_Person', 'Total_Leads', 'Converted']
        team_data['Conversion_Rate'] = (team_data['Converted'] / team_data['Total_Leads'] * 100).round(2)
        csv_team = team_data.to_csv(index=False)
        st.download_button(
            label="👥 Team Report",
            data=csv_team,
            file_name=f"team_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )
    
    with col4:
        # Source analysis export
        source_data = df[df['Source'].str.len() > 0].groupby('Source').agg({
            'Lead_Name': 'count',
            'Status': lambda x: (x == 'Converted').sum()
        }).reset_index()
        source_data.columns = ['Source', 'Total_Leads', 'Converted']
        source_data['Conversion_Rate'] = (source_data['Converted'] / source_data['Total_Leads'] * 100).round(2)
        csv_source = source_data.to_csv(index=False)
        st.download_button(
            label="📞 Source Analysis",
            data=csv_source,
            file_name=f"sources_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv"
        )

def create_executive_summary(df, metrics):
    """Executive summary dashboard"""
    st.subheader("📊 Executive Summary")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"""
        <div class="insight-box">
        <h3>📈 Performance Overview (Corrected)</h3>
        <b>Total Records Loaded:</b> {metrics['total_leads']:,}<br>
        <b>Conversion Rate:</b> {metrics['conversion_rate']:.1f}% (Only 'Converted' status)<br>
        <b>Pre-Qualified:</b> {metrics['pre_qualified']} leads (Not counted as converted)<br>
        <b>Contact Rate:</b> {metrics['contact_rate']:.1f}%<br>
        <b>Loss Rate:</b> {metrics['loss_rate']:.1f}%<br>
        <b>Monthly Growth:</b> {metrics['month_growth']:+.1f}%<br>
        <b>Active Team Members:</b> {metrics['active_salespeople']}
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Top performers - separate volume and conversion leaders
        salesperson_counts = df.groupby('Sales_Person').size()
        if len(salesperson_counts) > 0:
            top_volume = salesperson_counts.idxmax()
            top_volume_count = salesperson_counts.max()
        else:
            top_volume = "N/A"
            top_volume_count = 0
        
        # Find top converter
        converted_by_person = df[df['Status'] == 'Converted'].groupby('Sales_Person').size()
        if len(converted_by_person) > 0:
            top_converter = converted_by_person.idxmax()
            top_conversions = converted_by_person.max()
        else:
            top_converter = "N/A"
            top_conversions = 0
        
        month_counts = df.groupby('Month').size()
        if len(month_counts) > 0:
            best_month = month_counts.idxmax()
            best_month_count = month_counts.max()
        else:
            best_month = "N/A"
            best_month_count = 0
        
        st.markdown(f"""
        <div class="success-box">
        <h3>🏆 Top Achievements</h3>
        <b>Volume Leader:</b> {top_volume} ({top_volume_count} leads)<br>
        <b>Top Converter:</b> {top_converter} ({top_conversions} conversions)<br>
        <b>Best Month:</b> {best_month} ({best_month_count} leads)<br>
        <b>Converted Leads:</b> {metrics['converted_leads']} (Closed deals only)<br>
        <b>Pre-Qualified:</b> {metrics['pre_qualified']} (Pipeline)<br>
        <b>Active Leads:</b> {metrics['active_leads']}<br>
        <b>Lost Leads:</b> {metrics['lost_leads']} ({metrics['loss_rate']:.1f}%)
        </div>
        """, unsafe_allow_html=True)

# Main Application
uploaded_file = st.file_uploader(
    "📁 Upload Lead Data (CSV or Excel)",
    type=['csv', 'xlsx', 'xls'],
    help="Upload your CRM export file"
)

if uploaded_file is not None:
    with st.spinner("🔄 Processing data..."):
        df = load_data(uploaded_file)
    
    if df is not None and len(df) > 0:
        # st.success(f"✅ Loaded {len(df)} leads successfully!") # Moved inside load_data
        
        # Apply filters
        df_filtered = create_advanced_filters(df)
        
        # Calculate metrics
        metrics = calculate_metrics(df_filtered)
        
        # Display KPIs
        display_kpi_dashboard(metrics)
        
        st.markdown("---")
        
        # Executive summary
        create_executive_summary(df_filtered, metrics)
        
        st.markdown("---")
        
        # Tab layout
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Overview",
            "👥 Team Analytics",
            "🎯 Conversion & Funnel",
            "📞 Source Intelligence",
            "🏢 Company Analysis",
            "📋 Data Explorer"
        ])
        
        with tab1:
            st.header("Overview Analytics")
            create_monthly_trends_advanced(df_filtered)
            st.markdown("---")
            create_heatmap_analysis(df_filtered)
            st.markdown("---")
            create_forecast_analysis(df_filtered)
        
        with tab2:
            st.header("Team Performance & Productivity")
            create_team_performance_comprehensive(df_filtered)
        
        with tab3:
            st.header("Conversion Analysis")
            create_advanced_funnel(df_filtered)
        
        with tab4:
            st.header("Lead Source Intelligence")
            create_source_intelligence(df_filtered)
        
        with tab5:
            st.header("Company & Account Analysis")
            create_company_analysis(df_filtered)
        
        with tab6:
            st.header("Data Explorer & Export")
            create_detailed_data_explorer(df_filtered)
            st.markdown("---")
            export_reports(df_filtered, metrics)
    else:
        st.error("❌ Could not load data. Please check the file format and column names.")

else:
    # Welcome screen
    st.markdown("""
    ## 👋 Welcome to Enterprise Lead Analytics Dashboard
    
    ### 🚀 Professional Features:
    
    #### 📊 **Executive Dashboard**
    - Real-time KPIs with advanced metrics
    - Month-over-month growth tracking
    - Team performance benchmarking
    - Loss rate monitoring
    
    #### 📈 **Advanced Analytics**
    - **Monthly Trends**: Lead volume, moving averages, growth rates, and cumulative tracking
    - **Team Performance**: Multi-dimensional performance matrix with conversion analysis
    - **Conversion Funnel**: Complete pipeline with drop-off tracking and retention metrics
    - **Source Intelligence**: ROI analysis, volume vs. quality metrics, loss rate by source
    - **Company Analysis**: Target account identification, engagement duration, team coverage
    - **Predictive Forecasting**: 6-month forecast with confidence intervals
    - **Activity Heatmaps**: Pattern recognition across time, status, and salespeople
    
    #### 🎨 **Professional Design**
    - ✨ Modern UI with gradient effects
    - 🌓 Automatic light/dark mode support
    - 📱 Responsive design for all devices
    - 🎯 Color-coded insights and alerts
    - 💫 Smooth animations and transitions
    
    #### 🎛️ **Power User Features**
    - Multi-dimensional filtering
    - Date range selection
    - Real-time search functionality
    - Advanced data explorer
    - Comprehensive export options (Full data, Summary, Team, Source reports)
    - Interactive drill-down visualizations
    
    #### 💼 **Business Intelligence**
    - Identify high-value target accounts
    - Track sales team productivity
    - Optimize lead source allocation
    - Predict future lead generation
    - Monitor conversion bottlenecks
    - Performance tier classification
    
    ### 📁 Supported Formats:
    - ✅ CSV (.csv)
    - ✅ Excel (.xlsx, .xls)
    - ✅ Hierarchical CRM exports (auto-detected)
    
    ### 🎯 Get Started:
    Upload your lead export file above to unlock powerful analytics!
    
    ---
    
    <div style='text-align: center; color: #64748b; padding: 20px;'>
    <p><b>Enterprise Lead Analytics v4.0 Professional Edition</b></p>
    <p>Built with Streamlit • Plotly • Advanced Data Science</p>
    <p>🎨 Optimized for Light & Dark Mode | 📊 Production-Ready Analytics</p>
    </div>
    """, unsafe_allow_html=True)