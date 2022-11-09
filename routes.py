from flask import Flask, request
from app import App

class Routes():
    flask_app = Flask(__name__)
    application = App()
    
    ################Strategy#######################

    # route to add a strategy (with parameters)
    @flask_app.route("/add_simple", methods=['POST'])
    def add_strategy_simple():
        try:
            name = request.form['name']
            ticker = request.form['ticker']
            interval = float(request.form['interval'])
        except Exception as e:
            return str(e), 400

        # add the strategy to app
        return app.application.add_strategy_simple(name, ticker, interval)
    
    # route to add a strategy (with parameters)
    @flask_app.route("/add_rnn", methods=['POST'])
    def add_strategy_rnn():
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
        return app.application.add_strategy_RNN(name, ticker, interval, default)
    
    ###############################################

    # List all the strategies on the app
    @flask_app.route("/list_strategy", methods=['GET'])
    def list_strategy():
        return app.application.list_strategy()
    
    # List all workers on the app
    @flask_app.route("/list_worker", methods=['GET'])
    def list_worker():
        return app.application.list_worker()
    
    # Execute a estrategy
    @flask_app.route("/exec", methods=['POST'])
    def exec_strategy():
        strategy_name = request.form['strategy_name']
        worker_name = request.form['worker_name']
        return app.application.exec_strategy(strategy_name, worker_name)
    
    # Info of a worker
    @flask_app.route("/worker_info", methods=['POST'])
    def info_strategy():
        worker_name = request.form['name']
        return app.application.info_worker(worker_name)
    
    # Stop a strategy
    @flask_app.route("/stop", methods=['POST'])
    def stop_worker_strategy():
        worker_name = request.form['name']
        return app.application.stop_worker_strategy(worker_name)
    
    # Stop a strategy
    @flask_app.route("/start", methods=['POST'])
    def start_worker_strategy():
        worker_name = request.form['name']
        return app.application.start_worker_strategy(worker_name)
    
    # Worker status
    @flask_app.route("/status", methods=['POST'])
    def status_worker_strategy():
        worker_name = request.form['name']
        return app.application.status_worker_strategy(worker_name)

    # Delete a strategy
    @flask_app.route("/delete_strategy", methods=['POST'])
    def delete_strategy():
        strategy_name = request.form['name']
        return app.application.delete_strategy(strategy_name)
    
    # Delete a worker
    @flask_app.route("/delete_worker", methods=['POST'])
    def delete_worker_strategy():
        worker_name = request.form['name']
        return app.application.delete_worker(worker_name)

    # Stats of a worker
    @flask_app.route("/stats_worker", methods=['POST'])
    def stats_worker_strategy():
        worker_name = request.form['name']
        return app.application.stats_worker(worker_name)


if __name__ == '__main__':
    app = Routes()
    app.flask_app.run(host="0.0.0.0", debug=True, use_debugger=False, use_reloader=False)