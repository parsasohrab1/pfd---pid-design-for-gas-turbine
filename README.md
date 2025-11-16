عنوان: بسته اولیه PFD و P&ID — سامانه عملگر و کنترل ولو سوخت توربین زیمنس SGT600/IGT25 (جایگزین Heinzmann)

شرح کوتاه
این بسته حاوی پیش‌نویس‌های اولیه PFD و P&ID برای مدار سوخت (Main & Primary) با تمرکز بر عملگر کنترل ولو و متعلقات الکتریکال/ابزاردقیق جهت نصب بر روی توربین‌های زیمنس SGT600/IGT25 است. این نسخه برای شروع مهندسی (Class-Concept/FEED) تهیه شده و نیازمند تکمیل داده‌های فرآیندی و اینترفیس‌ها است.

فرضیات کلیدی (برای نسخه اولیه)
- سوخت: گاز طبیعی خشک، بازه فشار 20–70 barg (ASME Class تناسبی با سایت)، دمای 0–60°C
- دو مسیر سوخت Primary و Main با بای‌پس‌های سرویس/ایمن
- عملگر کنترل ولو الکتریکی/الکتروهیدرولیک (با گواهی Ex d/Ex e یا معادل)
- حلقه کنترلی سرعت/بار از PLC/ترباین کنترلر موجود (TGC)، استاندارد سیگنال 4–20 mA یا Fieldbus
- سطح SIL هدف برای حلقه ESD: SIL2 (طبق IEC 61511/61508 — نیاز به تایید کارفرما)
- مناطق خطر: Zone 1 یا Zone 2 (تایید ATEX/IECEx تجهیزات ابزاردقیق و درایوها)

استانداردهای مرجع
- IEC 60534 (کنترل ولوها)، IEC 61800 (درایوها)، ISO 6336 و AGMA 2001 (چرخ‌دنده — در صورت وجود در عملگر)
- API 6D/598 برای تست ولوها (در صورت کاربرد)، ISA-5.1 برای نمادگذاری و تگینگ
- IEC 60079 (Ex)، IEC 61511/61508 (SIS/SIL) — برای طراحی نهایی ایمنی

اقلام موجود در بسته
- PFD_SGT600_Fuel_Control.md — نمودار جریان فرآیند (Mermaid)
- PID_SGT600_Fuel_Control.md — نمودار لوله‌کشی و ابزار دقیق (Mermaid + لیست‌ها)

چک‌لیست داده‌های لازم جهت نهایی‌سازی
1) شرایط فرآیندی
   - فشار/دبی/دمای ورودی و خروجی سوخت (Min/Norm/Max)
   - کلاس فلنج‌ها، MOP، PSV set-pointها (در صورت وجود)
   - خورندگی/آلودگی، فیلتراسیون موردنیاز
2) مشخصات ولو و عملگر
   - Cv موردنیاز، Linear/Equal%, Seat/Trim، Leakage Class، Fail Action
   - نوع عملگر (الکتریکی/الکتروهیدرولیک)، زمان حرکت، گشتاور/نیروی لازم، حفاظت Ex و IP
   - نیاز به ESD مستقل و موقعیت Fail (Close/Open/Last)
3) ابزاردقیق و کنترل
   - سنسورها (PT/TT/FT/DP) و کلاس دقت/Ex، موقعیت نصب
   - سیگنال‌های I/O (آنالوگ/دیجیتال/فیلدباس)، منبع تغذیه، کابلیگ
   - فلسفه کنترلی (Speed/Load/Pressure control) و interlockها
4) الزامات ایمنی و SIL
   - SIFها، آزمون‌پذیری، نفرین/اثرات مد شکست، پوشش تست‌های Proof
5) مکانیک و پایپینگ
   - متریال لاین‌ها، سایزینگ لاین‌ها، کلاس عایق/تکیه‌گاه
   - اسپولهای جدید/تغییرات و فضای نصب/دسترسی
6) اسناد و الزامات سایت
   - Zone Classification، کابل‌رِوت‌ها، Junction Box/Marshall
   - استانداردهای کارفرما برای تگینگ، رنگ، لایه‌بندی نقشه

توجه
این اسناد پیش‌نویس مفهومی هستند و برای تولید/ساخت نهایی، نیازمند به‌روزرسانی با داده‌های واقعی سایت و تایید کارفرما می‌باشند. 





# pfd
design for production
عنوان: PFD — مدار سوخت و عملگر کنترل ولو (SGT600/IGT25)

هدف
نمایش ساده جریان فرآیند سوخت، نقاط اندازه‌گیری کلیدی و جایگاه عملگر کنترل ولو برای مسیرهای Primary و Main.

نمودار جریان فرآیند (Mermaid)

```mermaid
flowchart LR
    A[Fuel Gas Supply\n(20–70 barg)] --> F1[Filter/Coalescer]
    F1 --> KO[Knock-out / Separator]
    KO --> C[Conditioning/Heater\n(if required)]

    C --> TEE1{Split}
    TEE1 -->|Primary Line| P1[Piping Primary]
    TEE1 -->|Main Line| M1[Piping Main]

    P1 --> FCV_P[Fuel Control Valve\n(Primary) + Actuator (Ex)]
    M1 --> FCV_M[Fuel Control Valve\n(Main) + Actuator (Ex)]

    subgraph Measurements
      FT[FT/FE — Flow]
      PT[PT — Pressure]
      TT[TT — Temperature]
    end

    F1 --- PT
    KO --- TT
    P1 --- FT
    M1 --- FT

    FCV_P --> MIX[Mixing Header]
    FCV_M --> MIX
    MIX --> T[GTC/Turbine Combustion System]
```

جداول جریان و اندازه‌گیری‌ها (پیش‌نویس)
- جریان نامی: 100% بار — بر اساس دیتاشیت توربین (نیازمند داده واقعی)
- محدوده فلو: Min/TurnDown تا Max (تعیین Cv نهایی)
- نقاط اندازه‌گیری: Pressure upstream/downstream، Flow (per line)، Temperature

اقلام اصلی PFD
- واحد فیلتراسیون/کوآلسر برای حذف مایعات/ذرات
- جداکننده/درام ضربه برای محافظت از ولوها و احتراق
- Heater/Conditioning در صورت نیاز (دما/چگالی)
- انشعاب Primary/Main، ولوهای کنترل (Actuated) و ادغام به هدر مختلط
- ابزارهای FT/PT/TT در نقاط کلیدی

یادداشت‌ها
- مقادیر دقیق فلو/فشار/دما و انتخاب Heater اختیاری است و با داده‌های سایت جایگزین می‌شود.
- فلسفه خاموشی ایمن (Fail Close روی هر دو خط) در نسخه اولیه فرض شده است.


PID
عنوان: P&ID — مدار سوخت و عملگر کنترل ولو (SGT600/IGT25)

هدف
نمایش لاین‌ها، ولوها، ابزار دقیق، حلقه‌های کنترلی و اینترفیس‌های الکتریکال/ESD برای جایگزینی عملگر ولوهای Heinzmann.

نمادگذاری و لایه‌بندی (مختصر)
- استاندارد نماد: ISA-5.1
- تگینگ نمونه: FCV-PR-101 (Primary)، FCV-MN-201 (Main)
- رنگ/لایه: مطابق استاندارد کارفرما (به‌روزرسانی پس از دریافت)

نمودار P&ID (Mermaid — شماتیک ساده)

```mermaid
flowchart LR
  subgraph Fuel Supply
    S[Fuel Gas Inlet] --> F1[Filter/Coalescer]
    F1 --> KO[KO Drum]
  end

  KO --> PT1((PT-001))
  KO --> TT1((TT-001))

  KO --> SPLIT{TEE to Primary/Main}
  SPLIT --> PR_LINE[Primary Line]
  SPLIT --> MN_LINE[Main Line]

  %% Primary
  PR_LINE --> XV_PR[SDV/ESD-PR-001]
  XV_PR --> FT_PR((FT-PR-010))
  FT_PR --> FCV_PR[FCV-PR-101\nControl Valve + Actuator (Ex)]
  FCV_PR --> PSV_PR[PSV/Relief (if req.)]
  PSV_PR --> HDR[Mixing Header]

  %% Main
  MN_LINE --> XV_MN[SDV/ESD-MN-001]
  XV_MN --> FT_MN((FT-MN-020))
  FT_MN --> FCV_MN[FCV-MN-201\nControl Valve + Actuator (Ex)]
  FCV_MN --> PSV_MN[PSV/Relief (if req.)]
  PSV_MN --> HDR

  HDR --> PT2((PT-002))
  HDR --> GT[Turbine Combustion System]

  %% Control System
  subgraph Control & Safety
    PLC[PLC/TGC]
    SIS[SIS/ESD SIL2]
    AO1[[AO 4-20 mA / Fieldbus]]
    DO1[[DO Trip/Close]]
  end

  AO1 -.-> FCV_PR
  AO1 -.-> FCV_MN
  DO1 -.-> XV_PR
  DO1 -.-> XV_MN
  PT1 -.-> PLC
  FT_PR -.-> PLC
  FT_MN -.-> PLC
  PT2 -.-> PLC
  SIS -.-> DO1
```

حلقه‌های کنترلی (نمونه)
- LIC/FIC-PR-101: کنترل فلو خط Primary برای کنترل سرعت/بار — خروجی به عملگر FCV-PR-101
- LIC/FIC-MN-201: کنترل فلو خط Main — خروجی به عملگر FCV-MN-201
- PT-001/002 برای Interlock و حفاظت‌های فشار
- SDV/ESD-PR-001 و SDV/ESD-MN-001 فرمان‌پذیر از SIS (Trip → Close)

فلسفه ایمنی (پیش‌نویس)
- حالت ایمن: Fail Close برای FCVها و SDVها
- SIF نمونه: High-High Pressure at Header → Trip SDVها و فرمان Close FCVها (SIL2 هدف)
- تست‌پذیری ادواری (Proof Test) و بای‌پس امن با مجوز بهره‌بردار

اینترفیس‌های الکتریکال (خلاصه)
- تغذیه عملگرها: 24 VDC/110 VAC/400 VAC (طبق انتخاب عملگر) — با گواهی Ex و IP مناسب
- سیگنال‌ها: آنالوگ 4–20 mA یا Fieldbus (HART/Profibus/Profinet) طبق PLC موجود
- کابلینگ: شیلددار/زوج‌تابیده، زمین‌مرجع، JB/Marshall در Zone مناسب، گلند Ex

فهرست تگ‌های نمونه (Partial Tag List)
- FCV-PR-101، FCV-MN-201 — کنترل ولو + Actuator (Ex)
- FT-PR-010، FT-MN-020 — فلو ترانسمیتر
- PT-001 (Upstream)، PT-002 (Header) — پرشر ترانسمیتر
- SDV/ESD-PR-001، SDV/ESD-MN-001 — ولو قطع اضطراری
- PSV-PR-001، PSV-MN-001 — ولو اطمینان (در صورت نیاز)

I/O List (پیش‌نویس)
- آنالوگ ورودی: PT-001، PT-002، FT-PR-010، FT-MN-020
- آنالوگ خروجی: FCV-PR-101 (Position/Command)، FCV-MN-201 (Position/Command)
- دیجیتال خروجی: SDV/ESD-PR-001 (Close/Open)، SDV/ESD-MN-001 (Close/Open)
- دیجیتال ورودی: Limit Switches، Trip Status، ESD Status

یادداشت‌ها
- نمادها و تگ‌ها نمونه‌اند و با استاندارد کارفرما/سایت تطبیق داده خواهند شد.
- جایگذاری PSVها، هات-بای‌پس و اندازه سایزینگ لاین‌ها پس از دریافت دیتای فرآیندی نهایی می‌شود.



