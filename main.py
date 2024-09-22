import requests
import io
from bs4 import BeautifulSoup
import graphilibs as gl
from url import get_url
from PIL import Image
import time

win = gl.GraphWin("Uplaoder", 200, 500)
win.setCoords(0, 500, 200, 0)


def ajust_text(text, width):
    new_text = ""
    i = 0
    for c in text:
        if c == " " and i >= width:
            new_text += "\n"
            i = 0
        else:
            new_text += c
            i += 1
    return new_text


def schearch(query):
    url = get_url() + 'template-php/defaut/fetch.php/'
    response = requests.post(url, data={'query': query})
    page_content = response.text  # Récupère le contenu HTML de la page

    soup = BeautifulSoup(page_content, 'html.parser')
    a_s = soup.findAll("a")
    ret = []
    for a in a_s:
        ret.append({})
        ret[len(ret)-1]['src'] = a.img['src']
        ret[len(ret)-1]['text'] = a.h3.text
    return ret


def get_entry(coord):
    x, y = coord
    entry = gl.Entry(gl.Point(x, y), 20)
    entry.draw(win)
    entry.setText('')
    while not win.getKey() == "Return":
        time.sleep(0)
    return entry.getText()


if "__main__" == __name__:
    results = schearch(get_entry((100, 5)))
    idx = 0
    for result in results:
        idx += 1
        r = requests.get(result['src'])
        img = Image.open(io.BytesIO(r.content))
        img = img.resize((80, 45))
        img.save("t.gif")
        o_img = gl.Image(gl.Point(40, 50 * idx + 10), "t.gif")
        o_img.draw(win)
        t = gl.Text(gl.Point(140, 50 * idx + 10), ajust_text(result['text'], 10))
        t.draw(win)

    win.getMouse()


