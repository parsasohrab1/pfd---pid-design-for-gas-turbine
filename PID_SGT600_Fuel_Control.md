Title: P&ID — Fuel Circuit and Control Valve Actuator (Siemens SGT600/IGT25)

Scope
- Shows lines, valves, instrumentation, control loops, electrical/ESD interfaces and sample tagging for replacing/implementing the control valve actuator of the Primary and Main lines and merging into the turbine common header.

Standards and symbols
- ISA-5.1 for instrumentation symbols and tagging
- IEC 61511/61508 for SIS/SIL (SIL2 target for selected SIFs)
- IEC 60079 for explosion protection (Ex) of equipment
- API 6D/598 for valve testing (where applicable)

P&ID Diagram (Mermaid — simple schematic)

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

P&ID Diagram (Mermaid — actuator, SOV and limit switch details)

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

Sample tagging
- FCV-PR-101, FCV-MN-201 — control valve + Actuator (Ex) for the Primary/Main lines
- FT-PR-010, FT-MN-020 — flow transmitter of each line (measurement method per selection: orifice, Coriolis, ultrasonic)
- PT-001 (Upstream/KO Outlet), PT-002 (Header) — pressure transmitters
- SDV/ESD-PR-001, SDV/ESD-MN-001 — emergency shutdown valve commandable from the SIS
- PSV-PR-001, PSV-MN-001 — relief valve if needed (per Overpressure studies)

Control loops (sample)
- FIC-PR-101: Primary line flow control with AO output to FCV-PR-101 (4–20 mA signal or Fieldbus)
- FIC-MN-201: Main line flow control with AO output to FCV-MN-201
- PT-001/002 for pressure Interlock, sent to the PLC and protection logic
- SDVs commandable from the SIS; on Trip → Close

Safety philosophy and SIF (suggested, SIL2 target)
- SIF-1: Header High-High Pressure (PT-002 HH) → Close the SDVs (PR/MN) and Close command to the FCVs
- SIF-2: Upstream High-High Pressure (PT-001 HH) → same as above (if confirmed by HAZOP/LOPA)
- Safe state: Fail Close for FCV and SDV
- Proof Test: periodic testability program with a safe bypass and operator permit

Electrical interfaces (summary)
- Actuator power supply: 24 VDC/110 VAC/400 VAC (per actuator selection) with Ex certification and suitable IP
- Signals: analog 4–20 mA or Fieldbus (HART/Profibus/Profinet) per the existing PLC/TGC
- Cabling: twisted/shielded, reference ground, JB/Marshall in a suitable Zone, Ex gland

I/O List (draft for integration with PLC/TGC)
- Analog In (AI): PT-001, PT-002, FT-PR-010, FT-MN-020
- Analog Out (AO): FCV-PR-101 (Command/Position), FCV-MN-201 (Command/Position)
- Digital Out (DO): SDV/ESD-PR-001 (Close/Open), SDV/ESD-MN-001 (Close/Open)
- Digital In (DI): Limit Switches (Open/Close), Trip Status, ESD Status, Faults

I/O assignment to PLC/SIS (suggested)
- PLC-AI: PT-001, PT-002, FT-PR-010, FT-MN-020
- PLC-AO: FCV-PR-101 CMD, FCV-MN-201 CMD
- PLC-DI: LS-PR-OPEN, LS-PR-CLOSE, LS-MN-OPEN, LS-MN-CLOSE, Trip Status
- SIS-DO: SDV-PR-001 CLOSE/OPEN, SDV-MN-001 CLOSE/OPEN, SOV-PR-1 TRIP, SOV-MN-1 TRIP

Cabling and marshalling (draft)
- JB-Zone: Exe Junction Box in a suitable Zone for each line
- Instrument cable: shielded twisted pair 1.5 mm² for analog; 1.5–2.5 mm² for digital/command
- Gland: Exe/Exd per the equipment
- Marshalling: terminal TB-### allocation in the marshalling panel; numbering consistent with I/O

Line List (Draft)
- L-PR-001: Primary Fuel Line — ASME flange class (Site Data), NPS size (Site Data)
- L-MN-001: Main Fuel Line — ASME flange class (Site Data), NPS size (Site Data)
- L-HDR-001: Mixing Header to GT — class and size (Site Data)

Valve Data (Placeholders)
- FCV-PR-101: Size/Rating, Body/Trim, Characteristic (Linear/Equal%), Leakage Class, Cv
- FCV-MN-201: Size/Rating, Body/Trim, Characteristic, Leakage Class, Cv
- SDV-PR-001 / SDV-MN-001: type (Ball/Plug/Gate), Actuation (Solenoid/Pneumatic), Fail Action
- PSV-PR-001 / PSV-MN-001: Set Pressure, Orifice, API standard

Setpoints and Limits (Placeholders)
- PT-002 HH: Header Pressure Trip → Close command to the SDVs and SOV Trip
- PT-001 HH: Upstream Protection (if confirmed) → Close command
- Min Flow Limits: for combustion stability/actuator protection

Cause & Effect (summary)
- Cause: PT-002 = HH → Effect: SDV-PR-001 Close, SDV-MN-001 Close, SOV-PR/MN Trip, GT Fuel Shut
- Cause: ESD Pushbutton → Effect: same as above with SIS logic
- Cause: LS Mismatch (valve command Close but feedback Open) → Effect: Alarm + Action per philosophy

Logic Narrative (summary)
- AO command from the PLC to the Positioner for the FCVs, with Position/Status feedback to the PLC
- Trip/Close commands for the SDVs and SOVs from the SIS (safety priority)
- Interlocks based on PT-001/002 and GT conditions; Override/Bypass per operator permit and test procedure

Hazardous Area
- Instrumentation and actuators with Ex certification (ATEX/IECEx), Zone 1/2 classification per site classification
- Compliance with reference grounding and lightning protection per the site standard

Supplementary data required (for finalization)
- Calculated Cv of each FCV and selection of Trim/Characteristic (Linear/Equal%)
- Actuator speed, torque/force, closing/opening time and On/Off/Partial Stroke tests (if needed)
- Flow measurement method and instrument accuracy class (calibration/Ex criteria)
- Line sizing, flange classes, materials, and testing/inspection requirements
- Interlock/Shutdown logic with reference to Cause & Effect and HAZOP/LOPA results

Notes
- Symbols and tags are samples and will be updated based on the client/site standard.
- The placement of PSVs, hot bypass and final sizing will be finalized after receiving the final process data.

Version history
- v0.2: Added the actuator/Positioner/SOV/limit switch detail diagram, I/O assignment tables, Line List, Valve Data, Setpoints, C&E summary and Logic Narrative
- v0.1: Simple initial version


