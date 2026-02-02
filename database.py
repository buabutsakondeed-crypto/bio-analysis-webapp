import streamlit as st
from supabase import create_client

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def handle_login(email, password):
    # ในระบบจริงใช้ supabase.auth.sign_in_with_password
    return {"email": email, "id": "12345"} 

def add_to_queue(user_id, project_name, data_path, config):
    job = {
        "user_id": user_id,
        "project_name": project_name,
        "status": "in the queue",
        "data_path": data_path,
        "config": config
    }
    return supabase.table("projects").insert(job).execute()
