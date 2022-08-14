import requests
from bs4 import BeautifulSoup
import sys
import re 
from collections import namedtuple
import os
from pytube import YouTube


def downloader(name,method="slow"):
    print("Downloading {}".format(name),end="\n\n\n")
    if  not os.path.isdir("c:\\users\\aris\\desktop\\new_folder"):
        os.mkdir("c:\\users\\aris\\desktop\\new_folder")
    os.chdir("c:\\users\\aris\\desktop\\new_folder")
    #check if the name of the song is not an empty string
    if name.strip():
        temp_url="+".join([i.strip() for i in name.split()])
        url="https://www.youtube.com/results?search_query="+temp_url
        #parse the search results
        response=requests.get(url).text
        soup=BeautifulSoup(response,"lxml")
        text=soup.prettify()
        text=text.replace("\n","")
        #make a tuple for everysong
        song=namedtuple("Song",["title","url"])
        
        #split by every indidual video
        parts=text.split("videoId")
        
        #delete the first part of the list because it doesn't contain any video
        del[parts[0]]
        valid=[]
        for part in parts:
            title=re.findall(r"\"title\":{\"runs\":\[{\"text\"\:\"([^\"]*)\"",part)
            link=re.findall(r"\"(\/watch\?[a-zA-Z0-9?\/\=\-\_\&]+)\"",part)
            if (len(link)!=0) and (len(title)!=0): 
                valid.append(song(title[0],"https://www.youtube.com/"+link[0]))
        #the user chooses
        if method=="slow":
            for i,j in enumerate(valid[:3]):
                print("{}) ".format(i+1),j.title,j.url,sep="---> ",end="\n\n") 
            choice=int(input("Επίλεξε το τραγούδι που θές να κατεβάσεις: πάτα 1 και μετά enter αν θές το πρώτο, 2 και έντερ για το δεύτερο κλπ.\nΠληκτρολόγησε 0 αν θές να εμφανιστούν περισσότερες επιλογές: "))
            if choice==0:
                os.system("cls")
                for i,j in enumerate(valid[:10]):
                    print("{}) ".format(i+1),j.title,j.url,sep="---> ",end="\n\n")
                choice=int(input("Επίλεξε το τραγούδι που θές να κατεβάσεις: πάτα 1 και μετά enter αν θές το πρώτο, 2 και έντερ για το δεύτερο κλπ"))
            choice=valid[choice-1]
        else:
            choice=valid[0]
        
        #download the song
        yt = YouTube(choice.url)
        video = yt.streams.filter(only_audio=True).first()
        downloaded_file = video.download()
        old=downloaded_file
        downloaded_file=downloaded_file.replace(" ","")
        #need to get rid the & character because of a command we will need later
        downloaded_file=downloaded_file.replace("&","")
        os.rename(old,downloaded_file)
        base, ext = os.path.splitext(downloaded_file)
        new_file = base + '.mp3'
        #from mp4 to mp3
        op="ffmpeg  -i {} -vn {}".format(downloaded_file,new_file)
        os.system(op)
        os.system("del {}".format(downloaded_file))
        os.system("cls")
        print("Downloading of {} has finished".format(name),end="\n\n\n")
    else:
        print("Error in name")
if __name__=="__main__":
        if len(sys.argv)<=1:
            name=input("give name: ")
        else:
            name=sys.argv[1]
        downloader(name)
