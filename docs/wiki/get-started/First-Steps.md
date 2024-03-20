CSP is a graph-based stream processing library, where you create directed graphs for the streaming workflows.

In this introductory tutorial, you will write a CSP program to calculate the Bid-Ask Spread for specified `bid` and `ask` values.

> The bid–ask spread is the difference between the prices quoted for an immediate sale (ask) and an immediate purchase (bid) for stocks, futures contracts, options, or currency pairs in some auction scenario.
> ~ [Bid–ask spread on Wikipedia](https://en.wikipedia.org/wiki/Bid%E2%80%93ask_spread)

A CSP programs consist of:
* runtime components in the form of `csp.node` methods, and
* graph-building components in the form of `csp.graph` components.

CSP has a functional-style.

## Imports

After installation, you can import `csp`.

```python
from datetime import datetime, timedelta

import csp
from csp import ts
```

`ts` -> Time Series "type" input

## Create a `csp.node` to calculate spread

```python
@csp.node
def spread(bid: ts[float], ask: ts[float]) -> ts[float]:
    if csp.valid(bid, ask) and csp.ticked(bid, ask):
        return ask - bid
```

You can use the `@csp.node` decorator to create a node.

The `bid` and `ask` values are expected to be Time Series.

CSP is strictly typed, and the type is enforced by C++ engine.

This node needs to be executed each time the `ask` and `bid` values change.

`csp.valid` - ensure the values have ticked at least once.
A "tick" refers to any change in the input.

`csp.ticked(bid, ask)` - Check if ask OR bid have ticked

## Create the graph

Create a graph with thr `@csp.graph` decorator.

In the following graph, we:

1. Define the initial ask and bid values as `csp.const` - which are constants but Time Series.
2. Update the ask and bid values with a `csp.multiply` operation
3. Calculate the new spread.

```python
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
```

`csp.graph` components are only executed once, at application startup, to construct the graph. Once the graph is constructed, `csp.graph` code is no longer needed.

Once the graph is run, only the inputs, `csp.node`s, and outputs will be active as data flows through the graph.

The graph run is driven by input **ticks**.

csp.timer, csp.count - TODO

## Run the program

`csp.run` is the entry point to the graph.

```python
if __name__ == '__main__':
    csp.run(my_graph, starttime=datetime.utcnow(), endtime=timedelta(seconds=5))
```

The result of this would be:

```python-console
2024-03-20 21:48:32.788091 ask:4.0
2024-03-20 21:48:33.788091 ask:8.0
2024-03-20 21:48:34.288091 bid:4.0
2024-03-20 21:48:34.288091 spread:4.0
2024-03-20 21:48:34.788091 ask:12.0
2024-03-20 21:48:34.788091 spread:8.0
2024-03-20 21:48:35.788091 ask:16.0
2024-03-20 21:48:35.788091 spread:12.0
2024-03-20 21:48:36.788091 bid:8.0
2024-03-20 21:48:36.788091 ask:20.0
2024-03-20 21:48:36.788091 spread:12.0
```

## Visualize

In order to help visualize this graph, you can call

```python
csp.show_graph(my_graph)
```

![359407708](https://github.com/Point72/csp/assets/3105306/8cc50ad4-68f9-4199-9695-11c136e3946c)

Check out the complete example: [e_02_show_graph.py](examples/1_basics/e_02_show_graph.py)
