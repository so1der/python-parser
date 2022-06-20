<h1><b>Python News Parser!</b></h1>

So, this is a Python-based news parser. It also can send new posts to your telegram chat or channel. But you can delete telegram-related part, and do whatever you like. For example - make it collecting news in some file. Or something like that, I think you get it.
Main part of this script is the function called "mainParser". By calling this function you can execute parsing. This function have 7 parameters, by changing these parameters, you can adapt parser for certain website. Let's look at each of them:

_**name**_ - this is name of website that you parsing. This parameter needed for logs, and for json file

_**url**_ - this is url, which shows the post-page. You can see some examples in .py file

~~_**chat_id**_~~ - this is telegram chat id, where messages will be sent. I made it as a separate parameter, because maybe someone wants to send messages in differents chat/channels. 

**UPDATE: Scince v1.3 chat_id is no longer function parameter**

_**post_html_block**_ and _**post_html_class**_ - .py file have example for OtakuMode and AnimeNewsNetwork. You need to go to the url, and find html block with post. There you can find html tag and class, this will be these parameters.
More details you can see in the picture:
![alt tag](https://raw.githubusercontent.com/so1der/python-parser/main/images/post%20block%20example.png "post block at OtakuMode")​

_**text_html_block**_ and _**text_html_class**_ - just like last parameters, this is also html tag and class, but for clickable title of the post. Easier to see:

![alt tag](https://raw.githubusercontent.com/so1der/python-parser/main/images/text%20block%20example.png "title block at OtakuMode")​

Last 4 parameters vary from website to website, so to make parser more multipurpose, i make them as a separate parameters. For example, sometimes you don't need 'class' to designate clickable title, so **text_html_class** = None by default.

<h3>JSON file</h3>

Somehow, but parser need to understand, what he has already "posted", or "sended", or whatever he doing after you modified him. For the script to work correctly, you need to create file, named '_**data_file.json**_', and add there json parameters like this - {'name': 'url', 'name': 'url'}. _name_ from json file, and _name_ from functions parameters must match. This json file contains url of last post which he processed. An example is also in the files.

**UPDATE:** In v1.3 json file now have indents, so it can be more readable. You can also leave 'url' empty, in this case parser will post all posts from site, and write 'url' by himself.

<h3>Telegram Bot TOKEN</h3>

You also need to put your bot's token in API_TOKEN = '', so script can use your telegram bot to send messages.

<h3>Word about logs</h3>

I took out logs as a separate functions, so you can easily change them. For example, parsingEndLog() says that "parsing has been complete, next check after 1 hour", because my CRON launch this script once per hour. But maybe you want to lauch it more often? Go ahead! But don't forget to change this information in logs :) You can also modified it to save logs in txt file. Or whatever you like!

<h3>Work example</h3>
In the picture below you can see examples of posts by this parser. You can also see it in this telegram channel: https://t.me/animenewsparser

![alt tag](https://raw.githubusercontent.com/so1der/python-parser/main/images/work_example.png "posts example")​
