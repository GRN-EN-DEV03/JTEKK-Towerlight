import UNIT_DB.unit_db as ut
import Modbus.modbus_write as tcp_modbus
import os
import time

ADDRESS_ID = [5,6,7]
SLAVE_ID = 1

def get_color_request() :

    ''' 

        Select Data form NETCUBE Request Table to control Towerlight via ADAM   
    
    '''
    # Select Data from Request Table [v_towerlight]
    request = ut.select_data()
    # Show Data from Request  Code (1,2,3) and Color (Red,Yellow,Green)
    # 1 : [1,0,0]
    # 2 : [0,1,0]
    # 3 : [0,0,1]

    print("INPUT -----------------------------------------------------")
    print("Request Code : ",request[0])
    print("Request Color : ",request[1])
    print("-----------------------------------------------------------")
    # If the Request is update Send modbus data to write register following the request
    #tcp_modbus.main_write_register(ADDRESS_ID[request[0]-1],[False],SLAVE_ID)
    if tcp_modbus.read_coil_status(ADDRESS_ID[request[0]-1],SLAVE_ID) : 
        return
    else :   
        for adr_data in ADDRESS_ID : 
            if str(adr_data) == str(ADDRESS_ID[request[0]-1]) : 
                print(str(adr_data)+" : "+ str(ADDRESS_ID[request[0]-1]))
                print("True")
                tcp_modbus.main_write_register(adr_data,[True],SLAVE_ID)
            else :
                print("False")
                tcp_modbus.main_write_register(adr_data,[False],SLAVE_ID)

if __name__ == "__main__" : 
    # Infinity loop to check the request 
    while True : 
        get_color_request()
        time.sleep(1)