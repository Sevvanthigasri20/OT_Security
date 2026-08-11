"""
Hands-On Practical Lab 1: Pure Python Modbus TCP PLC Simulator
No external dependencies required (Uses built-in Python socket & struct).

Run this script to start a simulated Industrial PLC listening on 127.0.0.1:5020.
"""

import socket
import struct
import threading
import time

# Simulated Industrial PLC Memory Registers (Holding Registers)
# Address 1 (Index 0): Engine Temperature = 90°C
# Address 2 (Index 1): Water Pressure = 45 PSI
# Address 3 (Index 2): Pump Status = 1 (1 = ON, 0 = OFF)
plc_registers = [90, 45, 1, 0, 0, 0, 0, 0, 0, 0]

HOST = "127.0.0.1"
PORT = 5020

def handle_client(client_socket, client_address):
    print(f"[+] HMI / Client connected from {client_address[0]}:{client_address[1]}")
    
    try:
        while True:
            # Read Modbus TCP Request Header (7 bytes: MBAP Header)
            header = client_socket.recv(7)
            if not header or len(header) < 7:
                break
            
            transaction_id, protocol_id, length, unit_id = struct.unpack(">HHHB", header)
            
            # Read Remaining PDU (Protocol Data Unit) payload
            pdu_len = length - 1
            pdu = client_socket.recv(pdu_len)
            if not pdu or len(pdu) < 1:
                break
            
            function_code = pdu[0]
            
            # Function Code 3: Read Holding Registers
            if function_code == 3:
                start_addr, count = struct.unpack(">HH", pdu[1:5])
                print(f"[+] [PLC RECEIVED] Read Request for {count} register(s) starting at address {start_addr}")
                
                # Fetch requested register values from PLC memory
                requested_values = plc_registers[start_addr:start_addr + count]
                byte_count = len(requested_values) * 2
                
                # Build Modbus TCP Response Packet
                response_pdu = struct.pack(">BB", function_code, byte_count)
                for val in requested_values:
                    response_pdu += struct.pack(">H", val)
                
                response_len = 1 + len(response_pdu)
                response_mbap = struct.pack(">HHHB", transaction_id, protocol_id, response_len, unit_id)
                
                response_packet = response_mbap + response_pdu
                client_socket.sendall(response_packet)
                print(f"[+] [PLC SENT] Returned values: {requested_values}")
                
            # Function Code 6: Write Single Register
            elif function_code == 6:
                target_addr, new_val = struct.unpack(">HH", pdu[1:5])
                print(f"[!] [PLC WARN] Write Request received: Set Register {target_addr} = {new_val}")
                
                if target_addr < len(plc_registers):
                    old_val = plc_registers[target_addr]
                    plc_registers[target_addr] = new_val
                    print(f"[!] [PLC MEMORY UPDATED] Register {target_addr} changed from {old_val} to {new_val}")
                
                # Echo same PDU back as confirmation for FC6
                response_len = 1 + len(pdu)
                response_mbap = struct.pack(">HHHB", transaction_id, protocol_id, response_len, unit_id)
                client_socket.sendall(response_mbap + pdu)

    except Exception as e:
        print(f"[-] Client connection error: {e}")
    finally:
        client_socket.close()
        print(f"[-] Client {client_address[0]}:{client_address[1]} disconnected.")

def start_plc_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    
    print(f"==================================================")
    print(f"  SIMULATED INDUSTRIAL PLC SERVER IS RUNNING      ")
    print(f"  Listening on {HOST}:{PORT}                       ")
    print(f"  Initial PLC Memory Registers:                   ")
    print(f"    Register 0 (Engine Temp): {plc_registers[0]}°C ")
    print(f"    Register 1 (Water Press): {plc_registers[1]} PSI")
    print(f"    Register 2 (Pump Status): {plc_registers[2]}     ")
    print(f"==================================================")
    
    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

if __name__ == "__main__":
    start_plc_server()
