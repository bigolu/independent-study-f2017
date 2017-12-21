from pprint import pprint
import json
import sys

input = sys.argv[1]
#Casting input to a string with str(input)
with open(str(input)) as json_data:
    f = json.load(json_data)
    pprint(f)





