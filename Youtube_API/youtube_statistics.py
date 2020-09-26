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


        # 2) statistics per video

    def _get_channel_videos(self, limit= None):
        url= f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        print(url)

    
    def dump(self):
        if self.channel_statistics is None:
            return
        channel_title= "Vanessa Vega" #get channel name from data
        channel_title= channel_title.replace(" ", "_").lower()
        file_name= channel_title + '.json'
        with open(file_name, 'w') as f:
            json.dump(self.channel_statistics, f, indent=4)
        
        print('File dumped')


