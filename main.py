import argparse

import requests
from bs4 import BeautifulSoup
import re

search_url = "http://flibusta.site"

book_info = []

book_url_pattern = re.compile(r'/b/\d+')


def check_format(url):
    formats_list = {'epub': 'epub', 'fb2': 'zip', 'скачать pdf': 'pdf', 'mobi': 'mobi'}
    response = requests.get(url)
    html_code = response.text
    my_soup = BeautifulSoup(html_code, 'html.parser')
    for frmt in list(formats_list.keys()):

        all1 = my_soup.find('a', string=f'({frmt})')
        if all1:
            continue
        else:
            del formats_list[frmt]
    return formats_list


def search(book_name):
    _ = 0
    url = f"https://flibusta.site/booksearch?ask={book_name}"
    response = requests.get(url)
    html_code = response.text
    soup = BeautifulSoup(html_code, 'html.parser')

    for a in soup.find_all('a', href=book_url_pattern):
        book_title = a.get_text(strip=True)
        book_url = f"{search_url}{a['href']}"

        format_ = check_format(book_url)

        book_info.append({'title': book_title, 'url': book_url, 'formats': format_})

    return book_info


def save(url, title, frtt):
    try:
        response = requests.get(url=url)
        with open(f'{title}.{frtt}', 'wb') as file:
            file.write(response.content)

            print('Книга успещно сохранена, пирррррат...')

    except Exception as _ex:
        print('Upps...')


def save_by_title(title, format_):
    for i in book_info:
        title_ = i['title']
        if title == title_:
            url_to_dowload = i['url']

            save(url_to_dowload, title, format_)

            break


def main(search_name, format_, name):
    pass


if __name__ == '__main__':
    name = input("Введите название книги: ")
    search(name)
    print('найденные книги: ')
    for i in book_info:
        print(f'{i.get("title")} форматы: | {i.get("formats")}')
    title = input("Введите полное и точное название книги: ")
    format_ = input("Выберете формат из доступных: ")
    save_by_title(title, format_)
