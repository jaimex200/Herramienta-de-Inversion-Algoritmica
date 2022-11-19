import requests
import json
from time import sleep

conn = 'http://127.0.0.1:5000/'

def add_strategy_rnn(name, ticker, interval, qty, default, units, epoch):
    url = conn + 'add_rnn'
    myobj = {'name': name, 'ticker': ticker, 'interval': interval, 'qty': qty, 'default': default, 'units': units, 'epoch': epoch}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Add strategy rnn ["+ name, ticker, interval, default, units, epoch + "]", "->", "ERROR")
        return res

    #print("Add strategy rnn ["+ name, ticker, interval, default, units, epoch + "]", "->", "PASS")
    return res

def add_strategy_simple(name, ticker, interval, qty):
    url = conn + 'add_simple'
    myobj = {'name': name, 'ticker': ticker, 'interval': interval, 'qty': qty}

    try:
        res = requests.post(url, data = myobj)
    except:
        ##print("Add strategy simple ["+ name, ticker, str(interval) + "]", "->", "ERROR")
        return res

    #print("Add strategy simple ["+ name, ticker, str(interval) + "]", "->", "PASS")
    return res

def list_strategy():
    url = conn + 'list_strategy'

    
    try:
        res = requests.get(url)
        l = json.loads(res.text)
    except:
        ##print("List strategy", "->", "ERROR")
        return res

    ##print("List strategy", "->", "PASS")
    return res

def list_worker():
    url = conn + 'list_worker'

    try:
        res = requests.get(url)
        l = json.loads(res.text)
    except:
        ##print("List worker", "->", "ERROR")
        return res

    ##print("List worker", "->", "PASS")
    return res

def exec_strategy(name, name_worker):

    url = conn + 'exec'
    myobj = {'strategy_name': name, 'worker_name': name_worker}

    try:
        res = requests.post(url, data = myobj)
    except:
        ##print("Exec strategy ["+ name, name_worker + "]", "->", "ERROR")
        return res

    ##print("Exec strategy ["+ name, name_worker + "]", "->", "PASS")
    return res

def stop_worker(name):
    url = conn + 'stop'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        ##print("Stop worker ["+ name + "]", "->", "ERROR")
        return res

    #print("Stop worker ["+ name + "]", "->", "PASS")
    return res

def start_worker(name):
    url = conn + 'start'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Start worker ["+ name + "]", "->", "ERROR")
        return res

    #print("Start worker ["+ name + "]", "->", "PASS")
    return res

def info_strategy(name):
    url = conn + 'strategy_info'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Info worker ["+ name + "]", "->", "ERROR")
        return res

    #print("Info worker ["+ name + "]", "->", "PASS")
    return res

def is_active_worker(name):

    url = conn + 'is_active'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Is active worker ["+ name + "]", "->", "ERROR")
        return res

    #print("Is active worker ["+ name + "]", "->", "PASS")
    return res

def delete_strategy(name):

    url = conn + 'delete_strategy'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Delete strategy ["+ name + "]", "->", "ERROR")
        return res

    #print("Delete strategy ["+ name + "]", "->", "PASS")
    return res

def delete_worker(name):

    url = conn + 'delete_worker'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Delete worker ["+ name + "]", "->", "ERROR")
        return res

    #print("Delete worker ["+ name + "]", "->", "PASS")
    return res

def stats_worker(name):

    url = conn + 'stats_worker'
    myobj = {'name': name}

    try:
        res = requests.post(url, data = myobj)
    except:
        #print("Stats worker ["+ name + "]", "->", "ERROR")
        return res

    #print("Stats worker ["+ name + "]", "->", "PASS")
    return res

name_strategy = "test_simple"
name_rnn_def = "test_rnn_def"
name_rnn_not_def = "test_rnn_not_def"
name_worker = "test_e"

ticker = "BTC-USD"

# Strategy simple 
if (add_strategy_simple(name_strategy, ticker, 1, 0.01).text == "OK"):
    print("===============> PASS")
else:
    print("===============> ERROR add strategy" )

if (add_strategy_simple(name_strategy, ticker, 1, 0.01).text == name_strategy + " is in use, try other name"):
    print("===============> PASS")
else:
    print("===============> ERROR repeat name")

if (add_strategy_simple("3", "-----", 1, 0.01).text == "Ticker: -----, its not found"):
    print("===============> PASS")
else:
    print("===============> ERROR bad ticker")

if (add_strategy_simple("4", ticker, -2, 0.01).text == "Interval must be more than 1 day"):
    print("===============> PASS")
else:
    print("===============> ERROR bad interval")

##########################################################################################################
if (add_strategy_rnn(name_rnn_def, ticker, 1, 0.01, True, 10, 200).text == "OK"):
    print("===============> PASS")
else:
    print("===============> ERROR default rnn")

if (add_strategy_rnn(name_rnn_not_def, ticker, 1, 0.01, False, 10, 10).text == "OK"):
    print("===============> PASS")
else:
    print("===============> ERROR not default")

if (add_strategy_rnn("1", "-----", 1, 0.01, False, 10, 10).text == "Ticker: -----, its not found"):
    print("===============> PASS")
else:
    print("===============> ERROR bad ticker")

if (add_strategy_rnn("2", ticker, -2, 0.01, False, 10, 10).text == "Interval must be more than 1 day"):
    print("===============> PASS")
else:
    print("===============> ERROR bad interval")

if (add_strategy_rnn("4", ticker, 1, 0.01, False, -3, 10).text == "Units (u) between 1 and 300, epoch (e) between 1 and 500"):
    print("===============> PASS")
else:
    print("===============> ERROR bad units")

if (add_strategy_rnn("5", ticker, 1, 0.01, False, 10, -3).text == "Units (u) between 1 and 300, epoch (e) between 1 and 500"):
    print("===============> PASS")
else:
    print("===============> ERROR bad units")

##########################################################################################################

if (list_strategy().ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR list strategy")

if (list_worker().ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR list worker")

##########################################################################################################

if (exec_strategy("-----", name_worker).text == "Strategy name dont exist"):
    print("===============> PASS")
else:
    print("===============> ERROR bad name")

if (exec_strategy(name_strategy, name_worker).ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR bad worker name")

##########################################################################################################

if (stop_worker(name_worker).text == "OK"):
    print("===============> PASS")
else:
    print("===============> ERROR stop worker")

if (stop_worker("----").text == "Worker doesnt exist"):
    print("===============> PASS")
else:
    print("===============> ERROR bad name")

##########################################################################################################

if (start_worker(name_worker).text == "OK"):
    print("===============> PASS")
else:
    print("===============> ERROR start worker")

if (start_worker("----").text == "Worker doesnt exist"):
    print("===============> PASS")
    stop_worker(name_worker)
else:
    print("===============> ERROR bad name")
    stop_worker(name_worker)

##########################################################################################################

if (info_strategy(name_strategy).ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR info worker")

if (info_strategy("----").text == "Strategy doesnt exist"):
    print("===============> PASS")
else:
    print("===============> ERROR bad name")

##########################################################################################################

if (is_active_worker(name_worker).ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR is active worker")

if (is_active_worker("----").text == "Worker doesnt exist"):
    print("===============> PASS")
else:
    print("===============> ERROR bad name")

##########################################################################################################

if (stats_worker(name_worker).ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR stats worker")

if (stats_worker("----").text == "Worker doesnt exist"):
    print("===============> PASS")
else:
    print("===============> ERROR bad name")

##########################################################################################################

if (delete_strategy(name_strategy).ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR delete strategy")

if (delete_strategy(name_strategy).ok != True):
    print("===============> PASS")
else:
    print("===============> ERROR delete strategy")

##########################################################################################################
add_strategy_simple(name_strategy, ticker, 1, 0.01)
exec_strategy(name_strategy, name_worker)
stop_worker(name_worker)

if (delete_worker(name_worker).ok == True):
    print("===============> PASS")
else:
    print("===============> ERROR delete worker")

if (delete_strategy(name_worker).ok != True):
    print("===============> PASS")
else:
    print("===============> ERROR delete worker")

##########################################################################################################
