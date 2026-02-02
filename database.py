import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import handle_login, add_to_queue
from utils import create_pdf_report

# --- CONFIG & SESSION ---
st.set_page_config(page_title="Bioinformatics Platform", layout="wide")
if 'user' not in st.session_state: st.session_state.user = None
if 'step' not in st.session_state: st.session_state.step = "Home"

# --- AUTH SECTION (Step 1-4) ---
if not st.session_state.user:
    st.title("🧬 Bioinformatics Analysis Platform")
    auth_mode = st.radio("Select Mode", ["Login", "Register"])
    
    email = st.text_input("Email")
    pw = st.text_input("Password", type="password")
    if auth_mode == "Register":
        fn = st.text_input("First Name")
        ln = st.text_input("Last Name")
        cpw = st.text_input("Confirm Password", type="password")
    
    if st.button("Submit"):
        st.session_state.user = handle_login(email, pw)
        st.rerun()
    st.stop()

# --- HEADER (Step 3) ---
col_h1, col_h2 = st.columns([4, 1])
with col_h2:
    with st.expander(f"👤 {st.session_state.user['email']}"):
        if st.button("แก้ไขบัญชี"): st.info("เข้าสู่หน้าแก้ไข...")
        if st.button("ออกจากระบบ"): 
            st.session_state.user = None
            st.rerun()

# --- SIDEBAR & NAVIGATION ---
menu = st.sidebar.radio("Navigation", ["Home", "My Project", "About Us"])

# --- MAIN LOGIC ---
if menu == "Home":
    st.title("🚀 Analysis Dashboard")
    if st.button("➕ New Analysis"):
        st.session_state.analysis_active = True

    if st.session_state.get('analysis_active'):
        # Step 5: Choose Mode
        mode = st.radio("Choose Mode", ["Single File", "Multiple Files"])
        limit = 1 if mode == "Single File" else 3
        files = st.file_uploader(f"Upload {mode}", accept_multiple_files=(limit > 1))

        if files:
            all_dfs = [pd.read_csv(f) for f in (files if isinstance(files, list) else [files])]
            for i, d in enumerate(all_dfs): 
                st.write(f"Preview File {i+1}"); st.dataframe(d.head(3))

            # Step 6: Merge
            if mode == "Multiple Files":
                if st.button("Merge Data"):
                    merged = all_dfs[0]
                    for d in all_dfs[1:]: merged = pd.merge(merged, d, how='inner')
                    st.session_state.final_df = merged
                    st.success("Merge Complete!")

            # Step 7: Preprocessing
            if st.session_state.get('final_df') is not None or mode == "Single File":
                st.divider()
                st.header("⚙️ Preprocessing")
                col_l, col_r = st.columns([3, 1])
                with col_l: st.dataframe(all_dfs[0].head(10)) # โชว์ตัวอย่างข้อมูล
                with col_r:
                    miss = st.selectbox("Missing Data", ["dropna", "Mean", "Min"])
                    norm = st.selectbox("Normalization", ["Z-score", "Quantile", "MinMax"])
                    if st.button("Apply Preprocessing"):
                        st.session_state.ready_to_run = True

            # Step 8: Analysis
            if st.session_state.get('ready_to_run'):
                st.divider()
                st.header("🔬 Analysis Selection")
                run_mode = st.radio("Run Mode", ["Auto Mode", "Manual Mode"])
                models = ["Random Forest", "SVM", "XGBoost", "Neural Network"]
                selected = models if run_mode == "Auto Mode" else [m for m in models if st.checkbox(m)]
                
                if st.button("🚀 Start Running"):
                    # Step 9: Queue & Notification
                    add_to_queue(st.session_state.user['id'], "My_Project_01", "path/to/data", {"models": selected})
                    st.success("ส่งงานเข้าคิวสำเร็จ! ระบบจะแจ้ง Email เมื่อรันเสร็จ")
                    st.balloons()

elif menu == "My Project":
    st.title("📁 My Projects")
    # ตัวอย่างสถานะ (ในระบบจริงดึงจาก Supabase)
    projects = [
        {"Project": "Analysis_A", "Status": "complete", "Action": "View Result"},
        {"Project": "Analysis_B", "Status": "running", "Action": "-"},
        {"Project": "Analysis_C", "Status": "in the queue", "Action": "-"}
    ]
    for p in projects:
        c1, c2, c3 = st.columns(3)
        c1.write(p["Project"])
        c2.info(p["Status"]) if p["Status"] == "running" else c2.success(p["Status"]) if p["Status"] == "complete" else c2.warning(p["Status"])
        if p["Status"] == "complete":
            if c3.button("Download PDF", key=p["Project"]):
                report = create_pdf_report(p["Project"], "Confusion Matrix: ...")
                st.download_button("Click to Download", report, f"{p['Project']}.pdf")

elif menu == "About Us":
    st.title("ℹ️ About Us")
    st.write("แพลตฟอร์มนี้พัฒนาขึ้นเพื่อวิเคราะห์ข้อมูล Multi-omics...")
