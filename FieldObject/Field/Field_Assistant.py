

def get_params(pattern: list, wells_dict: dict, param: str) -> list:
    params_list = []

    for object_id in pattern:
        well = object_id[0]
        inflow_zones = object_id[1]
        param = wells_dict[well].get_param(param, inflow_zones)
        params_list.append(param)

    return params_list



