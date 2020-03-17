import SiteScrap
import json

with open('json_site_1.json', 'w', encoding='utf8') as json_file:
    json.dump(SiteScrap.get_site_1_json(), json_file, ensure_ascii=False)
with open('json_site_2.json', 'w', encoding='utf8') as json_file:
    json.dump(SiteScrap.get_site_2_json(), json_file, ensure_ascii=False)
