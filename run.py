from lib.csv_formatter import CsvFormatter
from lib.csv_aggregater import CsvAggregater

formatter = CsvFormatter('var/sa_log.csv')
formatter.execute()
target_file_path = formatter.get_output_file()

target_file_path = 'var/sa_log_converted.csv'
aggregater = CsvAggregater(target_file_path, {
    'period':'hour',
    'skip_header':True,
    'outputfile_suffix':'_aggregated_hourly'
})
aggregater.execute()

aggregater = CsvAggregater(target_file_path, {
    'period':'day',
    'skip_header':True,
    'outputfile_suffix':'_aggregated_daily'
})
aggregater.execute()
