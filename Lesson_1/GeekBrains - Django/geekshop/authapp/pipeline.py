from datetime import datetime
from social_core.exceptions import AuthForbidden
import requests

from authapp.models import ShopUserProfile
from django.conf import settings


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return
    url_method = 'https://api.vk.com/method/'
    access_token=response.get('access_token')
    fields = ','.join(['bdate','sex','about', 'photo_max_orig'])
    api_url = f'{url_method}users.get?fields={fields}&access_token={access_token}&v=5.131'

    response = requests.get(api_url)

    if response.status_code != 200:
        return
    data_json = response.json()['response'][0]

    if 'sex' in data_json:
        if data_json['sex'] == 1:
            user.shopuserprofile.gender = ShopUserProfile.FEMALE
        elif data_json['sex'] ==2:
            user.shopuserprofile.gender = ShopUserProfile.MALE
        else:
            user.shopuserprofile.gender = ShopUserProfile.OTHERS

    if 'bdate' in data_json:
        birthday = datetime.strptime(data_json['bdate'], '%d.%m.%Y')

        age = datetime.now().year - birthday.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.bakcends.vk.VKOAuth2')

        user.age = age

    if 'about' in data_json:
        user.shopuserprofile.about = data_json['about']

    if 'photo_max_orig' in data_json:
        photo_path = f'users_avatars/{user.pk}.jpeg'
        photo_full_path = f'{settings.MEDIA_ROOT}/{photo_path}'
        photo_data = requests.get(data_json['photo_max_orig'])
        with open(photo_full_path, 'wb') as photo_file:
            photo_file.write(photo_data.content)
        #user.avatar_url = data_json['photo_max_orig']
        user.avatar = photo_path

    user.save()