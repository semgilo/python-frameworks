import os
import xlrd
import json
from frameworks.utils.log import Log


class ExcelParser:
    """
    Excel format like these expected:
    id   |   name  |  age  |   products  | children
    int  |  string |  int  | vector<int> | vector<string>
    1    |  Frank  |  31   | 1|1|1       | Lucy|Lily|Jim
    ...
    """

    @classmethod
    def __init__(self):
        "docstring"
        self._fields = []
        self._types = []
        self._datas = {}

    @classmethod
    def save_to_json(self, path):
        file = open(path, "w")
        json.dump(self._datas, file)
        file.close()

    @classmethod
    def parse_value_by_type(self, value, type):
        if type == "int":
            return int(value)
        elif type == "string":
            return str(value)
        elif type == "vector<int>":
            values = value.split("|")
            int_values = []
            for var in values:
                int_values.append(int(var))
            return int_values
        elif type == "vector<string>":
            values = value.split("|")
            return values
        else:
            Log.w("unknow type: " + type)
            return value

    @classmethod
    def parse_line(self, line):
        line_value = {}
        for i in range(len(line)):
            var = line[i]
            type = self._types[i]
            field = self._fields[i]
            line_value[field] = self.parse_value_by_type(var, type)
        return line_value

    @classmethod
    def parse(self, path):
        if os.path.splitext(path)[1] != '.xlsx':
            Log.w('unavailable file type!')
            return
        self._datas = {}
        xlsx = xlrd.open_workbook(path)
        sheets = xlsx.sheets()
        table = sheets[0]
        rowcount = table.nrows

        for i in range(rowcount):
            if i == 0:
                self._fields = table.row_values(i)
            elif i is 1:
                self._types = table.row_values(i)
            else:
                line = table.row_values(i)
                line_value = self.parse_line(line)
                line_id = line_value['id']
                if line_id is None:
                    Log.e('The id field must be nonil expected')
                    continue

                if line_id in self._datas:
                    Log.w('The table contains multipe line in a same id')
                    continue

                self._datas[line_id] = line_value

        return self._datas
