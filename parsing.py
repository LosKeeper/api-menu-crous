import pycurl
import certifi
import datetime
from io import BytesIO

from bs4 import BeautifulSoup


def convert_to_date(menu_string):
    # Split the string into words
    words = menu_string.split()

    # Create a dictionary to map French month names to numbers
    month_dict = {
        'janvier': 1,
        'février': 2,
        'mars': 3,
        'avril': 4,
        'mai': 5,
        'juin': 6,
        'juillet': 7,
        'août': 8,
        'septembre': 9,
        'octobre': 10,
        'novembre': 11,
        'décembre': 12
    }

    # Extract the day and year from the string
    day = int(words[3])
    year = int(words[5])

    # Convert the month name to a number
    month = month_dict[words[4].lower()]

    # Return the date
    return datetime.date(year, month, day)


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


def parserIllkirch(htmlStr):

    menus = []

    soup = BeautifulSoup(htmlStr, 'html.parser')

    # Use to count the number of menu to parse the meal_foodies
    i = 0

    # Get all the menu for each day
    for time in soup.find_all('time', class_='menu_date_title'):
        cur_menu = soup.find('div', class_='meal_title').text
        # Create a new JSON object for each day
        menu = {
            "title": time.text,
            "date": str(convert_to_date(time.text)),
            cur_menu: {}
        }

        # Parse the menu the day
        uls = soup.find_all('ul', class_='meal_foodies')

        # For each <li> tag
        for li in uls[i].find_all('li'):
            # Get only the student menu wich start with "SALLE DES ETUDIANTS"
            if li.text.startswith('SALLE DES ETUDIANTS - '):
                # Get the name of the pole before the <ul> tag
                pole = str(li).split('<ul')[0].split(' - ')[1]
                menu[cur_menu][pole] = []

                # Add the menu to the JSON object inside all the <li> tag
                for li2 in li.find_all('li'):
                    if li2.text != 'ou':
                        menu[cur_menu][pole].append(
                            li2.text.replace('\'', ' '))

        menus.append(menu)
        i += 1

    return menus


def parserCronenbourg(htmlStr):

    menus = []

    soup = BeautifulSoup(htmlStr, 'html.parser')

    # Use to count the number of menu to parse the meal_foodies
    i = 0

    # Get all the menu for each day
    for time in soup.find_all('time', class_='menu_date_title'):
        cur_menu = soup.find('div', class_='meal_title').text
        # Create a new JSON object for each day
        menu = {
            "title": time.text,
            "date": str(convert_to_date(time.text)),
            cur_menu: {}
        }

        # Parse the menu the day
        uls = soup.find_all('ul', class_='meal_foodies')

        # For each <li> tag
        for li in uls[i].find_all('li'):
            # Get only the student menu wich start with "SALLE DES ETUDIANTS"
            if li.text.startswith('Grillade') or li.text.startswith('Plat du jour') or li.text.startswith('Végétarien') or li.text.startswith('Extension'):
                # Get the name of the pole before the <ul> tag
                pole = str(li).split('<ul')[0].split('>')[1]
                menu[cur_menu][pole] = []

                # Add the menu to the JSON object inside all the <li> tag
                for li2 in li.find_all('li'):
                    menu[cur_menu][pole].append(li2.text.replace('\'', ' '))

        menus.append(menu)
        i += 1

    return menus


def parserPaulAppell(htmlStr):

    menus = []

    soup = BeautifulSoup(htmlStr, 'html.parser')

    # Use to count the number of menu to parse the meal_foodies
    i = 0

    # Get all the menu for each day
    for time in soup.find_all('time', class_='menu_date_title'):
        # Create a new JSON object for each day
        menu = {
            "title": time.text,
            "date": str(convert_to_date(time.text))
        }

        for meal_type in soup.find_all('div', class_='meal_title'):

            cur_menu = meal_type.text

            menu[cur_menu] = {}

            # Parse the menu the day
            uls = soup.find_all('ul', class_='meal_foodies')

            # For each <li> tag
            for li in uls[i].find_all('li'):
                # Get only the student menu wich start with "SALLE DES ETUDIANTS"
                if li.text.startswith('Pôle végétal') or li.text.startswith('Flam and Co') or li.text.startswith('Plat du jour') or li.text.startswith('Annexe'):
                    # Get the name of the pole before the <ul> tag
                    pole = str(li).split('<ul')[0].split('>')[1]
                    menu[cur_menu][pole] = []

                    # Add the menu to the JSON object inside all the <li> tag
                    for li2 in li.find_all('li'):
                        if li2.text != 'OU':
                            menu[cur_menu][pole].append(
                                li2.text.replace('\'', ' '))

        menus.append(menu)
        i += 1

    return menus
