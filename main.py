# -*- coding: utf-8 -*-
from copilot_quota import CopilotQuota

# 1. เริ่มต้นสร้างระบบ
quota = CopilotQuota(limit_percent=100, reset_at_percent=90)

print("🚀 เริ่มทำการทดสอบเรียกใช้งาน:")

# 2. จำลองการใช้งานครั้งที่ 1 (บวกเพิ่ม 1%)
result1 = quota.use(1)
print(result1["message"])

# 3. ดูสถานะปัจจุบัน
print("📊 สถานะล่าสุด:", quota.status())
