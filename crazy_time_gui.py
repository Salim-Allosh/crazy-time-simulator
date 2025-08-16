#!/usr/bin/env python3
"""
واجهة رسومية لمحاكي Crazy Time
==============================
واجهة سهلة الاستخدام مع إحصائيات مباشرة وتحكم كامل
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import threading
import time
import json
import os
from datetime import datetime
import queue
import sys

# استيراد المحاكي
from full_crazy_time_simulator import FullCrazyTimeSimulator, SIMULATION_CONFIG

class CrazyTimeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("محاكي Crazy Time - الواجهة الرسومية")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2c3e50')
        
        # متغيرات التحكم
        self.simulator = None
        self.simulation_thread = None
        self.is_running = False
        self.is_paused = False
        self.should_stop = False
        
        # قائمة انتظار للرسائل بين الخيوط
        self.message_queue = queue.Queue()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # بدء تحديث الواجهة
        self.update_gui()
        
        # تحميل الإعدادات
        self.load_settings()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # تكوين الشبكة
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # العنوان
        title_label = tk.Label(main_frame, text="🎰 محاكي Crazy Time الكامل", 
                              font=("Arial", 20, "bold"), fg="#e74c3c", bg="#2c3e50")
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # إطار الإعدادات
        self.create_settings_frame(main_frame)
        
        # إطار التحكم
        self.create_control_frame(main_frame)
        
        # إطار الإحصائيات
        self.create_stats_frame(main_frame)
        
        # إطار السجل
        self.create_log_frame(main_frame)
    
    def create_settings_frame(self, parent):
        """إنشاء إطار الإعدادات"""
        settings_frame = ttk.LabelFrame(parent, text="⚙️ إعدادات المحاكاة", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N), padx=(0, 10))
        
        # الميزانية الأولية
        ttk.Label(settings_frame, text="الميزانية الأولية ($):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.initial_balance_var = tk.StringVar(value=str(SIMULATION_CONFIG['initial_balance']))
        ttk.Entry(settings_frame, textvariable=self.initial_balance_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=(5, 0))
        
        # الحد الأدنى
        ttk.Label(settings_frame, text="الحد الأدنى ($):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.min_threshold_var = tk.StringVar(value=str(SIMULATION_CONFIG['min_balance_threshold']))
        ttk.Entry(settings_frame, textvariable=self.min_threshold_var, width=10).grid(row=1, column=1, sticky=tk.W, padx=(5, 0))
        
        # عدد المحاولات
        ttk.Label(settings_frame, text="المحاولات لكل تركيبة:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.trials_var = tk.StringVar(value=str(SIMULATION_CONFIG['trials_per_combination']))
        ttk.Entry(settings_frame, textvariable=self.trials_var, width=10).grid(row=2, column=1, sticky=tk.W, padx=(5, 0))
        
        # نطاق الرهان
        ttk.Label(settings_frame, text="أقل رهان ($):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.min_bet_var = tk.StringVar(value=str(SIMULATION_CONFIG['min_bet_amount']))
        ttk.Entry(settings_frame, textvariable=self.min_bet_var, width=10).grid(row=3, column=1, sticky=tk.W, padx=(5, 0))
        
        ttk.Label(settings_frame, text="أكبر رهان ($):").grid(row=4, column=0, sticky=tk.W, pady=2)
        self.max_bet_var = tk.StringVar(value=str(SIMULATION_CONFIG['max_bet_amount']))
        ttk.Entry(settings_frame, textvariable=self.max_bet_var, width=10).grid(row=4, column=1, sticky=tk.W, padx=(5, 0))
        
        # فترة الحفظ
        ttk.Label(settings_frame, text="حفظ كل:").grid(row=5, column=0, sticky=tk.W, pady=2)
        self.save_interval_var = tk.StringVar(value=str(SIMULATION_CONFIG['save_interval']))
        ttk.Entry(settings_frame, textvariable=self.save_interval_var, width=10).grid(row=5, column=1, sticky=tk.W, padx=(5, 0))
        ttk.Label(settings_frame, text="تركيبة").grid(row=5, column=2, sticky=tk.W, padx=(5, 0))
        
        # زر تطبيق الإعدادات
        ttk.Button(settings_frame, text="تطبيق الإعدادات", command=self.apply_settings).grid(row=6, column=0, columnspan=3, pady=(10, 0))
    
    def create_control_frame(self, parent):
        """إنشاء إطار التحكم"""
        control_frame = ttk.LabelFrame(parent, text="🎮 التحكم", padding="10")
        control_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N), padx=(5, 5))
        
        # أزرار التحكم
        self.start_button = ttk.Button(control_frame, text="🚀 بدء المحاكاة", 
                                      command=self.start_simulation, style="Success.TButton")
        self.start_button.grid(row=0, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.pause_button = ttk.Button(control_frame, text="⏸️ إيقاف مؤقت", 
                                      command=self.pause_simulation, state="disabled")
        self.pause_button.grid(row=0, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.stop_button = ttk.Button(control_frame, text="⏹️ إيقاف نهائي", 
                                     command=self.stop_simulation, state="disabled", style="Danger.TButton")
        self.stop_button.grid(row=1, column=0, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        self.resume_button = ttk.Button(control_frame, text="▶️ استئناف", 
                                       command=self.resume_simulation, state="disabled")
        self.resume_button.grid(row=1, column=1, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        # شريط التقدم
        ttk.Label(control_frame, text="التقدم الإجمالي:").grid(row=2, column=0, columnspan=2, sticky=tk.W, pady=(10, 0))
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # نص التقدم
        self.progress_text = tk.StringVar(value="جاهز للبدء")
        ttk.Label(control_frame, textvariable=self.progress_text).grid(row=4, column=0, columnspan=2, pady=5)
        
        # تكوين الأعمدة
        control_frame.columnconfigure(0, weight=1)
        control_frame.columnconfigure(1, weight=1)
    
    def create_stats_frame(self, parent):
        """إنشاء إطار الإحصائيات"""
        stats_frame = ttk.LabelFrame(parent, text="📊 إحصائيات مباشرة", padding="10")
        stats_frame.grid(row=1, column=2, sticky=(tk.W, tk.E, tk.N), padx=(5, 0))
        
        # إحصائيات أساسية
        self.stats_labels = {}
        stats_data = [
            ("التركيبات المختبرة", "tested_combinations"),
            ("إجمالي التركيبات", "total_combinations"),
            ("نسبة التقدم", "progress_percentage"),
            ("الوقت المنقضي", "elapsed_time"),
            ("الوقت المتبقي", "remaining_time"),
            ("أفضل نتيجة", "best_result"),
            ("أفضل تركيبة", "best_combination"),
            ("معدل السرعة", "speed_rate"),
            ("آخر حفظ", "last_save"),
            ("حالة المحاكاة", "status")
        ]
        
        for i, (label, key) in enumerate(stats_data):
            ttk.Label(stats_frame, text=f"{label}:").grid(row=i, column=0, sticky=tk.W, pady=2)
            self.stats_labels[key] = tk.StringVar(value="--")
            ttk.Label(stats_frame, textvariable=self.stats_labels[key], 
                     foreground="#27ae60", font=("Arial", 9, "bold")).grid(row=i, column=1, sticky=tk.W, padx=(10, 0), pady=2)
    
    def create_log_frame(self, parent):
        """إنشاء إطار السجل"""
        log_frame = ttk.LabelFrame(parent, text="📝 سجل العمليات", padding="10")
        log_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        # منطقة النص
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, width=80, 
                                                 font=("Consolas", 9), bg="#34495e", fg="#ecf0f1")
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # أزرار السجل
        log_buttons_frame = ttk.Frame(log_frame)
        log_buttons_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(5, 0))
        
        ttk.Button(log_buttons_frame, text="مسح السجل", command=self.clear_log).grid(row=0, column=0, padx=(0, 5))
        ttk.Button(log_buttons_frame, text="حفظ السجل", command=self.save_log).grid(row=0, column=1, padx=5)
        ttk.Button(log_buttons_frame, text="فتح مجلد النتائج", command=self.open_results_folder).grid(row=0, column=2, padx=5)
        
        # تكوين الشبكة
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # رسالة ترحيب
        self.log_message("🎰 مرحباً بك في محاكي Crazy Time!")
        self.log_message("📋 قم بتعديل الإعدادات حسب الحاجة ثم اضغط 'بدء المحاكاة'")
    
    def apply_settings(self):
        """تطبيق الإعدادات"""
        try:
            # تحديث الإعدادات
            new_config = {
                'initial_balance': int(self.initial_balance_var.get()),
                'min_balance_threshold': int(self.min_threshold_var.get()),
                'trials_per_combination': int(self.trials_var.get()),
                'min_bet_amount': int(self.min_bet_var.get()),
                'max_bet_amount': int(self.max_bet_var.get()),
                'save_interval': int(self.save_interval_var.get()),
                'top_results_count': 100
            }
            
            # التحقق من صحة الإعدادات
            if new_config['min_bet_amount'] > new_config['max_bet_amount']:
                raise ValueError("أقل رهان يجب أن يكون أصغر من أكبر رهان")
            
            if new_config['initial_balance'] <= new_config['min_balance_threshold']:
                raise ValueError("الميزانية الأولية يجب أن تكون أكبر من الحد الأدنى")
            
            # حفظ الإعدادات
            with open('gui_settings.json', 'w', encoding='utf-8') as f:
                json.dump(new_config, f, indent=2, ensure_ascii=False)
            
            self.log_message("✅ تم تطبيق الإعدادات بنجاح")
            
            # حساب عدد التركيبات المتوقع
            total_combinations = self.calculate_total_combinations(new_config)
            estimated_time = (total_combinations * new_config['trials_per_combination'] * 0.0001) / 3600
            
            self.log_message(f"📊 إجمالي التركيبات المتوقعة: {total_combinations:,}")
            self.log_message(f"⏱️ الوقت المتوقع: ~{estimated_time:.1f} ساعة")
            
        except ValueError as e:
            messagebox.showerror("خطأ في الإعدادات", str(e))
            self.log_message(f"❌ خطأ في الإعدادات: {e}")
    
    def calculate_total_combinations(self, config):
        """حساب إجمالي التركيبات"""
        total = 0
        for k in range(config['min_bet_amount'], config['max_bet_amount'] + 1):
            # حساب C(k+7, 7) باستخدام الصيغة
            combinations = 1
            for i in range(7):
                combinations = combinations * (k + 7 - i) // (i + 1)
            total += combinations
        return total
    
    def start_simulation(self):
        """بدء المحاكاة"""
        if self.is_running:
            self.log_message("⚠️ المحاكاة قيد التشغيل بالفعل")
            return
        
        try:
            # تحميل الإعدادات
            if os.path.exists('gui_settings.json'):
                with open('gui_settings.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                self.apply_settings()
                with open('gui_settings.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
            
            # إنشاء المحاكي
            self.simulator = FullCrazyTimeSimulator(config)
            
            # تحديث حالة الأزرار
            self.start_button.config(state="disabled")
            self.pause_button.config(state="normal")
            self.stop_button.config(state="normal")
            
            # بدء المحاكاة في خيط منفصل
            self.is_running = True
            self.should_stop = False
            self.simulation_thread = threading.Thread(target=self.run_simulation_thread, daemon=True)
            self.simulation_thread.start()
            
            self.log_message("🚀 تم بدء المحاكاة...")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في بدء المحاكاة: {e}")
            self.log_message(f"❌ خطأ في بدء المحاكاة: {e}")
    
    def pause_simulation(self):
        """إيقاف مؤقت للمحاكاة"""
        if not self.is_running:
            return
        
        self.is_paused = True
        self.pause_button.config(state="disabled")
        self.resume_button.config(state="normal")
        self.log_message("⏸️ تم إيقاف المحاكاة مؤقتاً")
    
    def resume_simulation(self):
        """استئناف المحاكاة"""
        if not self.is_running:
            return
        
        self.is_paused = False
        self.pause_button.config(state="normal")
        self.resume_button.config(state="disabled")
        self.log_message("▶️ تم استئناف المحاكاة")
    
    def stop_simulation(self):
        """إيقاف نهائي للمحاكاة"""
        if not self.is_running:
            return
        
        result = messagebox.askyesno("تأكيد الإيقاف", "هل أنت متأكد من إيقاف المحاكاة؟\nسيتم حفظ التقدم الحالي.")
        
        if result:
            self.should_stop = True
            self.log_message("⏹️ جاري إيقاف المحاكاة وحفظ التقدم...")
    
    def run_simulation_thread(self):
        """تشغيل المحاكاة في خيط منفصل"""
        try:
            # توليد التركيبات
            if self.simulator.total_combinations == 0:
                self.message_queue.put(("log", "📊 توليد جميع التركيبات..."))
                all_combinations = self.simulator.generate_all_combinations()
                self.simulator.total_combinations = len(all_combinations)
                self.message_queue.put(("log", f"📈 إجمالي التركيبات: {self.simulator.total_combinations:,}"))
            else:
                all_combinations = self.simulator.generate_all_combinations()
            
            if self.simulator.start_time is None:
                self.simulator.start_time = time.time()
            
            last_save_time = time.time()
            last_update_time = time.time()
            
            # بدء المحاكاة
            for i in range(self.simulator.current_combination_index, len(all_combinations)):
                # فحص الإيقاف
                if self.should_stop:
                    break
                
                # فحص الإيقاف المؤقت
                while self.is_paused and not self.should_stop:
                    time.sleep(0.1)
                
                if self.should_stop:
                    break
                
                combination = all_combinations[i]
                
                # محاكاة التركيبة
                result = self.simulator.simulate_combination(combination)
                
                if result:
                    self.simulator.all_results.append(result)
                    self.simulator.update_top_results(result)
                    self.simulator.tested_combinations += 1
                
                self.simulator.current_combination_index = i + 1
                
                # تحديث الواجهة كل ثانية
                current_time = time.time()
                if current_time - last_update_time >= 1.0:
                    progress = ((i + 1) / len(all_combinations)) * 100
                    elapsed = current_time - self.simulator.start_time
                    
                    self.message_queue.put(("progress", {
                        "progress": progress,
                        "tested": self.simulator.tested_combinations,
                        "total": len(all_combinations),
                        "elapsed": elapsed,
                        "current_index": i + 1
                    }))
                    
                    last_update_time = current_time
                
                # حفظ دوري
                if (i + 1) % self.simulator.config['save_interval'] == 0:
                    self.simulator.save_to_excel()
                    self.simulator.save_checkpoint()
                    
                    self.message_queue.put(("log", f"💾 تم حفظ النتائج - التركيبة {i+1:,}"))
                    last_save_time = current_time
            
            # حفظ نهائي
            self.simulator.save_to_excel()
            self.simulator.save_checkpoint()
            
            if self.should_stop:
                self.message_queue.put(("log", "⏹️ تم إيقاف المحاكاة وحفظ التقدم"))
            else:
                self.message_queue.put(("log", "🎉 انتهت المحاكاة بنجاح!"))
            
            self.message_queue.put(("finished", None))
            
        except Exception as e:
            self.message_queue.put(("error", f"خطأ في المحاكاة: {e}"))
            self.message_queue.put(("finished", None))
    
    def update_gui(self):
        """تحديث الواجهة بناءً على رسائل الخيط"""
        try:
            while True:
                message_type, data = self.message_queue.get_nowait()
                
                if message_type == "log":
                    self.log_message(data)
                
                elif message_type == "progress":
                    self.update_progress(data)
                
                elif message_type == "error":
                    self.log_message(f"❌ {data}")
                    messagebox.showerror("خطأ", data)
                
                elif message_type == "finished":
                    self.simulation_finished()
                
        except queue.Empty:
            pass
        
        # جدولة التحديث التالي
        self.root.after(100, self.update_gui)
    
    def update_progress(self, data):
        """تحديث شريط التقدم والإحصائيات"""
        progress = data["progress"]
        tested = data["tested"]
        total = data["total"]
        elapsed = data["elapsed"]
        current_index = data["current_index"]
        
        # تحديث شريط التقدم
        self.progress_var.set(progress)
        self.progress_text.set(f"{progress:.3f}% ({current_index:,}/{total:,})")
        
        # تحديث الإحصائيات
        self.stats_labels["tested_combinations"].set(f"{tested:,}")
        self.stats_labels["total_combinations"].set(f"{total:,}")
        self.stats_labels["progress_percentage"].set(f"{progress:.3f}%")
        
        # الوقت
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        self.stats_labels["elapsed_time"].set(f"{hours:02d}:{minutes:02d}")
        
        # الوقت المتبقي
        if progress > 0:
            remaining_seconds = (elapsed / progress) * (100 - progress)
            remaining_hours = int(remaining_seconds // 3600)
            remaining_minutes = int((remaining_seconds % 3600) // 60)
            self.stats_labels["remaining_time"].set(f"{remaining_hours:02d}:{remaining_minutes:02d}")
        
        # أفضل نتيجة
        if self.simulator and self.simulator.top_results:
            best = self.simulator.top_results[0]
            self.stats_labels["best_result"].set(f"${best['final_balance']:.2f}")
            self.stats_labels["best_combination"].set(best['combination_str'][:20] + "...")
        
        # معدل السرعة
        if elapsed > 0:
            speed = tested / elapsed
            self.stats_labels["speed_rate"].set(f"{speed:.1f} تركيبة/ثانية")
        
        # آخر حفظ
        self.stats_labels["last_save"].set(datetime.now().strftime("%H:%M:%S"))
        
        # الحالة
        if self.is_paused:
            self.stats_labels["status"].set("متوقف مؤقتاً")
        elif self.is_running:
            self.stats_labels["status"].set("قيد التشغيل")
        else:
            self.stats_labels["status"].set("متوقف")
    
    def simulation_finished(self):
        """إنهاء المحاكاة"""
        self.is_running = False
        self.is_paused = False
        self.should_stop = False
        
        # تحديث الأزرار
        self.start_button.config(state="normal", text="🔄 استئناف المحاكاة")
        self.pause_button.config(state="disabled")
        self.stop_button.config(state="disabled")
        self.resume_button.config(state="disabled")
        
        self.stats_labels["status"].set("منتهي")
    
    def log_message(self, message):
        """إضافة رسالة للسجل"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, formatted_message)
        self.log_text.see(tk.END)
    
    def clear_log(self):
        """مسح السجل"""
        self.log_text.delete(1.0, tk.END)
        self.log_message("🗑️ تم مسح السجل")
    
    def save_log(self):
        """حفظ السجل"""
        try:
            log_content = self.log_text.get(1.0, tk.END)
            filename = f"simulation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(log_content)
            
            self.log_message(f"💾 تم حفظ السجل في: {filename}")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ السجل: {e}")
    
    def open_results_folder(self):
        """فتح مجلد النتائج"""
        try:
            import subprocess
            import platform
            
            current_dir = os.getcwd()
            
            if platform.system() == "Windows":
                subprocess.run(["explorer", current_dir])
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["open", current_dir])
            else:  # Linux
                subprocess.run(["xdg-open", current_dir])
                
        except Exception as e:
            self.log_message(f"⚠️ لا يمكن فتح المجلد: {e}")
    
    def load_settings(self):
        """تحميل الإعدادات المحفوظة"""
        try:
            if os.path.exists('gui_settings.json'):
                with open('gui_settings.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                self.initial_balance_var.set(str(config.get('initial_balance', 300)))
                self.min_threshold_var.set(str(config.get('min_balance_threshold', 100)))
                self.trials_var.set(str(config.get('trials_per_combination', 1000)))
                self.min_bet_var.set(str(config.get('min_bet_amount', 0)))
                self.max_bet_var.set(str(config.get('max_bet_amount', 20)))
                self.save_interval_var.set(str(config.get('save_interval', 10)))
                
                self.log_message("📂 تم تحميل الإعدادات المحفوظة")
        
        except Exception as e:
            self.log_message(f"⚠️ خطأ في تحميل الإعدادات: {e}")
    
    def on_closing(self):
        """عند إغلاق النافذة"""
        if self.is_running:
            result = messagebox.askyesno("تأكيد الإغلاق", 
                                       "المحاكاة قيد التشغيل. هل تريد إيقافها وإغلاق البرنامج؟\nسيتم حفظ التقدم الحالي.")
            if result:
                self.should_stop = True
                self.log_message("🔄 جاري إغلاق البرنامج...")
                # انتظار قصير لحفظ البيانات
                self.root.after(2000, self.root.destroy)
            return
        
        self.root.destroy()

def main():
    """الدالة الرئيسية"""
    # إنشاء النافذة الرئيسية
    root = tk.Tk()
    
    # تطبيق الستايل
    style = ttk.Style()
    style.theme_use('clam')
    
    # ألوان مخصصة
    style.configure("Success.TButton", foreground="white", background="#27ae60")
    style.configure("Danger.TButton", foreground="white", background="#e74c3c")
    
    # إنشاء التطبيق
    app = CrazyTimeGUI(root)
    
    # ربط حدث الإغلاق
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # بدء التطبيق
    root.mainloop()

if __name__ == "__main__":
    main()

