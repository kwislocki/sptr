from googleapiclient.discovery import build
import isodate
import csv

na = "not provided"

# API key
api_key = "API KEY"

# next page tokens for youtube
next_page = []

# query list
query = ['suicide workshop', 'suicide training', 'suicide education', 'suicide in-service', 'suicide webinar',
         'suicide learning', 'suicide online course', 'suicide certification', 'self-harm workshop',
         'self-harm training', 'self-harm education', 'self-harm in-service', 'self-harm webinar',
         'self-harm learning', 'self-harm online course', 'self-harm certification', 'self-injury workshop',
         'self-injury training', 'self-injury education', 'self-injury in-service', 'self-injury webinar',
         'self-injury learning', 'self-injury online course', 'self-injury certification']

# page tokens
try:
    pt = next_page[-1]

except IndexError:
    pt = ""

# building API request for each query phrase
for ele in query:
    api_service_name = "youtube"
    api_version = "v3"
    youtube = build(api_service_name, api_version, developerKey=api_key)
    request = youtube.search().list(
        part="snippet",
        maxResults=50,
        q=ele,
        videoCaption="any",
        videoDefinition="any",
        videoDimension="any",
        videoDuration="any",
        pageToken=pt
    )
    response = request.execute()
    response1 = response

    # changing token to next page token
    try:
        next_page.append(response1["nextPageToken"])
    except KeyError:
        print("Next page not found:", str(ele))


    # pulling information from API request
    for i in response1['items']:
        vid_cont = i['id']

        try:
            vid_id = str(vid_cont['videoId'])
        except KeyError:
            vid_id = na
        try:
            soup = i['snippet']
        except KeyError:
            pass

        try:
            date = isodate.parse_datetime(soup['publishedAt'])
        except KeyError:
            date = na

        try:
            title = soup['title']
        except KeyError:
            title = na

        try:
            desc = soup['description']
        except KeyError:
            desc = na

        try:
            channel = soup['channelId']
        except KeyError:
            channel = na


        try:
            if vid_id != "not provided":
                link = ("https://www.youtube.com/watch?v="+str(vid_id))
            else:
                link = "not provided"
        except KeyError:
            link = "not provided"


        source = "youtube"

        # writing CSV file with relevant data from API request
        with open("sptr.csv", "a") as yt_csv:
            writer = csv.writer(yt_csv)
            writer.writerow([vid_id, link, date, title, desc, channel, ele, source, next_page[-1]])

        # appending youtube data to master spreadsheet
        with open("sp_train.csv", "a") as m_csv:
            writer = csv.writer(m_csv)
            writer.writerow([link, title, desc, source, query])
