path = "pydata-book-1st-edition/ch02/usagov_bitly_data2012-03-16-1331923249.txt"
lines = open(path).readline()
print(lines)

import json
path = "pydata-book-1st-edition/ch02/usagov_bitly_data2012-03-16-1331923249.txt"
records = [json.loads(line) for line in open(path)]
print(records[0])