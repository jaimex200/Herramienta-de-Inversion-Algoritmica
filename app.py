from api import Api
from Strategies.strategySimple import StrategySimple
from Strategies.strategyRNN import StrategyRNN
from workerStrategy import WorkerStrategy
import json


class App():

    def __init__(self):
        # Informacion de la app
        self.strategy_map = {}
        self.workers_map = {}
        self.api = Api()
        

    #####################STRATEGIES##############################
    def add_strategy_simple(self, name, ticker, interval, qty):
        if (name in self.strategy_map.keys()):
            return name + " is in use, try other name", 400 
        if ("," in name):
            return "Not allow to use , in names", 400
        if (interval < 1):
            return "Interval must be more than 1 day", 400
        if (qty <= 0):
            return "Quantity must be more than 0", 400
 
        try:
            self.strategy_map[name] = StrategySimple(name, ticker, interval, qty)
        except  NameError as ne:
            return "Ticker: " + ne.args[0] + ", its not found", 400

        return "OK", 200
    

    def add_strategy_RNN(self, name, ticker, interval, qty, default, units = -1, epoch = -1):
        if (name in self.strategy_map.keys()):
            return name + " is in use, try other name", 400 
        if ("," in name):
            return "Not allow to use , in names", 400
        if (interval < 1):
            return "Interval must be more than 1 day", 400
        if (qty <= 0):
            return "Quantity must be more than 0", 400

        try:
            if default:
                self.strategy_map[name] = StrategyRNN(name, ticker, interval, qty)
            else:
                self.strategy_map[name] = StrategyRNN(name, ticker, interval, qty, u=units, e=epoch)
        except  NameError as ne:
            return "Ticker: " + ne.args[0] + ", its not found", 400
        except Exception as e:
            return str(e), 500

        return "OK", 200

    #############################################################

    # List of strategies (return list json)
    def list_strategy(self):
        return json.dumps(list(self.strategy_map.keys())), 200
    
    # List of workers (return list json)
    def list_worker(self):
        return json.dumps(list(self.workers_map.keys())), 200
    
    # Create and execute a worker
    def exec_strategy(self, strategy_name, worker_name):

        if (self.workers_map.get(worker_name, False)):
            return "Worker exist", 400

        if (not self.strategy_map.get(strategy_name, False)):
            return "Strategy name dont exist", 400

        self.workers_map[worker_name] = WorkerStrategy(worker_name, self.strategy_map[strategy_name])
        self.workers_map[worker_name].start()
        return "OK", 200

    # Info worker
    def info_strategy(self, name):
        if (not self.strategy_map.get(name, False)):
            return "Strategy doesnt exist", 400
        strategy = self.strategy_map[name]
        return json.dumps(strategy.get_info()), 200
    
    # Stop a worker
    def stop_worker_strategy(self, name):
        if (not self.workers_map.get(name, False)):
            return "Worker doesnt exist", 400
        if (self.workers_map[name].onExec == True):
            self.workers_map[name].stop()
        else:
            return "Is stop", 200
        return "OK", 200
    
    # Stop a worker
    def start_worker_strategy(self, name):
        if (not self.workers_map.get(name, False)):
            return "Worker doesnt exist", 400
        if (self.workers_map[name].onExec == False):
            self.workers_map[name].start()
        else:
            return "is running", 200
        return "OK", 200
    
    def is_active_worker_strategy(self, name):
        if (not self.workers_map.get(name, False)):
            return "Worker doesnt exist", 400

        return str(self.workers_map[name].onExec), 200

    def delete_strategy(self, name):
        if (not self.strategy_map.get(name, False)):
            return "Strategy doesnt exist", 400

        workers = self.workers_map.values()
        list_workers = []

        for w in workers:
            if (w.strategy.name == name):
                list_workers.append(w.name)
                
        for ele in list_workers:
            self.delete_worker(ele)
        
        self.strategy_map.pop(name, False)

        return "OK", 200

    def delete_worker(self, name):
        worker = self.workers_map.pop(name, False)
        if (worker):
            try:
                worker.stop()
            except:
                pass
            return "OK", 200
        else:
            return "Worker doesnt exist", 400
    
    def stats_worker(self, name):
        worker = self.workers_map.get(name, False)
        if (worker):
            ret = worker.stats()
            return json.dumps(ret), 200
        else:
            return "Worker doesnt exist", 400
        