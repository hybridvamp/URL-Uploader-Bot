#!/usr/bin/env python3


'''Impoting Libraries, Modules & Credentials'''
from os import listdir, linesep
from re import match
import aiofiles
from time import time
from aiohttp import ClientSession
from bot.messages import *
from bot.plugins.funcs import *

class Downloader:

    def __init__(self, event, url, bot):
        self.event = event
        self.url = url
        self.bot = bot
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246'}
    
    @classmethod
    async def start(cls, event, url, bot):
        self = cls(event, url, bot)
        if match('^https://(www.)?youtu(.)?be(.com)?/(.*)', url):
            await event.respond(youtube_url, parse_mode = 'html')
        else:   #Normal Url
            process_msg = await event.respond(processing_url, parse_mode = 'html')
            await self.url_downloader(self.event, process_msg, self.bot, self.url)
        return self

    async def url_downloader(self, event, process_msg, bot, url):

        msg = await bot.edit_message(process_msg, starting_to_download, parse_mode = 'html')
        userid = event.sender_id
        files_before = listdir()

        #Downloading File From Url
        
        file_name = url.split("filename=")[-1].split("name=")[-1].split("title=")[-1].split("&")[0].split('/')[-1].split('?')[0].split("&")[0]
        
        start_time = time()
        current_size = 0
        msg = await bot.edit_message(msg, "<b>Downloading... !! Keep patience...")
        self.n_msg = msg
        
        async with ClientSession() as session:
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    
                    file_size = int(resp.headers.get("Content-Length")) if resp.headers.get("Content-Length") else 0
                    if file_size > 1219430400: msg = await bot.edit_message(limit_exceeded); self.n_msg, self.filename = self.n_msg, None
                    
                    async with aiofiles.open(file_name, "wb") as f:
                        while True:
                            chunk = await resp.content.read(32768)
                            current_size += len(chunk)
                            diff = time()-start_time
                            if file_size > 0 and round(diff % 10.00) == 0:
                                percentage = current_size * 100 / file_size
                                speed = humanbytes(current_size / diff)
                                
                                msg = await bot.edit_message(msg, f"<b>Downloading... !! Keep patience...\n📊Percentage: {round(percentage, 2)}%\n✅Completed: {round(current_size / 1024 / 1024, 2)} MB\n🚀Speed: {speed}\n</b>", parse_mode = 'html')
                            
                            if not chunk: break
                            await f.write(chunk)
                         
                        n_msg = await bot.edit_message(msg, uploading_msg, parse_mode = 'html')
                        self.n_msg, self.filename = n_msg, file_name
                        return True
                
                else:
                    self.n_msg, self.filename = self.n_msg, None
                    return 
