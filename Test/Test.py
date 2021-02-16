from FieldObject.Field.Field import *
import datetime as dt

t = dt.datetime(2021, 1, 1)

Field = FieldConstructor.create_field()
Field.report()

print(Field.Schedule.bounds.get_limit(t, '101', None))
print(Field.get_pattern())

lc = Field.Schedule.get_current_boundaries(t, Field.get_pattern())

lc.get_report()

