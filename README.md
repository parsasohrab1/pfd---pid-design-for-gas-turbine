Title: Initial PFD and P&ID Package — Siemens SGT600/IGT25 Turbine Fuel Valve Actuator and Control System (Heinzmann Replacement)

Short description
This package contains initial PFD and P&ID drafts for the fuel circuit (Main & Primary), focusing on the control valve actuator and its electrical/instrumentation accessories for installation on Siemens SGT600/IGT25 turbines. This version is prepared for starting engineering (Class-Concept/FEED) and requires completion with process data and interfaces.

Key assumptions (for the initial version)
- Fuel: dry natural gas, pressure range 20–70 barg (ASME Class proportional to the site), temperature 0–60°C
- Two fuel paths, Primary and Main, with service/safety bypasses
- Electric/electro-hydraulic control valve actuator (with Ex d/Ex e certification or equivalent)
- Speed/load control loop from the existing PLC/turbine controller (TGC), 4–20 mA or Fieldbus signal standard
- Target SIL level for the ESD loop: SIL2 (per IEC 61511/61508 — requires client confirmation)
- Hazardous areas: Zone 1 or Zone 2 (ATEX/IECEx confirmation of instrumentation and drives)

Reference standards
- IEC 60534 (control valves), IEC 61800 (drives), ISO 6336 and AGMA 2001 (gearing — if present in the actuator)
- API 6D/598 for valve testing (where applicable), ISA-5.1 for symbols and tagging
- IEC 60079 (Ex), IEC 61511/61508 (SIS/SIL) — for final safety design

Items in the package
- PFD_SGT600_Fuel_Control.md — process flow diagram (Mermaid)
- PID_SGT600_Fuel_Control.md — piping and instrumentation diagram (Mermaid + lists)

Checklist of data required for finalization
1) Process conditions
   - Fuel inlet and outlet pressure/flow/temperature (Min/Norm/Max)
   - Flange classes, MOP, PSV set-points (if any)
   - Corrosiveness/contamination, required filtration
2) Valve and actuator specifications
   - Required Cv, Linear/Equal%, Seat/Trim, Leakage Class, Fail Action
   - Actuator type (electric/electro-hydraulic), travel time, required torque/force, Ex and IP protection
   - Need for independent ESD and the Fail position (Close/Open/Last)
3) Instrumentation and control
   - Sensors (PT/TT/FT/DP) and accuracy/Ex class, installation location
   - I/O signals (analog/digital/fieldbus), power supply, cabling
   - Control philosophy (Speed/Load/Pressure control) and interlocks
4) Safety and SIL requirements
   - SIFs, testability, failure mode effects, Proof test coverage
5) Mechanical and piping
   - Line materials, line sizing, insulation/support class
   - New spools/changes and installation space/access
6) Documents and site requirements
   - Zone Classification, cable routes, Junction Box/Marshall
   - Client standards for tagging, color, drawing layering

Notice
These documents are conceptual drafts and require updating with real site data and client approval for final production/construction.





# pfd
design for production
Title: PFD — Fuel Circuit and Control Valve Actuator (SGT600/IGT25)

Purpose
A simple display of the fuel process flow, key measurement points and the position of the control valve actuator for the Primary and Main paths.

Process Flow Diagram (Mermaid)

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

Flow and measurement tables (draft)
- Nominal flow: 100% load — based on the turbine datasheet (real data required)
- Flow range: Min/TurnDown to Max (determines final Cv)
- Measurement points: Pressure upstream/downstream, Flow (per line), Temperature

Main PFD items
- Filtration/coalescer unit for removing liquids/particles
- Separator/surge drum to protect valves and combustion
- Heater/Conditioning if needed (temperature/density)
- Primary/Main branch, control valves (Actuated) and merging into the mixed header
- FT/PT/TT instruments at key points

Notes
- Exact flow/pressure/temperature values and the Heater selection are optional and will be replaced with site data.
- The safe shutdown philosophy (Fail Close on both lines) is assumed in the initial version.


PID
Title: P&ID — Fuel Circuit and Control Valve Actuator (SGT600/IGT25)

Purpose
Shows lines, valves, instrumentation, control loops and electrical/ESD interfaces for replacing the Heinzmann valve actuators.

Symbols and layering (brief)
- Symbol standard: ISA-5.1
- Sample tagging: FCV-PR-101 (Primary), FCV-MN-201 (Main)
- Color/layer: per the client standard (to be updated after receipt)

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

Control loops (sample)
- LIC/FIC-PR-101: Primary line flow control for speed/load control — output to actuator FCV-PR-101
- LIC/FIC-MN-201: Main line flow control — output to actuator FCV-MN-201
- PT-001/002 for Interlock and pressure protections
- SDV/ESD-PR-001 and SDV/ESD-MN-001 commandable from the SIS (Trip → Close)

Safety philosophy (draft)
- Safe state: Fail Close for FCVs and SDVs
- Sample SIF: High-High Pressure at Header → Trip the SDVs and Close command to the FCVs (SIL2 target)
- Periodic testability (Proof Test) and a safe bypass with operator permit

Electrical interfaces (summary)
- Actuator power supply: 24 VDC/110 VAC/400 VAC (per actuator selection) — with Ex certification and suitable IP
- Signals: analog 4–20 mA or Fieldbus (HART/Profibus/Profinet) per the existing PLC
- Cabling: shielded/twisted pair, reference ground, JB/Marshall in a suitable Zone, Ex gland

Partial Tag List
- FCV-PR-101, FCV-MN-201 — control valve + Actuator (Ex)
- FT-PR-010, FT-MN-020 — flow transmitter
- PT-001 (Upstream), PT-002 (Header) — pressure transmitter
- SDV/ESD-PR-001, SDV/ESD-MN-001 — emergency shutdown valve
- PSV-PR-001, PSV-MN-001 — relief valve (if needed)

I/O List (draft)
- Analog input: PT-001, PT-002, FT-PR-010, FT-MN-020
- Analog output: FCV-PR-101 (Position/Command), FCV-MN-201 (Position/Command)
- Digital output: SDV/ESD-PR-001 (Close/Open), SDV/ESD-MN-001 (Close/Open)
- Digital input: Limit Switches, Trip Status, ESD Status

Notes
- Symbols and tags are samples and will be matched to the client/site standard.
- The placement of PSVs, hot bypass and line sizing will be finalized after receiving the final process data.


Project root
Overall structure of folders and files:

```
pfd-pid/
├─ README.md
├─ PFD_SGT600_Fuel_Control.md
├─ PID_SGT600_Fuel_Control.md
├─ tools/
│  ├─ requirements.txt
│  └─ generate_dxf.py
└─ cad/                ← created after running the script
   ├─ PFD_SGT600_Fuel_Control.dxf   (generated)
   └─ PID_SGT600_Fuel_Control.dxf   (generated)
```

Generating AutoCAD files (DXF)
For output that can be opened in AutoCAD/LibreCAD, a DXF script has been prepared:

1) Install the prerequisite
```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r tools\\requirements.txt
```

2) Generate the DXFs
```powershell
python tools\\generate_dxf.py
```

3) Output path
- Files are created in the `cad\\` folder:
  - `cad\\PFD_SGT600_Fuel_Control.dxf`
  - `cad\\PID_SGT600_Fuel_Control.dxf`

Notes
- These DXFs are engineering schematics for starting AutoCAD work (simple blocks/layers). We can customize the standard ISA symbols, layering, instrument blocks and Title Block per the client's standard.
- If the DWG format is needed, you can convert the DXF to DWG in AutoCAD with Save As.



