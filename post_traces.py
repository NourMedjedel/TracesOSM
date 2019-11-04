import requests
import xml.etree.ElementTree as ET


def post_osc_file(osc_file: str, model_url: str):
    tree = ET.parse(osc_file)
    root = tree.getroot()

    for change in root:

        for element in change:

            timestamp = element.attrib['timestamp']

            # ChangeNode
            if element.tag == 'node':
                json = {
                    '@type': '{}Node'.format(change.tag.title()),
                    'begin': '{}'.format(timestamp),
                    'end': '{}'.format(timestamp),
                    'id': element.attrib['id'],
                    'user': element.attrib['user'],
                    'uid': element.attrib['uid'],
                    'lat': element.attrib['lat'],
                    'lon': element.attrib['lon']
                }
                requests.post(url=model_url, json=json)

            # ChangeWay
            elif element.tag == 'way':
                json = {
                    '@type': '{}Way'.format(change.tag.title()),
                    'begin': '{}'.format(timestamp),
                    'end': '{}'.format(timestamp),
                    'id': element.attrib['id'],
                    'user': element.attrib['user'],
                    'uid': element.attrib['uid']
                }
                requests.post(url=model_url, json=json)

                # AddNd
                for nd in element.findall('nd'):
                    json = {
                        '@type': 'AddNd',
                        'begin': '{}'.format(timestamp),
                        'end': '{}'.format(timestamp),
                        'ref': nd.attrib['ref']
                    }
                    requests.post(url=model_url, json=json)

            elif element.tag == 'relation':
                json = {
                    '@type': '{}Relation'.format(change.tag.title()),
                    'begin': '{}'.format(timestamp),
                    'end': '{}'.format(timestamp),
                    'id': element.attrib['id'],
                    'user': element.attrib['user'],
                    'uid': element.attrib['uid']
                }
                requests.post(url=model_url, json=json)

                # AddMember
                for member in element.findall('member'):
                    json = {
                        '@type': 'AddMember',
                        'begin': '{}'.format(timestamp),
                        'end': '{}'.format(timestamp),
                        'type': member.attrib['type'],
                        'ref': member.attrib['ref'],
                        'role': member.attrib['role']
                    }
                    requests.post(url=model_url, json=json)

            # AddTag
            for tag in element.findall('tag'):
                json = {
                    '@type': 'AddTag',
                    'begin': '{}'.format(timestamp),
                    'end': '{}'.format(timestamp),
                    'key': tag.attrib['k'],
                    'value': tag.attrib['v']
                }
                requests.post(url=model_url, json=json)


if __name__ == '__main__':
    url = "http://localhost:8001/osm/traces"
