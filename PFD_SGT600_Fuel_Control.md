Title: PFD — Fuel Circuit and Control Valve Actuator (Siemens SGT600/IGT25)

Scope
- Shows the natural gas process flow, key measurement points, pretreatment/conditioning units and the position of control valve actuators for the Primary and Main lines, merging into the common header toward the turbine combustion system.

Design assumptions (version ready to start engineering)
- Fuel: dry natural gas, inlet pressure range 20–70 barg, temperature 0–60°C
- Two fuel paths, Primary and Main, with service/safety bypasses (shown conceptually at PFD level)
- Safe state: Fail Close for control valves and SDVs
- Ex certification for actuators and instrumentation suited to Zone 1/2
- Symbol standard: ISA-5.1 (for attachment to the P&ID)

Version and scope
- Version: v0.2 — ready for presentation for Concept/FEED
- Scope: from the unit fuel inlet to the mixing header at the inlet of the turbine combustion system (downstream nozzle details are outside the PFD scope)

Process Flow Diagram — Level 1 (Mermaid)

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

Process Flow Diagram — Level 2 (with bypass and conceptual SDV)

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

Main PFD items
- Filtration/coalescer unit for removing liquids/particles
- Surge/separator drum (KO Drum) to protect valves and combustion
- Heater/Conditioning if required by the process (density/dew point/icing)
- Primary/Main branch, actuated control valves and merging into the common header
- FT/PT/TT instruments at key points

Streams — Draft
- S-001: Fuel Gas Inlet — pressure 20–70 barg, temperature 0–60°C, composition: natural gas (Site Data)
- S-010: After filter/coalescer — pressure/pressure drop ΔP_FC (Site Data)
- S-020: KO Drum outlet — measured temperature TT-001
- S-030: Primary Upstream FCV — measurement FT-PR-010
- S-040: Main Upstream FCV — measurement FT-MN-020
- S-100: Mixing Header toward GT — pressure PT-002, Combustion Feed conditions

Equipment List (Draft)
- F1: Filter/Coalescer — class/size/allowable ΔP (Site Data)
- KO: Knock-out Drum — volume/Retention, Drain/Instrumentation connection
- HEAT: Heater/Conditioning — Duty, Utility, temperature control (optional)
- FCV-PR-101 / FCV-MN-201: control valves of each line — Trim/Characteristic, Leakage Class
- SDV-PR-001 / SDV-MN-001: emergency shutdown valves (Trip Close)
- HDR: mixing header — flange class and size

Measurement List (Draft)
- PT-001: pressure after filter/coalescer (protection/monitoring)
- TT-001: temperature after KO Drum
- FT-PR-010: Primary line flow (measurement for control/monitoring)
- FT-MN-020: Main line flow
- PT-002: mixing header pressure (Interlock/Monitoring)

Operating Cases
- Start-up / Light-off: use of Primary, Ramp/Rate limits per the controller
- Base-load: use of both lines, flow split per the control philosophy
- Part-load / Turndown: adjusting effective Cv and maintaining combustion stability
- Trip/ESD: closing the SDVs and Close command to the FCVs (Fail Close)

Design Data (placeholder — complete with site data)
- Nominal flow at 100% load: per the turbine datasheet (the real value must be entered)
- TurnDown flow range of each line: Min … Max (determines Cv and Trim specifications)
- Inlet/outlet pressure and allowable pressure drop of pretreatment units
- Heater requirements (Duty, target temperature, Utility and control)
- Flange class and test class per the client's standard

Notes
- Final flow/pressure/temperature values and equipment sizing should be updated with real site data and client approval.
- The Fail Close safety philosophy is assumed for the Primary and Main paths.
- For tagging details, control loops, ESD interfaces and I/O refer to the P&ID document.

Version history
- v0.2: Added the level 2 diagram (bypass/SDV), Streams/Equipment/Measurements tables and operating cases
- v0.1: Initial level 1 version per the README


