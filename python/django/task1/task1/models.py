from django.db import models
from django.utils import timezone

class SomeModel(models.Model):
    """
    Represents an entity with two configurable fields, an update counter,
    and a timestamp for the last modification.
    """
    field_a = models.CharField(
        max_length=10,
        verbose_name="Field A",
        help_text="A short text field, maximum 10 characters."
    )
    field_b = models.IntegerField(
        verbose_name="Field B",
        help_text="An integer value."
    )
    number_of_updates = models.IntegerField(
        default=0,
        verbose_name="Number of Updates",
        help_text="Counter for the number of times this instance has been modified via the API."
    )
    last_modified = models.DateTimeField(
        auto_now=True, # Automatically set to now every time the object is saved
        verbose_name="Last Modified",
        help_text="Timestamp of the last modification."
    )

    def __str__(self) -> str:
        """String representation of the SomeModel instance."""
        return f"ID: {self.id} | A: {self.field_a}, B: {self.field_b} | Updates: {self.number_of_updates}"

    class Meta:
        verbose_name = "Some Model Entry"
        verbose_name_plural = "Some Model Entries"
        ordering = ['-last_modified'] # Default ordering