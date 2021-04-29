import vimeo
import csv

# establishing empty dictionary for video information
vvs = {}

# credentials for API request
v = vimeo.VimeoClient(
    token="TOKEN",
    key="KEY",
    secret="SECRET"
)

# Query Phrases
queries = ['suicide workshop', 'suicide training', 'suicide education', 'suicide in-service', 'suicide webinar',
           'suicide learning', 'suicide online course', 'suicide certification', 'self-harm workshop',
           'self-harm training', 'self-harm education', 'self-harm in-service', 'self-harm webinar',
           'self-harm learning', 'self-harm online course', 'self-harm certification', 'self-injury workshop',
           'self-injury training', 'self-injury education', 'self-injury in-service', 'self-injury webinar',
           'self-injury learning', 'self-injury online course', 'self-injury certification']

# Looping through query list and calling API
for ele in queries:
    query = ele

    # Make the request to the server for the "/videos" endpoint.
    response = v.get('/videos', params={'query': query, 'url': "", 'per_page': 100, 'page': 1})
    response1 = response.json()

    # pulling video ids from nested dictionary from API request
    for i in response1['data']:
        vid_id = i['uri']
        title = i['name']
        date = i['release_time']
        link = i['link']
        desc = i['description']
        privacy = i['privacy']
        length = i['duration']
        publisher = i['user']
        language = i['language']
        name_publisher = publisher['name']
        link_publisher = publisher['link']
        bio_publisher = publisher['bio']
        location_publisher = publisher['location']
        source = "vimeo"


        vvs['uri'] = vid_id
        vvs['name'] = title
        vvs['publishedAt'] = date
        vvs['desc'] = desc
        vvs['privacy'] = privacy
        vvs['length (in minutes)'] = float((int(length)/60)/60)
        vvs['language'] = language
        vvs['publisher/channel name'] = name_publisher
        vvs['publisher/channel link'] = link_publisher
        vvs['publisher/channel bio'] = bio_publisher
        vvs['publisher/channel location'] = location_publisher
        vvs['source'] = "vimeo"


        # generating and populating vimeo specific csv with data
        with open("vvs.csv", "a") as vimeo_csv:
            writer = csv.writer(vimeo_csv)
            writer.writerow([vid_id, link, title, date, desc, privacy, length, language, name_publisher, link_publisher,
                            bio_publisher, location_publisher, vvs['source'], query])

        # appending vimeo data to master spreadsheet
        with open("sp_train.csv", "a") as m_csv:
            writer = csv.writer(m_csv)
            writer.writerow([link, title, desc, source, query])
