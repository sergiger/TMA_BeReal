import csv
import requests
import json
import urllib3
import re
import folium
import os
from folium.plugins import MarkerCluster
import webbrowser
from xml_to_dataFrames import transform
import pandas as pd


# convert image links to html tags
def path_to_image_html(path):
    return '<img src="' + path + '" width="100" >'

def program(dataFrame, choice):
    endpoints = set()
    locations = { }
    images = set()
    image_urls = { }

    for index, row in dataFrame.iterrows():
        ip = row['IP address']
        method = row['Method']
        hostname = row['Hostname']
        protocol = row['Protocol']
        port = row['Port']
        lenght = row['Response length']

        x = row['Path'].rfind('/')
        path=row['Path']
        path = path[x + 1 : ]
        file_name, file_extension = os.path.splitext(path)
        if file_extension != '' and ('cdn.bereal.network' in row['URL']):
            images.add(path)
            image_urls[path]=row['URL']

        if ip in endpoints:
            if locations[ip]['method'] != method:
                locations[ip]['method2']=method
                locations[ip]['length2']=int(lenght or 0)

            elif locations[ip]['method'] == method:
                locations[ip]['length'] = int(int(locations[ip]['length']) + int(lenght or 0))

            elif locations[ip]['method2'] == method:
                locations[ip]['length2'] = int(int(locations[ip]['length2']) + int(lenght or 0))

        else:
            endpoints.add(ip)
            info = { }
            info ['name'] = hostname
            info ['port'] = port
            info ['protocol'] = protocol
            info ['length'] = lenght
            info ['method'] = method
            locations[ip]=info

    for val in endpoints:
        req="http://ip-api.com/json/" + val
        response = requests.get(req)
        locations[val]['lon']=response.json()['lon']
        locations[val]['lat']=response.json()['lat']


    world_map= folium.Map(tiles="cartodbpositron")
    marker_cluster = MarkerCluster().add_to(world_map)
    for i in locations:
        lat = locations[i]['lat']
        long = locations[i]['lon']
        radius=5

        if 'method2' not in locations[i]:
            popup_text = """<b>IP</b> : {}<br>
                            <b>Hostname</b> : {}<br>
                            <b>Protocol</b> : {}<br>
                            <b>Port</b> : {}<br>
                            <b>Method</b> : {}<br>
                            <b>Bytes sent</b> : {}"""

            popup_text = popup_text.format(i,locations[i]['name'],locations[i]['protocol'],locations[i]['port'],locations[i]['method'],locations[i]['length'])

        else:
            popup_text = """<b>IP</b> : {}<br>
                            <b>Hostname</b> : {}<br>
                            <b>Protocol</b> : {}<br>
                            <b>Port</b> : {}<br>
                            <b>Method</b> : {}<br>
                            <b>Bytes sent</b> : {}<br>
                            <b>Method</b> : {}<br>
                            <b>Bytes sent</b> : {}"""
            popup_text = popup_text.format(i,locations[i]['name'],locations[i]['protocol'],locations[i]['port'],locations[i]['method'],locations[i]['length'],locations[i]['method2'],locations[i]['length2'])

        folium.CircleMarker(location = [lat, long], radius=radius, popup= popup_text, fill =True).add_to(marker_cluster)

    #images file

    df = pd.DataFrame.from_dict(image_urls, orient='index', columns=['URL'])

    urls = list(image_urls.values())
    df['Image'] = urls

    pd.set_option('display.max_colwidth', None)

    image_cols = ['Image']

    format_dict = {}
    for image_col in image_cols:
        format_dict[image_col] = path_to_image_html

    pattern = '(\w+)\.'
    result = re.search(pattern, choice)
    name = result.group(1)

    with open('../results/'+name +'_captured_images.html', 'w') as fo:
        fo.write(df.to_html(escape=False ,formatters=format_dict))

    webbrowser.open_new_tab('../results/'+ name +'_captured_images.html')

    #map
    world_map.save('../results/'+ name +'_map.html')
    webbrowser.open_new_tab('../results/'+ name +'_map.html')

def addData(dataFrame,name):
    add = input("Do you want to add more data? Yes --> 1 / No --> 0: ")
    while (add != "1" and add != "0"):
        add = input("Please, write 1 or 0, Do you want to add more data? Yes --> 1 / No --> 0: ")
    if (add == "1"):
        choice = "../resources/" + input("Which xml file you want to import?: ")  # <capture>.xml
        exist = os.path.isfile(choice)
        while not exist:
            choice = "../resources/" + input("Which xml file you want to import?: ")
            exist = os.path.isfile(choice)
        dataFrame2 = transform(choice)
        frames = [dataFrame, dataFrame2]
        dataFrame = pd.concat(frames)

        pattern = '(\w+)\.'
        resultDF2 = re.search(pattern, choice)
        name2 = resultDF2.group(1)
        resultDF = re.search(pattern, name)
        name1 = resultDF.group(1)

        name = name1 + "_" + name2 + ".xml"
        dataFrame, name = addData(dataFrame, name)

    return dataFrame, name

def menu():
    # Data imported from a xml file to dataFrame

	# ASIA Captures
    # capture_japan.xml
    # capture_usa_japan.xml

	# EUROPE Captures
    # capture_netherlands.xml
    # capture_spain_v1.xml
    # capture_spain_v2.xml
    # token.xml


    choice = "../resources/" + input("Which xml file you want to import?: ")  # <capture>.xml
    exist = os.path.isfile(choice)
    while not exist:
        choice = "../resources/" + input("Which xml file you want to import?: ")
        exist = os.path.isfile(choice)
    dataFrame = transform(choice)

    dataFrame,name = addData(dataFrame,choice)

    program(dataFrame,name)
menu()
