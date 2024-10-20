import serial
import time

esp32_port = 'COM9'  
baud_rate = 115200

try:
    
    ser = serial.Serial(esp32_port, baud_rate, timeout=1)
    time.sleep(2) 

    print("Starting to read serial data...")
    while True:
        data = ser.readline().decode('utf-8').strip()  
        if data: 
            print(data)

except Exception as e:
    print(f"Error: {e}")

finally:
    ser.close()  
    print("Closed serial port")
