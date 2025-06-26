import UNIT_DB.unit_db as ut
import Modbus.modbus_write as tcp_write
import os
import time

ADDRESS_ID = 5
SLAVE_ID = 1

def get_color_request() :
    request = ut.select_data()
    print("INPUT -----------------------------------------------------")
    print("Request Code : ",request[0])
    print("Request Color : ",request[1])
    print("-----------------------------------------------------------")
    if tcp_write.read_holding_register(ADDRESS_ID,SLAVE_ID) != request[0] :
        tcp_write.main_write_register(ADDRESS_ID,request[0],SLAVE_ID)
    else :
        os.system('cls')
        time.sleep(1)

if __name__ == "__main__" : 
    while True : 
        get_color_request()