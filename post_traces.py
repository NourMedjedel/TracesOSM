import requests
import xml.etree.ElementTree as ET
import sys


def post_osc_file(osc_file: str, model_url: str):
    tree = ET.parse(osc_file)
    root = tree.getroot()

    for change in root:

        for element in change:

            timestamp = element.attrib["timestamp"]

            # ChangeNode
            if element.tag == "node":
                json = {
                    "@id": "node_{}".format(element.attrib["id"]),
                    "@type": "m:{}Node".format(change.tag.title()),
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:id": element.attrib["id"],
                    "m:User": element.attrib["user"],
                    "m:Uid": element.attrib["uid"],
                    "m:Latitude": element.attrib["lat"],
                    "m:Longitude": element.attrib["lon"]
                }
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

            # ChangeWay
            elif element.tag == "way":
                json = {
                    "@id": "way_{}".format(element.attrib["id"]),
                    "@type": "m:{}Way".format(change.tag.title()),
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:id": element.attrib["id"],
                    "m:User": element.attrib["user"],
                    "m:Uid": element.attrib["uid"],
                    "m:AddNdTo": {"@id": "{}_{}".format(element.tag, element.attrib["id"])}
                }
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

                # AddNd
                for nd in element.findall("nd"):
                    json = {
                        "@type": "m:AddNd",
                        "beginDT": timestamp,
                        "endDT": timestamp,
                        "m:Ref": nd.attrib["ref"]
                    }
                    r = requests.post(url=model_url, json=json)
                    print(r.status_code, r.reason)

            elif element.tag == "relation":
                json = {
                    "@id": "relation_{}".format(element.attrib["id"]),
                    "@type": "m:{}Relation".format(change.tag.title()),
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:id": element.attrib["id"],
                    "m:User": element.attrib["user"],
                    "m:Uid": element.attrib["uid"]
                }
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

                # AddMember
                for member in element.findall("member"):
                    json = {
                        "@type": "m:AddMember",
                        "beginDT": timestamp,
                        "endDT": timestamp,
                        "m:Type": member.attrib["type"],
                        "m:Ref": member.attrib["ref"],
                        "m:Role": member.attrib["role"],
                        "m:AddMemberTo": {"@id": "{}_{}".format(element.tag, element.attrib["id"])}
                    }
                    r = requests.post(url=model_url, json=json)
                    print(r.status_code, r.reason)

            # AddTag
            for tag in element.findall("tag"):
                json = {
                    "@type": "m:AddTag",
                    "beginDT": timestamp,
                    "endDT": timestamp,
                    "m:Key": tag.attrib["k"],
                    "m:Value": tag.attrib["v"],
                    "m:AddTagTo": {"@id": "{}_{}".format(element.tag, element.attrib["id"])}
                }
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)


def main(argv):
    print("osc_file: {}".format(argv[1]))
    print("model_url: {}".format(argv[2]))
    post_osc_file(osc_file=argv[1], model_url=argv[2])


if __name__ == "__main__":
    argv = sys.argv
    main(argv)
