
import matplotlib.pyplot as plt
from Strategies.Training.EnumTrainPrice import EnumTrainPrice as et
import statistics

class dataStructure:
    # x -> numero de elementos al entrenar
    # y -> numero de elementos a mirar si es correcto el entrenamiento
    def __init__(self, x, y, train_price):
        self.train_vec = []
        self.correction_vec = []
        self.days_x = x
        self.days_y = y
        self.train_price = int(train_price)

    # Funcion para confirmar tendencias
    def print_vec(self, vec_x, vec_y):
        plt.clf()

        #plt.figure(figsize=(12,6))
        plt.plot(vec_x + vec_y)
        plt.show()

    def correction_max_min(self, max_y, min_y, next_vec, vec):
        buy = [1,0,0]
        sell = [0,1,0]
        stay = [0,0,1]

        # Tendencia alcista
        if max_y and not min_y:
            #print("tendencia alcista")
            #self.print_vec(vec, next_vec)
            return buy
        
        # Tendencia bajista
        if not max_y and min_y:
            
            #print("tendencia bajista")
            #self.print_vec(vec, next_vec)
            return sell
        
        # Acumulacion
        if not max_y and not min_y:
            #print("Acumulacion")
            #self.print_vec(vec, next_vec)
            return stay
        
        # Ruptura de acumulacion 
        if max_y and min_y:
            for elem in next_vec:
                if elem == max(next_vec):
                    max_first = True
                    #print("Ruptura acumulacion vendo")
                    #self.print_vec(vec, next_vec)
                    return sell
                    break
                if elem == min(next_vec):
                    max_first = False
                    #print("Ruptura acumulacion compro")
                    #self.print_vec(vec, next_vec)
                    return buy
                    break 
        
        return stay
    
    def vec_correction_peaks(self, vec, next_vec, max_price, min_price):
        
        
        if max_price < max(next_vec):
            max_y = True
        else:
            max_y = False
        
        if min_price > min(next_vec):
            min_y = True
        else:
            min_y = False
        
        #print("Antes", max_price, min_price)
        #print("Despues", max(next_vec), min(next_vec))
        return self.correction_max_min(max_y, min_y, next_vec, vec)
        
    def cast_elem(self, elem):
        return elem[self.train_price-2]
    
    def vec_correction_peaks_short(self, vec, next_vec):
        buy = 1.0
        sell = -1.0
        stay = 0.0

        vec_cast = list(map(self.cast_elem, vec))
        next_vec_cast = list(map(self.cast_elem, next_vec))
        if len(vec_cast) == 0:
            vec_max = 0
            vec_min = 0
        else: 
            vec_max = max(vec_cast)
            vec_min = min(vec_cast)

        if len(next_vec_cast) == 0:
            next_vec_max = 0
            next_vec_min = 0
        else:
            next_vec_max = max(next_vec_cast)
            next_vec_min = min(next_vec_cast)

        if vec_max < next_vec_max:
            max_y = True
        else:
            max_y = False
        
        if vec_min > next_vec_min:
            min_y = True
        else:
            min_y = False
        
        return self.correction_max_min(max_y, min_y, next_vec_cast, vec_cast)

    def create_data(self, data):
        price_vec = []
        price_vec_aux = []

        days_left = 0
        elem_pos = 0
        max_price = 0
        min_price = 999999999
        for elem in data:
            if days_left == self.days_x:
                # añadir vector correccion
                res = self.vec_correction_peaks(price_vec_aux, [e[self.train_price] for e in data[elem_pos:elem_pos + self.days_y]], max_price, min_price)
                self.correction_vec.append(res)

                price_vec.append(price_vec_aux)
                days_left = 0
                max_price = 0
                min_price = 999999999
                price_vec_aux = []

            if max_price < elem[self.train_price]:
                max_price = elem[self.train_price]
            
            if elem[self.train_price] < min_price:
                min_price = elem[self.train_price]

            price_vec_aux.append(elem[self.train_price])
            days_left += 1
            elem_pos += 1
        
        self.train_vec = price_vec

    
    def data_to_list(self, data):
        price_vec = []
        price_vec_aux = []
        volume_vec = []

        for elem in data:
            price_vec_aux.append(elem[int(et.CLOSE)])
            price_vec_aux.append(elem[int(et.HIGH)])
            price_vec_aux.append(elem[int(et.LOW)])
            price_vec_aux.append(elem[int(et.OPEN)])
            price_vec_aux.append(elem[int(et.VOLUME)])
            volume_vec.append(elem[int(et.VOLUME)])
            price_vec.append(price_vec_aux)
            price_vec_aux = []
        
        self.volume_vec = volume_vec

        self.volume_avg = statistics.mean(self.volume_vec)
        self.volume_std_des = statistics.pstdev(self.volume_vec)

        return price_vec
    
    def create_data_for_one_day(self, data):
        data_list = self.data_to_list(data)
        correction_list = []
        elem_pos = 0

        for elem in data_list:

            res = self.vec_correction_peaks_short(data_list[elem_pos-self.days_x:elem_pos], data_list[elem_pos:elem_pos+self.days_y])
            correction_list.append(res)
            elem_pos += 1
        
        self.train_vec = data_list
        self.correction_vec = correction_list
    
    def norm_func(self, elem):
        #normalizar 
        norm_vec_aux = []
        
        try:
            elem[0] = (elem[0] - elem[3]) / elem[3]
            elem[1] = (elem[1] - elem[3]) / elem[3]
            elem[2] = (elem[2] - elem[3]) / elem[3]
            
        except: 
            elem[0] = 0
            elem[1] = 0
            elem[2] = 0
        
        try:
            elem[4] = (elem[4] - self.volume_avg) / self.volume_std_des
        except:
            elem[4] = 0

        norm_vec_aux.append(elem[0])
        norm_vec_aux.append(elem[1])
        norm_vec_aux.append(elem[2])
        norm_vec_aux.append(elem[4])

        return norm_vec_aux

    def create_data_for_one_day_norm(self, data):
        data_list = self.data_to_list(data)
        correction_list = []
        elem_pos = 0
        
        
        for elem in data_list:

            res = self.vec_correction_peaks_short(data_list[elem_pos-self.days_x:elem_pos], data_list[elem_pos:elem_pos+self.days_y])
            correction_list.append(res)
            elem_pos += 1
        
        
        self.train_vec = list(map(self.norm_func, data_list))
        self.correction_vec = correction_list

    def create_tridimensional_matrix(self, lenght):
        pos = 0
        tridimensional_vec = []
        correction_vec = []
        vec_aux = []
        max_pos = len(self.train_vec)

        for elem in self.train_vec:
            vec_aux = []
            if max_pos <= pos + lenght:
                break
            for elem2 in self.train_vec[pos:pos + lenght]:
                vec_aux.append(elem2)
            tridimensional_vec.append(vec_aux)
            correction_vec.append(self.correction_vec[pos + lenght])
            pos += 1

        self.train_vec = tridimensional_vec
        self.correction_vec = correction_vec
    
    def data_to_list_eva(self, data):
        price_vec = []
        price_vec_aux = []

        Open =          list(data.to_dict()['Open'].items())
        High =          list(data.to_dict()['High'].items())
        Low =           list(data.to_dict()['Low'].items())
        Close =         list(data.to_dict()['Close'].items())
        Volume =        list(data.to_dict()['Volume'].items())

        for count in range(0, (len(Open))):
            price_vec_aux.append(Close[count][1])
            price_vec_aux.append(High[count][1])
            price_vec_aux.append(Low[count][1])
            price_vec_aux.append(Open[count][1])
            price_vec_aux.append(Volume[count][1])
            price_vec.append(self.norm_func(price_vec_aux))
            price_vec_aux = []

        return price_vec

    def create_tridimensional_matrix_evaluate(self, data):
        data_list_to_eval = self.data_to_list_eva(data)
        return data_list_to_eval

