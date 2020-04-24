# _*_ coding:utf-8 _*_
# Developer: https://github.com/matrixChimera
# Time: 2020-04-20
# File name: settings.py
# IDE: PyCharm
"""
Parameters to define/modify before executing the program.

"""

# region ★★★Define the way and information about logging in
ACCESS = 'institution'  # or 'cookies'

# <editor-fold desc="When logging in via your institution (VPN) – access=='institution'">
# ★★★Define your username:
USERNAME = ''
# ★★★Define your password:
PASSWORD = ''
# ★★★Define your institution:
INSTITUTION = ''
# </editor-fold>

# <editor-fold desc="When logging in via cookies – access=='cookies'">
# ★★★Define Chrome cookies of the URL with Scopus' access:
chrome_cookies = '__cfduid=de2cb44061c647ecd6176148427df848f1587395961;AMCV_4D6368F454EC41940A4C98A6%40AdobeOrg=1075005958%7CMCIDTS%7C18374%7CMCMID%7C11283931343287742372995584673768259797%7CMCAAMLH-1588061914%7C6%7CMCAAMB-1588061914%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1587464314s%7CNONE%7CMCAID%7CNONE%7CMCCIDH%7C-1847371947%7CvVersion%7C4.4.1;AMCVS_4D6368F454EC41940A4C98A6%40AdobeOrg=1;check=true;mbox=PC#52944626c4244004a53099b3b02dcc1f.26_0#1650701912|session#55dd103915ba4fefbf90e427e1995385#1587458905;optimizelyBuckets=%7B%7D;optimizelyEndUserId=oeu1586996998472r0.7901757372226244;optimizelySegments=%7B%22278797888%22%3A%22gc%22%2C%22278846372%22%3A%22false%22%2C%22278899136%22%3A%22none%22%2C%22278903113%22%3A%22referral%22%7D;s_pers=%20v8%3D1587457113963%7C1682065113963%3B%20v8_s%3DLess%2520than%25201%2520day%7C1587458913963%3B%20c19%3Dsc%253Asearch%253Adocument%2520searchform%7C1587458913974%3B%20v68%3D1587457110892%7C1587458913991%3B;s_sess=%20s_sq%3D%3B%20e41%3D1%3B%20s_cpc%3D0%3B%20s_cc%3Dtrue%3B%20s_ppvl%3Dsc%25253Asearch%25253Adocument%252520searchform%252C50%252C50%252C538%252C1024%252C538%252C1024%252C640%252C2%252CP%3B%20s_ppv%3Dsc%25253Asearch%25253Adocument%252520searchform%252C50%252C50%252C538%252C1024%252C538%252C1024%252C640%252C2%252CP%3B;_pk_id.2316.d989=f223f1f709b96ef2.1586963354.24.1587457114.1587457047.;_pk_ref.2316.d989=%5B%22%22%2C%22%22%2C1587457047%2C%22http%3A%2F%2Fwww.2447.net%2Fe%2Faction%2FShowInfo.php%3Fclassid%3D120%26id%3D2193%22%5D;_pk_ses.2316.d989=*;AWSELB=CB9317D502BF07938DE10C841E762B7A33C19AADB1EF83CFB4B2F4E661958A1DAB66E5926523ECF21168EF86C48D5FA693558F487C10BA32070D9964CEACBAE7C5777723B76A5777F7379A060D5A0ABCA8CD2D3536;javaScript=true;NEW_CARS_COOKIE=004D004D00450065006E004A00780055006B004300410053007100300041005300510038003800450033006F0063006C003200320031006C00350075005A00370078004F0041004400740067004C003200610042004300760059004C0050006600640050004A005900330052005700630037004C0035006600510068004100430065003400460077005A005700700071004A004400510062004A0061007600500062006B00660071002F004900350077004800490043006F006D00440077004600520036005700650048004100640038004F0054006600390048004700540062006200380053004B0056006C0039006800480054004E003900770063005400340034004F00620050007300340079007A005000710077003D;scopus.machineID=7DD3FEF74009A32433C0A792D5C1F2F9.wsnAw8kcdt7IPYLO0V48gA;scopusSessionUUID=9461fa86-9c06-4f0c-b;screenInfo="640:1024";SCSessionID=9D8BCB4DD7A64A57C24BFAE9B43FF959.wsnAw8kcdt7IPYLO0V48gA;xmlHttpRequest=true'
# Transform the format of cookies:
COOKIES = dict([l.split("=", 1) for l in chrome_cookies.split(";")])
# </editor-fold>
# endregion


# region Define search query and subyear
# ★★★Define the permissible query (without PUBYEAR) for advanced search:
QUERY = 'TITLE-ABS-KEY(neurofibroma) AND LANGUAGE(english) AND DOCTYPE(ar)'
# ★★★Define start_year & end_year for advanced search:
start_year = 2018
end_year = 2019
YEARS = [str(i) for i in range(start_year, end_year + 1)]
# endregion


# region Define time limit
# Define the longest time (second) of implicitly wait of Selenium' execution:
WAIT_TIME = 30
# Define the time limit to downloading:
DOWNLOAD_TIMEOUT = 90
# Define the sleep time for waiting for the rendering (of HTML/JavaScript):
# (If necessary, please prolong the sleep time,
# especially when your network is slowed down by the Great Firewall in Mainland China)
SLEEPTIME_LONG = 10  # Generally for waiting for redirecting/loading of the search page of Scopus
SLEEPTIME_MEDIUM = 5  # Generally for waiting for interacting with elements shown via rendering of JavaScript
SLEEPTIME_SHORT = 2  # Generally for waiting for interacting with elements shown via rendering of HTML
# Times limit to trying (to download) again:
TRY_AGAIN_TIMES = 5
# endregion
