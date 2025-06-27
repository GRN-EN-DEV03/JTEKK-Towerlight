from DataBaseModule.MSSQL.ms_sql import ms_db_connect

def insert_data() :
    try:
        data = ms_db_connect()
        table = '[JTEKK].[v_towerlight]'
        value =  "'1','Red'"
        data.connect_sql_insert(table,value)
    except Exception as e:
        print(f"An error occurred during select data : {e}")

def select_data() :
    try:
        data = ms_db_connect()
        table = '[JTEKK].[v_towerlight]'
        feild =  'Code,Name'
        data.connect_select(table,None,feild)
        for dat in data :
            pass
        return dat
    except Exception as e:
        print(f"An error occurred during select data : {e}")
        return (0,'ERROR')