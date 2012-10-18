from urllib import urlencode
from urllib2 import Request, urlopen, URLError
import xmltodict

from top_secret import CJ_DEV_KEY, CJ_WEB_ID

class HarvesterError(Exception):
    pass

def fetch_cj_data(params, url, item):
    params['records-per-page'] = params.get('records-per-page', 100)
    params['page-number'] = params.get('page-number', 1) - 1
    total_matched = 1
    data = list()
    while params['records-per-page']*params['page-number']<total_matched:
        params['page-number'] += 1
        request = Request('{link}?{args}'.format(link=url, args=urlencode(params)), headers={'authorization': CJ_DEV_KEY})
        try:
            xml_response = urlopen(request)
        except URLError, e:
            raise HarvesterError('Failed to fetch {}s from CJ: {}'.format(item, str(e)))

        response = xmltodict.parse(xml_response).get('cj-api', {}).get('{}s'.format(item))
        if not response:
            raise HarvesterError('Invalid CJ response')
        try:
            total_matched = int(response.get('@total-matched'))
        except (TypeError, ValueError):
            raise HarvesterError('Invalid CJ response: total_matched')

        data.extend(response.get(item, []))

    return data


def fetch_merchants(params=None):
    params = (isinstance(params, dict) and params) or {'keywords': 'video'}
    return fetch_cj_data(params, 'https://advertiser-lookup.api.cj.com/v3/advertiser-lookup/', 'advertiser')

def fetch_deals(params=None):
    params = (isinstance(params, dict) and params) or {'advertiser-ids': 3634487}
    params['website-id'] = params.get('website-id', CJ_WEB_ID)
    return fetch_cj_data(params, 'https://linksearch.api.cj.com/v2/link-search/', 'link')