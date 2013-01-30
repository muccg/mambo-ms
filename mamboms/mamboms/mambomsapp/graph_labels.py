'''
Classes abstracting working with matplot bar-labels.
'''

class BarLabels:
    def __init__(self, ax, bars, precision = 2):
        self.ax = ax
        self.bars = bars
        self.precision = precision

    def create_labels(self):
        self.labels = []
        for bar in self.bars:
            label = self.create_label_for(bar)
            self.labels.append(label)
        self.labels.sort(Label.cmp_by_vertical_pos)
    
    def create_label_for(self, bar):
        height = bar.get_height()
        middle = bar.get_x() + bar.get_width()/2.0
        pattern = '%%.%df' % self.precision
        text = self.ax.text(
                middle, height+30, (pattern % middle),
                ha = 'center', va = 'bottom',
                fontsize = 9)
        return Label(text, bar)

    def show_labels_between(self, datastart, dataend):
        for l in self.labels:
            bar_value = float(l.text)
            l.set_visible(datastart <= bar_value <= dataend)

    def remove_overlapping_labels(self):
        for i, l in enumerate(self.labels):
            if not l.visible: continue
            # there is no point in checking more than
            # the next 30 elements for overlaps
            for l2 in self.labels[i+1:i+31]:
                if l2.visible and l2.overlaps(l):
                    l2.hide()

class Label:
    def __init__(self, mpltext, bar):
        self.mpltext = mpltext
        self.bar = bar

    @property
    def text(self):
        return self.mpltext.get_text()

    @property
    def extent(self):
        return self.mpltext.get_window_extent()

    @property   
    def visible(self):
        return self.mpltext.get_visible()

    def set_visible(self, value):
        self.mpltext.set_visible(value)

    @property
    def x(self):
        return self.mpltext.get_position()[0]

    @property
    def y(self):
        return self.mpltext.get_position()[1]

    def show(self):
        self.set_visible(True)

    def hide(self):
        self.set_visible(False)

    def cmp_by_vertical_pos(self, other):
        return sign(self.x-other.x)

    def overlaps(self, other):
        if self.extent.count_overlaps([other.extent]) > 0:
            return True
        return False

def sign(number):
    if number <  0: return -1
    if number == 0: return  0
    if number >  0: return  1

