# symbol-predictor-server 

This a server including a simple API to run prediction on mathematical symbols and expressions.

## Prerequisites
1. Python 3
2. Pip (to your python 3 version)

## Running the server

Do the following steps to run the server:

1. Clone the repository (```git clone ...```)
2. Install the dependencies (```pip install -r /path/to/requirements.txt```)
3. Download the [combined_model](https://www.dropbox.com/sh/2v1fo8inmwb4h3l/AAAaqZ5HPyS4hNoGEpnMi3FPa?dl=0).
4. Add the model to the folder ```/classification/```
5. Run the server (```python /path/to/server.py```)


## Running the tests

To run the tests run the following command from the root directory:

```python -m unittest discover test/```

## API
The server has a single endpoint, a POST handler the on /api endpoint

```POST /api```

### Input
The endpoint expects data on the format application/JSON.

The request's body should be on the format:
```js
Coordinates2D = {x: number, y: number}

Trace = Array<Coordinates2D>

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
TraceGroup = Array<number> // List of indexes which combined creates a symbol (indexes from the "buffer" in input). 

Probability = number // Number between 0 and 1.
Probabilities = Array<Probability> // List of top 10 propabilities.

Label = string // A latex representation of a single symbol.
Labels = Array<Label> // List of top 10 labels (corresponds with Probabilities).

{
    "latex": string, // The full expression in latex
    "probabilities": {
        "tracegroup": Array<TraceGroup>, // trace indexes combined into symbols
        "labels": Array<Labels>, // The labels corresponding with each probability.
        "values": Array<Probabilities> // The probabilities with length equal to the number of predicted symbols
    }
}
```

### Example
```js
request = {
    "url": "/api",
    "method": "POST",
    "body": {
        buffer: [
            [
                {x: 0, y: 1},
                {x: 1, y: 2}
            ],
            [
                {x: 4, y: 8},
                {x: 5, y: 9}
            ]
        ]
    }
}

response = {
    "body": {
        "latex": "\sqrt{3}",
        "probabilities": {
            "tracegroup": [
                [0], 
                [1]
            ],
            "labels": [
                ["\sqrt", "\alpha", "y", ...], 
                ["3", "9", "\beta", ...]
            ],
            "values": [
                [0.7, 0.2, 0.05, ...], 
                [0.9, 0.03, 0.01, ...]
            ]
        }
    }
}
```
