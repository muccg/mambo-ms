from mamboms.mambomsapp.models import Compound, Point

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math

class SpectraGraph:
    def __init__(self, compound):
        self.compound = compound
        self.labelthreshold = 0.01
        print 'Initing labelsOn to False'
        self.labelsOn = False
        self.create_bar_graph()
        self._px_ratio = None
        self._xstart = self._xend = None
        self.set_newdatarange(self.mindata, self.maxdata)

    def create_bar_graph(self):
        self.figure = plt.figure(figsize=(7,3))
        self.ax = self.figure.add_subplot(111)
        self.rects = self.ax.bar(self.compound.xs, self.compound.ys, color="red", align='center')
                
        t = self.compound.name
        if len(t) > 60:
            lt = len(t)
            title = t[0:25] + '  ...  ' + t[lt-25:]
        else:
            title = t
        self.ax.set_title(title)
        
        #create labels
        print 'labelsOn - ', self.labelsOn
        #create a label subplot
        self.labels = []

        print dir(self.ax)
        for rect in self.rects:
            print 'labelling'
            height = rect.get_height()
            self.labels.append(self.ax.text(rect.get_x()+rect.get_width()/2., height + 30, '%d'%(height), ha='center', va='bottom' ) )
       
        #now, remove them all:
        for l in self.labels:
            self.ax.texts.remove(l)

    def enable_labels(self, state):
        dir(self.ax)
        if state:
            self.labelsOn = True
            for l in self.labels:
                self.ax.texts.append(l)
        else:
            self.labelsOn = False
            for l in self.labels:
                try:
                    self.ax.texts.remove(l)
                except:
                    #happens when we remove a label that isnt there.
                    #no big deal. 
                    pass

    @property
    def px_ratio(self):
        if self._px_ratio is None:
            # TODO 700px hardcoded
            self._px_ratio = self.figure.canvas.get_width_height()[0] / 700.0 
        return self._px_ratio

    @property
    def mindata(self):
        return math.ceil(self.ax.xaxis.get_data_interval()[0])

    @property
    def maxdata(self):
        return math.floor(self.ax.xaxis.get_data_interval()[1])

    @property
    def datastart(self):
        return math.floor(self.ax.xaxis.get_view_interval()[0])

    @property
    def dataend(self):
        return math.ceil(self.ax.xaxis.get_view_interval()[1])

    @property
    def datarange(self):
        return self.dataend - self.datastart

    @property
    def xstart(self):
        if self._xstart is None:
            self._xstart = int(self.ax.transData.transform_point([self.datastart, 0])[0])
        return self._xstart

    @property
    def xend(self):
        if self._xend is None:
            self._xend = int(self.ax.transData.transform_point([self.dataend, 0])[0])
        return self._xend

    def matplot_to_real_pixel(self, matplot_pixel):
        return matplot_pixel / self.px_ratio

    def real_to_matplot_pixel(self, real_pixel):
        return real_pixel * self.px_ratio

    def zoom_to(self, newxstart, newxend):
        newxstart = self.real_to_matplot_pixel(newxstart)
        newxend = self.real_to_matplot_pixel(newxend)

        data_range = self.dataend - self.datastart
        x_range = self.xend - self.xstart
        relative_xstart = newxstart - self.xstart
        relative_xend = newxend - self.xstart
        
        newdatastart = math.floor( self.datastart + relative_xstart * data_range / x_range )
        newdataend   = math.ceil ( self.datastart + relative_xend   * data_range / x_range )

        self.set_newdatarange(newdatastart, newdataend)
        
    def set_newdatarange(self, datastart, dataend):
        aymin, aymax = self.ax.get_ylim()
        self.ax.axis([ 
            float(max(datastart, self.mindata)), 
            float(min(dataend, self.maxdata)), 
            aymin, aymax
        ])
        self.labelTest(datastart, dataend)

    def move_left(self):
        newdatastart = max(self.datastart - self.datarange, self.mindata)
        newdataend = newdatastart + self.datarange
        self.set_newdatarange(newdatastart,newdataend)

    def move_right(self):
        newdataend = min(self.dataend + self.datarange, self.maxdata)
        newdatastart = newdataend - self.datarange
        self.set_newdatarange(newdatastart, newdataend)

    def to_imageinfo(self):
        return {
            'compoundId': self.compound.id,
            'datastart': int(self.datastart),
            'dataend':  int(self.dataend),
            'xstart': int(self.matplot_to_real_pixel(self.xstart)),
            'xend': int(self.matplot_to_real_pixel(self.xend))
        }

    def labelTest(self, datastart, dataend ):
        #Turn on labels if we are less than 10% of the total data range
        newdatarange = dataend - datastart
        total_data_range = self.maxdata - self.mindata
        ratio_of_total = newdatarange / total_data_range
        if ratio_of_total < self.labelthreshold:
            print 'Turning Labels On:'
            self.enable_labels(True) 
        else:
            print 'Turning Labels Off'
            self.enable_labels(False)
        print 'Ratio: ', ratio_of_total, 'labelsOn: ', self.labelsOn


    def write(self, stream):
        self.figure.savefig(stream)


