from pymodbus.client import ModbusTcpClient
import time

# Set up the connection to the PLC
PLC_IP = "169.254.155.80"  # Replace with the actual IP address of your KV-7500
PLC_PORT = 8501  # Default Modbus TCP port
SENSOR_COIL_ADDRESS = 0x3400  # Replace with the actual coil address for the sensor

client = ModbusTcpClient(PLC_IP, port=PLC_PORT)

def read_sensor_state():
    # Connect to PLC
    connection = client.connect()
    if connection:
        print("Connected to PLC")

        # Read coil (on/off) status of the sensor at the given address
        result = client.read_coils(SENSOR_COIL_ADDRESS, 1)  # Read 1 coil from the sensor's address
        if not result.isError():
            sensor_state = result.bits[0]
            print(f"Sensor state (on/off): {'ON' if sensor_state else 'OFF'}")
        else:
            print("Error reading sensor state")

        # Close the connection
        client.close()
    else:
        print("Failed to connect to PLC")

if __name__ == "__main__":
    while True:
        read_sensor_state()
        time.sleep(1)  # Poll the sensor every 1 second
