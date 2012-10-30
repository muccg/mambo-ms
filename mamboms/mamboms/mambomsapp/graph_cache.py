from mamboms.mambomsapp.spectra_graph import SpectraGraph
from threading import Lock
from decorators import mutex

class SpectraGraphCache():
    CacheLock = Lock()

    def __init__(self):
        self.cache = {}
        # contains the keys in the order of addition
        self.ordered_keys = []
        self.max_entries = 50

    @mutex(CacheLock)
    def pop(self, key):
        graph = None
        try:
            graph = self.cache.pop(key)
            self.ordered_keys.remove(key)
        except KeyError:
            pass
        return graph

    def pop_or_create(self, spectrum, datastart, dataend):
        key = self.key(spectrum, datastart, dataend)
        graph = self.pop(key)
        if graph is None:
            graph = self.create(spectrum, datastart, dataend)
        return graph

    @mutex(CacheLock)
    def put(self, graph):
        key = self.key(graph.spectrum, graph.datastart, graph.dataend)
        self.cache[key] = graph
        self.update_ordered_keys(key)
        self.keep_entries_below_max_entries() 

    def update_ordered_keys(self, key):
        '''Append the key to ordered keys and make sure it is unique'''
        if key in self.ordered_keys:
            self.ordered_keys.remove(key)
        self.ordered_keys.append(key)

    def keep_entries_below_max_entries(self):
        while len(self.ordered_keys) > self.max_entries:
            key = self.ordered_keys[0]
            del(self.ordered_keys[0])
            del(self.cache[key])

    def key(self, spectrum, datastart, dataend):
        return (spectrum.id, int(datastart), int(dataend))

    def create(self, spectrum, datastart, dataend):
        graph = SpectraGraph.build_graph(spectrum)
        if datastart is not None and dataend is not None:
            if graph.datastart != datastart or graph.dataend != dataend:
                graph.set_newdatarange(datastart, dataend)
        return graph

cache = SpectraGraphCache()

