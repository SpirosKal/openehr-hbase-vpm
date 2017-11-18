import pandas as pd
from itertools import groupby
from operator import itemgetter
import base64
import sys
import numpy as np
from ordereddict import OrderedDict
import requests
import json

baseurl = "http://hostname:51777"


def load_to_hbase (row):
	rows = []
        jsonOutput = { "Row" : rows }
        rowkey = str(row['rowkey'])
        rowKeyEncoded = base64.b64encode(rowkey)
	
	cell = OrderedDict([
                        ("key", rowKeyEncoded),
                        ("Cell",
                        [
                                        { "column" : base64.b64encode("Data:Weight"), "$" : base64.b64encode(str(row['Weight'])) },
                                        { "column" : base64.b64encode("Data:Comment"), "$" : base64.b64encode(str(row['Comment'])) },
                                        { "column" : base64.b64encode("Data:Synopsis"), "$" : base64.b64encode(str(row['Synopsis'])) },
					{ "column" : base64.b64encode("Events:Event"), "$" : base64.b64encode(str(row['Event'])) }
                        ])
                ])

	rows.append(cell)
        jsonOutput = {"Row" : rows}
        #print jsonOutput
        req = requests.post(baseurl + "/vpm/" + rowkey, data=json.dumps(jsonOutput), headers={"Content-Type" : "application/json", "Accept" : "application/json"})
        print "New data has been added for rowkey:" +rowkey+"\n"



initial_df = pd.read_csv(sys.argv[1], sep=',',header=0,encoding='utf8')
print "File procecced:"+sys.argv[1]

initial_df[['time_hours', 'time_ms']] = initial_df['ts_time'].str.split(".", expand=True)
initial_df = initial_df[['part_id','ts_date','Weight','Comment','Any Event','Synopsis','type','archetype_id']].reset_index()
initial_df['rowkey'] = initial_df['part_id'].map(str) + '_' + initial_df['ts_date'].map(str) + '_' + initial_df['type'].map(str) + '_' + initial_df['archetype_id'].map(str)

# Check if dataframe is empty
if final_df.empty:
	print('DataFrame is empty!')
else:

	for index, row in initial_df.iterrows():
		load_to_hbase(row)

