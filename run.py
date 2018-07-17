from lib.csv_formatter import CsvFormatter

#csv_formatter = CsvFormatter('sa_log.csv', {'debug':True})
csv_formatter = CsvFormatter('var/sa_log.csv')
csv_formatter.execute()
#csv_formatter.compile('hourly')
#csv_formatter.compile('daily')
