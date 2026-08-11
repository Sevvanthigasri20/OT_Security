# OT Security from Scratch: Module 2 — Sensors, Actuators, and PLCs

A simple guide to the 3 core building blocks of every industrial control system.

## Introduction

In Module 1, we learned that OT (Operational Technology) controls physical machines in the real world—like ship engines, power generators, and water pumps.

Now, how does a computer actually control a physical machine? 

Every OT process relies on a simple 3-step loop:
**Sense ➔ Decide ➔ Act**

## 1. The Sensor (The Eyes & Ears)

**What it does:** Measures physical conditions in the real world (temperature, pressure, speed, water level).

**Example:** An engine temperature sensor reading 95°C.

**OT Security Risk (False Data Injection):** If an attacker tampers with a sensor signal, the system receives fake numbers. Real engine heat is **120°C** (Overheating!), but the sensor reads **70°C**, deceiving the operator.

## 2. The PLC / Controller (The Brain)

**PLC** stands for **Programmable Logic Controller**.

**What it does:** A small, rugged industrial computer that receives sensor data, checks its programmed rules, and makes a decision.

**Example Logic:** *"If engine temperature > 90°C, turn ON the cooling pump."*

**OT Security Risk (Logic Manipulation):** If an attacker gains unauthorized access to a PLC and changes its programmed rule from **90°C** to **200°C**, the cooling pump will never turn on, causing the engine to overheat and melt down!

## 3. The Actuator (The Hands & Muscles)

**What it does:** Converts the electronic command from the PLC into physical movement or action.

**Examples:** Electric motors, hydraulic valves, water pumps, circuit breakers.

**Example:** Opening the seawater valve when instructed by the PLC.

## 4. The Complete 3-Step Physical Loop Example

Imagine a Yacht Engine Cooling System:
1. **Sensor:** Detects engine temperature has reached 95°C.
2. **PLC:** Evaluates rule (95°C > 90°C = True) and decides to activate cooling.
3. **Actuator:** Opens the seawater cooling valve and starts the water pump.
4. **Physical Outcome:** Engine temperature drops safely back to 80°C.

## 5. Key Takeaways from Module 2

- **Sensors** measure the physical world (Eyes & Ears).
- **PLCs** make automated decisions based on rules (Brain).
- **Actuators** perform physical actions (Hands & Muscles).
- **OT Security** protects all 3 parts from physical damage, false data, and unauthorized command changes.
