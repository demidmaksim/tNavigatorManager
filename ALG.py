from ManagementObject.Field import *
from tNav.For_Debugging import *


def __init_script__():
    field = FieldConstructor.create_field_for_init()
    field.report()
    print('Успешно инициализированно!')


def alg():
    field = FieldConstructor.create_field()
    print('Модель управления успешно создана!')
    t = get_current_date()
    field.optimization(t, 'Simple')
    field.report_param()
    print('Алгоритм успшно реализован!')


__init_script__()

alg()
