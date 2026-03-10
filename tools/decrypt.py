from sys import argv
import json
from src.utils.crypt import decrypt

fileName = argv[1]
outJson = argv[2]

data = {}
with open(fileName, 'rb') as f:
    data = decrypt(f.read())

with open(outJson, 'w') as f:
    f.write(json.dumps(data, indent=True))