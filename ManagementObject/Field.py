from ManagementObject.Well import *
from Eclipse_Binary_Parser import *
from BaseFunction.Readers.Loader import *
from OptimizationModel.SimpleModel import *
from BaseFunction.Readers.MnimonicAPI import *
from ManagementObject.AdditionalSchedule.Schedule import *


class Field:
    def __init__(self, name: str):
        self.name = name
        self.wells = dict()
        self.bounds = None
        self.Schedule = None

    def get_pattern(self) -> list:
        """
        :return: Возаращает список скважин с зонами притока в стогом порядке
        """
        pattern = []
        wells = list(self.wells.keys())
        wells.sort()

        for well_name in wells:
            inflow_zones = list(self.wells[well_name].InflowZones.keys())
            inflow_zones.sort()
            for inflow_zone in inflow_zones:
                pattern.append([well_name, inflow_zone])

        return pattern

    def get_well(self, unique=True, name=False):
        """

        :param unique: вернуть уникальный список скважин
        :param name: возвращать имена
        :return: возвращает объекты скважин в строгом порядке
        """
        pattern = self.get_pattern()
        pattern = np.array(pattern)
        wells = pattern[:, 0]

        if unique:
            wells = list(set(wells))
            wells.sort()
        if not name:
            for well in wells:
                yield self.wells[well]
        else:
            for well in wells:
                yield self.wells[well].name

    def get_inflow_zone(self):
        """
        :return: Возвращает объекты скважины в строгом порядке
        """
        pattern = self.get_pattern()
        for field_object in pattern:
            well_name = field_object[0]
            segment = field_object[1]
            yield self.wells[well_name].InflowZones[segment]

    def get_well_params(self, param_name, number=None) -> list or int:
        """

        :param param_name: имя параметра который необходимо аернуть
        :param number: какой по счету параметр необходимо вернуть
        :return: возращает или весь соответсвующий вектор или конктерное значеин
         с вызванного шага
        """
        params_list = []

        for well in self.get_well():
            param = well.get_param(param_name, None)

            if number == 'Last':
                params_list.append(param[-1])
            else:
                params_list.append(param)

        return list(params_list)

    def get_inflowzone_params(self, param_name: str, number=None) \
            -> list or int:
        """

        :param param_name: имя параметра который необходимо аернуть
        :param number: какой по счету параметр необходимо вернуть
        :return: возращает или весь соответсвующий вектор или конктерное значеин
         с вызванного шага
        """

        params = []

        for inflow_zone in self.get_inflow_zone():

            well = inflow_zone.well
            segm = inflow_zone.segm
            param = self.wells[well].get_param(param_name, segm)

            if number == 'Last':
                params.append(param[-1])
            else:
                params.append(param)

        return list(params)

    def get_last_active_param(self, param_name):
        """
        возрвщвет вектор значений параметра с последнего шага, на котором
         работала соответсвующая скважина
        :param param_name: имя параметра который необходимо вернуть
        :return: возвращает вектор значений соотсветсвующий строгому порядку
        """
        param_list = []

        for inflowzone in self.get_inflow_zone():
            param = inflowzone.get_last_active_param(param_name)
            param_list.append(param)

        return param_list

    def __liq_limit(self, now_time, swct):
        mlc = self.Schedule.get_boundaries(now_time, self.get_pattern(), swct,
                                           'LIQ')
        return simple_minimization_water(swct, mlc)

    def __oil_limit(self, now_time, swct):
        mlc = self.Schedule.get_boundaries(now_time, self.get_pattern(), swct,
                                           'OIL')
        return simple_minimization_water(swct, mlc)

    def __oil_limit_is_not_met(self, now_time,  liq, swct):
        oil_limit = self.Schedule.bounds.get_limit(now_time, 'FIELD', -1, 'OIL')
        if oil_limit[DebitLimits.max_vol] < sum(liq.x * (1 - swct)):
            return True
        else:
            return False

    @staticmethod
    def exercise_field_control(max_oil, max_liq):
        """

        :param max_oil: максимальное значение дебита нефти на месторождении
        :param max_liq: максимальное значение дебита жидкости на месторождении
        """
        max_oil = max_oil['max liquid']
        max_liq = max_liq['max liquid']
        control = 'GCONPROD\n' \
                  'FIELD ORAT {} 2* {} RATE 5* RATE /\n' \
                  '/'.format(max_oil, max_liq)
        print(control)
        add_keyword(control)

    def exercise_well_control(self, liq):
        pattern = self.get_pattern()
        for well in self.get_well():
            liqu = []
            segm = []
            for segment in well.InflowZones.keys():
                ind = pattern.index([well.name, segment])
                segm.append(segment)
                liqu.append(round(liq.x[ind], 3))

            well.exercise_control(segm, liqu)

            print("{}:\t{}".format(well.name, segm))
            print("{}:\t{}".format(well.name, liqu))

    @staticmethod
    def report_optimization(liq, swct):
        np.set_printoptions(linewidth=1000, precision=3)
        print("Liq: {}".format(np.around(liq.x, 3)))
        print("Oil: {}".format(np.around(liq.x * (1-swct), 3)))
        print("swct: {}".format(swct))
        print("LIQ: {}".format(sum(liq.x)))
        print("OIL: {}".format(sum(liq.x * (1 - swct))))

    def report_param(self):
        for well in self.get_well():
            for key_w in ['WWCT', 'WOPR', 'WOPR', 'WBHP']:
                value = np.array(well.get_param(key_w, None))
                results = '{}, len: {}, value: {}'.format(key_w,
                                                          len(value), value)
                print(results)
            for segm in list(well.InflowZones.keys()):
                for key_w in ['SOFR', 'SWFR', 'SWCT', 'SPR']:
                    value = np.array(well.get_param(key_w, segm))
                    results = '{}, len: {}, value: {}'.format(key_w,
                                                              len(value), value)
                    print(results)

    def __simple_optimization(self, now_t):

        swct = np.array(self.get_last_active_param('SWCT'))
        max_oil = self.Schedule.bounds.get_limit(now_t, 'FIELD', -1, 'OIL')
        max_liq = self.Schedule.bounds.get_limit(now_t, 'FIELD', -1, 'LIQ')

        liq = self.__liq_limit(now_t, swct)
        if self.__oil_limit_is_not_met(now_t, liq, swct):
            liq = self.__oil_limit(now_t, swct)

        self.exercise_field_control(max_oil, max_liq)
        self.exercise_well_control(liq)
        self.report_optimization(liq, swct)

    def optimization(self, now_time, method='Simple'):
        if method == 'Simple':
            self.__simple_optimization(now_time)

    def report(self):
        """
        выводит отчет о созданом объекте местрождения
        """
        print("Name field: {}".format(self.name))
        for well in self.wells:
            well = self.wells[well]
            print('-'*50)
            print("\t Well name: {}".format(well.name))
            for inflowzone in well.InflowZones:
                inflowzone = well.InflowZones[inflowzone]
                print("\t|\t inflowzone: {}\t".format(inflowzone.segm),
                      "Device Type: {}".format(inflowzone.device_type))

        self.Schedule.report()

    def get_save_order(self) -> tuple:
        """
        :return: возвращает вектора c порядком сохраненя в бинарных файлах
        """
        w_names = list(self.get_well(name=True))
        w_params = InflowZone.target_params['well_params']
        s_params = InflowZone.target_params['valve_params']

        s_well = []
        s_name = []
        for infzone in self.get_inflow_zone():
            s_well.append(infzone.well)
            s_name.append(infzone.segm)

        return w_names, w_params, s_well, s_name, s_params


class FieldConstructor:

    @staticmethod
    def get_smspec_link() -> str:
        """
        :return: Возвращает ссылку на SMSPEC файл
        """
        this_folder = get_project_folder() + '\\'
        return this_folder + 'tNavigatorManager.SMSPEC'

    @staticmethod
    def get_unsmry_link() -> str:
        """
        :return: Возвращает ссылку на UNSMRY файл
        """
        this_folder = get_project_folder() + '\\'
        return this_folder + 'tNavigatorManager.UNSMRY'

    @staticmethod
    def __create_empty_field(name: str) -> Field:
        """
        Создан для больщей абстаркии при инициализации метсорождениия и
         простоты дальнейшего расширения скрипта
        :param name: имя месторождения
        :return: возвращает пустой объект месторождения
        """
        return Field(name)

    @staticmethod
    def __add_schedule(field: Field, additional_data: dict) -> None:
        """
        Создан для больщей абстаркии при инициализации метсорождениия и
         простоты дальнейшего расширения скрипта
        :param field: объект месторождения к которому необходимо добавить
         объект скважины
        :param additional_data: данный необходимые для создания объекта скважины
        """

        schedule = ScheduleConstructor.create_schedule(additional_data)
        field.Schedule = schedule

    @staticmethod
    def __add_well(field: Field, well: Well) -> None:
        """
        Создан для больщей абстаркии при инициализации метсорождениия и
         простоты дальнейшего расширения скрипта
        :param field: объект месторождения к которому необходимо добавить
         объект скважины
        :param well: объект скважины для добавления
        """
        field.wells[well.name] = well

    @staticmethod
    def __add_inflowzone(field: Field, inflowzone: InflowZone) -> None:
        """
        :param field: объект месторождения к которому необходимо добавить
         объект зону притока(клапан)
        :param inflowzone: объект зона притока(клапан) для добавления
        """

        if inflowzone.well not in field.wells:
            well = WellConstructor.create_well(inflowzone.well)
            WellConstructor.add_zone(well, inflowzone)
            FieldConstructor.__add_well(field, well)
        else:
            well = field.wells[inflowzone.well]
            WellConstructor.add_zone(well, inflowzone)

    @staticmethod
    def __read_additional_schedule(field) -> None:
        """
        :param field: объект месторождения к которому необходимо добавить данные
        из дополнительного расписания
        """
        additional_data = read_additional_schedule()

        for inflowzone in additional_data['INFLOWZO']:
            inflowzone = InflowZoneConstructor.from_dict(inflowzone)
            FieldConstructor.__add_inflowzone(field, inflowzone)

        FieldConstructor.__add_schedule(field, additional_data)

    @staticmethod
    def __for_read_in_summ_file(field) -> tuple:
        """

        :param field: объект месторождения,
        :return: возвращает ветора для записи в бинарные файлы
        """
        wells, main_params, nums = [], [], []

        for well in field.get_well():
            for param in InflowZone.target_params['well_params']:
                wells.append(well.name)
                main_params.append(param)
                nums.append(None)

            for inflow_zone in well.get_inflow_zone():
                for param in InflowZone.target_params['valve_params']:
                    wells.append(inflow_zone.well)
                    main_params.append(param)
                    nums.append(inflow_zone.segm)

        return wells, main_params, nums

    @staticmethod
    def __create_summry(field, start_d) -> None:
        """
        Создает smspec, unsmry файлы для записи результатов
        :param field: объект месторождения из которого берется шаблон для записи
        :param start_d: стартовая дата
        """

        smspec_file = FieldConstructor.get_smspec_link()
        unsmry_file = FieldConstructor.get_unsmry_link()

        w_name, w_param, s_well, s_name, s_param = field.get_save_order()
        targ = create_keyword_vectors(w_name, w_param, s_well, s_name, s_param)

        create_summary(smspec_file, targ[0], targ[1], targ[2], targ[3], start_d)
        write_summary(unsmry_file, [0] * len(targ[0]))

    @staticmethod
    def __save_new_data(field) -> None:
        """
        Сохраняет данные в smspec, unsmry файлы из мнимоник API tNavigator
        :param field: объект месторождения из которого берется шаблон для записи
        """

        smspec_file = FieldConstructor.get_smspec_link()
        unsmry_file = FieldConstructor.get_unsmry_link()

        summary_reader = SUMMARYReader(smspec_file)
        w_name, w_param, s_well, s_name, s_param = field.get_save_order()
        targ = create_keyword_vectors(w_name, w_param, s_well, s_name, s_param)

        target_mnemonics = InflowZone.target_params['well_params'][:]
        target_mnemonics.extend(InflowZone.target_params['valve_params'])
        all_mnemonic_results = read_target_mnemonic(target_mnemonics)
        now_dat = get_current_date()
        start_d = summary_reader.SMSPEC.time.start_date

        values = [(now_dat - start_d).days]

        for k_id, keyword in enumerate(targ[0]):
            if k_id != 0:
                well = targ[1][k_id]
                segm = targ[2][k_id]
                if segm == 0:
                    segm = None
                value = all_mnemonic_results.get_param(keyword, well, segm)
                values.append(value)

        write_summary(unsmry_file, values)

    @staticmethod
    def __read_summary_file(field: Field) -> None:
        """
        Читает данные из smspec, unsmry файлой
        :param field: объект месторождения для записи
        """

        smspec_file = FieldConstructor.get_smspec_link()

        summary_reader = SUMMARYReader(smspec_file)
        wells, params, nums = FieldConstructor.__for_read_in_summ_file(field)
        summary = summary_reader.get(wells, params, nums)

        for well in field.get_well():
            well.param = summary.get_well_param(well.name)

        for inflow_zone in field.get_inflow_zone():
            inflow_zone.param = summary.get_segment_param(inflow_zone.well,
                                                          inflow_zone.segm)

    @staticmethod
    def create_field() -> Field:
        """
        :return: Создает объект месторожедния со всеми данными
        """
        field = FieldConstructor.__create_empty_field('name')
        FieldConstructor.__read_additional_schedule(field)
        FieldConstructor.__save_new_data(field)
        FieldConstructor.__read_summary_file(field)
        return field

    @staticmethod
    def create_field_for_init() -> Field:
        """
        :return: Возвращаетобъект месторождения для __init_script__
        """
        field = FieldConstructor.__create_empty_field('name')
        FieldConstructor.__read_additional_schedule(field)
        start_date = get_current_date()
        d = start_date.day
        m = start_date.month
        y = start_date.year
        start_date = [d, m, y, 0, 0, 0]
        FieldConstructor.__create_summry(field, start_date)
        return field
