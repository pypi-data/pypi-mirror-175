# perform_draw
A simple app that will randomly draw a given set up numbers from a list.


## Installation

Run the following to install:
```python
pip install perform_draw
```

## Usage

```command line
python3 perform_draw.py
```
Please enter the total number of balls to be placed in the bag:
You must enter a whole number (integer) greater than 0
15
 
Please enter the total number of balls to be drawn:
You must enter a whole number (integer) greater than 0
and less than 15.
5

Numbers drawn are: [12, 9, 1, 8, 4]


When the object is called, you pass the following variables:

number:     The number of items in the pool to be picked from.
            example:    number = 5 
                        will create a pool [1, 2, 3, 4, 5]

pick:       The number of items to be randomly drawn from the pool.
            example:    pick = 2
                        will return a list of the randomly drawn items, say [4, 2]

put_back:   Whether an item is put back into the pool prior to the next draw.
            Input as a boolean True or False, with a default of False.


## Install Requires

This package uses the following standard library packages:
1. math
2. random

## In Closing

This package has been built as part of my learning Python so may contain coding that is not best practice.  I am happy for more experienced Python users to feedback any areas that could be improved.  Once I get to understand uploading packages to PyPI I will set up development dependencies.