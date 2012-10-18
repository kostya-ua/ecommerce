from urllib import urlencode
from urllib2 import Request, urlopen, URLError
import xmltodict

from top_secret import CJ_DEV_KEY, CJ_WEB_ID

class HarvesterError(Exception):
    pass

def fetch_merchants(params=None):
    params = (isinstance(params, dict) and params) or {'keywords': 'video'}
    params['records-per-page'] = params.get('records-per-page', 100)
    params['page-number'] = params.get('page-number', 0)
    total_matched = 1
    merchants = list()
    while params['records-per-page']*params['page-number']<total_matched:
        params['page-number'] += 1
        url = 'https://advertiser-lookup.api.cj.com/v3/advertiser-lookup?{}'.format(urlencode(params))
        print url
        request = Request(url, headers={'authorization': CJ_DEV_KEY})
        try:
            xml_response = urlopen(request)
        except URLError, e:
            raise HarvesterError('Failed to fetch merchants from CJ: {}'.format(str(e)))

        response = xmltodict.parse(xml_response).get('cj-api', {}).get('advertisers', {})
        if not response:
            raise HarvesterError('Invalid CJ response')
        try:
            total_matched = int(response.get('@total-matched'))
        except (TypeError, ValueError):
            raise HarvesterError('Invalid CJ response: total_matched')

        merchants.extend(response.get('advertiser', []))

    return merchants