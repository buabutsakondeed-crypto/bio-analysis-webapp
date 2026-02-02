import streamlit as st
import pandas as pd

# 1. ตั้งค่าเมนูและสถานะ (Session State)
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# 2. ส่วนแถบด้านบน (User Profile & Navigation)
st.sidebar.title("🧬 Bio Analysis")
st.sidebar.write("User: Guest") # ในอนาคตจะเชื่อมระบบ Login

menu = st.sidebar.radio("Menu", ["Home", "My Project", "About Us"])

# 3. หน้า Home
if menu == "Home":
    st.title("ยินดีต้อนรับสู่ระบบวิเคราะห์ข้อมูล")
    
    if st.button("➕ New Analysis"):
        st.session_state.show_options = True

    if st.session_state.get('show_options'):
        st.subheader("กรุณาเลือกรูปแบบไฟล์")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📄 Single File"):
                st.session_state.mode = "single"
                st.write("คุณเลือกแบบไฟล์เดียว (ข้าม Merge)")
        with col2:
            if st.button("📚 Multiple Files"):
                st.session_state.mode = "multiple"
                st.write("คุณเลือกแบบหลายไฟล์ (สูงสุด 3 ไฟล์)")

# 4. หน้า My Project (แสดงสถานะตามที่คุณต้องการ)
elif menu == "My Project":
    st.title("📁 โครงการของฉัน")
    # ตัวอย่างตารางสถานะ
    df_status = pd.DataFrame({
        "Project Name": ["Project_A", "Project_B"],
        "Status": ["Running 🏃", "In the queue ⏳"]
    })
    st.table(df_status)

elif menu == "About Us":
    st.title("ℹ️ วิธีการใช้งาน")
    st.write("คำอธิบายขั้นตอนการทำงานของระบบ...")


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# --- ส่วนต่อจากโค้ดเดิมที่เลือก Mode ---

if 'mode' in st.session_state:
    st.divider()
    st.subheader(f"Step: Upload Data ({st.session_state.mode})")
    
    # กำหนดจำนวนไฟล์ตามโหมดที่เลือก
    limit = 1 if st.session_state.mode == "single" else 3
    uploaded_files = st.file_uploader(f"อัปโหลดไฟล์ (สูงสุด {limit} ไฟล์)", 
                                      accept_multiple_files=(limit > 1), 
                                      type=['csv', 'txt'])

    if uploaded_files:
        all_dfs = []
        # Preview ข้อมูล
        for i, file in enumerate(uploaded_files if isinstance(uploaded_files, list) else [uploaded_files]):
            df = pd.read_csv(file)
            df['Batch'] = i + 1  # ใส่เลข Batch ตามที่ต้องการ
            all_dfs.append(df)
            st.write(f"🔍 Preview: {file.name}")
            st.dataframe(df.head(5))

        # --- กรณี Multiple Files (Step 6) ---
        if st.session_state.mode == "multiple" and len(all_dfs) > 1:
            if st.button("🔗 Merge Data"):
                with st.spinner("กำลังทำการ Inner Merge..."):
                    # Logic: Inner Merge
                    merged_df = all_dfs[0]
                    for next_df in all_dfs[1:]:
                        merged_df = pd.merge(merged_df, next_df, how='inner')
                    
                    st.session_state.final_df = merged_df
                    st.success("Merge สำเร็จ!")
                    st.write(f"ขนาดข้อมูลหลัง Merge: {merged_df.shape}")
                    st.write(f"พบค่า Missing ทั้งหมด: {merged_df.isnull().sum().sum()} จุด")
                    st.button("Next to Preprocessing ➡️")

        # --- หน้า Preprocessing (Step 7) ---
        if st.session_state.get('final_df') is not None or st.session_state.mode == "single":
            if st.session_state.mode == "single": 
                st.session_state.final_df = all_dfs[0]

            st.divider()
            st.header("⚙️ Data Preprocessing")
            
            col_left, col_right = st.columns([3, 1]) # แบ่งกล่องซ้าย (Data) กล่องขวา (Options)
            
            with col_left:
                st.subheader("Data Table")
                st.dataframe(st.session_state.final_df.head(10))
            
            with col_right:
                st.subheader("Options")
                missing_tool = st.selectbox("Missing Data", ["dropna", "Fill Mean", "Fill Min"])
                norm_tool = st.selectbox("Normalization", ["Z-score", "Quantile", "MinMax"])
                
                if st.button("Apply Preprocessing"):
                    # ตรงนี้คือจุดที่เอาโค้ดจาก Colab มาใส่ (เช่น df.dropna())
                    st.session_state.processed_ready = True
                    st.success("Preprocessing เสร็จสมบูรณ์!")
                    # แสดงกราฟ (ตัวอย่าง)
                    fig, ax = plt.subplots()
                    sns.histplot(st.session_state.final_df.iloc[:, 1], kde=True)
                    st.pyplot(fig)
                    st.button("Next to Analysis ➡️")
