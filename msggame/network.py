import networkx

from . import models


def get_network():
    qs = models.Link.objects.filter(round=models.current_round()).values_list('source_id', 'destination_id')
    G = networkx.DiGraph()
    for src, dst in qs:
        G.add_edge(src, dst)
    return G
