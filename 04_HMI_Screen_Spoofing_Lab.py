"""
Hands-On Practical Lab 2: HMI Operator Deception / Screen Spoofing Simulator

Demonstrates how an attacker tampering with HMI display feeds deceives human operators into believing an overheating engine is operating normally.
"""

import time

def run_hmi_spoofing_simulation():
    print("==========================================================")
    print("  SIMULATING HMI OPERATOR SCREEN & PHYSICAL ENGINE LOOP   ")
    print("==========================================================\n")
    
    # Real physical engine temperature (Overheating!)
    real_engine_temp = 140  # °C
    
    # Tampered HMI screen temperature (Fake Normal reading!)
    hmi_displayed_temp = 70  # °C
    
    print("--- REAL PHYSICAL WORLD ---")
    print(f"[PHYSICAL PROCESS] Real Engine Temperature: {real_engine_temp}°C")
    print(f"[PHYSICAL DANGER] Engine Status: OVERHEATING CRITICAL (Danger Threshold: 90°C)\n")
    
    time.sleep(1)
    
    print("--- HMI OPERATOR DISPLAY SCREEN ---")
    print(f"[HMI SCREEN DISPLAY] Temperature Shown to Operator: {hmi_displayed_temp}°C")
    print(f"[HMI STATUS DISPLAY] Display Status: NORMAL / SAFE\n")
    
    time.sleep(1)
    
    print("--- OPERATOR DECISION & SECURITY IDENTIFICATION ---")
    if hmi_displayed_temp <= 90:
        print("[OPERATOR ACTION] Operator sees 70°C (Normal) ➔ Does NOT activate Emergency Cooling Pump.")
        print("[CRITICAL CONSEQUENCE] Physical Engine continues to overheat at 140°C and suffers catastrophic physical damage!")
    else:
        print("[OPERATOR ACTION] Operator sees Overheating warning ➔ Activates Emergency Cooling.")
        
    print("\n==========================================================")
    print("  LAB 2 SECURITY FINDING IDENTIFIED:                       ")
    print("  1. Operator Deception: HMI graphic spoofing hides real  ")
    print("     physical engine overheating.                         ")
    print("  2. Lack of Independent Validation: Operator relied 100% ")
    print("     on HMI screen without secondary physical alarms.     ")
    print("==========================================================")

if __name__ == "__main__":
    run_hmi_spoofing_simulation()
