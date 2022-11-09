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
    
    def get_info(self):
        info = {}
        info["exec"] = self.onExec
        return info

    def stats(self):
        orders = []

        f =open("Strategies/history.txt", "r")
        lines = f.readlines()
        print(lines)
        for elem in lines:
            order = json.loads(elem)
            if self.name == order[0]:
                orders.append(order[1])
        f.close()

        return orders

    # Worker Function
    def exec(self):
        while(True):
            try:
                str_order = self.strategy.strategy()
                if str_order.option == "stay":
                    print("stay")
                    print()
                else:
                    order = self.api.send_order(str_order)
                    print(order)
                    print()

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