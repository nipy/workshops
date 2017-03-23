name: inverse
layout: true
class: center, middle, inverse
---
# Writing unit and regression tests

---
layout: false
<span style="color:purple">## Outline</span>

- ### Learning objectives
- ### Requirements
- ### Introduction
- ### Tools
- ### Exercises
- ### Review questions

---
name: inverse
layout: true
class: center, middle, inverse
---
## Learning objectives
---
layout: false

- What are the various types of tests people are using

- Why do we write tests

- What are the Python framework for testing

---
name: inverse
layout: true
class: center, middle, inverse
---
## Requirements
---
layout: false

- Python (basics of NumPy, Jupyter)

- Nipype Function Interfaces

---
name: inverse
layout: true
class: center, middle, inverse
---
## Introduction
---
layout: false

### <span style="color:purple"> Why do we test software?</span>

&nbsp;

--

- mistakes happens and always will

--

  - guard against them
  - raise your confidence during development

&nbsp;

--

- makes you think about desirable output

--

  - helps you to write a better code

&nbsp;

--

- improves readability of your code

--

  - helps to reuse your code

---
###<span style="color:purple">Various types of tests</span>

--

- Unit tests

  - test isolated parts of the program

&nbsp;

--

- Integration tests

  - combine individual software modules and test as a group

&nbsp;

--

- Regression tests

  - verify that software previously developed and tested still performs correctly even after it was changed or interfaced with other software

  - you don't have to knows the expected result, the assumption is that the past results were correct.

--

- and many others...

We will concentrate on unit and regression tests

---
name: inverse
layout: true
class: center, middle, inverse
---
## Tools
---
layout: false

### <span style="color:purple">Unit tests with simple assert statement</span>

```python
def mean_diameter(radius):
    diameter = 2 * radius
    return sum(diameter) / len(diameter)```

--

```python
assert mean_diameter([3, 4, 5]) == 8
```

--

- no meaningful output

- no automation
---
### <span style="color:purple">Unit tests with Unittest built-in library</span>

```python
def mean_diameter(radius):
    diameter = 2 * radius
    return sum(diameter) / len(diameter)

import unittest

class TestDiv(unittest.TestCase):
    def test_div5(self):
        self.assertEqual(mean_diameter([3, 4, 5]), 8)

if __name__ == ’__main__’:
    unittest.main()
```

--

- supports test automation

- but a lot of boilerplate code

---
### <span style="color:purple">Unit tests with Pytest library</span>

```python
def mean_diameter(radius):
    diameter = 2 * radius
    return sum(diameter) / len(diameter)

def test_with_pytest():
    assert mean_diameter([3, 4, 5]) == 8
```

--

- it’s easy to get started

- straightforward asserting with the assert statement

- helpful traceback and failing assertion reporting

- automatic test discovery
---

name: inverse
layout: true
class: center, middle, inverse
---
## Exercises
---
layout: false
TODO

- output of a function
- type of an object
- parametrization of arguments
- fixtures to create data
- skipping test: skipif
- expecting tests to fail: xfail
- testing exceptions: pytest.raises
-


---
name: inverse
layout: true
class: center, middle, inverse
---
# Questions?
