# OT Security from Scratch: Module 3 — What is an Industrial Protocol & Why is it Vulnerable?

A beginner-friendly guide to how industrial devices talk to each other, and why OT protocols are vulnerable to cyber attacks.

## Introduction

In Module 2, we learned that an OT system has 3 main parts: **Sensors, PLCs, and Actuators**.

Now, how do these devices talk to each other over a cable or network? 

They use a **Protocol**.

---

## 1. What is a Protocol? (In Plain English)

Think of a **Protocol** as a **language and set of rules**.

### Human Example:
- If two people want to talk, they must speak the same language (e.g., both speak English).
- If one person speaks English and the other speaks Japanese, they cannot communicate!

### Computer Example:
- A **Protocol** is the language computers use to send messages back and forth.
- When your web browser opens a website, it speaks the **HTTP / HTTPS** protocol (Web Language).
- When a ship engine PLC talks to a bridge display screen, it speaks an **OT Industrial Protocol** (Industrial Language).

---

## 2. Common Industrial Languages (OT Protocols)

### A. Modbus TCP
- **Full Form:** Modicon Bus Transmission Control Protocol
- **Why we use it:** It is the simplest and most widely supported industrial language in the world. Almost every factory PLC and ship engine controller understands Modbus TCP.
- **What happens if we DON'T use it?** Devices built by different manufacturers (e.g., Siemens PLC talking to a Schneider sensor) wouldn't understand each other without expensive custom software.

### B. OPC UA
- **Full Form:** Open Platform Communications Unified Architecture
- **Why we use it:** It is the modern, secure industrial protocol. It allows PLCs to safely send data to factory SCADA systems and cloud databases using **passwords, digital certificates, and encryption**.
- **What happens if we DON'T use it?** Connecting industrial controllers to corporate IT networks or cloud servers would expose plain-text machine data to cyber attacks.

### C. NMEA 0183 / NMEA 2000
- **Full Form:** National Marine Electronics Association (0183 / 2000)
- **Why we use it:** It is the universal marine language used on ships and luxury yachts. It lets equipment from different marine brands (Garmin GPS, Raymarine Radar, Simrad Autopilot) talk to each other over a single shared cable.
- **What happens if we DON'T use it?** The ship's Autopilot wouldn't receive GPS coordinates, the Radar couldn't display depth data, and navigation equipment from different brands wouldn't work together!

---

## 3. Why are Traditional OT Protocols Vulnerable?

When protocols like **Modbus** and **NMEA** were created decades ago, factory machines and ship bridges were completely disconnected from the internet. 

Engineers assumed that anyone touching the machine was a trusted friend. Because of this, traditional OT protocols have **3 big security flaws**:

1. **No Authentication (No Passwords):** The PLC does not ask *"Who are you?"*. If any device on the network sends a command, the PLC executes it without asking for a password.
2. **No Encryption (Sent in Plain Text):** Data travels across the wire in plain text. Anyone watching network traffic (using Wireshark) can read sensor values clearly.
3. **No Integrity Protection:** Commands can be modified in transit without the PLC detecting the tampering.

---

## 4. Why Do We Still Use Modbus TCP if it is Insecure?

If Modbus TCP is insecure by default, why do industrial facilities and ships still use it?

1. **20–30 Year Equipment Lifespan:** Ship engines, generators, and factory PLCs last for decades. Replacing billions of dollars of working equipment just to change a network protocol is too expensive.
2. **Simplicity & Speed:** Modbus uses very little processing power. Adding heavy encryption to old microcontrollers could introduce delays in real-time physical control.
3. **Universal Compatibility:** Every industrial vendor in the world supports Modbus.

### How OT Security Engineers Secure Modbus (Defense-in-Depth):
Since we cannot change the Modbus protocol inside old PLCs, **we protect the network AROUND the PLC**:

- **Network Segmentation (Firewalls):** We isolate Modbus devices inside dedicated OT network zones (Zone 7 / Zone 8). An attacker on Guest Wi-Fi or VSAT is blocked by firewalls from reaching port 502.
- **Industrial Firewalls (DPI):** We use firewalls that inspect Modbus packets and block unauthorized write commands.
- **Passive Monitoring (OT IDS / Wireshark):** We monitor network traffic to alert us if an unknown IP tries to send Modbus write commands.

---

## 5. Hands-On Practical Lab 1 (Modbus Simulation & Identification)

### Objective:
Demonstrate and identify how an unauthenticated Modbus TCP request can read and modify PLC memory registers over a network.

### Scripts Used:
1. **`03_Modbus_PLC_Simulation.py`:** Simulates a PLC Server listening on port `5020`.
2. **`03_Modbus_HMI_Client.py`:** Simulates an HMI Client sending read & write requests.

### Execution & Observed Results:
When running `03_Modbus_HMI_Client.py` against the running PLC server:

```text
[+] Connecting to Simulated PLC Server at 127.0.0.1:5020...
[+] Connected successfully!

--- STEP 1: Reading Normal PLC Values ---
[HMI CLIENT] Read Response from PLC: Register Values = [90, 45, 1]

--- STEP 2: Sending Control Command (Setting Engine Temp to 120°C) ---
[HMI CLIENT] Write Command sent: Set Register 0 = 120

--- STEP 3: Reading PLC Values After Update ---
[HMI CLIENT] Read Response from PLC: Register Values = [120, 45, 1]
```

### What We Identified (Security Finding):
1. **Unauthenticated Read Identification:** The client successfully retrieved PLC memory registers (`[90°C, 45 PSI, 1]`) without supplying any password or authentication token.
2. **Unauthenticated Control Identification:** The client successfully overwrote Register 0 (Engine Temp) from `90°C` to `120°C` using Modbus Function Code 6 (`FC6`). The PLC accepted and applied the write command without verifying the caller's identity.

---

## 6. Key Takeaways from Module 3

- A **Protocol** is simply the language devices use to communicate.
- **Modbus TCP** (Modicon Bus TCP) = Simple industrial standard.
- **OPC UA** (Open Platform Communications UA) = Modern secure industrial standard.
- **NMEA** (National Marine Electronics Association) = Universal maritime vessel standard.
- Traditional protocols trust all commands blindly because they lack passwords and encryption.
- **Why Still Used:** Legacy equipment lifespan (20-30 years), simplicity, and universal compatibility.
- **How Secured:** Network segmentation, firewalls, and passive monitoring keep unauthorized traffic away from OT devices.
