import requests
import xml.etree.ElementTree as ET
import sys


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
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

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
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

                # AddNd
                for nd in element.findall('nd'):
                    json = {
                        '@type': 'AddNd',
                        'begin': '{}'.format(timestamp),
                        'end': '{}'.format(timestamp),
                        'ref': nd.attrib['ref']
                    }
                    r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

            elif element.tag == 'relation':
                json = {
                    '@type': '{}Relation'.format(change.tag.title()),
                    'begin': '{}'.format(timestamp),
                    'end': '{}'.format(timestamp),
                    'id': element.attrib['id'],
                    'user': element.attrib['user'],
                    'uid': element.attrib['uid']
                }
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)

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
                    r = requests.post(url=model_url, json=json)
                    print(r.status_code, r.reason)

            # AddTag
            for tag in element.findall('tag'):
                json = {
                    '@type': 'AddTag',
                    'begin': '{}'.format(timestamp),
                    'end': '{}'.format(timestamp),
                    'key': tag.attrib['k'],
                    'value': tag.attrib['v']
                }
                r = requests.post(url=model_url, json=json)
                print(r.status_code, r.reason)


def main(argv):
    print('osc_file: {}'.format(argv[1]))
    print('model_url: {}'.format(argv[2]))
    post_osc_file(osc_file=argv[1], model_url=argv[2])


if __name__ == '__main__':
    argv = sys.argv
    main(argv)
