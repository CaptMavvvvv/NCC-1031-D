import sqlite3

def createtable():
    try:
        con = sqlite3.connect('produtDB.db')
        sql = 'CREATE TABLE IF NOT EXISTS product'\
            '(pid INT PRIMARY KEY NOT NULL,'\
            'pname TEXT, totalA INT, totalB INT,'\
            'pprice REAL);'
        con.execute(sql)
        con.commit()
        sql = 'CREATE TABLE IF NOT EXISTS transfer'\
                '(tid TEXT PRIMARY KET NOT NULL.'\
                'pid TEXT, pqty INT);'
        con.execute(sql)
        con.commit()
    except con.Error as e:
        if con:
            print("error is " + e)
    con.close()

def insertproducttale(*data):
    try:
        con = sqlite3.connect('productDB.db')
        sql = 'INSERT INTO product (pid, pname, totalA, totalB)'\
            'VALUES ("'+ data[0] + '","'+ data[1] + '",'+\
            str(data[2]) + ',' + str(data[3]) +')'
        con.execute(sql)
        con.commit()
        return True
    except con.Error as e:
        if con:
            print("error is " + e)
            return False
    con.close()

