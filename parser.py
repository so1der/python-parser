from bs4 import BeautifulSoup
import telebot
import requests
import asyncio
import logging
import time
import json
import re

API_TOKEN = ''
bot = telebot.TeleBot(API_TOKEN)


def mainParser(name, url, chat_id, post_html_block, post_html_class, text_html_block, text_html_class = None):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'method' : 'GET',
        'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    global clear_url
    clear_url = (re.match("^(https?:\/\/)?(www.){0,1}([0-9A-Za-z]+.)([A-Za-z]+)", url)).group()

    global chatid
    chatid = chat_id
    
    try:
        response = requests.get(url, headers = headers)
    except:
        noAccessLog(name)
        return
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all(str(post_html_block), class_=str(post_html_class))

    global list_count
    global links_storage
    global titles_storage
    global json_list
    list_count = 0
    links_storage =  []
    titles_storage = []
    
    for post in posts:
        if text_html_class  == None:     
            post = post.find(str(text_html_block))
        else:
            post = post.find(text_html_block,{'class':text_html_class})

        if post is not None:
            links_storage.append(str(post.get('href')))
            titles_storage.append(str(post.text))
            list_count += 1

    list_count = 0

    with open("data_file.json") as json_file:
        json_list = json.load(json_file)
        json_file.close()

    newPostPoster(current_post_id = 0, name = name)

    parsingEndLog(name)


def newPostPoster(current_post_id, name):

    global list_count
    global json_list
    global clear_url
    current_post_id = 0

    if links_storage[list_count] == json_list[name]:
        list_count -= 1
        return
    else:
        list_count += 1
        newPostPoster(current_post_id = 1, name = name)
        try:
            compllink = clear_url + links_storage[list_count]
            messageHendler(url = compllink, title = titles_storage[list_count], name = name)
        except:
            telegramErrorLog()
            return
        json_list[name] = links_storage[list_count]
        with open('data_file.json', 'w') as json_file:
            json_file.write(json.dumps(json_list))
            json_file.close()

        list_count -= 1
        return
        
def messageHendler(url, title, name):
    global clear_url
    global chatid
    html_link = "<a href=\"" + url + "\">Source</a>"
    newPostLog(name)
    bot.send_message(chatid, title + "\n \n" + html_link + "\n",parse_mode="HTML")



def parsingEndLog(name):
    named_tuple = time.localtime()
    print("["+ time.strftime("%H:%M:%S", named_tuple) + "] " + name + " parsing has been complete, next check after 1 hour")

def noAccessLog(name):
    print("There is no access to " + name + ". Check internet, restart script, or wait half an hour, script will try again.")

def newPostLog(name):
    print("New post has been posted from " + name + "!")

def telegramErrorLog():
    print("An error occurred while sending a message to telegram")



if __name__ == '__main__':
    mainParser(name = "AnimeNewsNetwork", url = "https://www.animenewsnetwork.com/all/?topic=games", chat_id = "837475124", post_html_block = "div", post_html_class = "wrap", text_html_block = "a")
    mainParser(name = "OtakuMode", url = "https://otakumode.com/news?q=", chat_id = "837475124", post_html_block = "article", post_html_class = "p-article p-article-list__item c-hit", text_html_block = "a", text_html_class = "inherit")
    time.sleep(10)
    exit()


