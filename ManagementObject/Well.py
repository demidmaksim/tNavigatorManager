from ManagementObject.InflowZone import *


class Well:
    def __init__(self, name: str):
        self.name = name
        self.InflowZones = dict()
        self.param = dict()

    def get_inflow_zone(self):
        for key in self.InflowZones.keys():
            yield self.InflowZones[key]

    def get_param(self, param: str, inflow_zones: int or None):
        """

        :param param: имя мнимоники
        :param inflow_zones: имя зоны притока, для которой необходимо устоновить
         данный параметр, если это не указано то устанавливает для скважины
        :return:
        """
        if inflow_zones is None:
            return self.param[param]
        else:
            return self.InflowZones[inflow_zones].get_param(param)

    def exercise_control(self, segments, liquid):
        sum_liq = sum(liquid)

        if sum_liq != 0:
            status = 'OPEN'
            weill_control = "WCONPROD\n" \
                            "'{}' {} GRUP 3* 1* 1* 10 0 /\n" \
                            "/".format(self.name, status, sum_liq)
            add_keyword(weill_control)
            weill_control = "WGRUPCON\n" \
                            "'{}' YES {} LIQ 1 /\n" \
                            "/".format(self.name, sum_liq)

            add_keyword(weill_control)
        else:
            status = 'SHUT'
            sum_liq = 0
            weill_control = "WCONPROD\n" \
                            "'{}' {} GRUP 3* 1* 1* 10 0 /\n" \
                            "/".format(self.name, status, sum_liq)
            add_keyword(weill_control)

        max_liq = max(np.abs(liquid))

        if len(list(self.InflowZones.keys())) > 1 and max_liq != 0:
            for s_id, segm in enumerate(segments):

                this_liq = liquid[s_id]
                if this_liq < 0.01 * max_liq:
                    share = 0.01
                else:
                    share = this_liq / max_liq

                self.InflowZones[segm].set_valve_size(share)


class WellConstructor:
    def __init__(self):
        pass

    @staticmethod
    def add_zone(well: Well,  inflow_zone: InflowZone) -> None:
        """
        :param well: объект скважина для который необходимо добавить
        зону притока
        :param inflow_zone: зона притока, которую необходимо добваить
        """
        well.InflowZones[inflow_zone.segm] = inflow_zone

    @staticmethod
    def create_well(name: str, inflow_zones: list or None = None) -> Well:
        """
        Создат объект скважины и устанавливет зону притока
        :param name: имя скважина
        :param inflow_zones: зоны притока этой скважины
        :return: объект скважины
        """
        well = Well(name)
        if inflow_zones is not None:
            for inflow_zone in inflow_zones:
                WellConstructor.add_zone(well, inflow_zone)
        return well
