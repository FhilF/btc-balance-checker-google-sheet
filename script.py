import csv
import requests
import json
import gspread


gc = gspread.service_account(filename='credentials.json')
sh = gc.open_by_key('1Po6VBuXYCSJW8bP26fQbbHD0wBLjyUZQS2L8a-5kSLc')
worksheet = sh.sheet1


def toFloatStr(bitcoin):
    x = float(bitcoin)
    return str(x/100000000)

result = []
with open("wallets.csv", "r") as f:
    reader = csv.reader(f, delimiter="\t")
    for i, line in enumerate(reader):
        result.append(line)

info = []
for line in result:
    result = str(line).strip("[]'")
    info.append([str(result.split(",")[0]),str(result.split(",")[1]),str(result.split(",")[2]),str(result.split(",")[3]),str(result.split(",")[4]),str(result.split(",")[5])])

wallets = ""
for line in info:
    wallets += line[1] + '|'
wallets = (wallets[:-1]) + '&n=0'
url = "https://blockchain.info/multiaddr?active=" + wallets

response = requests.get(url)


if response.status_code == 200:
    print('success')

    requestResult = response.json()

    finalResult = []
    for req in requestResult['addresses']:
        address = req['address']
        for details in info:
            if details[1] == address:
                finalResult.append([details[0], details[1], toFloatStr(req['total_sent']), toFloatStr(req['total_received']), toFloatStr(req['final_balance']), details[2],details[3], details[4], details[5]])

    print(finalResult)
    worksheet.append_rows(finalResult)
