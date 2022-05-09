import json
import string

def clean_up_name(name: str) -> str:
	name = name.replace("http://", "").replace("https://", "")
	for punc in string.punctuation:
		name = name.replace(punc, "_")
	return name

def save(file_name: str, data: any):
	file_name = clean_up_name(file_name)
	with open("./data/" + file_name, "w") as f:
		f.write(json.dumps(data))

def get(file_name: str) -> any:
	file_name = clean_up_name(file_name)
	with open("./data/" + file_name, "r") as f:
		return json.loads(f.read())