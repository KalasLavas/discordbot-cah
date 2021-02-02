'''CS:GO Marketplace API'''
import requests

URL_INIT = "https://steamcommunity.com/market/appfilters/"
URL_SEARCH = "https://steamcommunity.com/market/search/render/"
URL_IMG = "https://community.cloudflare.steamstatic.com/economy/image/"

class CSGOMarket():
    '''CS:GO Marketplace API'''
    ID = None
    facets = {}
    colors = {}
    def __init__(self, ID):
        self.ID = ID
        '''Get filters'''
        r = requests.get(f"{URL_INIT}{self.ID}")
        filters = r.json()["facets"]
        for i in filters:
            f = {}
            f["name"] = filters[i]["localized_name"]
            f["tags"] = {}
            for j in filters[i]["tags"]:
                f["tags"][j] = filters[i]["tags"][j]["localized_name"]
            self.facets[i] = f
        for i in filters["730_Rarity"]["tags"]:
            self.colors[filters["730_Rarity"]["tags"][i]["localized_name"]] = int(filters["730_Rarity"]["tags"][i]["color"], 16)

    async def search(self, **kwargs):
        '''Search marketplace'''
        q = {
            "start": 0,
            "count": 10,
            "search_descriptiosns": 0,
            "sort_column": "price",
            "sort_dir": "asc",
            "query": "",
            "appid": self.ID,
            "norender": 1,
        }
        params = ""
        for i in q:
            params += f"&{i}={q[i]}"
        for i in kwargs:
            params += f"&{i}={kwargs[i]}"

        j = requests.get(f"{URL_SEARCH}?{params[1:]}").json()
        if j["success"] is not True:
            return {"success": False, "comment": -1}
        j = j["results"]

        res_list = []
        for item in j:
            res = {}
            res["name"] = item["name"] # name_hash ?
            res["listings"] = item["sell_listings"] # name_hash ?
            res["price"] = item["sell_price_text"] # name_hash ?
            res["link"] = f"https://steamcommunity.com/market/listings/{self.ID}/{requests.utils.quote(item['name'])}"
            res["thumbnail"] = f"{URL_IMG}{item['asset_description']['icon_url']}/64fx64f"
            res["color"] = 11584473
            for c in self.colors:
                if c in item["asset_description"]["type"]:
                    res["color"] = self.colors[c]

            res_list.append(res)
        print(res_list)
        return res_list
