# symbol-predictor-server 

This a server including a simple API to run prediction on mathematical symbols and expressions.

## API
The server has a single endpoint, a POST handler the on /api endpoint

```POST /api```

### Input
The endpoint expects data on the format application/JSON.

The request's body should be on the format:
```js
type Coordinates2D = {x: number, y: number}

type Trace = Array<Coordinates2D>

{
    "buffer": "Array<Trace>"
}
```
### Output
The output from the endpoint includes:

1. The prediction converted to LaTeX.
2. A list of all the symbols segmented from the traces.
3. A list of the top ten probabilities for each segmented symbol

The response body will be on the format:
```js
type TraceGroup = Array<number> // List of indexes which combined creates a symbol (indexes from the "buffer" in input). 

type Probability = number // Number between 0 and 1.
type Probabilities = Array<Probability> // List of top 10 propabilities.

type Label = string // A latex representation of a single symbol.
type Labels = Array<Label> // List of top 10 labels (corresponds with Probabilities).

{
    "latex": string, // The full expression in latex
    "probabilities": {
        "tracegroup": Array<TraceGroup>, // trace indexes combined into symbols
        "labels": Array<Labels>, // The labels corresponding with each probability.
        "values": Array<Probabilities> // The probabilities with length equal to the number of predicted symbols
    }
}
```
