import requests
import xml.etree.ElementTree as ET
import sys


def post(url, json):
    r = requests.post(url=url, json=json)
    if r.status_code >= 300:
        print(r.status_code, r.reason)
        print(json)


def post_osc_file(osc_file: str, trace_url: str):
    tree = ET.parse(osc_file)
    root = tree.getroot()

    for change in root:

        for element in change:

            timestamp = element.attrib["timestamp"]

            # ChangeNode
            if element.tag == "node":
                json = {
                    "@id": "node_{}_{}".format(element.attrib["id"], element.attrib["version"]),
                    "@type": "m:{}Node".format(change.tag.title()),
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:id": int(element.attrib["id"]),
                    "m:User": element.attrib["user"],
                    "m:Uid": int(element.attrib["uid"]),
                    "m:Version": int(element.attrib["version"]),
                    "m:Latitude": float(element.attrib["lat"]),
                    "m:Longitude": float(element.attrib["lon"])
                }
                post(url=trace_url, json=json)

            # ChangeWay
            elif element.tag == "way":
                json = {
                    "@id": "way_{}_{}".format(element.attrib["id"], element.attrib["version"]),
                    "@type": "m:{}Way".format(change.tag.title()),
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:id": int(element.attrib["id"]),
                    "m:User": element.attrib["user"],
                    "m:Uid": int(element.attrib["uid"]),
                    "m:Version": int(element.attrib["version"])
                }
                post(url=trace_url, json=json)

                # AddNd
                for nd in element.findall("nd"):
                    json = {
                        "@type": "m:AddNd",
                        "beginDT": timestamp,
                        "endDT": timestamp,
                        "m:Ref": int(nd.attrib["ref"]),
                        "m:AddNdTo": {
                            "@id": "{}_{}_{}".format(element.tag, element.attrib["id"], element.attrib["version"])}
                    }
                    post(url=trace_url, json=json)

            # ChangeRelation
            elif element.tag == "relation":
                json = {
                    "@id": "relation_{}_{}".format(element.attrib["id"], element.attrib["version"]),
                    "@type": "m:{}Relation".format(change.tag.title()),
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:id": int(element.attrib["id"]),
                    "m:User": element.attrib["user"],
                    "m:Uid": int(element.attrib["uid"]),
                    "m:Version": int(element.attrib["version"])
                }
                post(url=trace_url, json=json)

                # AddMember
                for member in element.findall("member"):
                    json = {
                        "@type": "m:AddMember",
                        "beginDT": timestamp,
                        "endDT": timestamp,
                        "m:Type": member.attrib["type"],
                        "m:Ref": int(member.attrib["ref"]),
                        "m:Role": member.attrib["role"],
                        "m:AddMemberTo": {
                            "@id": "{}_{}_{}".format(element.tag, element.attrib["id"], element.attrib["version"])}
                    }
                    post(url=trace_url, json=json)

            # AddTag
            for tag in element.findall("tag"):
                json = {
                    "@type": "m:AddTag",
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:Key": tag.attrib["k"],
                    "m:Value": tag.attrib["v"],
                    "m:AddTagTo": {
                        "@id": "{}_{}_{}".format(element.tag, element.attrib["id"], element.attrib["version"])}
                }
                post(url=trace_url, json=json)


def post_trace(base_url: str, trace_id, model_id):
    model_url = base_url + model_id
    json = {
        "@id": "{}".format(trace_id),
        "@type": "StoredTrace",
        "hasModel": model_url,
        "origin": "1970-01-01T00:00:00Z"
    }
    post(url=base_url, json=json)
    return "{}{}/".format(base_url, trace_id)


def post_dir():
    base_url = "http://localhost:8001/osm/"
    for i in range(300, 318):
        osc_file = "donnees_bbox/{}.osc".format(i)
        trace_url = post_trace(base_url=base_url, trace_id=i, model_id="model1")
        print(osc_file, trace_url)
        post_osc_file(osc_file=osc_file, trace_url=trace_url)


if __name__ == "__main__":
    argv = sys.argv
    # post_osc_file(osc_file=argv[1], trace_url=argv[2])
    post_dir()
