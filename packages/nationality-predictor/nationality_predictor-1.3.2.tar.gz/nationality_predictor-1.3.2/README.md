# nationality-predictor

[![npm](https://img.shields.io/pypi/v/nationality-predictor.svg)](https://pypi.org/project/nationality-predictor/)

This engine attempts to predict the nationality of a person's name.

## Installation

Run the following to install:

```console
pip install nationality-predictor
```

## Usage

### Predictor

```python
Predictor()
```

Params:

```
Name: String ? The name that has to be predicted.
```

Demo:

```python
from nationality_predictor import Predictor

name = Predictor("Thomas")
print(name.predict())
```

Result:
```
Prediction: json()
```

# License
[MIT](https://github.com/dewittethomas/nationality-predictor/blob/master/LICENSE)