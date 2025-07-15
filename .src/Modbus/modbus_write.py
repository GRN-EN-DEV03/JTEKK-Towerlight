from pymodbus.client import ModbusTcpClient
import time

# --- Configuration ---
# Replace with the IP address or hostname of your Modbus TCP device
MODBUS_HOST = 'localhost'
# Replace with the Modbus TCP port (default is 502)
MODBUS_PORT = 502
# Slave ID (Unit ID) of the Modbus device (usually 1 for RTU over TCP or 1 for many TCP devices)

# --- Modbus Client Initialization ---
# Create a Modbus TCP client instance.
# You can also use ModbusSerialClient for RTU or ASCII over serial (e.g., 'rtu', port='/dev/ttyUSB0')
client = ModbusTcpClient(MODBUS_HOST,port=MODBUS_PORT)

def connect_to_modbus():
    """
    Attempts to connect to the Modbus TCP device.
    """
    print(f"Attempting to connect to Modbus device at {MODBUS_HOST}:{MODBUS_PORT}...")
    if client.connect():
        print("Successfully connected to Modbus device.")
        return True
    else:
        print(f"Failed to connect to Modbus device at {MODBUS_HOST}:{MODBUS_PORT}. "
              "Please ensure the device is running and accessible.")
        return False

def write_coil_status(address,value,MODBUS_SLAVE_ID):
    """
    Writes a single value to a single coils register.

    Args:
        address (int): The Modbus register address (0-based).
        value (int): The integer value to write to the register.
        MODBUS_SLAVE_ID : Meter ID or Device ID of modbus
    """
    print(f"\nAttempting to write value {value} to coils register address {address}..")
    try:
        # Write the single coils register
        # The 'unit' parameter is the slave ID
        result = client.write_coils(address-1, value, slave=MODBUS_SLAVE_ID)
        #print(result)
        if result.isError():
            print(f"Error writing single register: Modbus Exception - {result}")
        else:
            print(f"Successfully wrote {value} to coils register {address}.")
    except Exception as e:
        print(f"An error occurred during single register write: {e}")

def read_coil_status(address,MODBUS_SLAVE_ID) :
    """
    Read a single value to a single coils register.

    Args:
        address (int): The Modbus register address (0-based).
        MODBUS_SLAVE_ID : Meter ID or Device ID of modbus
    """
    #print(f"\nAttempting to read value from coils register address {address}...")
    try:
        # Write the single coils register
        # The 'unit' parameter is the slave ID
        #response = client.read_coils(1,count=10 ,slave=1)
        response = client.read_coils(address-1,count=1 ,slave=MODBUS_SLAVE_ID)
        datas = response.bits
        print("OUTPUT ----------------------------------------------------")
        #print(response)
        print("Modbus Response : ",datas[0])
        print("-----------------------------------------------------------")
        if response.isError():
            print(f"Error reading single register: Modbus Exception - {response}")
            return 1
        else:
            print(f"Successfully read from coils register {address}.")
            return datas[0]
    except Exception as e:
        print(f"An error occurred during single register read: {e}")

# --- Main execution block ---
def main_write_register(address,value,MODBUS_SLAVE_ID) :
    # Ensure pymodbus is installed: pip install pymodbus
    if connect_to_modbus():
        # Write value 123 to register address 0
        write_coil_status(address,value,MODBUS_SLAVE_ID)
        time.sleep(0.1) # Small delay to ensure command completes
        read_coil_status(address,MODBUS_SLAVE_ID)
        # Close the Modbus connection when done
        client.close()
        print("\nModbus connection closed.")
    else:
        print("\nCould not connect to Modbus device. Please check host, port, and device status.")
