"""
Hands-On Practical Lab 1: Pure Python Modbus HMI Client
Sends Read & Write Modbus TCP requests to the simulated PLC.
"""

import socket
import struct
import time

HOST = "127.0.0.1"
PORT = 5020

def send_read_request(sock, transaction_id, start_addr=0, count=3):
    """Function Code 3: Read Holding Registers"""
    unit_id = 1
    function_code = 3
    
    # Modbus PDU: FC (1 byte) + Start Address (2 bytes) + Quantity (2 bytes)
    pdu = struct.pack(">BHH", function_code, start_addr, count)
    
    # MBAP Header: TransID (2b) + ProtoID (2b) + Length (2b) + UnitID (1b)
    length = 1 + len(pdu)
    mbap = struct.pack(">HHHB", transaction_id, 0, length, unit_id)
    
    packet = mbap + pdu
    sock.sendall(packet)
    
    # Receive response header + PDU
    res_mbap = sock.recv(7)
    if not res_mbap:
        return
    res_trans, res_proto, res_len, res_unit = struct.unpack(">HHHB", res_mbap)
    
    res_pdu = sock.recv(res_len - 1)
    fc = res_pdu[0]
    byte_count = res_pdu[1]
    
    values = []
    for i in range(0, byte_count, 2):
        val = struct.unpack(">H", res_pdu[2+i:4+i])[0]
        values.append(val)
        
    print(f"[HMI CLIENT] Read Response from PLC: Register Values = {values}")
    return values

def send_write_request(sock, transaction_id, target_addr=0, new_value=120):
    """Function Code 6: Write Single Register (Tamper / Command)"""
    unit_id = 1
    function_code = 6
    
    pdu = struct.pack(">BHH", function_code, target_addr, new_value)
    length = 1 + len(pdu)
    mbap = struct.pack(">HHHB", transaction_id, 0, length, unit_id)
    
    packet = mbap + pdu
    sock.sendall(packet)
    
    # Receive echo response
    res_mbap = sock.recv(7)
    res_pdu = sock.recv(5)
    print(f"[HMI CLIENT] Write Command sent: Set Register {target_addr} = {new_value}")

def run_lab():
    print("[+] Connecting to Simulated PLC Server at 127.0.0.1:5020...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    print("[+] Connected successfully!\n")
    
    # Step 1: Read normal PLC values
    print("--- STEP 1: Reading Normal PLC Values ---")
    send_read_request(sock, transaction_id=1, start_addr=0, count=3)
    time.sleep(1)
    
    # Step 2: Send a Write Command (Simulated control or tampering)
    print("\n--- STEP 2: Sending Control Command (Setting Engine Temp to 120°C) ---")
    send_write_request(sock, transaction_id=2, target_addr=0, new_value=120)
    time.sleep(1)
    
    # Step 3: Read values again to verify update
    print("\n--- STEP 3: Reading PLC Values After Update ---")
    send_read_request(sock, transaction_id=3, start_addr=0, count=3)
    
    sock.close()
    print("\n[+] Lab 1 Complete!")

if __name__ == "__main__":
    run_lab()
