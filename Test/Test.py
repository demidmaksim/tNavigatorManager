from ManagementObject.Field import *
import datetime as dt
np.set_printoptions(precision=2, linewidth=1000)

t = dt.datetime(2021, 1, 1)

Field = FieldConstructor.create_field()
Field.report()

print(Field.Schedule.bounds.get_limit(t, '101', None))
print(Field.get_pattern())

lc = Field.Schedule.get_current_boundaries(t, Field.get_pattern(), np.arange(0, 25)/100)

lc.get_report()

