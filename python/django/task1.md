# Task 1

Consider a following Django database model

```python
from django.db import models
class SomeModel(models.Model):
field_a = models.CharField(max_length=10)
field_b = models.IntegerField(max_length=10)
number_of_updates = models.IntegerField(default=0)
```


The goal of the task is to allow modifying a selected instance of this model via an HTTP request in the
following way:
- set value of fields field_a and field_b to values specified in the HTTP request
- increment value of number_of_updates field by one
- store timestamp of the last modification

You can add an additional field to the model to store timestamp of the last modification.
You don't have to set up a full Django application to present the solution, but please provide code snippets for
the parts that you consider essential to the solution. You may use any framework; we recommend django-
ninja.