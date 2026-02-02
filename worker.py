# สคริปต์นี้จะรันวนลูปใน Colab
import time
from database import supabase # เชื่อมตัวเดียวกัน

while True:
    # 1. เช็ค Database ว่ามีงาน 'in the queue' ไหม
    job = supabase.table("projects").select("*").eq("status", "in the queue").limit(1).execute()
    
    if job.data:
        job_id = job.data[0]['id']
        # 2. อัปเดตสถานะเป็น 'running'
        supabase.table("projects").update({"status": "running"}).eq("id", job_id).execute()
        
        # 3. รัน Pipeline (ยกโค้ดจาก Colab ของคุณมาใส่ตรงนี้ทั้งหมด)
        print(f"กำลังประมวลผลงาน ID: {job_id}...")
        time.sleep(10) # จำลองการรัน
        
        # 4. อัปเดตเป็น 'complete' และส่ง Email
        supabase.table("projects").update({"status": "complete"}).eq("id", job_id).execute()
        print("เสร็จสิ้น!")
        
    time.sleep(60) # พัก 1 นาทีแล้วเช็คใหม่
