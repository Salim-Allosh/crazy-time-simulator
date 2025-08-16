#!/usr/bin/env python3
"""
محاكي Crazy Time الكامل والقابل للتخصيص
========================================
- محاكاة شاملة لجميع التركيبات الممكنة
- متغيرات قابلة للتعديل في بداية البرنامج
- حفظ تلقائي وإمكانية الاستئناف
- تخصيص كامل للمعايير
"""

import random
import pandas as pd
import json
import time
import os
from datetime import datetime
from openpyxl import load_workbook, Workbook

# ==========================================
# 🎯 المتغيرات القابلة للتخصيص
# ==========================================

# معايير المحاكاة الأساسية
SIMULATION_CONFIG = {
    'initial_balance': 300,          # الميزانية الأولية
    'min_balance_threshold': 100,    # الحد الأدنى للاستمرار
    'trials_per_combination': 1000,  # عدد المحاولات لكل تركيبة
    'min_bet_amount': 0,             # أقل مبلغ رهان (0 = بدون رهان)
    'max_bet_amount': 20,            # أكبر مبلغ رهان
    'save_interval': 10,             # حفظ كل كم تركيبة
    'top_results_count': 100         # عدد أفضل النتائج المحفوظة
}

# تكوين عجلة اللعبة (عدد المواضع لكل نتيجة)
WHEEL_CONFIG = {
    '$1': 21,
    '$2': 13,
    '$5': 7,
    '$10': 4,
    'Coin Flip': 4,
    'Pachinko': 2,
    'Cash Hunt': 2,
    'Crazy Time': 1
}

# متوسطات الأرباح الرسمية للألعاب الإضافية (من Wizard of Odds)
BONUS_MULTIPLIERS = {
    'Coin Flip': 9.28,
    'Pachinko': 17.64,
    'Cash Hunt': 19.47,
    'Crazy Time': 36.43
}

# مضاعفات الأرقام
NUMBER_MULTIPLIERS = {
    '$1': 1,
    '$2': 2,
    '$5': 5,
    '$10': 10
}

# أسماء خيارات الرهان
BETTING_OPTIONS = ['$1', '$2', '$5', '$10', 'Coin Flip', 'Pachinko', 'Cash Hunt', 'Crazy Time']

# إعدادات الملفات
FILE_CONFIG = {
    'excel_file': 'crazy_time_full_results.xlsx',
    'checkpoint_file': 'full_simulation_checkpoint.json',
    'progress_log': 'simulation_progress.log'
}

# ==========================================
# 🎰 فئة المحاكي الرئيسية
# ==========================================

class FullCrazyTimeSimulator:
    def __init__(self, config=None):
        # تحميل الإعدادات
        self.config = config or SIMULATION_CONFIG
        self.wheel_config = WHEEL_CONFIG
        self.bonus_multipliers = BONUS_MULTIPLIERS
        self.number_multipliers = NUMBER_MULTIPLIERS
        self.betting_options = BETTING_OPTIONS
        self.file_config = FILE_CONFIG
        
        # إنشاء العجلة المرجحة
        self.wheel = []
        for outcome, count in self.wheel_config.items():
            self.wheel.extend([outcome] * count)
        
        # متغيرات التتبع
        self.all_results = []
        self.top_results = []
        self.current_combination_index = 0
        self.total_combinations = 0
        self.tested_combinations = 0
        self.start_time = None
        
        # تحميل التقدم السابق
        self.load_checkpoint()
        
        # طباعة الإعدادات
        self.print_configuration()
    
    def print_configuration(self):
        """طباعة إعدادات المحاكاة"""
        print("🎰 إعدادات محاكي Crazy Time الكامل")
        print("=" * 60)
        print("📋 معايير المحاكاة:")
        print(f"   • الميزانية الأولية: ${self.config['initial_balance']}")
        print(f"   • الحد الأدنى للاستمرار: ${self.config['min_balance_threshold']}")
        print(f"   • المحاولات لكل تركيبة: {self.config['trials_per_combination']:,}")
        print(f"   • نطاق الرهان: ${self.config['min_bet_amount']} - ${self.config['max_bet_amount']}")
        print(f"   • حفظ كل: {self.config['save_interval']} تركيبات")
        print(f"   • حفظ أفضل: {self.config['top_results_count']} نتيجة")
        
        print(f"\n🎲 تكوين العجلة:")
        total_positions = sum(self.wheel_config.values())
        for outcome, count in self.wheel_config.items():
            percentage = (count / total_positions) * 100
            print(f"   • {outcome}: {count} موضع ({percentage:.1f}%)")
        
        print(f"\n💰 متوسطات الأرباح:")
        for game, multiplier in self.bonus_multipliers.items():
            print(f"   • {game}: {multiplier:.2f}x")
        
        print(f"\n📁 ملفات الإخراج:")
        print(f"   • Excel: {self.file_config['excel_file']}")
        print(f"   • نقطة التوقف: {self.file_config['checkpoint_file']}")
        print("=" * 60)
    
    def generate_bonus_multiplier(self, bonus_type):
        """توليد مضاعف عشوائي حول المتوسط الرسمي"""
        base_avg = self.bonus_multipliers[bonus_type]
        
        if bonus_type == 'Coin Flip':
            # Coin Flip: جانب منخفض (2-5) أو عالي (7-25)
            if random.random() < 0.5:
                return random.uniform(2, 5)
            else:
                return random.uniform(7, min(25, base_avg * 2))
                
        elif bonus_type == 'Cash Hunt':
            # Cash Hunt: توزيع واقعي من 5x إلى 500x
            return random.choices(
                [5, 7, 10, 15, 20, 25, 50, 75, 100, 200, 500],
                weights=[20, 18, 25, 15, 12, 6, 3, 2, 1, 0.5, 0.2]
            )[0]
            
        elif bonus_type == 'Pachinko':
            # Pachinko مع إمكانية المضاعفة
            base_multiplier = random.choices(
                [7, 10, 15, 20, 25, 50, 100],
                weights=[30, 25, 20, 15, 8, 2, 1]
            )[0]
            
            # إمكانية المضاعفة (5.47% حسب البيانات الرسمية)
            while random.random() < 0.0547:
                base_multiplier *= 2
                if base_multiplier > 10000:  # حد أقصى معقول
                    break
            return min(base_multiplier, 10000)
            
        elif bonus_type == 'Crazy Time':
            # Crazy Time: نظام عجلات معقد
            base_multiplier = random.choices(
                [10, 15, 20, 25, 50, 100, 200, 500],
                weights=[25, 20, 18, 15, 12, 8, 2, 1]
            )[0]
            
            # تطبيق مضاعفات إضافية
            if random.random() < 0.1:  # 10% فرصة للمضاعفة
                base_multiplier *= random.choice([2, 3, 5])
            
            return min(base_multiplier, 20000)
            
        return base_avg
    
    def spin_wheel(self):
        """محاكاة دوران العجلة"""
        return random.choice(self.wheel)
    
    def calculate_payout(self, bets, outcome):
        """حساب المكسب/الخسارة لرهان معين ونتيجة"""
        total_bet = sum(bets)
        payout = 0
        
        if outcome in self.number_multipliers:
            # نتيجة رقم
            multiplier = self.number_multipliers[outcome]
            bet_index = self.betting_options.index(outcome)
            payout = bets[bet_index] * multiplier
            
        else:
            # نتيجة لعبة إضافية
            bet_index = self.betting_options.index(outcome)
            if bets[bet_index] > 0:
                bonus_multiplier = self.generate_bonus_multiplier(outcome)
                payout = bets[bet_index] * bonus_multiplier
        
        return payout - total_bet  # صافي الربح/الخسارة
    
    def simulate_combination(self, combination):
        """محاكاة تركيبة رهان واحدة"""
        balance = self.config['initial_balance']
        wins = 0
        losses = 0
        total_profit = 0
        total_loss = 0
        max_single_win = 0
        max_single_loss = 0
        win_streak = 0
        max_win_streak = 0
        loss_streak = 0
        max_loss_streak = 0
        
        total_bet = sum(combination)
        
        if total_bet == 0:
            return None  # تخطي التركيبات بدون رهان
            
        for trial in range(self.config['trials_per_combination']):
            # فحص إمكانية الاستمرار
            if balance < total_bet or balance < self.config['min_balance_threshold']:
                break
                
            # دوران العجلة
            outcome = self.spin_wheel()
            
            # حساب النتيجة
            net_result = self.calculate_payout(combination, outcome)
            balance += net_result
            
            # تتبع الإحصائيات
            if net_result > 0:
                wins += 1
                total_profit += net_result
                max_single_win = max(max_single_win, net_result)
                win_streak += 1
                max_win_streak = max(max_win_streak, win_streak)
                loss_streak = 0
            else:
                losses += 1
                total_loss += abs(net_result)
                max_single_loss = max(max_single_loss, abs(net_result))
                loss_streak += 1
                max_loss_streak = max(max_loss_streak, loss_streak)
                win_streak = 0
        
        trials_completed = trial + 1
        
        return {
            'combination': combination,
            'combination_str': f"[{','.join(map(str, combination))}]",
            'total_bet': total_bet,
            'final_balance': balance,
            'trials_completed': trials_completed,
            'wins': wins,
            'losses': losses,
            'win_rate': wins / trials_completed if trials_completed > 0 else 0,
            'total_profit': total_profit,
            'total_loss': total_loss,
            'max_single_win': max_single_win,
            'max_single_loss': max_single_loss,
            'max_win_streak': max_win_streak,
            'max_loss_streak': max_loss_streak,
            'profit_percentage': ((balance - self.config['initial_balance']) / self.config['initial_balance']) * 100,
            'average_win': total_profit / wins if wins > 0 else 0,
            'average_loss': total_loss / losses if losses > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def generate_all_combinations(self):
        """توليد جميع التركيبات الممكنة"""
        combinations = []
        min_bet = self.config['min_bet_amount']
        max_bet = self.config['max_bet_amount']
        
        for total_bet in range(min_bet, max_bet + 1):
            for combo in self._generate_combinations_with_sum(8, total_bet):
                combinations.append(combo)
        
        return combinations
    
    def _generate_combinations_with_sum(self, num_variables, target_sum):
        """توليد التركيبات التي مجموعها = target_sum"""
        if num_variables == 1:
            yield [target_sum]
        else:
            for i in range(target_sum + 1):
                for combo in self._generate_combinations_with_sum(num_variables - 1, target_sum - i):
                    yield [i] + combo
    
    def save_to_excel(self):
        """حفظ النتائج في ملف Excel"""
        if not self.all_results:
            return
            
        # إنشاء DataFrame
        df = pd.DataFrame(self.all_results)
        
        # ترتيب الأعمدة
        column_order = [
            'combination_str', 'total_bet', 'final_balance', 'profit_percentage',
            'trials_completed', 'wins', 'losses', 'win_rate',
            'max_single_win', 'max_single_loss', 'max_win_streak', 'max_loss_streak',
            'average_win', 'average_loss', 'timestamp'
        ]
        df = df[column_order]
        
        # أسماء الأعمدة بالعربية
        df.columns = [
            'التركيبة', 'إجمالي الرهان', 'المبلغ النهائي', 'نسبة الربح%',
            'عدد الجولات', 'الانتصارات', 'الخسائر', 'معدل الفوز',
            'أكبر ربح', 'أكبر خسارة', 'أطول سلسلة فوز', 'أطول سلسلة خسارة',
            'متوسط الربح', 'متوسط الخسارة', 'الوقت'
        ]
        
        # حفظ في Excel
        with pd.ExcelWriter(self.file_config['excel_file'], engine='openpyxl') as writer:
            # ورقة جميع النتائج
            df.to_excel(writer, sheet_name='جميع النتائج', index=False)
            
            # ورقة أفضل النتائج
            if self.top_results:
                top_df = pd.DataFrame(self.top_results)
                top_df = top_df[column_order]
                top_df.columns = df.columns
                top_df.to_excel(writer, sheet_name='أفضل النتائج', index=False)
            
            # ورقة الملخص الإحصائي
            self._create_summary_sheet(writer)
        
        print(f"💾 تم حفظ {len(self.all_results)} نتيجة في {self.file_config['excel_file']}")
    
    def _create_summary_sheet(self, writer):
        """إنشاء ورقة الملخص الإحصائي"""
        if not self.all_results:
            return
            
        results = self.all_results
        
        summary_data = {
            'المعلومة': [
                'إجمالي التركيبات المختبرة',
                'أفضل نتيجة',
                'أسوأ نتيجة',
                'متوسط المبلغ النهائي',
                'معدل النجاح الإجمالي',
                'أعلى نسبة ربح',
                'أقل نسبة خسارة',
                'متوسط عدد الجولات',
                'أكبر ربح في جولة واحدة',
                'أطول سلسلة فوز',
                'الوقت الإجمالي للمحاكاة',
                'آخر تحديث'
            ],
            'القيمة': [
                len(results),
                f"${max(r['final_balance'] for r in results):.2f}",
                f"${min(r['final_balance'] for r in results):.2f}",
                f"${sum(r['final_balance'] for r in results) / len(results):.2f}",
                f"{sum(1 for r in results if r['final_balance'] > self.config['initial_balance']) / len(results):.1%}",
                f"{max(r['profit_percentage'] for r in results):.1f}%",
                f"{min(r['profit_percentage'] for r in results):.1f}%",
                f"{sum(r['trials_completed'] for r in results) / len(results):.0f}",
                f"${max(r['max_single_win'] for r in results):.2f}",
                max(r['max_win_streak'] for r in results),
                f"{(time.time() - self.start_time) / 3600:.1f} ساعة" if self.start_time else "غير محدد",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ]
        }
        
        summary_df = pd.DataFrame(summary_data)
        summary_df.to_excel(writer, sheet_name='ملخص إحصائي', index=False)
    
    def save_checkpoint(self):
        """حفظ نقطة التوقف"""
        checkpoint_data = {
            'current_combination_index': self.current_combination_index,
            'total_combinations': self.total_combinations,
            'tested_combinations': self.tested_combinations,
            'config': self.config,
            'start_time': self.start_time,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(self.file_config['checkpoint_file'], 'w', encoding='utf-8') as f:
            json.dump(checkpoint_data, f, indent=2, ensure_ascii=False)
    
    def load_checkpoint(self):
        """تحميل نقطة التوقف"""
        if os.path.exists(self.file_config['checkpoint_file']):
            try:
                with open(self.file_config['checkpoint_file'], 'r', encoding='utf-8') as f:
                    checkpoint_data = json.load(f)
                
                self.current_combination_index = checkpoint_data.get('current_combination_index', 0)
                self.total_combinations = checkpoint_data.get('total_combinations', 0)
                self.tested_combinations = checkpoint_data.get('tested_combinations', 0)
                self.start_time = checkpoint_data.get('start_time', None)
                
                print(f"📂 تم تحميل نقطة التوقف: التركيبة {self.current_combination_index:,}")
                
            except Exception as e:
                print(f"⚠️ خطأ في تحميل نقطة التوقف: {e}")
                self.current_combination_index = 0
        else:
            print("🆕 بدء محاكاة جديدة")
    
    def update_top_results(self, result):
        """تحديث قائمة أفضل النتائج"""
        if result is None:
            return
            
        self.top_results.append(result)
        self.top_results.sort(key=lambda x: x['final_balance'], reverse=True)
        
        if len(self.top_results) > self.config['top_results_count']:
            self.top_results = self.top_results[:self.config['top_results_count']]
    
    def log_progress(self, message):
        """تسجيل التقدم في ملف"""
        with open(self.file_config['progress_log'], 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
    
    def run_full_simulation(self):
        """تشغيل المحاكاة الكاملة"""
        print("🚀 بدء المحاكاة الكاملة لجميع التركيبات...")
        print("=" * 60)
        
        # توليد جميع التركيبات
        if self.total_combinations == 0:
            print("📊 توليد جميع التركيبات...")
            all_combinations = self.generate_all_combinations()
            self.total_combinations = len(all_combinations)
            print(f"📈 إجمالي التركيبات: {self.total_combinations:,}")
            
            # تقدير الوقت
            estimated_hours = (self.total_combinations * self.config['trials_per_combination'] * 0.0001) / 3600
            print(f"⏱️ الوقت المتوقع: ~{estimated_hours:.1f} ساعة")
        else:
            all_combinations = self.generate_all_combinations()
            print(f"🔄 استئناف المحاكاة من التركيبة {self.current_combination_index:,}")
        
        print("=" * 60)
        
        if self.start_time is None:
            self.start_time = time.time()
        
        last_save_time = time.time()
        
        try:
            # بدء المحاكاة من النقطة المحفوظة
            for i in range(self.current_combination_index, len(all_combinations)):
                combination = all_combinations[i]
                
                # محاكاة هذه التركيبة
                result = self.simulate_combination(combination)
                
                if result:
                    self.all_results.append(result)
                    self.update_top_results(result)
                    self.tested_combinations += 1
                
                self.current_combination_index = i + 1
                
                # حفظ دوري
                if (i + 1) % self.config['save_interval'] == 0:
                    self.save_to_excel()
                    self.save_checkpoint()
                    
                    # تحديث التقدم
                    elapsed = time.time() - self.start_time
                    save_elapsed = time.time() - last_save_time
                    progress = ((i + 1) / len(all_combinations)) * 100
                    remaining_combinations = len(all_combinations) - (i + 1)
                    estimated_remaining_time = (remaining_combinations * elapsed / (i + 1)) / 3600
                    
                    progress_msg = f"⏳ التقدم: {progress:.3f}% ({i+1:,}/{len(all_combinations):,})"
                    time_msg = f"⏱️ الوقت: {elapsed/3600:.1f}h | المتبقي: ~{estimated_remaining_time:.1f}h"
                    
                    print(progress_msg)
                    print(time_msg)
                    
                    if self.top_results:
                        best = self.top_results[0]
                        best_msg = f"🏆 أفضل نتيجة: ${best['final_balance']:.2f} - {best['combination_str']}"
                        print(best_msg)
                    
                    # تسجيل في ملف
                    self.log_progress(f"{progress_msg} | {time_msg}")
                    
                    print("-" * 60)
                    last_save_time = time.time()
        
        except KeyboardInterrupt:
            print("\n⏸️ تم إيقاف المحاكاة بواسطة المستخدم")
            self.save_to_excel()
            self.save_checkpoint()
            print("💾 تم حفظ التقدم الحالي")
            return
        
        except Exception as e:
            print(f"\n❌ خطأ في المحاكاة: {e}")
            self.save_to_excel()
            self.save_checkpoint()
            print("💾 تم حفظ التقدم قبل الخطأ")
            return
        
        # حفظ نهائي
        self.save_to_excel()
        self.save_checkpoint()
        
        total_time = time.time() - self.start_time
        print(f"\n🎉 انتهت المحاكاة الكاملة بنجاح!")
        print(f"⏱️ الوقت الإجمالي: {total_time/3600:.1f} ساعة")
        print(f"📊 إجمالي التركيبات المختبرة: {self.tested_combinations:,}")
        
        if self.top_results:
            print(f"🏆 أفضل نتيجة: ${self.top_results[0]['final_balance']:.2f}")
            print(f"🥇 أفضل تركيبة: {self.top_results[0]['combination_str']}")
    
    def print_current_status(self):
        """طباعة حالة المحاكاة الحالية"""
        print(f"\n📊 حالة المحاكاة:")
        print(f"   • التركيبة الحالية: {self.current_combination_index:,}")
        print(f"   • إجمالي التركيبات: {self.total_combinations:,}")
        print(f"   • التركيبات المختبرة: {self.tested_combinations:,}")
        
        if self.total_combinations > 0:
            progress = (self.current_combination_index / self.total_combinations) * 100
            print(f"   • نسبة التقدم: {progress:.3f}%")
        
        if self.top_results:
            print(f"   • أفضل نتيجة حالياً: ${self.top_results[0]['final_balance']:.2f}")

def main():
    """الدالة الرئيسية"""
    print("🎰 محاكي Crazy Time الكامل والقابل للتخصيص")
    print("=" * 60)
    
    # إنشاء المحاكي
    simulator = FullCrazyTimeSimulator()
    
    # عرض الحالة الحالية
    simulator.print_current_status()
    
    # سؤال المستخدم عن الاستئناف
    if simulator.current_combination_index > 0:
        response = input(f"\n❓ هل تريد الاستئناف من التركيبة {simulator.current_combination_index:,}؟ (y/n): ")
        if response.lower() != 'y':
            simulator.current_combination_index = 0
            simulator.tested_combinations = 0
            simulator.all_results = []
            simulator.start_time = None
            print("🆕 بدء محاكاة جديدة")
    
    # تأكيد بدء المحاكاة الكاملة
    print(f"\n⚠️ تحذير: هذه المحاكاة ستختبر {simulator.total_combinations or '3+ مليون'} تركيبة!")
    print(f"⏱️ الوقت المتوقع: 80+ ساعة")
    confirm = input("❓ هل أنت متأكد من بدء المحاكاة الكاملة؟ (yes/no): ")
    
    if confirm.lower() == 'yes':
        try:
            simulator.run_full_simulation()
        except KeyboardInterrupt:
            print("\n👋 تم إنهاء البرنامج")
    else:
        print("❌ تم إلغاء المحاكاة")

if __name__ == "__main__":
    main()

