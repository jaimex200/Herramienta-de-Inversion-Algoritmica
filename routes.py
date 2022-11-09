from flask import Flask, request
from app import App
import time

class Routes():
    flask_app = Flask(__name__)
    application = App()
    
    ################Strategy#######################

    # route to add a strategy (with parameters)
    @flask_app.route("/add_simple", methods=['POST'])
    def add_strategy_simple():
        inicio = time.time()
        try:
            name = request.form['name']
            ticker = request.form['ticker']
            interval = float(request.form['interval'])
        except Exception as e:
            return str(e), 400

        # add the strategy to app
        res = app.application.add_strategy_simple(name, ticker, interval)
        fin = time.time()
        print("add_strategy_simple", fin-inicio)
        return res
    
    # route to add a strategy (with parameters)
    @flask_app.route("/add_rnn", methods=['POST'])
    def add_strategy_rnn():
        inicio = time.time()
        try:
            name = request.form['name']
            ticker = request.form['ticker']
            interval = float(request.form['interval'])

            
            default = True if request.form['default'] == "True" else False
            if not default:
                units = int(request.form['units'])
                epoch = int(request.form['epoch'])

                return app.application.add_strategy_RNN(name, ticker, interval, default, units=units, epoch=epoch)
        except Exception as e:
            return str(e), 400

        # add the strategy to app
        res = app.application.add_strategy_RNN(name, ticker, interval, default)
        fin = time.time()
        print("add_strategy_rnn", fin-inicio)
        return res
    
    ###############################################

    # List all the strategies on the app
    @flask_app.route("/list_strategy", methods=['GET'])
    def list_strategy():
        inicio = time.time()
        res = app.application.list_strategy()
        fin = time.time()
        print("list_strategy", fin-inicio)
        return res
    
    # List all workers on the app
    @flask_app.route("/list_worker", methods=['GET'])
    def list_worker():
        inicio = time.time()
        res = app.application.list_worker()
        fin = time.time()
        print("list_worker", fin-inicio)
        return res
    
    # Execute a estrategy
    @flask_app.route("/exec", methods=['POST'])
    def exec_strategy():
        inicio = time.time()
        strategy_name = request.form['strategy_name']
        worker_name = request.form['worker_name']
        res = app.application.exec_strategy(strategy_name, worker_name)
        fin = time.time()
        print("exec_strategy", fin-inicio)
        return res
    
    # Info of a worker
    @flask_app.route("/worker_info", methods=['POST'])
    def info_strategy():
        inicio = time.time()
        worker_name = request.form['name']
        res = app.application.info_worker(worker_name)
        fin = time.time()
        print("info_strategy", fin-inicio)
        return res
    
    # Stop a strategy
    @flask_app.route("/stop", methods=['POST'])
    def stop_worker_strategy():
        inicio = time.time()
        worker_name = request.form['name']
        res = app.application.stop_worker_strategy(worker_name)
        fin = time.time()
        print("stop_worker_strategy", fin-inicio)
        return res
    
    # Stop a strategy
    @flask_app.route("/start", methods=['POST'])
    def start_worker_strategy():
        inicio = time.time()
        worker_name = request.form['name']
        res = app.application.start_worker_strategy(worker_name)
        fin = time.time()
        print("start_worker_strategy", fin-inicio)
        return res
    
    # Worker status
    @flask_app.route("/is_active", methods=['POST'])
    def status_worker_strategy():
        inicio = time.time()
        worker_name = request.form['name']
        res = app.application.is_active_worker_strategy(worker_name)
        fin = time.time()
        print("status_worker_strategy", fin-inicio)
        return res

    # Delete a strategy
    @flask_app.route("/delete_strategy", methods=['POST'])
    def delete_strategy():
        inicio = time.time()
        strategy_name = request.form['name']
        res = app.application.delete_strategy(strategy_name)
        fin = time.time()
        print("delete_strategy", fin-inicio)
        return res
    
    # Delete a worker
    @flask_app.route("/delete_worker", methods=['POST'])
    def delete_worker_strategy():
        inicio = time.time()
        worker_name = request.form['name']
        res = app.application.delete_worker(worker_name)
        fin = time.time()
        print("delete_worker_strategy", fin-inicio)
        return res

    # Stats of a worker
    @flask_app.route("/stats_worker", methods=['POST'])
    def stats_worker_strategy():
        inicio = time.time()
        worker_name = request.form['name']
        res = app.application.stats_worker(worker_name)
        fin = time.time()
        print("stats_worker_strategy", fin-inicio)
        return res


if __name__ == '__main__':
    app = Routes()
    app.flask_app.run(host="0.0.0.0", debug=True, use_debugger=False, use_reloader=False)