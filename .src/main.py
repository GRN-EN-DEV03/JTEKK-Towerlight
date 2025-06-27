import UNIT_DB.unit_db as ut
import Modbus.modbus_write as tcp_write
import os
import time

ADDRESS_ID = 5
SLAVE_ID = 1

def get_color_request() :

    ''' 
    
        Select Data form NETCUBE Request Table to control Towerlight via ADAM   
    
    '''

    # Select Data from Request Table [v_towerlight]
    request = ut.select_data()
    # Show Data from Request  Code (1,2,3) and Color (Red,Yellow,Green)
    print("INPUT -----------------------------------------------------")
    print("Request Code : ",request[0])
    print("Request Color : ",request[1])
    print("-----------------------------------------------------------")
    # If the Request is update Send modbus data to write register following the request
    if tcp_write.read_holding_register(ADDRESS_ID,SLAVE_ID) != request[0] :
        tcp_write.main_write_register(ADDRESS_ID,request[0],SLAVE_ID)
    else :
        os.system('cls')
        time.sleep(1)

# Test
if __name__ == "__main__" : 
    # Infinity loop to check the request 
    while True : 
        get_color_request()