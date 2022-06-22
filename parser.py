from bs4 import BeautifulSoup
import telebot
import requests
import time
import json
import re

API_TOKEN = ''
chat_id = ''
bot = telebot.TeleBot(API_TOKEN)


def mainParser(name, url, post_html_block, post_html_class, text_html_block, text_html_class=None):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
        'method': 'GET',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }

    global clear_url
    clear_url = (re.match("^(https?:\/\/)?(www.){0,1}([0-9A-Za-z]+.)([A-Za-z]+)", url)).group()
    try:
        response = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        noAccessLog(name)
        return
    soup = BeautifulSoup(response.text, "html.parser")
    posts = soup.find_all(str(post_html_block), class_=str(post_html_class))

    global links_storage
    global titles_storage
    global json_list
    list_count = 0
    links_storage = []
    titles_storage = []

    for post in posts:
        if text_html_class is None:
            post = post.find(str(text_html_block))
        else:
            post = post.find(text_html_block, {'class': text_html_class})

        if post is not None:
            links_storage.append(str(post.get('href')))
            titles_storage.append(str(post.text))
            list_count += 1
    links_amount = list_count
    list_count = 0

    with open("data_file.json") as json_file:
        json_list = json.load(json_file)

    if newPostPoster(name=name, list_count=list_count, links_amount=links_amount):
        with open('data_file.json', 'w') as json_file:
            json_file.write(json.dumps(json_list, indent=4))
    parsingEndLog(name)


def newPostPoster(name, list_count, links_amount):
    global json_list
    if list_count == links_amount:
        return
    if links_storage[list_count] == json_list[name]:
        list_count -= 1
        sending_success = False
        return sending_success
    else:
        list_count += 1
        newPostPoster(name=name, list_count=list_count, links_amount=links_amount)
        try:
            list_count -= 1
            compllink = clear_url + links_storage[list_count]
            messageHendler(url=compllink, title=titles_storage[list_count], name=name)
            sending_success = True
        except:
            sending_success = False
            telegramErrorLog()
            return sending_success
        json_list[name] = links_storage[list_count]
        return sending_success


def messageHendler(url, title, name):
    html_link = f"<a href=\"{url}\">Source</a>"
    bot.send_message(chat_id,f"{title}\n \n{html_link}\n", parse_mode="HTML")
    newPostLog(name)


def parsingEndLog(name):
    current_time = time.strftime("%H:%M:%S", time.localtime())
    print(f"[{current_time}] {name} parsing has been complete, next check after 1 hour")


def noAccessLog(name):
    print(f"There is no access to {name}. Check internet, restart script, or wait half an hour, script will try again.")


def newPostLog(name):
    print(f"New post has been posted from {name}!")


def telegramErrorLog():
    print("An error occurred while sending a message to telegram")


if __name__ == '__main__':
    #mainParser(name="AnimeNewsNetwork", url="https://www.animenewsnetwork.com/all/?topic=games", post_html_block="div", post_html_class="wrap", text_html_block="a")
    mainParser(name="OtakuMode", url="https://otakumode.com/news?q=", post_html_block="article", post_html_class="p-article p-article-list__item c-hit", text_html_block="a", text_html_class="inherit")
    time.sleep(5)
    exit()
