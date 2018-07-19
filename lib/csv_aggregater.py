from .csv_handler import CsvHandler

class CsvAggregater(CsvHandler):
    def __init__(self, input_path, options={}):
        super().__init__(input_path, options)
        self.check_options()
        self.index = 0
        self.calcvals_tmp = {}
        self.reset_calcvals()


    def check_options(self):
        try:
            period = self.options['period']
        except KeyError:
            raise Exception('Period is not set')

        if not period in ['day', 'hour']:
            raise Exception('Period is invalid')


    def execute_each(self):
        self.check_period_and_output()
        self.add_value()


    def post_execute(self):
        self.output_value_for_period()


    def set_format_header(self):
        header = ['id', 'datetime', 'input_GB', 'output_GB']
        self.output(header)


    def check_period_and_output(self):
        period_key = self.conv_period_key(self.row_input[1])
        if not self.calcvals_tmp['period_key']:
            self.calcvals_tmp['period_key'] = period_key
            return
        if self.calcvals_tmp['period_key'] == period_key:
            return
        self.output_value_for_period()


    def output_value_for_period(self):
        self.set_row_output()
        self.output()
        self.reset_calcvals()


    def conv_period_key(self, datetime_str):
        if self.options['period'] == 'day':
            cut_num = 10
        elif self.options['period'] == 'hour':
            cut_num = 13
        return datetime_str.strip()[0:cut_num]


    def add_value(self):
        self.calcvals_tmp['input'] += float(self.row_input[4])
        self.calcvals_tmp['output'] += float(self.row_input[5])


    def reset_calcvals(self):
        self.calcvals_tmp = {
            'period_key': '',
            'input': 0,
            'output': 0,
        }


    def set_row_output(self):
        self.index += 1

        datetime = self.calcvals_tmp['period_key']
        if self.options['period'] == 'hour':
            datetime += ':00'

        self.row_output = [
            self.index,
            datetime,
            self.calcvals_tmp['input'] / 1024,
            self.calcvals_tmp['output'] / 1024
        ]

