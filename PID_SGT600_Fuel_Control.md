عنوان: P&ID — مدار سوخت و عملگر کنترل ولو (Siemens SGT600/IGT25)

دامنه
- نمایش لاین‌ها، ولوها، ابزار دقیق، حلقه‌های کنترلی، اینترفیس‌های الکتریکال/ESD و تگینگ نمونه برای جایگزینی/پیاده‌سازی عملگر کنترل ولو خطوط Primary و Main و ادغام به هدر مشترک توربین.

استانداردها و نمادگذاری
- ISA-5.1 برای نمادگذاری ابزار دقیق و تگینگ
- IEC 61511/61508 برای SIS/SIL (هدف SIL2 برای SIFهای منتخب)
- IEC 60079 برای حفاظت انفجاری (Ex) تجهیزات
- API 6D/598 برای تست ولوها (در صورت کاربرد)

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

  %% Primary Line
  PR_LINE --> BYP_PR[Service/Bypass (if any)]
  PR_LINE --> XV_PR[SDV/ESD-PR-001]
  XV_PR --> FT_PR((FT-PR-010))
  FT_PR --> FCV_PR[FCV-PR-101\nControl Valve + Actuator (Ex)]
  FCV_PR --> PSV_PR[PSV-PR-001 (if req.)]
  PSV_PR --> HDR[Mixing Header]

  %% Main Line
  MN_LINE --> BYP_MN[Service/Bypass (if any)]
  MN_LINE --> XV_MN[SDV/ESD-MN-001]
  XV_MN --> FT_MN((FT-MN-020))
  FT_MN --> FCV_MN[FCV-MN-201\nControl Valve + Actuator (Ex)]
  FCV_MN --> PSV_MN[PSV-MN-001 (if req.)]
  PSV_MN --> HDR

  HDR --> PT2((PT-002))
  HDR --> GT[Turbine Combustion System]

  %% Control & Safety
  subgraph Control & Safety
    PLC[PLC/TGC]
    SIS[SIS/ESD SIL2]
    AO1[[AO 4-20 mA / Fieldbus]]
    DO1[[DO Trip/Close]]
    DI1[[DI Status/Limits]]
  end

  AO1 -.-> FCV_PR
  AO1 -.-> FCV_MN
  DO1 -.-> XV_PR
  DO1 -.-> XV_MN
  PT1 -.-> PLC
  FT_PR -.-> PLC
  FT_MN -.-> PLC
  PT2 -.-> PLC
  DI1 -.-> PLC
  SIS -.-> DO1
```

نمودار P&ID (Mermaid — جزئیات عملگر، SOV و لیمیت‌سوئیچ‌ها)

```mermaid
flowchart LR
  subgraph Primary Details
    FT_PR((FT-PR-010)) --> FCV_PR[FCV-PR-101]
    FCV_PR --> POS_PR((Positioner))
    POS_PR --- FB_PR1((LS Open))
    POS_PR --- FB_PR2((LS Close))
    SV_PR[SOV-PR-1 (Fail Close)] -. Pneumatic .-> FCV_PR
    DO_SIS_PR[[SIS DO Trip]] -.-> SV_PR
  end

  subgraph Main Details
    FT_MN((FT-MN-020)) --> FCV_MN[FCV-MN-201]
    FCV_MN --> POS_MN((Positioner))
    POS_MN --- FB_MN1((LS Open))
    POS_MN --- FB_MN2((LS Close))
    SV_MN[SOV-MN-1 (Fail Close)] -. Pneumatic .-> FCV_MN
    DO_SIS_MN[[SIS DO Trip]] -.-> SV_MN
  end

  FB_PR1 -.-> PLC
  FB_PR2 -.-> PLC
  FB_MN1 -.-> PLC
  FB_MN2 -.-> PLC
```

تگینگ نمونه
- FCV-PR-101، FCV-MN-201 — کنترل ولو + Actuator (Ex) برای خطوط Primary/Main
- FT-PR-010، FT-MN-020 — فلوترانسمیتر هر خط (روش اندازه‌گیری مطابق انتخاب: اوریفیس، کوریولیس، آلتراسونیک)
- PT-001 (Upstream/KO Outlet)، PT-002 (Header) — پرشر ترانسمیترها
- SDV/ESD-PR-001، SDV/ESD-MN-001 — ولو قطع اضطراری فرمان‌پذیر از SIS
- PSV-PR-001، PSV-MN-001 — ولو اطمینان در صورت نیاز (مطابق مطالعات Overpressure)

حلقه‌های کنترلی (نمونه)
- FIC-PR-101: کنترل فلو خط Primary با خروجی AO به FCV-PR-101 (سیگنال 4–20 mA یا Fieldbus)
- FIC-MN-201: کنترل فلو خط Main با خروجی AO به FCV-MN-201
- PT-001/002 جهت Interlock فشار، ارسال به PLC و منطق‌های حفاظتی
- SDVها فرمان‌پذیر از SIS؛ در شرایط Trip → Close

فلسفه ایمنی و SIF (پیشنهادی، هدف SIL2)
- SIF-1: Header High-High Pressure (PT-002 HH) → Close SDVها (PR/MN) و فرمان Close به FCVها
- SIF-2: Upstream High-High Pressure (PT-001 HH) → همانند بالا (در صورت تایید HAZOP/LOPA)
- حالت ایمن: Fail Close برای FCV و SDV
- Proof Test: برنامه آزمون‌پذیری ادواری با بای‌پس امن و مجوز بهره‌بردار

اینترفیس‌های الکتریکال (خلاصه)
- تغذیه عملگرها: 24 VDC/110 VAC/400 VAC (طبق انتخاب عملگر) با گواهی Ex و IP مناسب
- سیگنال‌ها: آنالوگ 4–20 mA یا Fieldbus (HART/Profibus/Profinet) مطابق PLC/TGC موجود
- کابلینگ: زوج‌تابیده/شیلددار، زمین‌مرجع، JB/Marshall در Zone مناسب، گلند Ex

I/O List (پیش‌نویس برای ادغام با PLC/TGC)
- Analog In (AI): PT-001، PT-002، FT-PR-010، FT-MN-020
- Analog Out (AO): FCV-PR-101 (Command/Position)، FCV-MN-201 (Command/Position)
- Digital Out (DO): SDV/ESD-PR-001 (Close/Open)، SDV/ESD-MN-001 (Close/Open)
- Digital In (DI): Limit Switches (Open/Close)، Trip Status، ESD Status، Faults

I/O تخصیص به PLC/SIS (پیشنهادی)
- PLC-AI: PT-001، PT-002، FT-PR-010، FT-MN-020
- PLC-AO: FCV-PR-101 CMD، FCV-MN-201 CMD
- PLC-DI: LS-PR-OPEN، LS-PR-CLOSE، LS-MN-OPEN، LS-MN-CLOSE، Trip Status
- SIS-DO: SDV-PR-001 CLOSE/OPEN، SDV-MN-001 CLOSE/OPEN، SOV-PR-1 TRIP، SOV-MN-1 TRIP

کابلینگ و مارshalling (پیش‌نویس)
- JB-Zone: Junction Box Exe در Zone مناسب برای هر خط
- کابل ابزار: زوج‌تابیده شیلددار 1.5 mm² برای آنالوگ؛ 1.5–2.5 mm² برای دیجیتال/فرمان
- گلند: Exe/Exd مطابق تجهیز
- مارشالینگ: تخصیص ترمینال TB-### در مارشال پانل؛ شماره‌گذاری همروند با I/O

Line List (Draft)
- L-PR-001: Primary Fuel Line — کلاس فلنج ASME (Site Data)، سایز NPS (Site Data)
- L-MN-001: Main Fuel Line — کلاس فلنج ASME (Site Data)، سایز NPS (Site Data)
- L-HDR-001: Mixing Header به GT — کلاس و سایز (Site Data)

Valve Data (Placeholders)
- FCV-PR-101: Size/Rating، Body/Trim، Characteristic (Linear/Equal%)، Leakage Class، Cv
- FCV-MN-201: Size/Rating، Body/Trim، Characteristic، Leakage Class، Cv
- SDV-PR-001 / SDV-MN-001: نوع (Ball/Plug/Gate)، Actuation (Solenoid/Pneumatic)، Fail Action
- PSV-PR-001 / PSV-MN-001: Set Pressure، Orifice، استاندارد API

Setpoints و Limits (Placeholders)
- PT-002 HH: Header Pressure Trip → فرمان Close SDVها و SOV Trip
- PT-001 HH: Upstream Protection (در صورت تایید) → فرمان Close
- Min Flow Limits: برای پایداری احتراق/حفاظت عملگرها

Cause & Effect (خلاصه)
- Cause: PT-002 = HH → Effect: SDV-PR-001 Close، SDV-MN-001 Close، SOV-PR/MN Trip، GT Fuel Shut
- Cause: ESD Pushbutton → Effect: همانند بالا با لاجیک SIS
- Cause: LS Mismatch (Valve command Close ولی Feedback Open) → Effect: Alarm + Action per philosophy

Logic Narrative (خلاصه)
- فرمان AO از PLC به Positioner برای FCVها، با Feedback Position/Status به PLC
- فرمان‌های Trip/Close برای SDVها و SOVها از SIS (اولویت ایمنی)
- Interlockها بر اساس PT-001/002 و شرایط GT؛ Override/Bypass مطابق مجوز بهره‌بردار و روش تست

حوزه خطر (Hazardous Area)
- تجهیزات ابزاردقیق و عملگرها با گواهی Ex (ATEX/IECEx)، دسته‌بندی Zone 1/2 مطابق طبقه‌بندی سایت
- رعایت زمین‌مرجع و حفاظت در برابر صاعقه طبق استاندارد سایت

داده‌های تکمیلی موردنیاز (برای نهایی‌سازی)
- Cv محاسباتی هر FCV و انتخاب Trim/Characteristic (Linear/Equal%)
- سرعت عملگر، گشتاور/نیرو، زمان بسته/باز شدن و تست‌های On/Off/Partial Stroke (در صورت نیاز)
- روش اندازه‌گیری فلو و کلاس دقت ابزار (معیار کالیبراسیون/Ex)
- سایزینگ لاین‌ها، کلاس فلنج‌ها، متریال، و الزامات تست/باگاه
- منطق‌های Interlock/Shutdown با اشاره به Cause & Effect و نتایج HAZOP/LOPA

یادداشت‌ها
- نمادها و تگ‌ها نمونه‌اند و براساس استاندارد کارفرما/سایت به‌روزرسانی خواهند شد.
- جایگذاری PSVها، هات-بای‌پس و سایزینگ نهایی پس از دریافت دیتای فرآیندی نهایی تثبیت می‌شود.

تغییرات نسخه
- v0.2: افزودن دیاگرام جزئیات عملگر/Positioner/SOV/لیمیت‌سوئیچ‌ها، جداول I/O تخصیص، Line List، Valve Data، Setpoints، C&E خلاصه و Logic Narrative
- v0.1: نسخه ساده اولیه


