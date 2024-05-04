import json
from typing import List

from config import paths
from utils import api_calls
from utils import file_operations


def download_events(event_type_ids: List[int], max_results: int, market_starting_after: str, market_starting_before: str):
    payload = json.dumps({
        "filter": {
            "marketBettingTypes": [
                "ODDS"
            ],
            "marketTypeCodes": [
                "MATCH_ODDS"
            ],
            "eventTypeIds": event_type_ids,
            "productTypes": [
                "EXCHANGE"
            ],
            "selectBy": "RANK",
            "contentGroup": {
                "language": "en",
                "regionCode": "UK"
            },
            "maxResults": max_results,
            "marketStartingAfter": market_starting_after,
            "marketStartingBefore": market_starting_before
        },
        "facets": [
            {
                "type": "COMPETITION",
                "maxValues": max_results,
                "skipValues": 0,
                "applyNextTo": 0
            }
        ],
        "currencyCode": "EUR",
        "locale": "en_GB"
    })

    headers = {
        'authority': 'scan-inbf.betfair.com',
        'accept': 'application/json',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'cookie': 'vid=0bca211f-d02b-4f43-b113-bcc555ffc0d3; language=en_GB; betexPtk=betexLocale%3Den%7EbetexRegion%3DGBR; storageSSC=lsSSC%3D1; PI=4546; rfr=4546; _gcl_au=1.1.722555148.1680258028; OptanonAlertBoxClosed=2023-03-31T10:20:51.866Z; Qualtrics_Cookie=123456; TEAL=v:5187372f322604947993333317086516526265d8bb8$t:1680259852653$s:1680258052651%3Bexp-sess$sn:1$en:1; _scid=8a59b9aa-d907-46ee-af22-5fb5f5d71c04; wsid=7dc534d1-d084-11ed-808d-fa163eb1f54f; bfsd=ts=1680350300853|st=rp; BETEX_ESD=accountservices; _gid=GA1.2.783234290.1680350309; promotionCode=EXC520; TrackingTags=promotionCode=EXC520; StickyTags=promotionCode=EXC520; _=1680350305338; exp=ex; _ga=GA1.2.134311722.1680258028; _uetsid=8f6e6800d08411ed9288d3b4c09fac9f; _uetvid=b73d5790cfad11edbde397c061670382; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+01+2023+13%3A59%3A23+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=6.18.0&isIABGlobal=false&hosts=&consentId=5f92b82f-76b6-4523-90b1-c812111187af&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; _gat=1; _ga_K0W97M6SNZ=GS1.1.1680350327.2.1.1680350786.31.0.0',
        'origin': 'https://www.betfair.com',
        'pragma': 'no-cache',
        'referer': 'https://www.betfair.com/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = api_calls.call_api("POST", "/www/sports/navigation/facet/v1/search?_ak=nzIFcwyWhrlwYMrh&alt=json",
                                  payload, headers)
    file_operations.save_json(paths.events_filename, response)


def download_markets(market_ids: List[str], limit: int):
    market_ids = ",".join(market_ids)

    payload = ''
    headers = {
        'authority': 'ero.betfair.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        'cookie': 'vid=0bca211f-d02b-4f43-b113-bcc555ffc0d3; language=en_GB; betexPtk=betexLocale%3Den%7EbetexRegion%3DGBR; storageSSC=lsSSC%3D1; PI=4546; rfr=4546; _gcl_au=1.1.722555148.1680258028; OptanonAlertBoxClosed=2023-03-31T10:20:51.866Z; Qualtrics_Cookie=123456; TEAL=v:5187372f322604947993333317086516526265d8bb8$t:1680259852653$s:1680258052651%3Bexp-sess$sn:1$en:1; _scid=8a59b9aa-d907-46ee-af22-5fb5f5d71c04; wsid=7dc534d1-d084-11ed-808d-fa163eb1f54f; bfsd=ts=1680350300853|st=rp; BETEX_ESD=accountservices; _gid=GA1.2.783234290.1680350309; promotionCode=EXC520; TrackingTags=promotionCode=EXC520; StickyTags=promotionCode=EXC520; _=1680350305338; exp=ex; _ga=GA1.2.134311722.1680258028; _uetsid=8f6e6800d08411ed9288d3b4c09fac9f; _uetvid=b73d5790cfad11edbde397c061670382; OptanonConsent=isGpcEnabled=0&datestamp=Sat+Apr+01+2023+13%3A59%3A23+GMT%2B0200+(czas+%C5%9Brodkowoeuropejski+letni)&version=6.18.0&isIABGlobal=false&hosts=&consentId=5f92b82f-76b6-4523-90b1-c812111187af&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&geolocation=%3B&AwaitingReconsent=false; _gat=1; _ga_K0W97M6SNZ=GS1.1.1680350327.2.1.1680350787.30.0.0',
        'origin': 'https://www.betfair.com',
        'pragma': 'no-cache',
        'referer': 'https://www.betfair.com/',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36'
    }
    response = api_calls.call_api("GET",
                                  f"/www/sports/exchange/readonly/v1/bymarket?_ak=nzIFcwyWhrlwYMrh&alt=json&currencyCode=EUR&locale=en_GB&marketIds={market_ids}&rollupLimit={limit}&rollupModel=STAKE&types=MARKET_STATE,MARKET_RATES,MARKET_DESCRIPTION,EVENT,RUNNER_DESCRIPTION,RUNNER_STATE,RUNNER_EXCHANGE_PRICES_BEST,RUNNER_METADATA,MARKET_LINE_RANGE_INFO",
                                  payload, headers)
    file_operations.save_json(paths.markets_filename, response)
