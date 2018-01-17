
import requests
import time
import re
import sys
import json


'''Данная программа Выводит список групп в ВК в которых состоит пользователь, но не состоит никто из его друзей.
   Ввод имени пользователя производится через параметр командной строки, но можно задать и вручную в коде изменив
   присвоив соответствующее значение переменной NAME'''

AUTHORIZER_URL = "https://oauth.vk.com/authorize"
VERSION = "5.69"
ID = ""

TOKEN = "5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128"


def get_groups_id(user_id):
    params = {
        "user_id": user_id,
        "access_token": TOKEN,
        "v": VERSION,
        "extended": 1
    }
    groups = []
    groups_id = []
    try:
        print(".")
        resp = requests.get("https://api.vk.com/method/groups.get", params)
        groups = resp.json()["response"]["items"]
    except:
        print("Ошибка доступа")
    for group in groups:
        groups_id.append(group["id"])

    return groups_id


def get_friends(user_id):  # возвращает список id друзей
    params = {
            "user_id": user_id,
            "access_token": TOKEN,
            "v": VERSION
        }
    print(".")
    response = requests.get("https://api.vk.com/method/friends.get", params)
    friends = response.json()["response"]["items"]

    return friends


def searching_friends(user_id):
    my_groups = set(get_groups_id(user_id))
    friends = get_friends(user_id)
    for f in friends:
        try:
            print(".")
            friend_groups = set(get_groups_id(f))
            my_groups = my_groups - friend_groups
            time.sleep(0.3333)
        except Exception as e:
            print("KeyError:", e)
            continue

    return my_groups


def get_info(groups_id):
    groups_info = []
    for id in groups_id:
        params = {

            "group_id": id,
            "fields": "members_count",
            "access_token": TOKEN,
            "v": VERSION
        }

        response = requests.get("https://api.vk.com/method/groups.getById", params)
        print('.')
        time.sleep(0.3)
        info = response.json()["response"][0]
        del info['is_closed']
        del info['photo_100']
        del info['photo_200']
        del info['photo_50']
        del info['screen_name']
        del info['type']
        groups_info.append(info)
    return groups_info


def create_file(data):
        with open("groups.json", "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


def get_user_id(name):
    params = {

        "user_ids": name,
        "access_token": TOKEN,
        "v": VERSION
    }
    try:
        print(".")
        response = requests.get("https://api.vk.com/method/users.get", params)
        info = response.json()["response"][0]["id"]
    except:
        print("Некорректное имя пользователя:")
        return name

    return info


def check_name(name):  # дополнительная проверка на валидность ввода
        if re.search(r'[A-Za-z0-9_]', name):
            return get_user_id(name)
        else:
            print("Invalid User_name")


def get_user_name():
    if __name__ == "__main__":
        user_name = sys.argv[1]
    return user_name

NAME = get_user_name()
ID = check_name(NAME)
create_file(get_info(searching_friends(ID)))


