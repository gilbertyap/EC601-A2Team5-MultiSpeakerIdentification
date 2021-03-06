# Download YouTube videos from a text file of youtube links
# Then separate out the audio file and video file
from pytube import YouTube
import os, random

videoPrefix = 'https://www.youtube.com/watch?v='

print('Getting all videos from links.txt...')
videoLinks = []
with open('links.txt','r') as f:
    videoLinks = f.readlines()

# Make video folder
downloadPath = './downloadedVideos/'
if not os.path.isdir(downloadPath):
    os.mkdir(downloadPath)

print('Downloading links...')
for link in videoLinks:
    try:
        # Initiate the download of the combined video/audio mp4
        print('Attempting to download video from {}'.format(link))
        yt = YouTube(videoPrefix+link)
        # Try to download video at 720p quality if possible
        yt.streams.filter(progressive=True, file_extension='mp4', resolution='720p').first().download(downloadPath, filename=link)
        print('Download succeeded!')
    except:
       print('Unable to download this video.')
       continue

print('Finished downloading all videos')