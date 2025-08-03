import json
import os
from typing import List, Dict, Optional

class TeacherManager:
    """نظام إدارة المعلمين والصلاحيات"""
    
    def __init__(self, teachers_file: str = "teachers.json"):
        self.teachers_file = teachers_file
        self.teachers = self.load_teachers()
    
    def load_teachers(self) -> Dict:
        """تحميل بيانات المعلمين من الملف"""
        if os.path.exists(self.teachers_file):
            try:
                with open(self.teachers_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"خطأ في تحميل ملف المعلمين: {e}")
                return {}
        return {}
    
    def save_teachers(self):
        """حفظ بيانات المعلمين إلى الملف"""
        try:
            with open(self.teachers_file, 'w', encoding='utf-8') as f:
                json.dump(self.teachers, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ ملف المعلمين: {e}")
    
    def add_teacher(self, user_id: int, name: str, role: str = "teacher") -> bool:
        """إضافة معلم جديد"""
        if str(user_id) not in self.teachers:
            self.teachers[str(user_id)] = {
                "name": name,
                "role": role,
                "active": True,
                "upload_count": 0,
                "created_at": self.get_current_timestamp()
            }
            self.save_teachers()
            return True
        return False
    
    def remove_teacher(self, user_id: int) -> bool:
        """إزالة معلم"""
        if str(user_id) in self.teachers:
            del self.teachers[str(user_id)]
            self.save_teachers()
            return True
        return False
    
    def is_authorized(self, user_id: int) -> bool:
        """التحقق من صلاحية المعلم"""
        teacher = self.teachers.get(str(user_id))
        return teacher is not None and teacher.get("active", False)
    
    def get_teacher_info(self, user_id: int) -> Optional[Dict]:
        """الحصول على معلومات المعلم"""
        return self.teachers.get(str(user_id))
    
    def increment_upload_count(self, user_id: int):
        """زيادة عداد رفع الفيديوهات"""
        if str(user_id) in self.teachers:
            self.teachers[str(user_id)]["upload_count"] += 1
            self.save_teachers()
    
    def get_all_teachers(self) -> Dict:
        """الحصول على جميع المعلمين"""
        return self.teachers
    
    def get_active_teachers(self) -> Dict:
        """الحصول على المعلمين النشطين فقط"""
        return {k: v for k, v in self.teachers.items() if v.get("active", False)}
    
    def update_teacher_role(self, user_id: int, new_role: str) -> bool:
        """تحديث دور المعلم"""
        if str(user_id) in self.teachers:
            self.teachers[str(user_id)]["role"] = new_role
            self.save_teachers()
            return True
        return False
    
    def toggle_teacher_status(self, user_id: int) -> bool:
        """تفعيل/إلغاء تفعيل المعلم"""
        if str(user_id) in self.teachers:
            current_status = self.teachers[str(user_id)].get("active", False)
            self.teachers[str(user_id)]["active"] = not current_status
            self.save_teachers()
            return True
        return False
    
    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات المعلمين"""
        total_teachers = len(self.teachers)
        active_teachers = len(self.get_active_teachers())
        total_uploads = sum(teacher.get("upload_count", 0) for teacher in self.teachers.values())
        
        return {
            "total_teachers": total_teachers,
            "active_teachers": active_teachers,
            "total_uploads": total_uploads,
            "average_uploads": total_uploads / total_teachers if total_teachers > 0 else 0
        }
    
    def get_current_timestamp(self) -> str:
        """الحصول على الطابع الزمني الحالي"""
        from datetime import datetime
        return datetime.now().isoformat()
    
    def export_teachers_list(self) -> List[int]:
        """تصدير قائمة معرفات المعلمين المصرح لهم"""
        return [int(user_id) for user_id, teacher in self.teachers.items() 
                if teacher.get("active", False)]

# مثال على الاستخدام
if __name__ == "__main__":
    manager = TeacherManager()
    
    # إضافة معلم تجريبي
    manager.add_teacher(123456789, "أحمد محمد", "teacher")
    manager.add_teacher(987654321, "فاطمة علي", "admin")
    
    # طباعة الإحصائيات
    stats = manager.get_statistics()
    print("إحصائيات المعلمين:")
    print(f"إجمالي المعلمين: {stats['total_teachers']}")
    print(f"المعلمين النشطين: {stats['active_teachers']}")
    print(f"إجمالي الرفعات: {stats['total_uploads']}")
    
    # تصدير قائمة المعلمين المصرح لهم
    authorized_list = manager.export_teachers_list()
    print(f"قائمة المعلمين المصرح لهم: {authorized_list}")