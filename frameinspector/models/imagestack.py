import numpy as np
import fabio
import glob

class imageStack(object):
    def __init__(self):
        self.fns = []
    def load(self, fnp):
        if fnp[:7] == 'file://':
            fnp = fnp[7:]
        fns = glob.glob(fnp)
        if len(fns) > 0:
            fns.sort()
            self.fns = fns
            myshape = fabio.open(self.fns[0]).data.shape
            dat = []
            for f in fns:
                _ = fabio.open(f).data
                if _.shape == myshape:
                    dat.append(_)
                else:
                    print("skipping {} because it has different shape!".format(f))
            self.dat = np.stack(dat)
    def get_sum(self):
        if len(self.fns) > 0:
            return self.dat.sum(axis=0)
        else:
            return None
