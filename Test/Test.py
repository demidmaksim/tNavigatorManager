from FieldObject.Field.Field import *
import datetime as dt

t = dt.datetime(2020, 1, 1)

Field = FieldConstructor.create_field()
Field.report()

print(Field.Schedule.bounds.get_limit(t, '101', None))
