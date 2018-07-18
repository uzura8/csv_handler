import os
import csv

class CsvHandler():
    def __init__(self, input_path, options={}):
        if not input_path or not os.path.isfile(input_path):
            raise Exception('Invalid input_path')

        self.options = self.init_options(options)
        self.output_file = ''
        self.set_output_file(input_path)
        self.row_input = []
        self.row_input_before = []
        self.row_output = []
        self.row_output_before = []
        self.header = ''

        if not os.path.exists(input_path):
            raise Exception('Input file not exists')
        self.fr = open(input_path, 'r')
        self.reader = csv.reader(self.fr) # readerオブジェクトを作成
        if self.options['skip_header']:
            self.header = next(self.reader)  # ヘッダーを読み飛ばしたい時
        self.fw = open(self.output_file, 'w')
        self.writer = csv.writer(self.fw,
                                lineterminator=self.options['lineterminator'])


    def init_options(self, options):
        default_options = {
            'skip_header':False,
            'lineterminator':'\n',
            'debug':False,
            'outputfile_suffix':'_converted',
            'period':'',
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


    def set_output_file(self, input_file_path):
        file_name, ext = os.path.splitext(input_file_path)
        suffix = self.options['outputfile_suffix']
        self.output_file = '{}{}{}'.format(file_name, suffix, ext)


    def get_output_file(self):
        return self.output_file


    def execute(self):
        self.set_format_header()
        self.pre_execute()
        for self.row_input in self.reader:
            self.execute_each()
            self.row_input_before = self.row_input
            self.row_output_before = self.row_output
        self.post_execute()
        self.fr.close()
        self.fw.close()


    def pre_execute(self):
        pass


    def post_execute(self):
        pass


    def output(self, row=[]):
        if not row:
            row = self.row_output
        self.writer.writerow(row)


    def is_debug(self):
        return self.options['debug']

