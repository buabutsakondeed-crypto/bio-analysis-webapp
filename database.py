import streamlit as st
from supabase import create_client

# เชื่อมต่อ Supabase (ใช้ Secrets ของ Streamlit เพื่อความปลอดภัย)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def sign_up(email, password, first_name, last_name):
    res = supabase.auth.sign_up({"email": email, "password": password})
    return res

def sign_in(email, password):
    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
    return res

def add_project(user_id, project_name, config):
    # เพิ่มงานลงในคิว
    data = {
        "user_id": user_id,
        "project_name": project_name,
        "status": "in the queue",
        "config": config # เก็บค่าว่าเลือกโมเดลไหนบ้าง, preprocessing แบบไหน
    }
    return supabase.table("projects").insert(data).execute()

def get_my_projects(user_id):
    return supabase.table("projects").select("*").eq("user_id", user_id).execute()
