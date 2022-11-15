from time import sleep
import multiprocessing as mp
from api import Api
import uuid
import json

class WorkerStrategy():
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.api = Api()
        self.onExec = False

    def start(self):
        self.worker = mp.Process(target=self.exec)
        self.worker.start()
        self.onExec = True
    
    def stop(self):
        self.onExec = False
        self.worker.terminate()
        self.worker.join()
        self.worker.close()

    def stats(self):
        orders = []
        buy = 0
        sell = 0
        stay = 0

        f =open("Strategies/history.txt", "r")
        lines = f.readlines()
        for elem in lines:
            order = json.loads(elem)
            if self.name == order[0]:
                if order[1][2] == "buy":
                    buy += 1
                elif order[1][2] == "sell":
                    sell += 1
                else:
                    stay += 1
                orders.append(order[1])
        f.close()
        total = buy + sell + stay
        if buy != 0:
            buy = buy/total
        if sell != 0:
            sell = buy/total
        if stay != 0:
            stay = buy/total
        return [orders, {"buy": buy, "sell": sell, "stay": stay}]

    # Worker Function
    def exec(self):
        while(True):
            try:
                str_order = self.strategy.strategy()
                if str_order.option == "stay":
                    pass
                else:
                    order = self.api.send_order(str_order)

                f =open("Strategies/history.txt", "a")
                while (True):
                    if f.writable:
                        f.write(json.dumps([self.name, str_order.toList()]) + "\n")
                        break
                f.close()
                sleep(self.strategy.interval)
            except Exception as e:
                print("ERROR")
                print(e)