import glob
import json
import os

import requests
from acdh_tei_pyutils.tei import TeiReader
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

env = Environment(loader=FileSystemLoader("src/templates"))
template = env.get_template("tei-header.xml")

LETTERS_SOURCE = "letters.json"
OUT_DIR = os.path.join("data", "editions")

os.makedirs(OUT_DIR, exist_ok=True)

files = sorted(glob.glob("transkribus-out/*/*lb-*.xml"))
try:
    with open(LETTERS_SOURCE, "r", encoding="utf-8") as fp:
        metadata = json.load(fp)
except FileNotFoundError:
    print(f"{LETTERS_SOURCE} does not exist, need to download it first")
    metadata = requests.get(
        f"https://raw.githubusercontent.com/loepold-briefe/leopold-entities/refs/heads/main/json_dumps/{LETTERS_SOURCE}"
    ).json()
    with open(LETTERS_SOURCE, "w", encoding="utf-8") as fp:
        json.dump(metadata, fp, ensure_ascii=False)


for x in tqdm(files, total=len(files)):
    file_name = os.path.split(x)[1]
    save_path = os.path.join(OUT_DIR, file_name)
    doc_id = str(int(file_name.replace(".xml", "").replace("lb-", "")))
    doc = TeiReader(x)
    context = metadata[doc_id]
    output = template.render(context)
    header_doc = TeiReader(output)
    header_node = header_doc.any_xpath("./tei:teiHeader")[0]
    for bad in doc.any_xpath(".//tei:teiHeader"):
        bad.getparent().remove(bad)
    doc.tree.getroot().insert(0, header_node)
    doc.tree_to_file(save_path)
