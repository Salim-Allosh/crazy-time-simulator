# 🎰 Crazy Time Simulator

محاكي شامل ومتقدم للعبة Crazy Time مع واجهة رسومية وتحليل رياضي دقيق.

## 🚀 التحميل السريع

### للمستخدمين العاديين:
1. اذهب إلى [Releases](../../releases)
2. حمل أحدث إصدار `CrazyTimeSimulator-Windows.zip`
3. فك الضغط وشغل `CrazyTimeSimulator.exe`

### للمطورين:
```bash
git clone https://github.com/YOUR_USERNAME/crazy-time-simulator.git
cd crazy-time-simulator
pip install -r requirements.txt
python run_gui.py
```

## ✨ المميزات

- 🖥️ **واجهة رسومية متقدمة** - تحكم كامل وسهل الاستخدام
- 🎯 **محاكاة شاملة** - جميع الاحتمالات الممكنة (3+ مليون تركيبة)
- 💾 **حفظ تلقائي** - لا تفقد تقدمك أبداً
- ⏸️ **إيقاف واستئناف** - تحكم كامل في المحاكاة
- 📊 **إحصائيات مباشرة** - مراقبة التقدم والنتائج لحظياً
- 📈 **نتائج Excel مفصلة** - تحليل شامل وقابل للفلترة
- 🛡️ **حماية من التعليق** - إيقاف آمن في أي وقت
- ⚙️ **إعدادات قابلة للتخصيص** - تحكم في جميع المعايير

## 📋 متطلبات النظام

### للملف التنفيذي (.exe):
- **Windows 7/8/10/11** (64-bit)
- **4 GB RAM** على الأقل
- **2 GB مساحة** للبرنامج + 5 GB للنتائج

### للتشغيل من الكود:
- **Python 3.7+**
- **المكتبات**: pandas, openpyxl, tkinter, matplotlib

## 🎮 كيفية الاستخدام

### 1. تشغيل البرنامج
- **Windows**: شغل `CrazyTimeSimulator.exe`
- **من الكود**: `python run_gui.py`

### 2. تخصيص الإعدادات
- **الميزانية الأولية**: المبلغ الذي تبدأ به (افتراضي: $300)
- **الحد الأدنى**: المبلغ الذي عنده تتوقف المحاكاة (افتراضي: $100)
- **المحاولات لكل تركيبة**: عدد الجولات (افتراضي: 1000)
- **نطاق الرهان**: من $0 إلى $20

### 3. بدء المحاكاة
- اضغط **"🚀 بدء المحاكاة"**
- راقب التقدم في الإحصائيات المباشرة
- استخدم **"⏸️ إيقاف مؤقت"** أو **"⏹️ إيقاف نهائي"** حسب الحاجة

### 4. مراجعة النتائج
- النتائج تُحفظ تلقائياً في `crazy_time_full_results.xlsx`
- 3 أوراق: جميع النتائج، أفضل 100، ملخص إحصائي

## 📊 فهم النتائج

### أوراق Excel:
1. **جميع النتائج**: كل التركيبات المختبرة مع تفاصيلها
2. **أفضل النتائج**: أفضل 100 تركيبة مرتبة حسب الربحية
3. **ملخص إحصائي**: إحصائيات شاملة ومعدلات النجاح

### المعايير المهمة:
- **المبلغ النهائي**: المبلغ بعد 1000 جولة
- **نسبة الربح**: النسبة المئوية للربح/الخسارة
- **معدل الفوز**: نسبة الجولات الرابحة
- **أكبر ربح/خسارة**: أعلى مكسب وخسارة في جولة واحدة

## ⚠️ تحذيرات مهمة

### المحاكاة الكاملة:
- **الوقت**: 80+ ساعة للمحاكاة الكاملة
- **المساحة**: عدة GB للنتائج النهائية
- **الاستهلاك**: عالي للمعالج والذاكرة

### نصائح للأداء الأمثل:
1. أغلق البرامج الأخرى أثناء المحاكاة
2. تأكد من الطاقة (شاحن متصل للابتوب)
3. استخدم فترة حفظ قصيرة (10 تركيبات)
4. لا تغلق البرنامج أثناء رسالة "جاري الحفظ"

## 🔧 استكشاف الأخطاء

### مشاكل شائعة:

#### **"Python is not recognized"** (للكود):
```bash
# تأكد من تثبيت Python مع PATH
python --version
pip install -r requirements.txt
```

#### **"No module named 'pandas'"**:
```bash
pip install pandas openpyxl matplotlib
```

#### **البرنامج لا يستجيب**:
1. اضغط زر "إيقاف نهائي"
2. انتظر رسالة "جاري الحفظ"
3. أعد تشغيل البرنامج للاستئناف

#### **تحذير أمني (Windows)**:
- اختر "تشغيل على أي حال" أو "More info" → "Run anyway"
- أضف البرنامج لاستثناءات مكافح الفيروسات

## 🏗️ البناء التلقائي

يتم بناء ملف .exe تلقائياً باستخدام GitHub Actions عند كل push:

1. **الكود يُرفع** → GitHub Actions يبدأ تلقائياً
2. **البناء على Windows** → PyInstaller ينشئ ملف .exe
3. **الاختبار والتحقق** → فحص سلامة الملف
4. **الرفع كـ Artifact** → متاح للتحميل فوراً

### لبناء إصدار جديد:
1. ادفع الكود إلى `main` branch
2. اذهب إلى Actions tab
3. انتظر انتهاء البناء (~10 دقائق)
4. حمل الـ Artifact من صفحة الـ workflow

## 📁 هيكل المشروع

```
crazy-time-simulator/
├── 🐍 full_crazy_time_simulator.py    # المحاكي الأساسي
├── 🖥️ crazy_time_gui.py              # الواجهة الرسومية
├── ▶️ run_gui.py                      # مشغل الواجهة
├── 📦 requirements.txt                # المكتبات المطلوبة
├── 📖 README.md                       # هذا الملف
└── 🔧 .github/workflows/
    └── build-exe.yml                  # GitHub Actions للبناء التلقائي
```

## 🤝 المساهمة

### للمطورين:
1. Fork المشروع
2. أنشئ branch جديد (`git checkout -b feature/amazing-feature`)
3. Commit التغييرات (`git commit -m 'Add amazing feature'`)
4. Push إلى Branch (`git push origin feature/amazing-feature`)
5. افتح Pull Request

### للمستخدمين:
- أبلغ عن الأخطاء في Issues
- اقترح مميزات جديدة
- شارك تجربتك ونتائجك

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - انظر ملف [LICENSE](LICENSE) للتفاصيل.

## 🙏 شكر وتقدير

- **Wizard of Odds** - للبيانات الرسمية لمتوسطات الأرباح
- **Edward Thorp** - للأسس الرياضية لنظريات القمار
- **مجتمع Python** - للمكتبات الرائعة المستخدمة

---

## 🎰 English Version

# Crazy Time Simulator

A comprehensive and advanced simulator for the Crazy Time game with GUI and precise mathematical analysis.

## 🚀 Quick Download

### For Regular Users:
1. Go to [Releases](../../releases)
2. Download latest `CrazyTimeSimulator-Windows.zip`
3. Extract and run `CrazyTimeSimulator.exe`

### For Developers:
```bash
git clone https://github.com/YOUR_USERNAME/crazy-time-simulator.git
cd crazy-time-simulator
pip install -r requirements.txt
python run_gui.py
```

## ✨ Features

- 🖥️ **Advanced GUI** - Full control and easy to use
- 🎯 **Complete Simulation** - All possibilities (3+ million combinations)
- 💾 **Auto-Save** - Never lose progress
- ⏸️ **Pause/Resume** - Full simulation control
- 📊 **Live Statistics** - Real-time progress monitoring
- 📈 **Detailed Excel Results** - Comprehensive analysis
- 🛡️ **Freeze Protection** - Safe stopping anytime
- ⚙️ **Customizable Settings** - Control all parameters

## 📋 System Requirements

### For Executable (.exe):
- **Windows 7/8/10/11** (64-bit)
- **4 GB RAM** minimum
- **2 GB space** for program + 5 GB for results

### For Running from Code:
- **Python 3.7+**
- **Libraries**: pandas, openpyxl, tkinter, matplotlib

## 🎮 How to Use

### 1. Run Program
- **Windows**: Run `CrazyTimeSimulator.exe`
- **From Code**: `python run_gui.py`

### 2. Customize Settings
- **Initial Balance**: Starting amount (default: $300)
- **Minimum Threshold**: Stop amount (default: $100)
- **Trials per Combination**: Number of rounds (default: 1000)
- **Bet Range**: From $0 to $20

### 3. Start Simulation
- Click **"🚀 Start Simulation"**
- Monitor progress in live statistics
- Use **"⏸️ Pause"** or **"⏹️ Stop"** as needed

### 4. Review Results
- Results auto-saved to `crazy_time_full_results.xlsx`
- 3 sheets: All Results, Top 100, Statistical Summary

## 📊 Understanding Results

### Excel Sheets:
1. **All Results**: Every tested combination with details
2. **Top Results**: Best 100 combinations by profitability
3. **Statistical Summary**: Comprehensive stats and success rates

### Important Metrics:
- **Final Balance**: Amount after 1000 rounds
- **Profit Percentage**: Profit/loss percentage
- **Win Rate**: Percentage of winning rounds
- **Max Win/Loss**: Highest gain and loss in single round

## ⚠️ Important Warnings

### Full Simulation:
- **Time**: 80+ hours for complete simulation
- **Storage**: Several GB for final results
- **Usage**: High CPU and memory consumption

### Performance Tips:
1. Close other programs during simulation
2. Ensure power supply (laptop charger)
3. Use short save intervals (10 combinations)
4. Don't close during "Saving..." message

## 🔧 Troubleshooting

### Common Issues:

#### **"Python is not recognized"** (for code):
```bash
# Ensure Python installed with PATH
python --version
pip install -r requirements.txt
```

#### **"No module named 'pandas'"**:
```bash
pip install pandas openpyxl matplotlib
```

#### **Program not responding**:
1. Click "Stop" button
2. Wait for "Saving..." message
3. Restart program to resume

#### **Security warning (Windows)**:
- Choose "Run anyway" or "More info" → "Run anyway"
- Add program to antivirus exceptions

## 🏗️ Automated Building

EXE file is built automatically using GitHub Actions on every push:

1. **Code pushed** → GitHub Actions starts automatically
2. **Build on Windows** → PyInstaller creates .exe
3. **Test & Verify** → File integrity check
4. **Upload as Artifact** → Available for download immediately

### To build new release:
1. Push code to `main` branch
2. Go to Actions tab
3. Wait for build completion (~10 minutes)
4. Download Artifact from workflow page

## 📁 Project Structure

```
crazy-time-simulator/
├── 🐍 full_crazy_time_simulator.py    # Core simulator
├── 🖥️ crazy_time_gui.py              # GUI interface
├── ▶️ run_gui.py                      # GUI launcher
├── 📦 requirements.txt                # Required libraries
├── 📖 README.md                       # This file
└── 🔧 .github/workflows/
    └── build-exe.yml                  # GitHub Actions for auto-build
```

## 🤝 Contributing

### For Developers:
1. Fork the project
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### For Users:
- Report bugs in Issues
- Suggest new features
- Share your experience and results

## 📄 License

This project is licensed under MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Wizard of Odds** - For official bonus multiplier data
- **Edward Thorp** - For mathematical foundations of gambling theory
- **Python Community** - For excellent libraries used

---

**🎰 استمتع بأكثر محاكي Crazy Time تقدماً! | Enjoy the most advanced Crazy Time Simulator!**

#   c r a z y - t i m e - s i m u l a t o r  
 