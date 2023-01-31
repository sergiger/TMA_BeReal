# Importing the required libraries
import xml.etree.ElementTree as Xet
import pandas as pd


def transform(fileToTransform):

    cols = ["Time", "URL", "Hostname", "IP address", "Port", "Protocol", "Method", "Path", "status", "Response length"]
    rows = []

    # Parsing the XML file
    xmlparse = Xet.parse(fileToTransform) #../resources/capturev1.xml
    root = xmlparse.getroot()
    for i in root:
        time = i.find("time").text
        url = i.find("url").text
        host = i.find("host").text
        ip = i.find("host").attrib['ip']
        port = i.find("port").text
        protocol = i.find("protocol").text
        method = i.find("method").text
        path = i.find("path").text
        status = i.find("status").text
        responselength = i.find("responselength").text
        response = i.find("response").text
        request = i.find("request").text

        rows.append({"Time": time,
                     "URL": url,
                     "Hostname": host,
                     "IP address": ip,
                     "Port": port,
                     "Protocol": protocol,
                     "Method": method,
                     "Path": path,
                     "status": status,
                     "Response length": responselength,
                     "Response": response,
                     "Request": request
                     })

    df = pd.DataFrame(rows, columns=cols)

    return df