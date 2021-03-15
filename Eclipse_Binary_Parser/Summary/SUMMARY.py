import numpy as np


class SUMMARY:
    def __init__(self, position_matrix: list, data: list or np.array):
        self.position_matrix = position_matrix
        self.data = data

    def report(self):
        for point in self.position_matrix:
            point("Name: {}\t".format(point[0]),
                  'KeyWord: {}\t'.format(point[1]),
                  'Num: {}'.format(point[2]))

    def get_well_param(self, well_name):
        results = dict()

        for so_id, s_object in enumerate(self.position_matrix):
            if well_name == s_object[0]:
                results[s_object[1]] = self.data[:, so_id]

        return results

    def get_segment_param(self, well_name, segment_name):
        results = dict()

        for so_id, s_object in enumerate(self.position_matrix):
            if well_name == s_object[0] and segment_name == s_object[2]:
                results[s_object[1]] = self.data[:, so_id]

        return results

    def get(self, names: str or list, keywords: str or list,
            nums: int or list) -> list or None:

        if type(names) == list:
            results = []
            for name_id, name in enumerate(names):
                keyword = keywords[name_id]
                num = nums[name_id]

                try:
                    ind = self.position_matrix.index([name, keyword, num])
                except ValueError:
                    print("NO VALUE!")
                    return None

                results.append(self.data[ind])
                return results
        else:

            try:
                ind = self.position_matrix.index([names, keywords, nums])
            except ValueError:
                print("NO VALUE!")
                return None

            return self.data[ind]
