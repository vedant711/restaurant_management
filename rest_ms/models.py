from django.db import models
from .forms import StringListField
# from django.contrib import ListField
import ast

# class OrderField(ListField):
#     def formfield(self, **kwargs):
#         return models.Field.formfield(self, StringListField, **kwargs)

class ListField(models.TextField):
    # __metaclass__ = models.SubfieldBase
    # description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# Create your models here.
class Orders(models.Model):
    # id=models.AutoField(primary_key=True)
    table =models.IntegerField()
    order = ListField()
    total = models.FloatField()
    feedback = models.CharField(max_length=20)
    feedback_comments = models.TextField()

class Menu(models.Model):
    item = models.CharField(max_length=50)
    price = models.IntegerField()
