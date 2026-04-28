from lxml import etree


def wrap_pb_sections_in_divs(doc):
    ns_uri = doc.tree.getroot().nsmap.get(None)
    if not ns_uri:
        return

    pb_tag = f"{{{ns_uri}}}pb"
    div_tag = f"{{{ns_uri}}}div"
    parents = {pb.getparent() for pb in doc.any_xpath(".//tei:pb")}

    for parent in parents:
        children = list(parent)
        if not children or not any(child.tag == pb_tag for child in children):
            continue

        new_children = []
        current_div = None
        for child in children:
            if child.tag == pb_tag:
                current_div = etree.Element(div_tag)
                current_div.attrib["type"] = "page"
                current_div.append(child)
                new_children.append(current_div)
            elif current_div is not None:
                current_div.append(child)
            else:
                new_children.append(child)

        parent[:] = new_children
