import requests
import xml.etree.ElementTree as ET
import os


def get_node(node_id):
    r = requests.get('https://api.openstreetmap.org/api/0.6/node/{}'.format(node_id))
    if r.content:
        root = ET.fromstring(r.content)
        node = root.find('node')
        return node
    else:
        root = get_node_history(node_id=node_id)
        node = root[-2]
        return node


def get_way(way_id):
    r = requests.get('https://api.openstreetmap.org/api/0.6/way/{}'.format(way_id))
    if r.content:
        root = ET.fromstring(r.content)
        way = root.find('way')
        return way
    else:
        root = get_way_history(way_id=way_id)
        way = root[-2]
        return way


def get_relation(relation_id):
    r = requests.get('https://api.openstreetmap.org/api/0.6/relation/{}'.format(relation_id))
    if r.content:
        root = ET.fromstring(r.content)
        relation = root.find('relation')
        return relation
    else:
        root = get_relation_history(relation_id=relation_id)
        relation = root[-2]
        return relation


def get_node_history(node_id):
    r = requests.get('https://api.openstreetmap.org/api/0.6/node/{}/history'.format(node_id))
    root = ET.fromstring(r.content)
    return root


def get_way_history(way_id):
    r = requests.get('https://api.openstreetmap.org/api/0.6/way/{}/history'.format(way_id))
    root = ET.fromstring(r.content)
    return root


def get_relation_history(relation_id):
    r = requests.get('https://api.openstreetmap.org/api/0.6/relation/{}/history'.format(relation_id))
    root = ET.fromstring(r.content)
    return root


def node_in_bbox(node, min_lat: float, max_lat: float, min_lon: float, max_lon: float):
    try:
        lat, lon = float(node.attrib['lat']), float(node.attrib['lon'])
    except AttributeError:
        return False

    if min_lat < lat < max_lat and min_lon < lon < max_lon:
        print(node.attrib['id'])
        return True
    else:
        return False


def add_user_to_node(node):
    api_node = get_node(node.attrib['id'])
    node.set('user', api_node.attrib['user'])
    node.set('uid', api_node.attrib['uid'])


def add_user_to_way(way):
    api_way = get_way(way.attrib['id'])
    way.set('user', api_way.attrib['user'])
    way.set('uid', api_way.attrib['uid'])


def add_user_to_relation(relation):
    api_relation = get_relation(relation.attrib['id'])
    relation.set('user', api_relation.attrib['user'])
    relation.set('uid', api_relation.attrib['uid'])


def way_in_bbox(way, min_lat: float, max_lat: float, min_lon: float, max_lon: float):
    for nd in way.findall('nd'):

        ref = nd.attrib['ref']
        node = get_node(node_id=ref)

        if not node_in_bbox(node=node, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon):
            return False

    return True


def keep_bbox(input_osc: str, output_osc: str, min_lat: float, max_lat: float, min_lon: float, max_lon: float):
    tree = ET.parse(input_osc)
    root = tree.getroot()

    remove_change_list = []

    # modify, create, or delete
    for change in root:

        remove_element_list = []

        for element in change:

            # node
            if element.tag == 'node':

                if not node_in_bbox(node=element, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon):
                    remove_element_list.append(element)

                else:
                    add_user_to_node(element)

            # way
            elif element.tag == 'way':

                for nd in element.findall('nd'):

                    node = get_node(nd.attrib['ref'])

                    if not node_in_bbox(node=node, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon):
                        remove_element_list.append(element)
                        break

                else:
                    add_user_to_way(element)

            # relation
            elif element.tag == 'relation':

                for member in element.findall('member'):

                    # way_id or node_id
                    ref = member.attrib['ref']

                    if member.attrib['type'] == 'node':

                        node = get_node(node_id=ref)
                        if not node_in_bbox(node=node, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon,
                                            max_lon=max_lon):
                            remove_element_list.append(element)
                            break

                    elif member.attrib['type'] == 'way':

                        way = get_way(way_id=ref)

                        if not way_in_bbox(way, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon, max_lon=max_lon):
                            remove_element_list.append(element)
                            break

                else:
                    add_user_to_relation(element)

        for element in remove_element_list:
            change.remove(element)

        if not list(change):
            remove_change_list.append(change)

    for change in remove_change_list:
        root.remove(change)

    tree.write(output_osc)


def parse_directory(in_dir, out_dir):
    min_lat, max_lat, min_lon, max_lon = 45.56679859541312, 45.93530810820467, 4.601434326171898, 5.207186510351221
    files = os.listdir(in_dir)
    for f in files:
        _, extension = os.path.splitext(f)
        input_osc = "{}/{}".format(in_dir, f)
        output_osc = "{}/{}".format(out_dir, f)
        if extension == ".osc":
            print(f)
            keep_bbox(input_osc=input_osc, output_osc=output_osc, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon,
                      max_lon=max_lon)


if __name__ == '__main__':
    """    filename = '{}.osc'.format('test')
        input_osc = 'donnees_osm/{}'.format(filename)
        output_osc = 'donnees_bbox/{}'.format(filename)
        min_lat, max_lat, min_lon, max_lon = 45.56679859541312, 45.93530810820467, 4.601434326171898, 5.207186510351221
        keep_bbox(input_osc=input_osc, output_osc=output_osc, min_lat=min_lat, max_lat=max_lat, min_lon=min_lon,
                  max_lon=max_lon)
                  """
    parse_directory('donnees_osm', 'donnees_bbox')
