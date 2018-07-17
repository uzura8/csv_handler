import os
import csv
from pprint import pprint

class CsvHandler():
    def __init__(self, input_path, options={}):
        if not input_path or not os.path.isfile(input_path):
            raise Exception('Invalid input_path')

        self.options = self.init_options(options)
        output_file = self.get_output_file_path(input_path)
        self.row_input = []
        self.row_input_before = []
        self.row_output = []
        self.row_output_before = []

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
            'outputfile_suffix':'_converted',
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


    def get_output_file_path(self, input_file_path):
        file_name, ext = os.path.splitext(input_file_path)
        suffix = self.options['outputfile_suffix']
        return '{}{}.{}'.format(file_name, suffix, ext)


    def execute(self):
        self.set_format_header()
        for self.row_input in self.reader:
            self.row_input_before = self.row_input
            self.format_each()
            self.row_output_before = self.row_output


    def output(self, row=[]):
        if not row:
            row = self.row_output
        self.writer.writerow(row)


    def is_debug(self):
        return self.options['debug']

