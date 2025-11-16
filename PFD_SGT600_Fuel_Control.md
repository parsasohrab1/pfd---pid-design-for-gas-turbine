عنوان: PFD — مدار سوخت و عملگر کنترل ولو (Siemens SGT600/IGT25)

دامنه
- نمایش جریان فرآیندی سوخت گاز طبیعی، نقاط اندازه‌گیری کلیدی، واحدهای پیش‌تصفیه/شرایط‌دهی و جایگاه عملگرهای کنترل ولو برای خطوط Primary و Main با ادغام در هدر مشترک به سمت سامانه احتراق توربین.

فرضیات طراحی (نسخه آماده برای شروع مهندسی)
- سوخت: گاز طبیعی خشک، بازه فشار ورودی 20–70 barg، دما 0–60°C
- دو مسیر سوخت Primary و Main با بای‌پس‌های سرویس/ایمن (در سطح PFD نمایش مفهومی)
- حالت ایمن: Fail Close برای کنترل ولوها و SDVها
- گواهی Ex برای عملگرها و ادوات ابزار دقیق متناسب با Zone 1/2
- استاندارد نمادگذاری: ISA-5.1 (برای پیوست با P&ID)

نسخه و محدوده
- نسخه: v0.2 — آماده ارائه برای Concept/FEED
- محدوده: از ورودی سوخت واحد تا هدر اختلاط ورودی سامانه احتراق توربین (Downstream جزئیات نازل‌ها خارج از محدوده PFD)

نمودار جریان فرآیند — سطح 1 (Mermaid)

```mermaid
flowchart LR
    A[Fuel Gas Supply\n(20–70 barg, 0–60°C)] --> F1[Filter/Coalescer]
    F1 --> KO[KO Drum / Separator]
    KO --> C[Conditioning/Heater\n(if required)]

    C --> TEE1{Split}
    TEE1 -->|Primary Line| P1[Primary Fuel Line]
    TEE1 -->|Main Line| M1[Main Fuel Line]

    %% Control Valves
    P1 --> FCV_P[Fuel Control Valve (Primary)\nActuator (Ex)]
    M1 --> FCV_M[Fuel Control Valve (Main)\nActuator (Ex)]

    %% Measurements (Conceptual)
    subgraph Measurements
      FT[FT/FE — Flow]
      PT[PT — Pressure]
      TT[TT — Temperature]
    end

    F1 --- PT
    KO --- TT
    P1 --- FT
    M1 --- FT

    %% Merge to Header
    FCV_P --> MIX[Mixing Header]
    FCV_M --> MIX
    MIX --> T[GT Combustion System (SGT600/IGT25)]
```

نمودار جریان فرآیند — سطح 2 (با بای‌پس و SDV مفهومی)

```mermaid
flowchart LR
    IN[Fuel Gas Inlet] --> F1[Filter/Coalescer]
    F1 --> KO[KO Drum]
    KO --> HEAT[Conditioning/Heater (if req.)]
    HEAT --> SPLIT{TEE}

    SPLIT --> P_LINE[Primary Line]
    SPLIT --> M_LINE[Main Line]

    %% Primary branch
    subgraph Primary Branch
      P_LINE --> BYP_P[Service Bypass (if any)]
      P_LINE --> SDV_P[SDV-PR-001 (Trip Close)]
      SDV_P --> FT_P((FT-PR-010))
      FT_P --> FCV_P[FCV-PR-101 + Actuator (Ex)]
      FCV_P --> HDR[Mixing Header]
    end

    %% Main branch
    subgraph Main Branch
      M_LINE --> BYP_M[Service Bypass (if any)]
      M_LINE --> SDV_M[SDV-MN-001 (Trip Close)]
      SDV_M --> FT_M((FT-MN-020))
      FT_M --> FCV_M[FCV-MN-201 + Actuator (Ex)]
      FCV_M --> HDR
    end

    %% Measurements
    KO --- TT1((TT-001))
    F1 --- PT1((PT-001))
    HDR --- PT2((PT-002))

    HDR --> GT[Turbine Combustion System]
```

اقلام اصلی PFD
- واحد فیلتراسیون/کوآلسر جهت حذف مایعات/ذرات
- درام ضربه/جداکننده (KO Drum) برای محافظت از ولوها و احتراق
- Heater/Conditioning در صورت نیاز فرآیندی (چگالی/نقطه شبنم/یخ‌زدگی)
- انشعاب Primary/Main، کنترل ولوهای عملگر‌دار و ادغام به هدر مشترک
- ابزارهای FT/PT/TT در نقاط کلیدی

جریان‌ها (Streams) — پیش‌نویس
- S-001: Fuel Gas Inlet — فشار 20–70 barg، دما 0–60°C، ترکیب: گاز طبیعی (Site Data)
- S-010: پس از فیلتر/کوآلسر — فشار/افت فشار ΔP_FC (Site Data)
- S-020: خروجی KO Drum — دمای اندازه‌گیری TT-001
- S-030: Primary Upstream FCV — اندازه‌گیری FT-PR-010
- S-040: Main Upstream FCV — اندازه‌گیری FT-MN-020
- S-100: Mixing Header به سمت GT — فشار PT-002، شرایط Combustion Feed

فهرست تجهیزات (Draft)
- F1: Filter/Coalescer — کلاس/اندازه/ΔP مجاز (Site Data)
- KO: Knock-out Drum — حجم/Retention، اتصال Drain/Instrumentation
- HEAT: Heater/Conditioning — Duty، Utility، کنترل دما (اختیاری)
- FCV-PR-101 / FCV-MN-201: کنترل ولوهای هر خط — Trim/Characteristic، Leakage Class
- SDV-PR-001 / SDV-MN-001: ولوهای قطع اضطراری (Trip Close)
- HDR: هدر اختلاط — کلاس فلنج و سایز

فهرست اندازه‌گیری‌ها (Draft)
- PT-001: فشار پس از فیلتر/کوآلسر (حفاظت/مانیتورینگ)
- TT-001: دمای پس از KO Drum
- FT-PR-010: فلو خط Primary (اندازه‌گیری برای کنترل/مانیتورینگ)
- FT-MN-020: فلو خط Main
- PT-002: فشار هدر اختلاط (Interlock/Monitoring)

سناریوهای بهره‌برداری (Operating Cases)
- Start-up / Light-off: استفاده از Primary، محدودیت Ramp/Rate مطابق کنترلر
- Base-load: استفاده از هر دو خط، تقسیم فلو طبق فلسفه کنترلی
- Part-load / Turndown: تنظیم Cv موثر و حفظ پایداری احتراق
- Trip/ESD: بستن SDVها و فرمان Close به FCVها (Fail Close)

داده‌های طراحی (جای‌گیر — تکمیل با داده‌های سایت)
- دبی نامی در 100% بار: طبق دیتاشیت توربین (لازم به درج مقدار واقعی)
- محدوده TurnDown دبی هر خط: Min … Max (تعیین Cv و مشخصات Trim)
- فشار ورودی/خروجی و افت فشار مجاز واحدهای پیش‌تصفیه
- نیازمندی Heater (Duty، دمای هدف، Utility و کنترل)
- کلاس فلنج‌ها و کلاس تست مطابق استاندارد کارفرما

یادداشت‌ها
- مقادیر نهایی فلو/فشار/دما و سایزینگ تجهیزات با داده‌های واقعی سایت و تایید کارفرما به‌روزرسانی شود.
- فلسفه ایمنی Fail Close برای مسیرهای Primary و Main در نظر گرفته شده است.
- برای جزئیات تگینگ، حلقه‌های کنترلی، اینترفیس‌های ESD و I/O به سند P&ID مراجعه شود.

تغییرات نسخه
- v0.2: افزودن دیاگرام سطح 2 (بای‌پس/SDV)، جداول Streams/Equipment/Measurements و سناریوهای بهره‌برداری
- v0.1: نسخه اولیه سطح 1 مطابق README


