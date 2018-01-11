from pprint import pprint

import requests
import time

AUTHORIZER_URL = "https://oauth.vk.com/authorize"
VERSION = "5.69"
# ID = "105932"
ID = "171691064"

TOKEN = "5dfd6b0dee902310df772082421968f4c06443abecbc082a8440cb18910a56daca73ac8d04b25154a1128"


def get_groups_id(user_id):
    params = {
        "user_id": user_id,
        "access_token": TOKEN,
        "v": VERSION,
        "extended": 1
    }
    resp = requests.get("https://api.vk.com/method/groups.get", params)
    groups = resp.json()["response"]["items"]
    groups_id = []

    for group in groups:
        groups_id.append(group["id"])

    return groups_id


def get_friends(user_id):  # возвращает список id друзей
    params = {
            "user_id": user_id,
            "access_token": TOKEN,
            "v": VERSION
        }

    response = requests.get("https://api.vk.com/method/friends.get", params)
    friends = response.json()["response"]["items"]

    return friends


def searching_friends(user_id, groups): # Вариант №1
    matched = []
    for g in groups:
        params = {
            "user_id": user_id,
            "group_id": g,
            "filter": "friends",
            "access_token": TOKEN,
            "v": VERSION
        }

        response = requests.get("https://api.vk.com/method/groups.isMember", params)
        print(".")
        time.sleep(0.3333)
        try:
            count = response.json()["response"]

        except:
            print("KeyError")
            continue
        if count == 0:
            matched.append(g)
        else:
            continue
    return matched

# def searching_friends(friends, groups): # Вариант №2
#     matched = []
#     for g in groups:
#         is_in_group = True
#         for f in friends:
#             params = {
#                 "user_id": f,
#                 "group_id": g,
#                 "access_token": TOKEN,
#                 "v": VERSION
#             }
#
#             response = requests.get("https://api.vk.com/method/groups.isMember", params)
#             print(".")
#             time.sleep(0.3)
#             try:
#              count = response.json()["response"]
#             except:
#                 print("KeyError")
#                 continue
#             if count == 1:
#                 is_in_group = True
#                 break
#             elif count == 0:
#                 is_in_group = False
#         if not is_in_group:
#             matched.append(g)
#
#     return matched

# def searching_friends(user_id):              # Вариант № 3
#     my_groups = set(get_groups_id(user_id))
#     friends = get_friends(user_id)
#     for f in friends:
#         try:
#             friend_groups = set(get_groups_id(f))# тут возникает ошибка ключа, поэтому обрабатываю
#             my_groups = my_groups - friend_groups
#             time.sleep(0.3)
#         except:
#             print("Error in searching_friends")
#
#     return friend_groups


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
        try:
            info = response.json()["response"][0]
            groups_info.append(info)
        except:
            print("Error in get_info")
            continue
    print()
    print()
    return groups_info

# pprint(get_friends())
# pprint(get_info(searching_friends(get_groups_id())))
print(searching_friends(ID, get_groups_id(ID)))
