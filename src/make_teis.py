import glob
import json
import os

import requests
from acdh_tei_pyutils.tei import TeiReader
from tqdm import tqdm

files = sorted(glob.glob("transkribus-out/*/*lb-*.xml"))
print(files)


metadata = requests.get(
    "https://raw.githubusercontent.com/loepold-briefe/leopold-entities/refs/heads/main/json_dumps/letters.json"
).json()
with open("letters.json", "w", encoding="utf-8") as fp:
    json.dump(metadata, fp, ensure_ascii=False)


for x in tqdm(files, total=len(files)):
    file_name = os.path.split(x)[1]
    doc_id = int(file_name.replace(".xml", "").replace("lb-", ""))
    doc = TeiReader(x)
