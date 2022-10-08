import psycopg2

def openConnection():
    file = open("db.config", "r")
    lines = file.readlines()

    data = list(map( lambda x: x.strip("\n").split("="), lines))

    host_db     = data[0][1]
    user_db     =  data[1][1]
    ps_db       = data[2][1]
    name_db     = data[3][1]

    return psycopg2.connect( host=host_db, user=user_db, password=ps_db, dbname=name_db)

def getDayData(id):
    conn = openConnection()
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("select * from daydata where tid = %s;", (id,))

    result = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return result

def getMinData(id):
    conn = openConnection()
    conn.autocommit = True
    cur = conn.cursor()
    
    cur.execute("select * from mindata where tid = %s;", (id,))

    result = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    return result