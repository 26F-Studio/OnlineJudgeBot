import re

import bs4

import requests


async def get_question_info(question: str):
    print(question)
    link = f"https://www.luogu.com.cn/problem/{question}"
    headers = {
        "user-agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / "
                      "85.0.4183.121 Safari / 537.36 "
    }
    response = requests.get(link, headers=headers)
    if response.status_code != 200:
        return link, None
    elif response.text.find("Exception") != -1:
        return link, None
    bs = bs4.BeautifulSoup(response.text, "html.parser")
    article_str = bs.select("article")[0]
    article_markdown = str(article_str)
    article_markdown = re.sub("<h1>", "# ", article_markdown)
    article_markdown = re.sub("<h2>", "## ", article_markdown)
    article_markdown = re.sub("<h3>", "#### ", article_markdown)
    article_markdown = re.sub("<code>", "```\n", article_markdown)
    article_markdown = re.sub("</code>", "\n```", article_markdown)
    article_markdown = re.sub("</?[a-zA-Z]+[^<>]*>", "", article_markdown)
    html = markdown.markdown(article_markdown)
    img = imgkit.from_string(html, False)
    return link, img
