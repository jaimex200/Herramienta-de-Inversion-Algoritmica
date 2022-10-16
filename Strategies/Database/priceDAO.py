import psycopg2

def openConnection():
    file = open("app.config", "r")
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

def infoToSQL (df, stock):
    # Abre conexion a bd y cursor
    conn = openConnection()
    cur = conn.cursor()

    try:
        cur.execute("CREATE TABLE daydata ( tid varchar(10), tdate TIMESTAMP, topen real, thigh real, tlow real, tclose real, tvolume bigint, tdivi real, tstocksplit integer, PRIMARY KEY (tid, tdate));")
        conn.commit()
    except psycopg2.errors.DuplicateTable:
        pass

    Open =          list(df.to_dict()['Open'].items())
    High =          list(df.to_dict()['High'].items())
    Low =           list(df.to_dict()['Low'].items())
    Close =         list(df.to_dict()['Close'].items())
    Volume =        list(df.to_dict()['Volume'].items())
    Dividends =     list(df.to_dict()['Dividends'].items())
    StockSplits =   list(df.to_dict()['Stock Splits'].items())  
    print(stock)
    # Insertar en base de datos
    for count in range(0, (len(Open))):
        try:
            cur.execute("Insert into dayData (tid, tdate, topen, thigh, tlow, tclose, tvolume, tdivi, tstocksplit) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                stock, Open[count][0], Open[count][1], High[count][1], Low[count][1], Close[count][1], Volume[count][1], Dividends[count][1], StockSplits[count][1]))
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
        except psycopg2.errors.NumericValueOutOfRange:
            print(stock, Open[count][0], Open[count][1], High[count][1], Low[count][1], Close[count][1], Volume[count][1], Dividends[count][1], StockSplits[count][1])
            conn.rollback()
        except:
            conn.rollback()

    cur.close()
    conn.close()