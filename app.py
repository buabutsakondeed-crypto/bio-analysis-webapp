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
