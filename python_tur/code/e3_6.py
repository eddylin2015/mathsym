import requests
_url=f" https://xml.smg.gov.mo/c_actual_brief.xml "
_res = requests.get(_url)
_res.encoding = "utf-8"
print(_res.text)
