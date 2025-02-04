import requests
import os
import pandas
from airflow.models import Variable


def generate_acess_token():
    client_id = Variable.get('CLIENT_ID')
    client_secret = Variable.get('CLIENT_SECRET')
    region = 'eu'
    data = {"grant_type": "client_credentials"}
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))
    if response.status_code == 200:
        return response.json()["access_token"]
    else :
        return None

def item_api_call():
    min_id_in_page = 1
    access_token = generate_acess_token()
    next_page = True
    idList = []
    nameList = []
    itemSubClassList = []
    itemClassList = []
    qualityList = []
    if access_token is not None :
        while next_page == True:

            url = f"https://eu.api.blizzard.com/data/wow/search/item?namespace=static-eu&orderby=id&_pageSize=1000&_page=1&id=[{str(min_id_in_page)},]"

            result = requests.get(url,
                headers={'Content-Type':'application/json',
                        'Authorization': 'Bearer {}'.format(access_token)})
            json_result = result.json()
            json_result=json_result["results"]
            
            for item in json_result :
                idList.append(item.get("data", {}).get("media", {}).get("id", None))
                nameList.append(item.get("data", {}).get("name", {}).get("en_US", None))
                itemSubClassList.append(item.get("data", {}).get("item_subclass", {}).get("name", {}).get("en_US", None))
                itemClassList.append(item.get("data", {}).get("item_class", {}).get("name", {}).get("en_US", None))
                qualityList.append(item.get("data", {}).get("quality", {}).get("name", {}).get("en_US", None))

            if min_id_in_page == idList[len(idList)-1]+1 :
                next_page = False
            else :
                min_id_in_page = idList[len(idList)-1]+1

        df = pandas.DataFrame({'id': idList, 'name': nameList, "subClass": itemSubClassList, 'class': itemClassList, 'quality': qualityList})
        df.set_index('id',inplace=True)
        df.to_csv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../dbt_WoW_Auction_House/seeds/item_list.csv"))

if __name__ == "__main__":
    item_api_call()