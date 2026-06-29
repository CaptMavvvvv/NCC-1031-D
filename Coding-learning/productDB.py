import sqlite3

def createtable():
    try:
        con = sqlite3.connect('productDB.db')
        sql = '''CREATE TABLE IF NOT EXISTS product (
            pid INT PRIMARY KEY NOT NULL,
            pname TEXT,
            totalA INT,
            totalB INT,
            pprice REAL
        );'''
        con.execute(sql)
        con.commit()
        sql = '''CREATE TABLE IF NOT EXISTS transfer (
            tid TEXT PRIMARY KEY NOT NULL,
            pid TEXT,
            pqty INT
        );'''
        con.execute(sql)
        con.commit()
    except sqlite3.Error as e:
        print("error is " + str(e))
    finally:
        if con:
            con.close()

def insertproducttable(*data):
    try:
        con = sqlite3.connect('productDB.db')
        sql = 'INSERT INTO product (pid, pname, totalA, totalB, pprice) VALUES (?, ?, ?, ?, ?)'
        con.execute(sql, (data[0], data[1], data[2], data[3], data[4]))
        con.commit()
        return True
    except sqlite3.Error as e:
        print("error is " + str(e))
        return False
    finally:
        if con:
            con.close()

def updateproducttable(*data):
    try:
        con = sqlite3.connect('productDB.db')
        sql = 'UPDATE product SET pname = ?, totalA = ?, totalB = ?, pprice = ? WHERE pid = ?'
        con.execute(sql, (data[1], data[2], data[3], data[4], data[0]))
        con.commit()
        return True
    except sqlite3.Error as e:
        print("error is " + str(e))
        return False
    finally:
        if con:
            con.close()

def selectproductid():
    try:
        con = sqlite3.connect('productDB.db')
        sql = 'SELECT pid FROM product ORDER BY pid'
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return [row[0] for row in data]
    except sqlite3.Error as e:
        print("error is " + str(e))
        return []
    finally:
        if con:
            con.close()

def selectallproducts():
    try:
        con = sqlite3.connect('productDB.db')
        sql = 'SELECT * FROM product ORDER BY pid'
        cur = con.cursor()
        cur.execute(sql)
        data = cur.fetchall()
        return data
    except sqlite3.Error as e:
        print("error is " + str(e))
        return []
    finally:
        if con:
            con.close()

def deleteproduct(pid):
    try:
        con = sqlite3.connect('productDB.db')
        sql = 'DELETE FROM product WHERE pid = ?'
        con.execute(sql, (pid,))
        con.commit()
        return True
    except sqlite3.Error as e:
        print("error is " + str(e))
        return False
    finally:
        if con:
            con.close()
