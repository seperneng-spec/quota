# -*- coding: utf-8 -*-
import json
from datetime import datetime
from pathlib import Path

class CopilotQuota:
    def __init__(self, limit_percent=100, reset_at_percent=90, data_file="copilot_usage.json"):
        self.LIMIT = limit_percent
        self.RESET_AT = reset_at_percent
        self.data_path = Path(data_file)
        self._load_data()
        self._print_status()
    
    def _load_data(self):
        if self.data_path.exists():
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.usage_percent = data.get("usage_percent", 0)
                    self.cycle = data.get("current_cycle", 1)
                    self.total_resets = data.get("total_resets", 0)
            except Exception:
                self._reset_variables()
        else:
            self._reset_variables()
            self._save_data()
            
    def _reset_variables(self):
        self.usage_percent = 0
        self.cycle = 1
        self.total_resets = 0
    
    def _save_data(self):
        data = {
            "usage_percent": self.usage_percent,
            "current_cycle": self.cycle,
            "total_resets": self.total_resets,
            "last_updated": datetime.now().isoformat()
        }
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _print_status(self):
        print("=" * 55)
        print("🤖 ระบบควบคุมการใช้งาน — พร้อมทำงาน")
        print(f"📊 ขีดจำกัด: {self.LIMIT}%")
        print(f"🔁 รีเซ็ตอัตโนมัติเมื่อใช้ถึง: {self.RESET_AT}%")
        print(f"✨ สถานะปัจจุบัน: {self.usage_percent}%")
        print(f"🔄 รอบที่: {self.cycle} | รีเซ็ตแล้ว: {self.total_resets} ครั้ง")
        print("=" * 55 + "\n")
    
    def use(self, percent_used=1):
        self.usage_percent += percent_used
        self._save_data()
        
        if self.usage_percent >= self.RESET_AT:
            return self._auto_reset()
        
        remaining = self.LIMIT - self.usage_percent
        return {
            "status": "active",
            "message": f"✅ ใช้งานปกติ — {self.usage_percent}% เหลือ {remaining}%"
        }
    
    def _auto_reset(self):
        old_percent = self.usage_percent
        self.usage_percent = 0
        self.cycle += 1
        self.total_resets += 1
        self._save_data()
        
        return {
            "status": "reset",
            "message": f"🔁 รีเซ็ตอัตโนมัติ! ใช้ไป {old_percent}% → กลับมา 0% เริ่มรอบใหม่"
        }
    
    def status(self):
        return {
            "usage": f"{self.usage_percent}%",
            "limit": f"{self.LIMIT}%",
            "remaining": f"{self.LIMIT - self.usage_percent}%",
            "cycle": self.cycle,
            "total_resets": self.total_resets
        }

