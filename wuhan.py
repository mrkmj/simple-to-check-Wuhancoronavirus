
# coding=utf-8

import requests
import re
import json
import os


targetProvinceName = {}

# 额外看到的省份
additionProvinceName = {"广东"}


# 武汉加油

def showProvinceInfo(province):
    provinceName = province.get('provinceShortName')
    provinceConfirmedCount = province.get('confirmedCount')
    provinceDeadCount = province.get('deadCount')
    provinceCuredCount = province.get('curedCount')

    displayString = "%s 确: %s 亡: %s 愈: %s" % (
        provinceName, provinceConfirmedCount, provinceDeadCount, provinceCuredCount)
    print(displayString)



def main():
    bitBarDarkMode = os.getenv('BitBarDarkMode', 0)
    textColor = "black"
    if bitBarDarkMode:
        textColor = "white"

    response = requests.get('https://3g.dxy.cn/newh5/view/pneumonia')
    response.encoding = 'utf-8'

    rawresult = re.search(
        '<script id="getAreaStat">(.*)</script>', response.text)
    provincedata = re.search(
        '\[.*\]', rawresult.group(1)).group(0).split('catch')

    finalresult = provincedata[0]
    finalresult = finalresult[0:-1]

    jsondata = json.loads(finalresult)

    chinaConfirmCount = 0
    chinaCuredCount = 0
    chinaDeadCount = 0

    for province in jsondata:
        chinaConfirmCount += province.get('confirmedCount')
        chinaDeadCount += province.get('deadCount')
        chinaCuredCount += province.get('curedCount')

    displayString = "全国 确: %s 亡: %s 愈 %s" % (
        chinaConfirmCount, chinaDeadCount, chinaCuredCount)
    print(displayString)
    print('---前五省份数据---')

    if len(targetProvinceName) > 0:
        for province in jsondata:
            showProvinceInfo(province)
    else:
        for index in range(5):
            province = jsondata[index]
            provinceName = province.get('provinceShortName')
            showProvinceInfo(province)
    
    print('---广东省份数据---')

    for province in jsondata:
        provinceName = province.get('provinceShortName')
        if provinceName in additionProvinceName:
            
            showProvinceInfo(province)

            comment = province.get("comment")
            if comment:
                print('--' + comment)

            cityList = province.get('cities')
            for city in cityList:
                cityDataStr = "%s 确：%s 亡：%s 愈：%s" % (city.get('cityName'), city.get(
                    'confirmedCount'), city.get('deadCount'), city.get('curedCount'))
                print('--' + cityDataStr)

    print('\n------END------')


if __name__ == "__main__":
    main()
