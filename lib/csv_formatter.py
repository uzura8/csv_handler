import os
import csv
import time
import datetime
from pprint import pprint

class CsvFormatter():
    def __init__(self, input_path, options={}):
        if not input_path or not os.path.isfile(input_path):
            raise Exception('Invalid input_path')

        input_file_name, ext = os.path.splitext(input_path)
        output_file =  '{}_formatted.csv'.format(input_file_name)
        self.options = options
        self.row_input = []
        self.row_input_before = []
        self.row_output = []
        self.row_output_before = []
        self.data_loss_threshold_sec = 62
        self.options = self.init_options(options)
        self.current_is_am = True

        self.fr = open(input_path, 'r')
        self.reader = csv.reader(self.fr) # readerオブジェクトを作成
        self.fw = open(output_file, 'w')
        self.writer = csv.writer(self.fw,
                                lineterminator=self.options['lineterminator'])

    def __del__(self):
        if self.fr:
            self.fr.close()
        if self.fw:
            self.fw.close()

    def init_options(self, options):
        default_options = {
            'lineterminator':'\n',
            'debug':False,
        }
        if not options:
            return default_options

        ret_options = {}
        for key, value in default_options.items():
            try:
                ret_options[key] = options[key]
            except KeyError:
                ret_options[key] = value

        return ret_options


    def format(self):
        self.set_format_header()
        for self.row_input in self.reader:
            self.format_each()
            self.row_input_before = self.row_input


    def format_each(self):
        self.check_and_change_time_period()
        self.set_row_output()
        self.fill_missing_row()
        self.output()
        self.row_output_before = self.row_output


    def set_format_header(self):
        header = ['unix_time', 'datetime', 'input(kB/s)', 'output(kB/s)',
                    'input total(MB)', 'output total(MB)']
        self.output(header)


    def check_and_change_time_period(self):
        if not self.row_input_before:
            return
        hour_str_before = self.row_input_before[1][0:2]
        if hour_str_before != '11':
            return
        hour_str_current = self.row_input[1][0:2]
        if hour_str_current != '12':
            return
        self.current_is_am = not(self.current_is_am)


    def set_row_output(self):
        row = self.row_input
        ts = self.get_format_timestamp(row[0], row[1])
        self.row_output = self.get_format_row(ts, row[4], row[5])


    def get_format_row(self, timestamp, input_per_sec, output_per_sec):
        dt_formatted = self.convert_dateime_format(timestamp)
        return [timestamp, dt_formatted, input_per_sec, output_per_sec,
                self.calc_size_total(input_per_sec),
                self.calc_size_total(output_per_sec)]


    def calc_size_total(self, per_sec_size):
        per_sec_size = float(per_sec_size)
        return per_sec_size * 60 / 1024


    def get_format_timestamp(self, date_str, time_str):
        period = 'AM' if self.current_is_am else 'PM'
        date_time_str = '{} {}{}'.format(date_str, time_str, period)
        dt_raw = time.strptime(date_time_str, '%Y%m%d %I:%M:%S%p')
        return int(time.mktime(dt_raw))


    def fill_missing_row(self):
        if len(self.row_output_before) < 4:
            return
        before = self.row_output_before
        current = self.row_output
        if current[0] - before[0] < self.data_loss_threshold_sec:
            return

        ts = before[0] + 60
        row = self.get_format_row(ts, before[2], before[3])
        self.output(row)
        before = row
        if self.is_debug():
            pprint(row)


    def convert_dateime_format(self, ts):
        return datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M')


    def output(self, row=[]):
        if not row:
            row = self.row_output
        self.writer.writerow(row)


    def is_debug(self):
        return self.options['debug']

