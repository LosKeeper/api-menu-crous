# <img src="assets/icon.svg" alt="icon" width="4%"/> API Menu Crous
[![Github Version](https://img.shields.io/github/v/release/loskeeper/api-menu-crous)](https://github.com/LosKeeper/api-menu-crous)
[![Github License](https://img.shields.io/github/license/loskeeper/api-menu-crous)](https://github.com/LosKeeper/api-menu-crous/blob/main/LICENSE)
[![Github Last Commit](https://img.shields.io/github/last-commit/loskeeper/api-menu-crous)](https://github.com/LosKeeper/api-menu-crous/commits)
[![Github Issues](https://img.shields.io/github/issues/loskeeper/api-menu-crous)](https://github.com/LosKeeper/api-menu-crous/issues)

[![Python Version](https://img.shields.io/pypi/pyversions/discord-py-interactions)](https://www.python.org/downloads/)

[![Author](https://img.shields.io/badge/author-@LosKeeper-blue)](https://github.com/LosKeeper)
> This bot is used to create an API for many Crous restaurants in Strasbourg.

## 🧾 Table of Contents
1. [🐋 Docker](#-docker)
2. [🔧 Normal Setup with Python](#-normal-setup-with-python)
3. [🚀 Launch with Python](#-launch-with-python)
4. [📝 How to use it](#-how-to-use-it)
5. [🐞 Bugs and TODO](#-bugs-and-todo)


## 🐋 Docker
A Docker file is provided to make the installation easier. You need to create configuration file name `.env` (you can use the `.env.example` file as a template) :
```ini
# URL of the API
HOST=

# URL of the ILLKIRCH menu website
ILLKIRCH=

# URL of the CRONENBOURG menu website
CRONENBOURG=

# URL of the PAUL APPELL menu website
PAUL_APPELL=
```
To use it, you need to build the Docker image :
```bash
docker build -t api-menu-crous .
```
Then, you can run the Docker image :
```bash
docker run -p <WANTED_PORT>:5000 --env-file .env -d api-menu-crous
```

## 🔧 Normal Setup with Python
Many libraries are needed to make this bot work :
```bash
pip install -r requirements.txt
```
> <picture>
>   <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/light-theme/info.svg">
>   <img alt="Info" src="https://raw.githubusercontent.com/Mqxx/GitHub-Markdown/main/blockquotes/badge/dark-theme/info.svg">
> </picture><br>
>
> If you have some troubles with the installation of the `pycurl` library, make sure to have installed the `libcurl4-openssl-dev` and the `libssl-dev` packages :
> ```bash
> sudo apt install libcurl4-openssl-dev libssl-dev
> ```

To configure the api, you need to create configuration file name `.env` (you can use the `.env.example` file as a template) :
```ini
# URL of the API
HOST=

# URL of the ILLKIRCH menu website
ILLKIRCH=

# URL of the CRONENBOURG menu website
CRONENBOURG=

# URL of the PAUL APPELL menu website
PAUL_APPELL=
```

## 🚀 Launch with Python
To launch the bot, you need to run the `main.py` file :
```bash
python3 main.py
```

## 📝 How to use it
To use it, you need to connect to the API URL you have configured in the `.env` file with the port 5000. The accessibles URL are :
- `/` : Display the available routes
- `/illkirch` : Display the menu of the ILLKIRCH restaurant
- `/cronenbourg` : Display the menu of the CRONENBOURG restaurant
- `/paul-appell` : Display the menu of the PAUL APPELL restaurant

An example of the output for the `/illkirch` route can be find in the `example.json` file.


## 🐞 Bugs and TODO
- [ ] Test the Dockerfile