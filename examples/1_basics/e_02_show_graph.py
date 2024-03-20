from datetime import datetime, timedelta

import csp
from csp import ts


@csp.node
def spread(bid: ts[float], ask: ts[float]) -> ts[float]:
    if csp.valid(bid, ask) and csp.ticked(bid, ask):
        return ask - bid


@csp.graph
def my_graph():
    bid = csp.count(csp.timer(timedelta(seconds=2.5), True))
    ask = csp.count(csp.timer(timedelta(seconds=1), True))
    bid = bid * 4.0
    ask = ask * 4.0
    s = spread(bid, ask)

    csp.print("bid", bid)
    csp.print("ask", ask)
    csp.print("spread", s)


def main():
    # open in graphviz viewer
    # csp.show_graph(my_graph)
    # or output to file
    csp.show_graph(my_graph, graph_filename="tmp.png")
    csp.run(my_graph, starttime=datetime.now(), endtime=timedelta(seconds=5))


if __name__ == "__main__":
    main()
