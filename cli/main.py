import requests
from selenium import webdriver
import os
from bs4 import BeautifulSoup
from url import get_url
from lecteur import get_html
from PIL import Image
import time

path_sd = "C:/Users/Marius/Documents/code/python/Liseuse_cli"  # Remplacez par le chemin approprié pour votre système Linux
path_scan = "/scan/vf"
results = []

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

def create_dir(path: str):
    parent_path = "/".join(path.split("/")[0:-1])
    if not os.path.exists(path):
        create_dir(parent_path)
        try:
            os.mkdir(path=path)
        except:
            pass

def display_results():
    for idx, result in enumerate(results):
        print(f"{idx + 1}. {result['text']}")

def download_images(index, start_chap, end_chap):
    try:
        chap = ['a'] * (end_chap + 1)
        driver = webdriver.Chrome()
        url = results[index]['href'] + path_scan
        driver.get(url)
        valid_chap = driver.execute_script(
            "var ret = [];Array.prototype.slice.call(document.getElementById('selectChapitres')).forEach((e, i, arr) => {ret.push(e.text.split(' ')[1])});return ret;"
        )

        for needed in range(start_chap, end_chap + 1):
            driver.execute_script(f"document.getElementById('selectChapitres').value = 'Chapitre {needed}';selectChapitre();")
            while True:
                time.sleep(0.1)
                page_content = driver.page_source
                soup = BeautifulSoup(page_content, 'html.parser')
                placement = soup.find("div", {"id": "scansPlacement"}, True)
                if placement.find_all("img")[-1]['src'] == "https://cdn.statically.io/gh/Anime-Sama/IMG/img/autres/loading_scans.gif":
                    continue
                else:
                    break
            ep = int(driver.execute_script(
                'var ret = "";Array.prototype.slice.call(document.getElementById("selectChapitres").options).forEach(e => {if (e.selected) {ret = e.value;}});return ret;').split(" ")[1])
            chap[ep] = len(placement.find_all("img"))
            imgs = placement.find_all("img")
            for img in imgs:
                path_dir = f"{path_sd}Scan/{results[index]['text']}/{ep}/"
                path_file = img['src'].split("/")[-1]
                path_full = os.path.join(path_dir, path_file)

                r = requests.get(img['src'])

                create_dir(f"{path_sd}Scan/{results[index]['text']}/{ep}/")

                with open(path_full, "wb") as save_file:
                    save_file.write(r.content)

            driver.execute_script("nextChap();")

        with open(f"{path_sd}Scan/{results[index]['text']}/index.html", "w") as html:
            html.write(get_html(results[index]['text'], str(chap)))

        driver.quit()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}\nChap : {chap}")

if __name__ == "__main__":
    while True:
        query = input("Entrez votre recherche (ou 'exit' pour quitter) : ")
        if query.lower() == 'exit':
            break
        results = search(query)
        display_results()
        choice = input("Choisissez un résultat (numéro) pour télécharger les images ou 'exit' pour quitter : ")
        if choice.lower() == 'exit':
            break
        try:
            index = int(choice) - 1
            if 0 <= index < len(results):
                start_chap = int(input("Entrez le numéro du premier chapitre à télécharger : "))
                end_chap = int(input("Entrez le numéro du dernier chapitre à télécharger : "))
                download_images(index, start_chap, end_chap)
            else:
                print("Choix invalide.")
        except ValueError:
            print("Entrée invalide. Veuillez entrer un numéro.")