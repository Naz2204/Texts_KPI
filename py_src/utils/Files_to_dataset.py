from pypdf import PdfReader
from os import listdir
import json

texts = []
labels = []
for i in listdir("../training_data/manual/"):
    reader = PdfReader("../training_data/manual/" + i)
    extracted = "".join([page.extract_text() for page in reader.pages])
    texts.append(extracted)
    labels.append("manual")


for i in listdir("../training_data/report/"):
    reader = PdfReader("../training_data/report/" + i)
    extracted = "".join([page.extract_text() for page in reader.pages])
    texts.append(extracted)
    labels.append("report")


for i in listdir("../training_data/research/"):
    reader = PdfReader("../training_data/research/" + i)
    extracted = "".join([page.extract_text() for page in reader.pages])
    texts.append(extracted)
    labels.append("research")



with open("./extracted_data.json", "w") as out_file:
    json.dump({
        "texts": texts,
        "labels": labels
    }, out_file, indent=3)