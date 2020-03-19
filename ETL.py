import json
import pandas as pd
import sys

def reference(df):
    headers = ['Last Name', 'Age', 'Address', 'Occupation']
    setlists = list()
    for header in headers:
        name = header.lower().replace(' ', '')
        name = set()
        for v in df[header].values:
            if v not in name:
                name.add(v)
        setlists.append(list(name))
    return setlists # => [[lastnames], [ages], [add], [jobs]]

def add_tag(ref_lists):
    result = dict()
    lastnames, ages, address, jobs = [i for i in ref_lists]
    counts = list()
    for lastname in lastnames:
        count = list()
        sub_df = df[df['Last Name'] == lastname]
        count.append(('lastname', lastname, len(sub_df)))
        for age in ages:
            if len(sub_df[sub_df['Age'] == age]) != 0:
                count.append(('age', age, len(sub_df[sub_df['Age'] == age])))
        for add in address:
            if len(sub_df[sub_df['Address'] == add]) != 0:
                count.append(('add', add, len(sub_df[sub_df['Address'] == add])))
        for job in jobs:
            if len(sub_df[sub_df['Occupation'] == job]) != 0:
                count.append(('job', job, len(sub_df[sub_df['Occupation'] == job])))
        counts.append(count)
    return counts # => [(tag, data, count)]

def outcome(tagged_data):
    result = dict()
    for i in range(len(tagged_data)):
        for j in range(len(tagged_data[i])):

            tag = tagged_data[i][j][0]
            k = tagged_data[i][j][1]
            v = tagged_data[i][j][2]

            if tag == 'lastname':
                key = k
                result[key] = dict()
                result[key]['count'] = v
            if tag == 'age':
                try:
                    result[key]['age']
                except:
                    result[key]['age']= dict()
                result[key]['age'][str(k)] = v
            if tag == 'add':
                try: 
                    result[key]['address']
                except:
                    result[key]['address'] = dict()
                result[key]['address'][k] = v
            if tag == 'job':
                try:
                    result[key]['job']
                except:
                    result[key]['job'] = dict()
                result[key]['job'][k] = v
    return result




with open(sys.argv[1], 'r') as f:
    data = json.load(f)

firstname = list()
lastname = list()
age = list()
address = list()
occupation = list()

for name, v in data.items():
    firstname.append(name.split()[0])
    lastname.append(name.split()[-1])
    age.append(v['age'])
    address.append(v['address'])
    occupation.append(v['occupation'])

df = pd.DataFrame({'First Name': firstname,
                'Last Name': lastname,
        'Age': age,
        'Address': address,
        'Occupation': occupation})

df.to_csv('output_CSV.csv')

ref_lists = reference(df)
tagged_data = add_tag(ref_lists)
outcome = outcome(tagged_data)

json_obj = json.dumps(outcome, indent=2)
with open('output_JSON.json', 'w') as outfile:
    outfile.write(json_obj)

