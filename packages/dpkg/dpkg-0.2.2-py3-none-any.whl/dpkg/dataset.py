import pickle
#import pyreadstat pyreadstat==1.1.9

class Khane:
    def __init__(self):
        with open(file='data/khane.pickle', mode='rb') as f:
            self.khane_ds = pickle.load(f)

    def load_data(self, datatype=None):
        if datatype is not None:    
            if datatype == 'main':
                target_ds, target_meta = self.khane_ds[0], self.khane_ds[1]
            elif datatype == 'ffq':
                target_ds, target_meta = self.khane_ds[2], self.khane_ds[3]
            elif datatype == 'rc24':
                target_ds, target_meta = self.khane_ds[4], self.khane_ds[5]
            elif datatype == 'oe':
                target_ds, target_meta = self.khane_ds[6], self.khane_ds[7]
            else:
                raise Exception('dataset type error~!!')
        else:
            target_ds, target_meta = self.khane_ds[0], self.khane_ds[1]
        return target_ds, target_meta