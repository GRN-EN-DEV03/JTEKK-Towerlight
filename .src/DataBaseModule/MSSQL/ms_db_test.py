from ms_sql import ms_db_connect

table = "[dbo].[test_1]"

def insert_test() :
    data = ms_db_connect()
    #table = "[dbo].[test_1]"
    value = "'Tae', 12, '2025-04-12 17:00:00'" # removed the ()
    rows_inserted_direct = data.connect_sql_insert(table, value)
    if rows_inserted_direct > 0:
        print(f"Successfully inserted {rows_inserted_direct} rows using direct call.")
    else:
        print(f"Failed to insert data using direct call.")

def select_test() :
    data = ms_db_connect()
    data.connect_select(table,None,'*')
    for out in data :
        print(out)
        for op in out :
            print(op)
    pass

def update_test() :
    data = ms_db_connect()
    value = "name = 'Jaja'"
    condition = "user_id = 1"
    data.connect_update(table,value,condition)

def delete_test() :
    data = ms_db_connect()
    condition = "user_id = 8"
    data.connect_delete(table,condition)



#------------------
#insert_test()
#update_test()
#delete_test()
#------------------
select_test()