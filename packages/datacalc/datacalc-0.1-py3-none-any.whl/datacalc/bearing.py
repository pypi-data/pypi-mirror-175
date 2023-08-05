import numpy as np
class bearing(object):
    def __init__(self, data1,data2):
        self.data1 = data1
        self.data2 = data2
    def bear(self):
        sum=np.add(self.data1,self.data2)
        return sum