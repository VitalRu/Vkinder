import os
from datetime import datetime

import vk_api
from dotenv import load_dotenv
from vk_api.exceptions import ApiError

load_dotenv()

access_token = os.getenv('access_token')
my_id = os.getenv('my_id')


class VkTools():
    def __init__(self, access_token):
        self.vkapi = vk_api.VkApi(token=access_token)

    def _bdate_to_age(self, bdate: str):
        user_birth_year = bdate.split('.')[2]
        now = datetime.now().year
        return (now - int(user_birth_year))

    def get_profile_info(self):

        try:
            info, = self.vkapi.method(
                'users.get',
                {
                    'id': 'id',
                    'fields': 'city, sex, bdate',
                }
            )
        except ApiError as e:
            info = {}
            print(f'error = {e}')
        # result = {

        #     'user_id': info.get('id'),

        #     'name': (info['first_name'] + ' ' + info['last_name']) if
        #     'first_name' in info and 'last_name' in info else None,

        #     'sex': info.get('sex') if 'sex' in info else None,

        #     'city': (info.get('city')['title'] if
        #              info.get('city') is not None else None),

        #     'age': (self._bdate_to_age(info.get('bdate')) if
        #             'bdate' in info else None),

        # }

        result = {

            'user_id': info.get('id'),

            'name': (info['first_name'] + ' ' + info['last_name']) if
            'first_name' in info and 'last_name' in info else None,

            'sex': None,

            'city': None,

            'age': None,

        }

        return result

    def search_worksheet(self, params, offset):
        try:
            users = self.vkapi.method(
                'users.search',
                {
                    'count': 50,
                    'offset': offset,
                    'hometown': params.get('city'),
                    'sex': 1 if params.get('sex') == 2 else 2,
                    'has_photo': True,
                    'age_from': params['age'] - 3,
                    'age_to': params['age'] + 3,
                    'relation': 1 or 6,
                }
            )
        except ApiError as e:
            users = []
            print(f' error = {e}')

        result = [
            {
                'id': item['id'],
                'name': item['first_name'] + ' ' + item['last_name'],
            } for item in users['items'] if item['is_closed'] is False
        ]

        return result

    def get_photos(self, id):
        try:
            photos = self.vkapi.method(
                'photos.get',
                {
                    'owner_id': id,
                    'album_id': 'profile',
                    'extended': 1,
                }
            )
        except ApiError as e:
            photos = {}
            print(f'error = {e}')

        result = [
            {
                'owner_id': item['owner_id'],
                'id': item['id'],
                'likes': item['likes']['count'],
                'comments': item['comments']['count'],
            } for item in photos['items']
        ]

        result.sort(key=lambda x: (x['likes'], x['comments']), reverse=False)

        return result[:3]


if __name__ == '__main__':
    tools = VkTools(access_token)
    params = tools.get_profile_info()
    print(params)
    worksheets = tools.search_worksheet(params, 10)
    worksheet = worksheets.pop()
    photos = tools.get_photos(worksheet['id'])
