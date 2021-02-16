from ManagementObject.Field import *
import datetime as dt
from OptimizationModel.SimpleModel import *
import numpy as np
np.set_printoptions(precision=2, linewidth=1000)

t = dt.datetime(2021, 1, 1)

Field = FieldConstructor.create_field()
Field.report()

water_cut = np.arange(0, 25)/100
lc = Field.Schedule.get_current_boundaries(t, Field.get_pattern(), water_cut)

lc.get_report()
lc = lc.to_scipy()
sol = minimization_water(np.arange(0, 25), lc)
print(sol)

