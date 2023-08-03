from tests.api import PetFriends
from tests.settings import valid_email, valid_password, invalid_email, invalid_password
import os


pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в результате содержится слово key"""

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert "key" in result


def test_get_api_pets_valid_key(filter=""):
    """ Проверяем что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Потом, используя этот ключ,
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'pets' либо '' """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_api_pets(auth_key, filter)
    assert status == 200
    assert len(result["pets"]) > 0


def test_add_new_pet_with_valid_data(name='Вася', animal_type='кот',
                                     age='5', pet_photo='images/01.jpg'):
    """Проверяем, что можно добавить питомца с корректными данными"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Лея', animal_type='Кошка', age=2):
    """Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_info_about_new_pet(name="Bob", animal_type='cat', age='7'):
    """Проверяем возможность добавления корректной информации о новом питомце без фото"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_simple_new_pet(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_to_pet(pet_photo='images/03.jpg'):
    """Проверяем возможноcnm добавить фото в карточку питомца"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 200
        assert 'image' in result['pet_photo']
    else:
        raise Exception("There is no my pets")


# 1
def test_update_empty_pet_info(name='?(%', animal_type='123456', age='йцук'):
    """Проверяем возможность обновления информации о питомце некорректными данными"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Баг!
        # 1. Поле для ввода "age" принимает строковые значения.
        # 2. Поле для ввода "animal_type" принимает числовые значения.
        # 3. Поле для ввода "name" принимает спецсимволы.
        # Поэтому получаем статус-код 200 вместо 400.
        assert status == 400
    else:
        raise Exception("There is no my pets")

# 2
def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Проверяем, что запрос списка питомцев пользователя возвращает не пустой список"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_api_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

# 3
def test_add_long_name_to_new_pet(name="UKDSzZzwxRdIxAMmigxNWgRrdTQyxnvBHrECglPavzGPeyLdvZKmUmQ"
                                       "pfUXGiCtCyPzzvZzxnaGCmhOEzcYFTXSBwLhjuuFKSodmwkrEIQPemO"
                                       "DvFJvbeqxIVPCOuyXGLLeuSovVjxPQVumIiIaqaGjYvxAKFfUoTTyqR"
                                       "WnflhqnlTxUgsJRZfowjEFATDwbUxQyxNhNaTBhzRlXFLPElltRxGQc"
                                       "TrmnsKaNIExGwpzouHBeudWwAmelDaSYmJke",
                                  animal_type='cat', age='6'):
    """Проверяем, что поле для ввода "name" не примает больше 255 симолов, возвращает статус-код 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_simple_new_pet(auth_key, name, animal_type, age)
    # Баг!
    # Поле для ввода "name" принимает больше 255 символов
    # Поэтому получаем статус-код 200 вместо 400.
    assert status == 400

# 4
def test_add_long_type_to_new_pet(name="Stif", animal_type="EmXnBvnHgXwOWlEUUbRgZANTvayRVLNlLQiqnjXHlhUbWGuMVGSl"
                                                           "NRWnZATawpekCPVFuCbuZAXzfLjolAimjwzoaxeCSyYDLehaEvZc"
                                                           "XbtASSDacMkrmVPwmxQZQcEMUJUnViDbOsLMcNsJYlfPbOPWnsAnX"
                                                           "aixGIuaqzZclZHpllwBgOWXCzdpfocegEybqMPywQtfXrDAiNvpnJ"
                                                           "vyqKknpETjOsSzsHGKKSGqFMakWhUolaWxSHyKKwSnETVo", age='8'):
    """Проверяем, что поле для ввода "animal_type" не примает больше 255 симолов, возвращает статус-код 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_simple_new_pet(auth_key, name, animal_type, age)
    # Баг!
    # Поле для ввода "animal_type" принимает больше 255 символов
    # Поэтому получаем статус-код 200 вместо 400.
    assert status == 400

# 5
def test_add_letter_symb_to_new_pet_age(name='Анфиса',
                                  animal_type='Кошка', age='один'):
    """Проверяем, что поле для ввода "age" не принимает строковые значения и возвращает статус 400"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_simple_new_pet(auth_key, name, animal_type, age)
    # Баг!
    # Поле для ввода "age" принимает строковые значения.
    # Поэтому получаем статус-код 200 вместо 400.
    assert status == 400

# 6
def test_get_api_key_for_invalid_user_password(email=valid_email, password=invalid_password):
    """Проверяем, что запрос API ключа с невалидным паролем возвращает статус-код 403,
    а в результате не содержится 'key'"""
    status, result = pf.get_api_key(email, password)

    assert status == 403
    assert "key" not in result

# 7
def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """Проверяем, что запрос API ключа с невалидным email возвращает статус-код 403,
    а в результате не содержится 'key'"""

    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert "key" not in result

# 8
def test_add_empty_info_about_new_pet(name="", animal_type='', age=''):
    """Проверяем, что приложение не дает отправить запрос на добавление информации
    о питомце с путыми полями для ввода и возвращает статус-код 400"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_simple_new_pet(auth_key, name, animal_type, age)
    # Баг!
    # Приложение принимает пустые значения в обязательных полях для ввода при обновлении информации.
    # Поэтому получаем статус-код 200 вместо 400.
    assert status == 400

# 9
def test_add_new_pet_with_invalid_data(name="", animal_type='', age='', pet_photo='images/04.jpg'):
    """Проверяем, что запрос к серверу на добавление питомца с пустыми обязательными полями ввода
    возвращает статус-код 400"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    # Баг!
    # Приложение принимает пустые значения в обязательных полях для ввода.
    # Поэтому получаем статус-код 200 вместо 400.
    assert status == 400

# 10
def test_add_incorrect_photo_to_pet(pet_photo='images/07.gif'):
    """Проверяем, что запрос к серверу с некорректным форматом
     прикрепленного изображения (.gif) возвращает статус 500"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_api_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_to_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)
        assert status == 500
    else:
        raise Exception("There is no my pets")
