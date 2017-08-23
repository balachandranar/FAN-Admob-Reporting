import requests


def fan_api_request(app_id, access_token, from_epoch_secs, to_epoch_secs, event_name ="fb_ad_network_revenue", agg_by ="SUM"):

    url = "https://graph.facebook.com/v2.10/" + app_id + "/app_insights/app_event/?"\
    "since="+str(from_epoch_secs)+"&"\
    "until="+str(to_epoch_secs)+"&"\
    "summary=true&"\
    "event_name=" + event_name + "&"\
    "aggregateBy=" + agg_by + "&"\
    "access_token=" + access_token

    res = requests.get(url)

    return res