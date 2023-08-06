# ease-image-processing

## Description. 

The package ease-image-processing is used to wrapper some functions of scikit image for ease of use, so the package features are:

- Structure:

  - Histogram matching 

  - Structural similarity 

  - Resize image

  - Drawing the image

- Utils:

  - Read image

  - Save image

  - Plot image


But the main goal of this project is to learn the main structures of a python package.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install ease-image-processing

```bash
pip install ease-image-processing
```

## Usage

```python
#Import libs and images:
from structure import combination, transformation
from utils import io, graphics
barca = io.read_image('../image/barcelona.png')
real = io.read_image('../image/real.png')

# Combining Barcelona and Real Madrid symbols:
real_barca = combination.transfer_histogram(real, barca)

# Showing the combined symbol:
graphics.plot_image(real_barca)
graphics.plot_result(real, barca, real_barca)
graphics.plot_histogram(real_barca)

# Drawing Real symbol:
draw_real = transformation.image_to_draw(real)
graphics.plot_image(draw_real)

```

## Add content 

- [Setuptools documentation](https://setuptools.readthedocs.io/en/latest/setuptools.html)

- [Automated tests](https://docs.pytest.org/en/latest/goodpractices.html)

- [Use of Tox](https://tox.readthedocs.io/en/latest/)

Tox is for use automated tests in differents versions of Python.


## Author
Vitor Pereira

## License
[MIT](https://choosealicense.com/licenses/mit/)
