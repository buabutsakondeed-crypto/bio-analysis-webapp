import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from database import sign_in, sign_up, add_project, get_my_projects

# --- 1. การตั้งค่าหน้าจอและ State ---
st.set_page_config(page_title="Multi-Omics Analysis Platform", layout="wide")

if 'user' not in st.session_state:
    st.session_state.user = None
if 'step' not in st.session_state:
    st.session_state.step = "Home"

# --- 2. ระบบ Login / Register (Step 1-4) ---
def login_page():
    st.title("🔐 เข้าสู่ระบบ")
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        email = st.text_input("Email", key="l_email")
        pw = st.text_input("Password", type="password", key="l_pw")
        if st.button("เข้าสู่ระบบ"):
            # Logic: เช็คกับ Supabase
            st.session_state.user = {"email": email, "id": "user_id_from_supabase"} 
            st.rerun()

    with tab2:
        fn = st.text_input("First Name")
        ln = st.text_input("Last Name")
        reg_email = st.text_input("Email")
        reg_pw = st.text_input("Password", type="password")
        conf_pw = st.text_input("Confirm Password", type="password")
        if st.button("สมัครสมาชิก"):
            if reg_pw == conf_pw:
                st.success("สมัครสมาชิกสำเร็จ! กรุณาไปที่หน้า Login")
            else:
                st.error("รหัสผ่านไม่ตรงกัน")

if not st.session_state.user:
    login_page()
    st.stop()

# --- 3. ส่วนของ Header (Step 3) ---
col_logo, col_user = st.columns([4, 1])
with col_user:
    with st.expander(f"👤 {st.session_state.user['email']}"):
        if st.button("แก้ไขบัญชี"): st.write("ไปหน้าแก้ไข...")
        if st.button("ออกจากระบบ"): 
            st.session_state.user = None
            st.rerun()

# --- 4. Sidebar Menu ---
menu = st.sidebar.radio("Navigation", ["Home", "My Project", "About Us"])

# --- 5. หน้า Home & New Analysis (Step 5-8) ---
if menu == "Home":
    st.title("🚀 วิเคราะห์ข้อมูลใหม่")
    if st.button("➕ New Analysis"):
        st.session_state.analysis_mode = st.radio("เลือกจำนวนไฟล์", ["Single File", "Multiple Files"])
        
    if 'analysis_mode' in st.session_state:
        # Step 5: Upload
        limit = 1 if st.session_state.analysis_mode == "Single File" else 3
        files = st.file_uploader(f"อัปโหลดไฟล์ ({st.session_state.analysis_mode})", accept_multiple_files=(limit>1))
        
        if files:
            all_dfs = [pd.read_csv(f) for f in (files if isinstance(files, list) else [files])]
            for i, df in enumerate(all_dfs):
                st.write(f"Preview ไฟล์ที่ {i+1}")
                st.dataframe(df.head(5))

            # Step 6: Merge
            if st.session_state.analysis_mode == "Multiple Files":
                if st.button("🔗 Merge Data"):
                    # Logic Inner Merge
                    merged = all_dfs[0]
                    for d in all_dfs[1:]: merged = pd.merge(merged, d, how='inner')
                    st.session_state.working_df = merged
                    st.success(f"Merge เสร็จสิ้น! เหลือข้อมูล {merged.shape[0]} แถว")

            # Step 7: Preprocessing
            st.divider()
            st.subheader("⚙️ Preprocessing Settings")
            col_l, col_r = st.columns([3, 1])
            with col_r:
                miss_opt = st.selectbox("Missing Data", ["dropna", "Mean", "Min"])
                norm_opt = st.selectbox("Normalization", ["Z-score", "Quantile", "MinMax"])
                if st.button("Apply"):
                    st.session_state.prepped = True
            
            # Step 8: Analysis Selection
            if st.session_state.get('prepped'):
                st.divider()
                st.subheader("🔬 Machine Learning Analysis")
                run_type = st.radio("โหมดการรัน", ["Auto (All Models)", "Manual (Select)"])
                if run_type == "Manual (Select)":
                    models = st.multiselect("เลือกโมเดล", ["Random Forest", "SVM", "XGBoost", "Neural Network"])
                
                if st.button("🚀 Start Analysis & Queue"):
                    # Step 9: ส่งงานเข้าคิว
                    st.success("ส่งงานเข้าคิวสำเร็จ! ระบบจะแจ้งเมลไปที่ " + st.session_state.user['email'])
                    st.balloons()

# --- 6. หน้า My Project (Step 3) ---
elif menu == "My Project":
    st.title("📁 โครงการของฉัน")
    # ดึงข้อมูลจาก Supabase มาแสดง
    projects = [
        {"Name": "Test_Project", "Status": "Complete", "Date": "2026-02-01"},
        {"Name": "Long_Covid_Study", "Status": "Running", "Date": "2026-02-02"}
    ]
    st.table(projects)

elif menu == "About Us":
    st.title("📖 เกี่ยวกับระบบ")
    st.write("ระบบวิเคราะห์ข้อมูลทางชีวสารสนเทศระดับสูง...")
