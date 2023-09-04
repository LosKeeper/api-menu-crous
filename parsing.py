import pycurl
import certifi
from io import BytesIO

import json
from bs4 import BeautifulSoup


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


def parser(htmlStr):

    menus = []

    soup = BeautifulSoup(htmlStr, 'html.parser')

    # Get all the menu for each day
    for time in soup.find_all('time', class_='menu_date_title'):
        cur_menu = soup.find('div', class_='meal_title').text
        # Create a new JSON object for each day
        menu = {
            "date": time.text,
            cur_menu: {}
        }

        # Parse the menu the day
        ul = soup.find('ul', class_='meal_foodies')

        # For each <li> tag
        for li in ul.find_all('li'):
            # Get only the student menu wich start with "SALLE DES ETUDIANTS"
            if li.text.startswith('SALLE DES ETUDIANTS - '):
                # Get the name of the pole before the <ul> tag
                pole = str(li).split('<ul')[0].split(' - ')[1]
                menu[cur_menu][pole] = []

                # Add the menu to the JSON object inside all the <li> tag
                for li2 in li.find_all('li'):
                    if li2.text != 'ou':
                        menu[cur_menu][pole].append(li2.text)

        menus.append(menu)

    return menus
