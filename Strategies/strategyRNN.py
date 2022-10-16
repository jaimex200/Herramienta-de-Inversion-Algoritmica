
from Strategies.strategy import Strategy
from order import Order
from Strategies.Training.dataStructure import dataStructure as DataStructure
from Strategies.Training.EnumTrainPrice import EnumTrainPrice
from Strategies.Information.GetData import get_data as get_data
import Strategies.Database.priceDAO as priceDAO
import keras
import keras.utils
import keras.optimizers
from keras import backend as K
from keras.layers import Dense, LSTM
from tensorflow import keras as keras_tf
import tensorflow as tf
import yfinance as yf
from datetime import datetime
from datetime import datetime, timedelta


class StrategyRNN(Strategy):
    # poder pasar vcalores ########### IMP ############
    def __init__(self, name, ticker, interval, d_x = 15, d_y = 5, d_m = 30, u = 100, e = 250):
        super().__init__(name, ticker, interval)
        # Add to db data to train
        file = open("db.config", "r")
        lines = file.readlines()
        data = list(map( lambda x: x.strip("\n").split("="), lines))
        num_days      = int(data[4][1])
        start_date      = (datetime.now() - timedelta(num_days)).strftime('%Y-%m-%d')
        end_date        = datetime.now().strftime('%Y-%m-%d')

        stockData = self.get_data(ticker, start_date=start_date, end_date=end_date)
        priceDAO.infoToSQL(stockData, ticker)


        ## Create rnn and train

        ## Values to the correction matrix, take x days and see y days to correct
        days_x = d_x
        days_y = d_y
        ###
        ## Indicates the number of days that the RNN uses to train 
        self.days_matrix = d_m
        ###

        if d_x <= 0 or d_y <= 0 or d_x > 40 or d_y > 30 or u <= 0 or u > 300 or e <= 0 or e > 500:
            raise Exception("Units (u) between 1 and 300, epoch (e) between 1 and 500")
        ## Percentaje that the RNN use to train and test
        ptrain = 0.8

        ########### RNN DATA CREATION ###########
        self.dataStructure = DataStructure(days_x, days_y, EnumTrainPrice.CLOSE)
        self.dataStructure.create_data_for_one_day_norm(priceDAO.getDayData(ticker))
        
        self.dataStructure.create_tridimensional_matrix(self.days_matrix)

        div_test = int(len(self.dataStructure.train_vec) * ptrain)

        # Train vec and correction
        train_vec = self.dataStructure.train_vec[:div_test]
        correction_train_vec = self.dataStructure.correction_vec[:div_test]

        # Test vec and correction
        test_vec = self.dataStructure.train_vec[div_test:]
        correction_test_vec = self.dataStructure.correction_vec[div_test:]
        ##########################################

        ############## RNN CREATION ##############
        units = u
        L1 = 0.00002
        L2 = 0.00002
        epoch = e
        batch = 10
        ###

        # Model
        K.clear_session()
        model = keras.Sequential()
        model.add(LSTM(units, activation='tanh', kernel_regularizer=keras.regularizers.l1_l2(l1=L1, l2=L2), recurrent_regularizer=keras.regularizers.l1_l2(l1=L1, l2=L2), input_shape=(self.days_matrix, 4), return_sequences=False, stateful=False, unroll=False))
        model.add(Dense(3, kernel_regularizer=keras.regularizers.l1_l2(l1=L1, l2=L2), activation='softmax'))

        model.compile(loss='binary_crossentropy', optimizer=keras_tf.optimizers.Adam(), metrics=['accuracy'])

        model.fit(train_vec, correction_train_vec, epochs=epoch, batch_size=batch, validation_data = (test_vec, correction_test_vec))

        ##########################################
        ## Guardar modelo
        self.model_path = "Strategies/Models/" + self.name + ".h5"
        model.save(self.model_path)
    
    def get_data(self, ticker, start_date, end_date):
        try:
            tickerData = yf.Ticker(ticker)

            stock_data = tickerData.history(period = 'id', start = start_date, end = end_date, interval="1d")
        except:
            self.get_data(ticker, start_date, end_date)
        return stock_data

    def strategy(self):
        K.clear_session()
        print("1", self.model_path)
        model = keras.models.load_model(self.model_path)
        print("2")
        start_date = datetime.now() - timedelta(self.days_matrix - 1)  
        end_date = datetime.now() 
        data = self.get_data(self.ticker, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        data_to_eval = self.dataStructure.create_tridimensional_matrix_evaluate(data)
        print("3")
        evaluation = model.predict([data_to_eval])[0]
        print(evaluation)
        maxNum = max(evaluation)
        if evaluation[0] == maxNum:
            return Order(0.01, self.ticker, "buy")
        if evaluation[1] == maxNum:
            return Order(0.01, self.ticker, "sell")
        if evaluation[2] == maxNum:
            return Order(0, self.ticker, "stay")