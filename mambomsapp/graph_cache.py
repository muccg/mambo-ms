from mamboms.mambomsapp.views import SpectraGraph


class SpectraGraphCache:
    def __init__(self):
        self.cache = {}

    def pop(self, compound, datastart, dataend):
        graph = None
        try:
            key = (compound.id, datastart, dataend)
            graph = self.cache.pop(key)
        except KeyError:
            pass
        return graph

    def pop_or_create(self, compound, datastart, dataend):
        datastart = int(datastart)
        dataend = int(dataend)
        graph = self.pop(compound, datastart, dataend)
        if graph is None:
            graph = SpectraGraph(compound)
            if datastart is not None and dataend is not None:
                if graph.datastart != datastart or graph.dataend != dataend:
                    graph.set_newdatarange(datastart, dataend)
        return graph

    def put(self, graph):
        key = (graph.compound.id, graph.datastart, graph.dataend)
        self.cache[key] = graph

cache = SpectraGraphCache()

