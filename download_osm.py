import urllib.request


url = "http://download.geofabrik.de/europe/france-updates/000/002/"
for i in range(300, 396):
    filename = str(i) + ".state.txt"
    ddl = url + filename
    urllib.request.urlretrieve(url + filename, "telechargement/" + filename)


