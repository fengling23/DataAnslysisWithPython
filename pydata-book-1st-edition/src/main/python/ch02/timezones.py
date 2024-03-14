import json
from collections import defaultdict
path = "pydata-book-1st-edition/ch02/usagov_bitly_data2012-03-16-1331923249.txt" 
records = [json.loads(line) for line in open(path)] 
print(records[0])

time_zones = [rec['tz'] for rec in records if 'tz' in rec] 
print(time_zones[:10])
# time_zones = []
# for rec in records:
# if 'tz' in rec: 
# time_zones.append(rec['tz'])
# print(time_zones[:10])

# Why's the output is diff for line 9 and line 14
# the reason is that the line 9 is a list of string, but line 14 is a list of char# the correct way to do this is to use apend instead of add

def get_counts(sequence) -> int:
    counts ={}
    for x in sequence:
        if x in counts:
            counts[x]+=1
        else:
            counts[x]=1
    return counts

counts = get_counts(time_zones)
print(counts['America/New_York'])

def get_counts2(sequence) -> int:
    counts = defaultdict(int)
    for x in sequence:
        counts[x] += 1
    return counts

counts2 = get_counts2(time_zones) 
print(counts2['America/New_York'])

def get_top_counts(counts_dict,n=10):
    value_key_pairs = [(tz, count) for tz, count in counts_dict.items()]
    # two way to sort list by give attribute
    # return sorted(value_key_pairs, key=lambda x:x[1],reverse=True)[:n]
    value_key_pairs.sort(key=lambda x:x[1], reverse=True)
    return value_key_pairs[:n] 
print(get_top_counts(counts))

# two way to reverse an list
# print(list(reversed(get_top_counts(counts))))
top_counts = get_top_counts(counts)
top_counts.reverse()
print(top_counts)

from collections import Counter 
top_counts2 = Counter(time_zones) 
print(top_counts2.most_common(10))