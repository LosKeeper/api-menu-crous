import pycurl
import certifi
import datetime
from io import BytesIO

from bs4 import BeautifulSoup

# Create a dictionary to map French month names to numbers
month_dict = {'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4, 'mai': 5, 'juin': 6,
              'juillet': 7, 'août': 8, 'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12}


def convert_to_date(menu_string):
    """Convert a string to a date

    Need month_dict to work

    Args:
        menu_string (str): The string to convert in French format (ex: "Mardi 12 janvier 2021")

    Returns:
        str: The date in ISO format (ex: "2021-01-12")
    """

    # Split the string into words
    words = menu_string.split()

    return datetime.date(int(words[5]), month_dict[words[4].lower()], int(words[3]))


def get_html(URL):
    """Get the html code of the menu webpage

    Returns:
        str: The html code
    """

    # Create a buffer to store the response
    buffer = BytesIO()

    # Create a pycurl object
    c = pycurl.Curl()

    # Set URL value
    c.setopt(c.URL, URL)

    # Write bytes that are utf-8 encoded
    c.setopt(c.WRITEDATA, buffer)

    # Set the User-Agent
    c.setopt(c.USERAGENT, 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

    # Use certifi to verify the certificate
    c.setopt(c.CAINFO, certifi.where())

    # Perform a file transfer
    c.perform()

    # End curl session
    c.close()

    # Decode the buffer
    body = buffer.getvalue().decode('utf-8')

    return body


def parse_menu(htmlStr, location):
    """Parse the html code to get the menu

    Args:
        htmlStr (str): The html code
        location (str): The location of the restaurant ("Illkirch", "Cronenbourg", "Paul-Appell", "Esplanade", "Gallia")

    Returns:
        str: The menu in JSON format
    """
    menus = []
    soup = BeautifulSoup(htmlStr, 'html.parser')
    previous = False
    i = 0

    for time in soup.find_all('time', class_='menu_date_title'):
        menu = {"title": time.text, "date": str(
            convert_to_date(time.text))}
        uls = soup.find_all('ul', class_='meal_foodies')

        for meal_type in soup.find_all('div', class_='meal_title'):

            cur_menu = meal_type.text

            if previous:
                if cur_menu != 'Dîner':
                    previous = False
                    break

            previous = True

            menu[cur_menu] = {}

            for li in uls[i].find_all('li'):
                if location == 'Illkirch' and li.text.startswith('SALLE DES ETUDIANTS - '):
                    pole = str(li).split('<ul')[0].split(' - ')[1]
                    menu[cur_menu][pole] = [li2.text.replace('\'', ' ') for li2 in li.find_all(
                        'li') if li2.text not in ['ou', 'Ou']]
                elif location == 'Cronenbourg' and li.text.startswith(('Grillade', 'Plat du jour', 'Végétarien', 'Extension')):
                    pole = str(li).split('<ul')[0].split('>')[1]
                    menu[cur_menu][pole] = [li2.text.replace(
                        '\'', ' ') for li2 in li.find_all('li')]
                elif location == 'Paul-Appell' and li.text.startswith(('Pôle végétal', 'Flam and Co', 'Plat du jour', 'Annexe')):
                    pole = str(li).split('<ul')[0].split('>')[1]
                    menu[cur_menu][pole] = [li2.text.replace('\'', ' ') for li2 in li.find_all(
                        'li') if li2.text not in ['ou', 'Ou']]
                elif location == 'Gallia' and li.text.startswith(('MENU ETUDIANT', 'Végétarien')):
                    pole = str(li).split('<ul')[0].split('>')[1]
                    menu[cur_menu][pole] = [li2.text.replace('\'', ' ') for li2 in li.find_all(
                        'li') if li2.text not in ['ou', 'Ou']]
                elif location == 'Esplanade' and li.text.startswith(('Menus', 'Desserts')):
                    pole = str(li).split('<ul')[0].split('>')[1]
                    menu[cur_menu][pole] = [li2.text.replace('\'', ' ') for li2 in li.find_all(
                        'li') if li2.text not in ['ou', 'Ou', '-']]

        menus.append(menu)
        i += 1

    return menus
