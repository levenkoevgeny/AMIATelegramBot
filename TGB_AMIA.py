import threading
import time
import config
import telebot
from telebot import apihelper, custom_filters
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage


class my_bot(telebot.TeleBot):
    def loop_message(self):
        while True:
            self.send_message(
                config.id_chat_group, 'Вас приветсвует телграмБот Академии МВД', reply_markup=config.group_button())
            time.sleep(14400)

    def start_action(self):
        thread = threading.Thread(target=self.loop_message)
        thread.start()


state_memory = StateMemoryStorage()

bot = my_bot(config.token, threaded=False, state_storage=state_memory)
apihelper.proxy = config.proxy

# bot.start_action()


class MyStateGroup(StatesGroup):
    None_State = State()
    Default_State = State()
    Set_review_state = State()
    Set_new_news_state = State()


@bot.message_handler(commands=['start'])
def start(message):
    a=bot.get_user_profile_photos(message.from_user.id)
    if a.total_count:
        photo = bot.download_file(bot.get_file(a.photos[0][-1].file_id).file_path)   #Фотография если есть
        f = open('a.jpg','wb')
        f.write(photo)
        f.close()
    bot.send_message(message.chat.id, config.get_menu_button()[
                     0], reply_markup=config.get_menu_button()[1])


@bot.message_handler(state=MyStateGroup.Default_State)
def default_inline_state(message):
    bot.send_message(message.chat.id, config.get_menu_button()[
                     0], reply_markup=config.get_menu_button()[1])

# Первая кнопка, для коментария

@bot.callback_query_handler(func=lambda c: c.data == 'set_review')
def callback_inline(call):
    bot.set_state(call.from_user.id,
                  MyStateGroup.Set_review_state, call.message.chat.id)
    bot.edit_message_text(config.get_review_button()[0], call.message.chat.id,
                          call.message.message_id, reply_markup=config.get_review_button()[1])


@bot.message_handler(content_types=['text', 'photo'], state=MyStateGroup.Set_review_state)
def set_review(message):
    if message.content_type == 'text':
        print(message.text)  # тут чисто коментарий без фото сохрани в бд
    else:
        a = bot.get_file(message.photo[-1].file_id)
        # скаченное изображение
        foto = bot.download_file(a.file_path)
        if message.caption:
            caption = message.caption                     # подпись к изображению
    bot.send_message(message.from_user.id, 'Спасибо за ваш отзыв')
    bot.send_message(message.from_user.id, config.get_menu_button()[
                     0], reply_markup=config.get_menu_button()[1])
    bot.set_state(message.from_user.id,
                  MyStateGroup.Default_State, message.chat.id)


@bot.callback_query_handler(func=lambda c: c.data == 'back_one1')
def back_inline(call):
    bot.set_state(call.from_user.id,
                  MyStateGroup.Default_State, call.message.chat.id)
    bot.edit_message_text(config.get_menu_button()[
                          0], call.message.chat.id, call.message.message_id, reply_markup=config.get_menu_button()[1])

# Вторая кнопка, для отзыва

@bot.callback_query_handler(func=lambda c: c.data == 'set_new_news')
def new_keyboard(call):
    bot.edit_message_text('Как вы хотите поделиться новостью?', call.message.chat.id,
                          call.message.message_id, reply_markup=config.get_menu2_button())


@bot.callback_query_handler(func=lambda c: c.data == 'anonim_button')
def anonim_func(call):
    bot.edit_message_text('Как вы хотите поделиться новостью?', call.message.chat.id,
                          call.message.message_id, reply_markup=config.get_menu2_button())


@bot.callback_query_handler(func=lambda c: c.data == 'no_anonim_button')
def no_anonim_func(call):
    bot.edit_message_text('Как вы хотите поделиться новостью?', call.message.chat.id,
                          call.message.message_id, reply_markup=config.get_menu2_button())


@bot.callback_query_handler(func=lambda c: c.data == 'back_one')
def back_inline2(call):
    bot.set_state(call.from_user.id,
                  MyStateGroup.Default_State, call.message.chat.id)
    bot.edit_message_text(config.get_menu_button()[
                          0], call.message.chat.id, call.message.message_id, reply_markup=config.get_menu_button()[1])


if __name__ == '__main__':
    bot.add_custom_filter(custom_filters.StateFilter(bot))
    bot.infinity_polling()
