# Customer datasets

`customer_dataset.py` defines a container for customer dictionaries and a premium
subclass. It filters customers by age, adds/replaces records, records update times
and displays source information. The subclass adds membership filtering and
extends the information display through `super()`.

Stack: Python standard library (`datetime`). Concepts: instance state,
`__len__`, `__repr__`, `__contains__`, list comprehensions, inheritance and method
overriding. The classes accept records in memory; they do not load a CSV file.

Status: substantive practice implementation. `__contains__` currently returns a
list despite its `bool` annotation. Python's `in` operator coerces that result to
truth, but a direct method call returns the list. This behavior is preserved for
manual review. Authorship of inherited/template portions cannot be established
from this file alone.
