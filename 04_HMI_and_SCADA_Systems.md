# OT Security from Scratch: Module 4 — HMI & SCADA Systems

A beginner-friendly guide to industrial control screens, central monitoring, and why HMIs are major targets for cyber attacks.

## Introduction

In Module 2 and Module 3, we learned about Sensors, PLCs, Actuators, and Industrial Protocols. 

Now, how does a human operator actually look at what the machine is doing? And how does an operator send commands without typing raw code?

They use **HMIs** and **SCADA Systems**.

```
┌────────────────────────────────────────────────────────┐
│           CENTRAL CONTROL ROOM (SCADA SERVER)          │
│           (Monitors the Entire Ship or Plant)          │
└───────────────────────────┬────────────────────────────┘
                            │ Connects to multiple HMIs
                            ▼
┌────────────────────────────────────────────────────────┐
│            LOCAL OPERATOR SCREEN (HMI)                 │
│         (Touchscreen at Engine 1 or Navigation)        │
└───────────────────────────┬────────────────────────────┘
                            │ Speaks Modbus / OPC UA
                            ▼
┌────────────────────────────────────────────────────────┐
│           PLC ──► SENSORS & ACTUATORS (Machinery)       │
└───────────────────────────┬────────────────────────────┘
```

---

## 1. What is an HMI? (Human-Machine Interface)

An **HMI (Human-Machine Interface)** is the touchscreen monitor or computer screen that allows a human operator to interact with an industrial machine.

### Real-World Examples of HMIs:
- **Ship Bridge:** Touchscreen displays showing engine RPM, fuel levels, water temperature, and pump status buttons.
- **Water Plant:** A control panel displaying water tank levels with buttons to open or close valves.
- **Factory Floor:** A screen mounted next to a conveyor belt displaying machine status and emergency stop buttons.

---

## 2. What is SCADA? (Supervisory Control and Data Acquisition)

**SCADA** stands for **Supervisory Control and Data Acquisition**.

While an **HMI** controls a single machine or section, a **SCADA System** is a central control room software that monitors and controls an **entire plant, power grid, or ship**.

### Difference Between HMI and SCADA:

| Feature | HMI (Human-Machine Interface) | SCADA (Supervisory Control & Data Acquisition) |
| :--- | :--- | :--- |
| **Scope** | Controls **ONE local machine** or single area | Manages **ENTIRE facility, power grid, or ship** |
| **Location** | Mounted directly on/near the physical machine | Located in a central control room |
| **Users** | Local machine operators / technicians | Fleet managers, chief engineers, plant directors |
| **Data Storage** | Displays real-time data | Stores historical data, logs, and trend graphs |

---

## 3. Why Are HMIs & SCADA Prime Targets for Cyber Attacks?

An attacker targeting an OT environment almost always tries to compromise the HMI or SCADA system. 

Here are the **3 Main Reasons Why**:

1. **Full Operational Control:**  
   HMIs have pre-configured buttons to start/stop pumps, trip circuit breakers, or change valve positions. If an attacker gains remote access to an HMI screen (e.g., via VNC, Remote Desktop, or web portals), they can control physical machinery with the click of a mouse!

2. **Operator Deception (False Screen Displays):**  
   If an attacker hacks an HMI software, they can manipulate the graphics on the screen. The HMI might display `"Engine Temp: 70°C (NORMAL)"`, while the real engine is overheating at **140°C**. The human operator is deceived and does not take action.

3. **Standard Operating Systems (Windows/Linux Vulnerabilities):**  
   Unlike PLCs (which use special firmware), HMI screens and SCADA servers often run standard **Windows or Linux**. This means they are vulnerable to traditional IT malware, unpatched OS bugs, ransomware, and weak passwords!

---

## 4. Hands-On Practical Lab 2 (HMI Screen Deception Simulation)

### Objective:
Demonstrate and identify how HMI graphics tampering deceives human operators into failing to trigger emergency cooling during physical engine overheating.

### Script Used:
- **`04_HMI_Screen_Spoofing_Lab.py`:** Simulates a physical engine temperature vs. spoofed HMI screen output.

### Execution & Observed Results:
Run the script in your terminal:
```powershell
python 04_HMI_Screen_Spoofing_Lab.py
```

Output observed:
```text
==========================================================
  SIMULATING HMI OPERATOR SCREEN & PHYSICAL ENGINE LOOP   
==========================================================

--- REAL PHYSICAL WORLD ---
[PHYSICAL PROCESS] Real Engine Temperature: 140°C
[PHYSICAL DANGER] Engine Status: OVERHEATING CRITICAL (Danger Threshold: 90°C)

--- HMI OPERATOR DISPLAY SCREEN ---
[HMI SCREEN DISPLAY] Temperature Shown to Operator: 70°C
[HMI STATUS DISPLAY] Display Status: NORMAL / SAFE

--- OPERATOR DECISION & SECURITY IDENTIFICATION ---
[OPERATOR ACTION] Operator sees 70°C (Normal) ➔ Does NOT activate Emergency Cooling Pump.
[CRITICAL CONSEQUENCE] Physical Engine continues to overheat at 140°C and suffers catastrophic physical damage!
```

### What We Identified (Security Finding):
1. **Operator Deception Identification:** Tampering with HMI display graphics effectively prevents human operators from detecting physical process emergencies.
2. **Lack of Independent Alarms:** Demonstrates the danger of relying solely on a single software HMI screen without secondary hardwired physical alarms.

---

## 5. Key Takeaways from Module 4

- **HMI** = Local touchscreen interface for controlling one machine.
- **SCADA** = Central control room software for managing an entire facility/vessel.
- **Security Risk:** Hacking an HMI gives attackers physical control of machinery and allows them to deceive human operators with false screen data.
- **Lab Finding:** Proved that HMI screen spoofing misleads operators into taking zero corrective action during physical overheating events.
