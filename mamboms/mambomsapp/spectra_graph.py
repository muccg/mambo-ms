from mamboms.mambomsapp.models import Compound, Point
import graph_labels as labels

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math


class SpectraGraph:
    @staticmethod
    def build_graph(spectrum):
        graph = SpectraGraph(spectrum)
        graph.initialize()
        return graph

    @staticmethod
    def build_map_graph(spectrum):
        graph = SpectraGraph(spectrum, 
                    figsize          = (9,1.5), 
                    show_title       = False, 
                    show_bar_labels  = False, 
                    axis_labels_size = 8)
        graph.initialize()
        return graph

    @staticmethod
    def build_head_to_tail_graph(spectrum, candidate = []):
        graph = SpectraGraph(spectrum, candidate = candidate, show_bar_labels=False)
        graph.initialize()
        return graph

    @staticmethod
    def build_head_to_tail_map_graph(spectrum, candidate = []):
        graph = SpectraGraph(spectrum,
                            figsize = (9,1.5),
                            show_title = False,
                            candidate = candidate, 
                            show_bar_labels=False,
                            axis_labels_size = 5)
        graph.initialize()
        return graph
        

    def __init__(self, spectrum, **kwargs):
        '''Use build_grap to create a graph or build_map_graph to build the map graph.'''
        self.spectrum = spectrum
        self.compound = self.spectrum.compound
        self.figsize = (9,3)
        self.show_title = True
        self.show_bar_labels = True
        self.axis_labels_size = None
        self.candidate = []
        for prop in kwargs:
            setattr(self, prop, kwargs[prop])

    def initialize(self):
        if len(self.candidate) <= 0:
            self.create_bar_graph()
        else:
            self.create_head_to_tail_graph()
        self.save_initial_range()
        self.set_newdatarange(self.axmin, self.axmax)

    def save_initial_range(self):
        self.axmin = math.floor(self.ax.axis()[0])
        self.axmax = math.ceil(self.ax.axis()[1])
        self.aymin = math.floor(self.ax.axis()[2])
        self.aymax = math.ceil(self.ax.axis()[3]) * 1.1 # add 10%
        self.axminx = int(self.ax.transData.transform_point([self.axmin, 0])[0])
        self.axmaxx = int(self.ax.transData.transform_point([self.axmax, 0])[0])

    def create_bar_graph(self):
        self.figure = plt.figure(figsize=self.figsize)
        self.ax = self.figure.add_subplot(111)
        title = None
        if self.compound.cas_name:
            title = self.compound.cas_name
        elif self.compound.compound_name:
            title = self.compound.compound_name
        else:
            title = 'Untitled'
        
        self.set_title(title)
        bars = self.ax.bar(self.spectrum.xs, self.spectrum.ys, 
                           color="red", align='center')
        self.add_labels_to(bars)
        self.set_axis_labels_size(self.ax)

    def create_head_to_tail_graph(self):
        self.figure = plt.figure(figsize = self.figsize)
        self.ax = self.figure.add_subplot(212)
        self.bx = self.figure.add_subplot(211, sharex=self.ax)
        if self.compound.cas_name:
            title = self.compound.cas_name
        elif self.compound.compound_name:
            title = self.compound.compound_name
        else:
            title = 'Untitled'

        #known compound graph
        bars = self.ax.bar(self.spectrum.xs, self.spectrum.ys, 
                           color="red", align='center')
        (ymin, ymax) = self.ax.get_ylim()
        self.ax.set_ylim(ymax, ymin) #invert y axis
        self.add_labels_to(bars)
        self.set_axis_labels_size(self.ax)

        #query spectra graph
        print "Candidate:", self.candidate
        print self.candidate[0::2]
        print self.candidate[1::2]
        bars = self.bx.bar(self.candidate[0::2], self.candidate[1::2], color="blue", align="center")
        
        self.add_labels_to(bars)
        self.set_axis_labels_size(self.bx)
        
        #move the tick labels for the query spectra to the top
        self.bx.tick_params(axis='x', bottom='off', top='on', labelbottom='off', labeltop='on')

        #set both graphs to have the same xlim
        (axx_min, axx_max) = self.ax.get_xlim()
        (bxx_min, bxx_max) = self.bx.get_xlim()
        self.ax.set_xlim(min([axx_min, bxx_min]), max([axx_max, bxx_max]) )
        self.bx.set_xlim(min([axx_min, bxx_min]), max([axx_max, bxx_max]) )
        self.figure.subplots_adjust(hspace=0, bottom=0.2, top=0.8)
        if (self.show_title):
            self.figure.text(0.5, 0.95, "Query Spectra", horizontalalignment='center')
            self.figure.text(0.5, 0.05, self.format_title(title), horizontalalignment='center')
        
        

        #in the new matplotlib we could just do..
        #self.bx.set_ticks_position('top')
        #lines = self.ax.get_xticklines()
        #labels = self.ax.get_xticklabels()
        #for line in lines:
        #    line.set_marker(matplotlib.lines.TICKDOWN)
        #for label in labels:
        #    label.set_y(-0.5)

    def format_title(self, title):
        ret = title 
        if len(title) > 60:
            ret = title[:25] + '  ...  ' + title[-25:]
        return ret

    def set_title(self, title):
        if not self.show_title: return
        self.ax.set_title(self.format_title(title))

    def add_labels_to(self, bars):
        if not self.show_bar_labels: return
        if self.compound.is_lcma:
            self.labels = labels.BarLabels(self.ax, bars, precision=4)
        else:
            self.labels = labels.BarLabels(self.ax, bars)
        self.labels.create_labels()

    def set_axis_labels_size(self, ax=None):
        if not self.axis_labels_size: return
        if ax is None:
            return
        axis_labels = ax.get_xticklabels() + ax.get_yticklabels()
        for label in axis_labels:
            label.set_size(self.axis_labels_size)

    def move_ticks_outside_graph(self):
        self.move_left_ticks_outside_graph()
        self.move_bottom_ticks_outside_graph()

    def move_bottom_ticks_outside_graph(self):
        lines = self.ax.get_xticklines()
        labels = self.ax.get_xticklabels()
        for line in lines:
            line.set_marker(matplotlib.lines.TICKDOWN)
        for label in labels:
            label.set_y(-0.02)

    def move_left_ticks_outside_graph(self):
        lines = self.ax.get_yticklines()
        labels = self.ax.get_yticklabels()
        for line in lines:
            line.set_marker(matplotlib.lines.TICKLEFT)
        for label in labels:
            label.set_x(-0.02)

    @property
    def px_ratio(self):
        # TODO 900px hardcoded
        return self.figure.canvas.get_width_height()[0] / 900.0 

    @property
    def datastart(self):
        return self._datastart

    def set_datastart(self,value):
        self._datastart = max(value, self.axmin)

    @property
    def dataend(self):
        return self._dataend

    def set_dataend(self,value):
        self._dataend = min(value, self.axmax)

    @property
    def datarange(self):
        return self.dataend - self.datastart

    @property
    def xstart(self):
        return int(self.ax.transData.transform_point([self.datastart, 0])[0])

    @property
    def xend(self):
        return int(self.ax.transData.transform_point([self.dataend, 0])[0])

    @property
    def xrange(self):
        return self.xend - self.xstart

    @property
    def mapxstart(self):
        xrange = self.axmaxx - self.axminx
        return math.floor(self.axminx + (self.datastart-self.axmin)*xrange/(self.axmax-self.axmin)) 

    @property
    def mapxend(self):
        xrange = self.axmaxx - self.axminx
        return math.ceil(self.axminx + (self.dataend-self.axmin)*xrange/(self.axmax-self.axmin)) 

    def to_real_pixel(self, matplot_pixel):
        return matplot_pixel / self.px_ratio

    def to_matplot_pixel(self, real_pixel):
        return real_pixel * self.px_ratio

    def zoom_range_to(self, rangestart, rangeend, newxstart, newxend):
        newxstart = self.to_matplot_pixel(newxstart)
        newxend = self.to_matplot_pixel(newxend)

        data_range = rangeend - rangestart
        relative_xstart = newxstart - self.xstart
        relative_xend = newxend - self.xstart
   
        newdatastart = math.floor(rangestart + relative_xstart * data_range / self.xrange )
        newdataend   = math.ceil (rangestart + relative_xend   * data_range / self.xrange )
        self.set_newdatarange(newdatastart, newdataend)

    def mapzoom_to(self, newxstart, newxend):
        self.zoom_range_to(self.axmin, self.axmax, newxstart, newxend)

    def zoom_to(self, newxstart, newxend):
        self.zoom_range_to(self.datastart, self.dataend, newxstart, newxend)

    def set_newdatarange(self, datastart, dataend):
        datastart, dataend = enlarge_to_minlength(datastart, dataend, 10)
        self.set_datastart(datastart)
        self.set_dataend(dataend)

        self.set_axis()

        self.move_ticks_outside_graph() 
        if self.show_bar_labels:        
            self.labels.show_labels_between(self.datastart, self.dataend)

    def set_axis(self):
        # adding a padding of 0.5 to avoid clipping half bars
        ds = max(self.datastart - 0.5, self.axmin)
        de = min(self.dataend + 0.5, self.axmax)
        self.ax.axis([ds, de, self.aymin, self.aymax ])

    def move_left(self):
        datarange = self.datarange
        self.set_datastart(self.datastart - datarange)
        self.set_newdatarange(self.datastart, self.datastart + datarange)

    def move_right(self):
        datarange = self.datarange
        self.set_dataend(self.dataend + datarange)
        self.set_newdatarange(self.dataend - datarange, self.dataend)

    def to_imageinfo(self):
        return {
            'spectrumId': self.spectrum.id,
            'datastart': int(self.datastart),
            'dataend':  int(self.dataend),
            'xstart': int(self.to_real_pixel(self.xstart)),
            'xend': int(self.to_real_pixel(self.xend)),
            'mapxstart': int(self.to_real_pixel(self.mapxstart)),
            'mapxend': int(self.to_real_pixel(self.mapxend))
        }

    def write(self, stream):
        # We need a renderer to calculate which labels overlap, but a
        # renderer is assigned only when the figure is saved, so we have 
        # to save the figure, remove the overlapping labels and then 
        # save the figure again for real.
        # Another option was to change matplotlib backend files
        # (according to the matplotlib mailing list) which would have 
        # caused packaging and deploying headaches.
        if self.show_bar_labels: 
            import StringIO
            self.figure.savefig(StringIO.StringIO())
            self.labels.remove_overlapping_labels()
        self.figure.savefig(stream)

def enlarge_to_minlength(start, end, minlength):
    start = int(start)
    end = int(end)
    while end-start < minlength:
        start -= 1
        end += 1
    if end-start == minlength+1: start -= 1
    return (start, end)
