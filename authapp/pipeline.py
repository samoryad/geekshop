import os
import urllib.request
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile, ShopUser


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('https',
                          'api.vk.com',
                          '/method/users.get',
                          None,
                          urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'country')),
                                                access_token=response['access_token'],
                                                v='5.92')),
                          None
                          ))
    resp = requests.get(api_url)
    if resp.status_code != 200:
        return

    data = resp.json()['response'][0]
    if data['sex'] == 2:
        user.shopuserprofile.gender = ShopUserProfile.MALE
    elif data['sex'] == 1:
        user.shopuserprofile.gender = ShopUserProfile.FEMALE

    if data['about']:
        user.shopuserprofile.aboutMe = data['about']

    if data['bdate']:
        bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

        age = timezone.now().date().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    data_country = data['country']
    if data_country['title'] == 'Россия':
        # и так далее с другими языками
        user.shopuserprofile.language = 'Русский'

    if data['id']:
        user.shopuserprofile.url_address = f'https://vk.com/id{data["id"]}'

    # if data['photo_200']:
    #     urllib.request.urlretrieve(
    #         data['photo_200'],
    #         os.path.join(settings.MEDIA_ROOT, 'users_avatars', f'{user.pk}.jpg')
    #     )
    #     user.avatar = os.path.join('users_avatars', f'{user.pk}.jpg')

    user.save()
