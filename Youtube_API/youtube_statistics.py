import requests
import json

class YTstats():

    def __init__(self, api_key, channel_id):
        self.api_key= api_key
        self.channel_id= channel_id
        self.channel_statistics= None
        self.vide_data= None 

    def get_channel_statistics(self):
        url= f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channel_id}&key={self.api_key}'
        #print(url)
        json_url= requests.get(url)
        data= json.loads(json_url.text)
        #print(data)

        try:
            data= data["items"][0]["statistics"]
        except: 
            data= None 

        self.channel_statistics= data
        
        return data

    def get_channel_video_data(self):
        # 1) Get all the video IDs 
        channel_videos= self._get_channel_videos(limit= 50)
        print(channel_videos)

        # Fancy printing: 
        # count= 0
        # for i,j in channel_videos.items():
        #     count += 1
        #     print("{0}: {1}".format(count, i))

        # 2) statistics per video

    def _get_channel_videos(self, limit= None):
        """
        This method allows you to read all videos until 10 pages.
        You can check until 10 pages which means until 500 videos, it's the limit of the YouTube API
        """
        url= f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
                
        vid, npt= self._get_channel_videos_per_page(url=url)
                
        idx= 0
        while (npt is not None and idx < 10): #you can check until 10 pages
            nexturl= url + "&pageToken=" + npt
            next_vid, npt= self._get_channel_videos_per_page(url= nexturl)
            vid.update(next_vid)
            idx += 1

        return vid
 

    def _get_channel_videos_per_page(self, url):
        """
        This method reads all youtube#video per page which are 50 video per page
        Returns an empty dict and None for TokenPage if there's not items inside data. This could be if you exceed your API quota
        """
        json_url= requests.get(url)
        data= json.loads(json_url.text) #json.loads from a str
        channel_videos= dict()

        if 'items' is not data:
            print("There's not items insde data: API exceed quota")
            return channel_videos, None

        item_data= data['items']
        nextPageToken= data.get("nextPageToken", None) #No Token then None
        for i in item_data: #item_data is a list 
            try:
                kind= i['id']['kind']
                if kind == "youtube#video":
                    video_id= i['id']['videoId']
                    channel_videos[video_id]= dict()
            except KeyError:
                print("There is not id/kind")
            
        return channel_videos, nextPageToken
    
    def dump(self):
        if self.channel_statistics is None:
            return
        channel_title= "Vanessa Vega" #get channel name from data
        channel_title= channel_title.replace(" ", "_").lower()
        file_name= channel_title + '.json'
        with open(file_name, 'w') as f:
            json.dump(self.channel_statistics, f, indent=4)
        
        print('File dumped')