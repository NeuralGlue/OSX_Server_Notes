# Script to convert URNs used for internal placeholders for OSX CalendarServer 
# into the more general email addressus used by everyone else

# Use this script as a workflow when exporting from 
# CalendarServer into something else

# Input file (userlist.csv) is in the format UUID,email

# fetch the userlist via: dscl /LDAPv3/127.0.0.1 list /Users GeneratedUID

import csv
import re
import os
import glob

def importUserList():
    users = {}
    with open('userlist.csv') as infile:
        reader = csv.reader(infile)
        users = {rows[0]:rows[1] for rows in reader}
    return users

def generate_regexp(userDictLine):
    urn = 'urn:x-uid:' + userDictLine[0]
    res = r"\s*".join(urn[i:i + 1] for i in range(0, len(urn), 1))
    # res = r'B\s?4\s?D\s?1\s?9\s?D\s?C\s?C\s?-\s?7\s?8\s?B\s?7\s+-\s+4\s+E\s+3\s+5\s+-\s+9\s+8\s+6\s+D\s+-\s+6\s+A\s+4\s+9\s+5\s+0\s+B\s+E\s+8\s+B\s+7\s+A'
    return res

def replace_urn_email(users, cal):
    for user in users.items():
        regexp = generate_regexp(user)
        mail = 'mailto:' + user[1]
        matches = re.compile(regexp)
        # print (len(matches.findall(cal)))
        cal = matches.sub(mail, cal)
    return cal

userdict = importUserList()

for filename in glob.glob(os.path.join('input', '*.ics')):
    f = open(filename, 'rb')
    inputcal = f.read().decode(encoding='UTF-8')
    print( 'processing: ' + os.path.split(filename)[1])
    outputcal = replace_urn_email(userdict, inputcal)
    g = open(os.path.join('output',os.path.split(filename)[1]), 'wb')
    g.write(outputcal.encode(encoding='UTF-8'))
    g.close()
    f.close()
