import time
from apiclient import sample_tools
from oauth2client import client
import TimeUtils

MAX_PAGE_SIZE = 50
DATE_FORMAT = '%Y-%m-%d'
MONTH_FORMAT = '%Y-%m'


def init_auth(argv=[]):
    # Authenticate and construct service.

    service, unused_flags = sample_tools.init(
        argv, 'adsense', 'v1.4', __doc__, __file__, parents=[],
        scope='https://www.googleapis.com/auth/adsense.readonly')
    return service


def get_account_id(service):
    """Gets the AdSense account id, letting the user choose if multiple exist.
    Args:
      service: the Adsense service used to fetch the accounts.
    Returns:
      The selected account id.
    """
    account_id = None
    accounts = service.accounts().list().execute()
    if len(accounts['items']) == 1:
        account_id = accounts['items'][0]['id']
    else:
        print ('Multiple accounts were found. Please choose:')
        for i, account in enumerate(accounts['items']):

            print (' %d) %s (%s)' % (i + 1, account['name'], account['id']))
        selection = (input('Please choose number 1-%d>'
                               % (len(accounts['items']))))
        account_id = accounts['items'][int(selection) - 1]['id']
    return account_id


def get_payments(service):
    try:
        # Let the user pick account if more than one.
        account_id = get_account_id(service)
        # Retrieve payments list in pages and display data as we receive it.
        request = service.accounts().payments().list(accountId=account_id)
        if request is not None:
            result = request.execute()
            if 'items' in result:
                payments = result['items']
                for payment in payments:
                    print ('Payment with id "%s" of %s %s and date %s was found. '
                           % (str(payment['id']),
                              payment['paymentAmount'],
                              payment['paymentAmountCurrencyCode'],
                              payment.get('paymentDate', 'unknown')))
            else:
                print ('No payments found!')
    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
        'application to re-authorize')


def get_earnings(service, start_date, end_date):
    try:
        # Let the user pick account if more than one.
        account_id = get_account_id(service)
        result = service.accounts().reports().generate(
            accountId=account_id, startDate=start_date, endDate=end_date,
            useTimezoneReporting=False,
            metric=['EARNINGS'],
            dimension=['DATE']).execute()
        if result is not None:
            days_earnings_tuple = result['rows']
            return days_earnings_tuple

    except client.AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
               'application to re-authorize')


