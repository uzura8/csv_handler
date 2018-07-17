import time
import datetime
from pprint import pprint
from .csv_handler import CsvHandler

class CsvFormatter(CsvHandler):
    def __init__(self, input_path, options={}):
        super().__init__(input_path, options)
        self.data_loss_threshold_sec = 62
        self.current_is_am = True


    def format_each(self):
        self.check_and_change_time_period()
        self.set_row_output()
        self.fill_missing_row()
        self.output()


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

