# database package
import sqlite3
import csv

## table read function
def getTable(table,add):
    # connect to database
    db = sqlite3.connect('baggerTool.db',timeout=5)

    # get the names of the columns
    cs = db.execute('SELECT * FROM ' + table)
    ns = [description[0] for description in cs.description]

    # turn the table into a dict list
    result = []
    rows = 1;
    for ci in cs:
        result.append(dict(zip(ns,ci)))
        rows = rows + 1
    if add:
        if table != "MACHINESTATUS":
            result.append(dict(zip(ns,[rows]+[None]*len(ns))))
    else:
        if not result:
            result.append(dict(zip(ns,[rows]+[None]*len(ns))))
    # close connection
    db.close()
    return result


### import database
target = getTable("TARGET",0)
eigenschap = getTable("EIGENSCHAP",0)
heeft = getTable("HEEFT",0)

# create empty sample dictionary
sample = {}

# read csv
with open('monster_8515374.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        for e in eigenschap:
            sample[str(e['EigID'])] = float(row[str(e['Name'])])

# create
target_scores = {}
target_max = {}
for t in target:
    target_scores[str(t['TargetID'])] = 0
    target_max[str(t['TargetID'])] = 0

# check the limits
for h in heeft:
    if h['Min'] <= sample[str(h['EigID'])] and h['Max'] >= sample[str(h['EigID'])]:
        target_scores[str(h['TargetID'])] = target_scores[str(h['TargetID'])] + h['Weight']
    target_max[str(h['TargetID'])] = target_max[str(h['TargetID'])] + h['Weight']

# display results
for t in target:
    print(t['Name']+":"+str(target_scores[str(t["TargetID"])]/target_max[str(t["TargetID"])]))



