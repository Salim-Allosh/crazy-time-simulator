#!/usr/bin/env python3
"""
مشغل الواجهة الرسومية لمحاكي Crazy Time
=====================================
ملف بسيط لتشغيل الواجهة الرسومية
"""

import sys
import os

def main():
    """تشغيل الواجهة الرسومية"""
    try:
        # التأكد من وجود الملفات المطلوبة
        required_files = ['full_crazy_time_simulator.py', 'crazy_time_gui.py']
        missing_files = []
        
        for file in required_files:
            if not os.path.exists(file):
                missing_files.append(file)
        
        if missing_files:
            print("❌ ملفات مفقودة:")
            for file in missing_files:
                print(f"   - {file}")
            print("\n🔧 تأكد من وجود جميع الملفات في نفس المجلد")
            return
        
        # استيراد وتشغيل الواجهة
        print("🚀 تشغيل واجهة محاكي Crazy Time...")
        
        from crazy_time_gui import main as gui_main
        gui_main()
        
    except ImportError as e:
        print(f"❌ خطأ في الاستيراد: {e}")
        print("🔧 تأكد من تثبيت المكتبات المطلوبة:")
        print("   pip3 install pandas openpyxl matplotlib")
        
    except Exception as e:
        print(f"❌ خطأ غير متوقع: {e}")
        print("🔧 تأكد من صحة الملفات وإعادة المحاولة")

if __name__ == "__main__":
    main()

