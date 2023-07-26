import os

import vk_api
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType, VkLongPoll
from vk_api.utils import get_random_id

from core import VkTools
from data_base import User

load_dotenv()

community_token = os.getenv('community_token')
access_token = os.getenv('access_token')


class BotInterface():

    def __init__(self, community_token, access_token):
        self.vk_session = vk_api.VkApi(token=community_token)
        self.longpoll = VkLongPoll(self.vk_session)
        self.vk_tools = VkTools(access_token)
        self.params = {}
        self.worksheets = []
        self.offset = 0
        self.waiting_for_user_info = False

    def request_info(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                return event.text

    def save_user_info(self, user_id):
        user_info = self.vk_tools.get_profile_info()
        if not user_info.get('sex'):
            self.send_message(user_id, 'Введите ваш пол (мужской/женский):')
            self.waiting_for_user_info = True
            user_sex = self.request_info()
        if user_sex.lower() == 'женский':
            user_info['sex'] = 1
        elif user_sex.lower() == 'мужской':
            user_info['sex'] = 2
        else:
            user_sex = None
            self.send_message(user_id, 'Неверное значение для пола')

        if not user_info.get('city'):
            self.send_message(user_id, 'Введите ваш город:')
            self.waiting_for_user_info = True
            user_info['city'] = self.request_info()

        if not user_info.get('age'):
            self.send_message(
                user_id, 'Введите ваш возраст:'
            )
            self.waiting_for_user_info = True
            user_info['age'] = self.request_info()

        user = User(user_info['sex'], user_info['city'], user_info['age'])
        self.send_message(user_id, 'Спасибо! Ваши данные сохранены.')
        self.waiting_for_user_info = False
        user_fields = {
            'sex': user.profile_sex,
            'city': user.profile_city,
            'age': user.profile_age,
        }

        profile_info = user_info.copy()
        profile_info.update(user_fields)

        return profile_info

    def send_message(self, user_id, message, attachment=None):
        self.vk_session.method(
            'messages.send',
            {
                'user_id': user_id,
                'message': message,
                'attachment': attachment,
                'random_id': get_random_id()
            }
        )

    def get_photos_from_worksheet(self, worksheet):
        photos = self.vk_tools.get_photos(worksheet['id'])
        photo_str = ''
        for photo in photos:
            photo_str += (f'photo{photo["owner_id"]}'
                          f'_{photo["id"]},')
        return photo_str

    def event_hanlder(self):

        for event in self.longpoll.listen():
            self.params = self.vk_tools.get_profile_info()
            if self.waiting_for_user_info:
                self.save_user_info(event.user_id)
                self.params = self.save_user_info(event.user_id)

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text.lower() == 'привет':
                    # self.params = self.vk_tools.get_profile_info()
                    self.send_message(
                        event.user_id, f'Привет, {self.params["name"]}'
                    )

                elif event.text.lower() == 'поиск':
                    self.send_message(event.user_id, 'Начинаем поиск')

                    if self.worksheets:
                        worksheet = self.worksheets.pop()
                        self.get_photos_from_worksheet(worksheet)
                    else:
                        self.worksheets = self.vk_tools.search_worksheet(
                            self.params, self.offset
                        )
                        worksheet = self.worksheets.pop()
                        self.get_photos_from_worksheet(worksheet)
                        self.offset += 50
                    self.send_message(
                        event.user_id,
                        (f'Имя {worksheet["name"]} '
                         f'ссылка: vk.com/id{worksheet["id"]}'),
                        attachment=self.get_photos_from_worksheet(worksheet)
                    )
                elif event.text.lower() == 'пока':
                    self.send_message(event.user_id, 'До новых встреч!')
                else:
                    self.send_message(event.user_id, 'Неизвестная команда')


if __name__ == '__main__':
    bot_interface = BotInterface(community_token, access_token)
    params = bot_interface.vk_tools.get_profile_info()
    if (params['age'] is None or params['city'] is None or
       params['sex'] is None):
        bot_interface.waiting_for_user_info = True
    user_id = user_id = bot_interface.vk_tools.get_profile_info()['user_id']
    print('>>>', bot_interface.save_user_info(user_id))
    print('>>>>>', bot_interface.vk_tools.get_profile_info())
    bot_interface.event_hanlder()
