import requests
from selenium import webdriver
import io
import os
from bs4 import BeautifulSoup
import graphilibs as gl
from url import get_url
from lecteur import get_html
from PIL import Image
import time

win = gl.GraphWin("Uplaoder", 200, 500)
win.setCoords(0, 500, 200, 0)

path_sd = "D:/"
path_scan = "/scan/vf"
results:list[dict] = []


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


def search(query):
    global results
    url = get_url() + 'template-php/defaut/fetch.php/'
    try:
        response = requests.post(url, data={'query': query}, timeout=5)
        response.raise_for_status()
        page_content = response.text  # Récupère le contenu HTML de la page

        soup = BeautifulSoup(page_content, 'html.parser')
        a_s = soup.findAll("a")
        results = []
        for a in a_s:
            results.append({
                'href': a['href'],
                'src': a.img['src'],
                'text': a.h3.text
            })
        return results

    except requests.exceptions.Timeout:
        print("La requête a expiré. Le serveur est peut-être lent.")
    except requests.exceptions.ConnectionError:
        print("Erreur de connexion. Vérifiez votre connexion réseau ou l'URL.")
    except requests.exceptions.HTTPError as err:
        print(f"Erreur HTTP : {err}")
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

    return []

def create_dir(path:str):
    parent_path = "/".join(path.split("/")[0:-1])
    if not os.path.exists(path):
        create_dir(parent_path)
        try:
            os.mkdir(path=path)
        except:
            pass


def mouse_click(p:gl.Point):
    global results
    if p.y >= 50 - 45 /2 and p.y <= 50 * 5 + 45 /2:
        y_img = p.y - 45 /2
        i = int((y_img - y_img % 50) / 50)
        try:
            min_want = 46
            max_want = 100
            results[i]
            chap:list[str | int] = ['a']*(max_want+1)
            driver = webdriver.Chrome()
            url = results[i]['href'] + path_scan
            driver.get(url)
            valid_chap = driver.execute_script("var ret = [];Array.prototype.slice.call(document.getElementById('selectChapitres')).forEach((e, i, arr) => {ret.push(e.text.split(' ')[1])});return ret;")
            
            for needed in range(min_want, max_want):
                driver.execute_script(f"document.getElementById('selectChapitres').value = 'Chapitre {needed}';selectChapitre();")
                while True:
                    time.sleep(.1)
                    page_content = driver.page_source
                    soup = BeautifulSoup(page_content, 'html.parser')
                    placement = soup.find("div", {"id": "scansPlacement"}, True)
                    if placement.find_all("img")[-1]['src'] == "https://cdn.statically.io/gh/Anime-Sama/IMG/img/autres/loading_scans.gif":
                        continue
                    else:
                        break
                ep = int(driver.execute_script('var ret = "";Array.prototype.slice.call(document.getElementById("selectChapitres").options).forEach(e => {if (e.selected) {ret = e.value;}});return ret;').split(" ")[1])
                chap[ep] = len(placement.find_all("img"))
                imgs = placement.find_all("img")
                for img in imgs:
                    path_dir = f"{path_sd}Scan/{results[i]['text']}/{ep}/"
                    path_file = img['src'].split("/")[-1]
                    path_full = os.path.join(path_dir, path_file)
                    
                    r = requests.get(img['src'])

                    create_dir(f"{path_sd}Scan/{results[i]['text']}/{ep}/")
                        
                    with open(path_full, "wb") as save_file:
                        save_file.write(r.content)
                    
                
                driver.execute_script("nextChap();")

            with open(f"{path_sd}Scan/{results[i]['text']}/index.html", "w") as html:
                html.write(get_html(results[i]['text'], str(chap)))
                        
            driver.quit()
        except Exception as e:
            print(f"Une erreur s'est produite : {e}\nChap : {chap}")
    


class My_entry:
    def __init__(self, coord):
        x, y = coord
        self.entry = gl.Entry(gl.Point(x, y), 20)
        self.entry.draw(win)

    def get_entry(self, key):
        if(bool(key)):
            while not win.checkKey() == key:
                pass
        win.update()
        return self.entry.getText()
    
class Rendue:
    def __init__(self, index) -> None:
        self.index = index
        self.Image = gl.Image(gl.Point(40, 50 * index + 50), 80, 45)
        self.Text = gl.Text(gl.Point(140, 50 * index + 50), "")

    def update(self, image, text):
        img = Image.open(io.BytesIO(image))
        img = img.resize((80, 45))
        img.save("t.gif")
        self.Image.undraw()
        self.Image = gl.Image(gl.Point(40, 50 * self.index + 50), "t.gif")
        self.Image.draw(win)
        self.Text.undraw()
        self.Text.setText(ajust_text(text, 10))
        self.Text.draw(win)
    def undraw(self):
        self.Image.undraw()
        self.Text.undraw()
        


if "__main__" == __name__:
    my_entry = My_entry((100, 10))
    my_Rendues: list[Rendue] = []
    for i in range(5):
        my_Rendues.append(Rendue(i))
    
    last_search = my_entry.get_entry(False)
    win.setMouseHandler(mouse_click)


    while True:
        if my_entry.get_entry(False) != last_search:
            last_search = my_entry.get_entry(False)
            results = search(last_search)
            for idx in range(5):
                try:
                    results[idx]
                    r = requests.get(results[idx]['src'])
                    my_Rendues[idx].update(r.content, results[idx]['text'])
                except:
                    my_Rendues[idx].undraw()

                # img = Image.open(io.BytesIO(r.content))
                # img = img.resize((80, 45))
                # img.save("t.gif")
                # o_img = gl.Image(gl.Point(40, 50 * idx + 10), "t.gif")
                # o_img.draw(win)
                # t = gl.Text(gl.Point(140, 50 * idx + 10), ajust_text(result['text'], 10))
                # t.draw(win)
        
