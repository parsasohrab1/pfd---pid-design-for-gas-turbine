# pfd---pid-design-for-gas-turbine
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


