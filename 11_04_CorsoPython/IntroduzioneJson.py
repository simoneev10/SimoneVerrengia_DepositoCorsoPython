import json

filejson = '{"nome":"Simone","cognome":"Verr"}'

dizionario = json.loads(filejson)

mydict = {'nome': 'Simone', 'cognome': 'Verr'}

myjson = json.dumps(mydict)

print(type(filejson))
print(type(dizionario))
print(myjson)
print(type(myjson))