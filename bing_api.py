import isodate
import requests
import csv

'''
This sample makes a call to the Bing Video Search API with a topic query and returns relevant video with data.

Documentation: https: // docs.microsoft.com/en-us/azure/cognitive-services/bing-web-search/
'''

# Bing Search V7 subscription key and endpoint to your environment variables.
subscriptionKey = "KEY"
endpoint = "VIDEO ENDPOINT"

# Search Query list
queries = ['suicide workshop', 'suicide training', 'suicide education', 'suicide in-service', 'suicide webinar',
           'suicide learning', 'suicide online course', 'suicide certification', 'self-harm workshop',
           'self-harm training', 'self-harm education', 'self-harm in-service', 'self-harm webinar',
           'self-harm learning', 'self-harm online course', 'self-harm certification', 'self-injury workshop',
           'self-injury training', 'self-injury education', 'self-injury in-service', 'self-injury webinar',
           'self-injury learning', 'self-injury online course', 'self-injury certification']

# Looping through queries
for ele in queries:
    query = ele

    # build API request
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscriptionKey
    }
    params = {"q": query, "count": 105, "offset": 0}

    # Call the API
    response = requests.get(endpoint, headers=headers, params=params)
    response1 = response.json()

    for i in response1['value']:
        title = i['name']

        if "datePublished" in i:
            date = isodate.parse_datetime(i['datePublished'])
        else:
            date = "not provided"

        link = i['contentUrl']

        if "description" in i:
            desc = i["description"]
        else:
            desc = "not provided"

        if "free" in i:
            free = i['isAccessibleForFree']
        else:
            free = "not provided"

        if 'duration' in i:
            length = isodate.parse_duration(i['duration'])
        else:
            length = "not provided"

        if "view" in i:
            views = i['viewCount']
        else:
            views = "not provided"

        if "creator" in i:
            cont_creator = i['creator']
            creator = cont_creator['name']
        else:
            creator = "not provided"

        if "publisher" in i:
            name_publisher = i['publisher']
        else:
            name_publisher = "not provided"

        try:
            link_publisher = i['hostPageUrl']
        except AttributeError:
            link_publisher = "not provided"

        source = "bing video"

        # generating and populating bing specific csv with data
        with open("bvs.csv", "a") as b_csv:
            writer = csv.writer(b_csv)
            writer.writerow([title, date, desc, free, length, views, creator,
                             name_publisher, link_publisher, source, params['q']])

        # appending bing data to master spreadsheet
        with open("sp_train.csv", "a") as m_csv:
            writer = csv.writer(m_csv)
            writer.writerow([link, title, desc, source, query])
