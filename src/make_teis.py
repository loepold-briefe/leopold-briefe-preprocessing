import glob
import json
import os

import requests
from acdh_tei_pyutils.tei import TeiReader
from jinja2 import Environment, FileSystemLoader
from tqdm import tqdm

from utils import wrap_pb_sections_in_divs

env = Environment(loader=FileSystemLoader("src/templates"))
template = env.get_template("tei-header.xml")

LETTERS_SOURCE = "letters.json"
OUT_DIR = os.path.join("data", "editions")
FALLBACK_TEI = os.path.join("src", "templates", "fallback.xml")
TEI_NS = "http://www.tei-c.org/ns/1.0"

os.makedirs(OUT_DIR, exist_ok=True)


files = sorted(glob.glob("tmp/*/*lb-*.xml"))
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

for key, value in tqdm(metadata.items()):
    file_name = f"{value['lb_id']}.xml"
    save_path = os.path.join(OUT_DIR, file_name)
    tei_file_path = next((path for path in files if path.endswith(file_name)), None)
    context = value
    senders = ", ".join([x["value"] for x in context["sender"]])
    receivers = ", ".join([x["label"] for x in context["receiver"]])
    context["title"] = f"{senders} an {receivers}, {context['written_date']}"
    output = template.render(context)
    header_doc = TeiReader(output)
    header_node = header_doc.any_xpath("./tei:teiHeader")[0]
    if tei_file_path is not None:
        doc = TeiReader(tei_file_path)
    else:
        doc = TeiReader(FALLBACK_TEI)
    for bad in doc.any_xpath(".//tei:teiHeader"):
        bad.getparent().remove(bad)

    new_tag = f"{{{TEI_NS}}}corr"
    for old_tag in doc.any_xpath(".//tei:corrected"):
        old_tag.tag = new_tag

    new_tag = f"{{{TEI_NS}}}w"
    for i, old_tag in enumerate(doc.any_xpath(".//tei:split_word"), start=1):
        old_tag.tag = new_tag
        if i % 2 == 0:
            old_tag.attrib["type"] = "end"
        else:
            old_tag.attrib["type"] = "start"

    doc.tree.getroot().insert(0, header_node)
    wrap_pb_sections_in_divs(doc)
    doc.tree_to_file(save_path)
