from time import sleep
import multiprocessing as mp
from api import Api
import uuid

class WorkerStrategy():
    def __init__(self, name, strategy):
        self.name = name
        self.strategy = strategy
        self.api = Api()
        self.onExec = False
        self.id = uuid.uuid4()

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

    # Worker Function
    def exec(self):
        while(True):
            try:
                str_order = self.strategy.strategy()
                if str_order == "stay":
                    print("stay")
                    print()
                else:
                    order = self.api.send_order(str_order)
                    print(order)
                    print()

                sleep(self.strategy.interval)
            except Exception as e:
                print("ERROR")
                print(e)