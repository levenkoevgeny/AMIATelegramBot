from cgitb import text
from re import L
from telebot import types

id_chat_group = -1001735796752

token = '5133469961:AAE3n4K3uzGCPkFxYFVfgwyKbj9WztAEZWc'
proxy = {'https': 'http://lavrenov_ba:3404@192.168.0.123:8080'}


def group_button():
    kb = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Академия МВД', url='amia.by')
    item2 = types.InlineKeyboardButton('ВК', url='vk.com')
    item3 = types.InlineKeyboardButton('Inst', url='instagram.com')
    item4 = types.InlineKeyboardButton('Ютуб', url='youtube.com')
    item5 = types.InlineKeyboardButton(
        'Наш телеграм Бот', url='t.me/MyAkademyBot')
    kb.row(item1)
    kb.add(item2, item3)
    kb.row(item4)
    kb.row(item5)
    return kb


def get_menu_button():
    text =  'Вас приветсвует телграмБот Академии МВД.'
    kb = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton(
        'Оставить отзыв об телеграм канале', callback_data='set_review')
    item2 = types.InlineKeyboardButton(
        'Поделиться новостью', callback_data='set_new_news')
    kb.row(item1)
    kb.row(item2)
    # a = []
    # print(a)
    return text, kb


def get_review_button():
    text = 'Напишите, пожалуйста, ваш отзыв. К отзыву можно прекрепить изображение.'
    kb = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Назад', callback_data='back_one1')
    kb.add(item1)
    return text,kb


def get_menu2_button():
    kb = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Анонимно',callback_data='anonim_button')
    item2 = types.InlineKeyboardButton('НЕ анонимно',callback_data='no_anonim_button')
    item3 = types.InlineKeyboardButton('Назад',callback_data='back_one')
    kb.add(item1)
    kb.add(item2)
    kb.add(item3)
    return kb