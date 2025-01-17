# VKINDER 
### Чат-бот для знакомств в социальной сети VK

#### Disclaimer

Данный проект является дипломной работой пользователя GitHub [LarissaRudenko](https://github.com/LarissaRudenko), которая писалась в рамках обучения курса Python-разработчик в обучающей организации Нетология. С cтороны пользователя [VitalRu](https://github.com/VitalRu) было оказано активное содействие в написании данного бота

#### Описание

![Static Badge](https://img.shields.io/badge/python-blue?style=for-the-badge&logo=python&color=FFC436) ![Static Badge](https://img.shields.io/badge/postgresql-%25?style=for-the-badge&logo=postgresql&color=F6F4EB) ![Static Badge](https://img.shields.io/badge/API_%7C_VK-%25?style=for-the-badge&logo=VK&color=279EFF)

Данный чат бот выдает по запросу пользователя страницу другого пользователя социальной сети VK. Исходя из данных профиля пользователя, делающего запрос, ему отдается страница пользователя противоположного пола, приблизительного равного по возрасту (плюс-минус 3 года), имеющего статус **не женат/не замужем/в активном поиске** и три лучшие фотографии со страницы на основе наибольшего количества полученных лайков у этих фотографий. Для реализации используется [API VK](https://dev.vk.com/ru/reference)

### Инструкция перед запуском

1. Для работы бота необходимо получить токен пользователя([access token](https://dev.vk.com/ru/api/access-token/getting-started)) и токен сообщества, где будет размещен бот ([community token](https://dev.vk.com/ru/api/access-token/getting-started))
2. В корневой директории проекта необходимо создать файл `.env`, и поместить туда значения токенов
3. Установить виртуальное окружение ```python -m venv venv``` 
4. Установить requirements.txt ```pip install -r requirements.txt``` 
5. Запустить программу (файл ```interface.py```) ```python interface.py```<br>
