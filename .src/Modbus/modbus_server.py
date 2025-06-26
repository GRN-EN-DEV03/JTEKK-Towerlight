# Import necessary classes from pymodbus
from pymodbus.server import StartTcpServer
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext, ModbusSparseDataBlock
import logging
import time

# --- Configuration for the Modbus Server ---
# The IP address the server will listen on (0.0.0.0 listens on all available interfaces)
SERVER_HOST = '0.0.0.0'
# The Modbus TCP port the server will listen on (default is 502)
SERVER_PORT = 502
# Slave ID (Unit ID) for this server (must match the client's MODBUS_SLAVE_ID)
SERVER_SLAVE_ID = 1

# --- Configure Logging (optional, but good for debugging) ---
logging.basicConfig()
log = logging.getLogger("pymodbus.server")
log.setLevel(logging.DEBUG) # Set to DEBUG to see detailed Modbus traffic

# --- Define Modbus Data Store ---
# ModbusSlaveContext holds the data for each type of Modbus register (coils, discrete inputs, holding registers, input registers)
# We will primarily focus on Holding Registers (hr) for this example, as your client writes to them.

# Initial values for holding registers.
# Addresses are 0-based in pymodbus.
# We'll initialize some registers for testing the client's writes.
# Example: register 0 will start at 100, register 1 at 200, etc.
# ModbusSparseDataBlock allows defining registers at specific addresses without defining all in between.
initial_holding_registers = {
    0: 100,
    1: 200,
    2: 300,
    3: 400,
    4: 500,
    5: 600, # This will be targeted by the single register write example in the client
    6: 700
}

# Create a data block for holding registers with initial values.
holding_registers_block = ModbusSparseDataBlock(initial_holding_registers)

# Create the slave context for a single slave ID.
# You can add other types of data blocks (coils, discrete inputs, input registers) if needed.
slave_context = ModbusSlaveContext(
    hr=holding_registers_block)

# Create the server context.
# If you have multiple slave IDs, you would pass a dictionary of slave_id:slave_context.
# For a single slave, you can pass it directly.
server_context = ModbusServerContext(slaves=slave_context, single=True)


# --- Main Server Start Function ---
def run_modbus_server():
    """
    Starts the Modbus TCP server.
    """
    print(f"Starting Modbus TCP Server on {SERVER_HOST}:{SERVER_PORT} for Slave ID {SERVER_SLAVE_ID}...")
    # StartTcpServer is a non-blocking function, it runs the server in the background.
    # It requires the server_context and the address to bind to.
    # The 'address' parameter should be a tuple (host, port).
    StartTcpServer(context=server_context, address=(SERVER_HOST, SERVER_PORT))
    print("Modbus TCP Server is running. Press Ctrl+C to stop.")

if __name__ == "__main__":
    # Ensure pymodbus is installed: pip install pymodbus
    # To run this server, open a terminal and execute: python your_server_script_name.py

    try:
        run_modbus_server()
        # Keep the main thread alive so the server can run in the background.
        # In a real application, you might have other tasks running here.
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nModbus TCP Server stopped by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
