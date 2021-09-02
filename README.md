# Pictures service

###  Сервис для обработки изображений!
***
    
###  Структура  
    pictures
    ├── user_images_service
        ├── config  #папка с настройками базы данных и прочего
        ├── repositories #каталог схем таблиц бд(моделей)
        ├── routers #каталог функций - роутингов 
        ├── schemas #каталог  json схем
        ├── service #каталог различных функций проверки  , jwt token и обработки изображения
        ├── static #каталог стилей javascript и изображений
        ├── Dockerfile
        ├── main.py #отправная точка приложения
        ├── requirements.txt #пакеты которые нужно установить
        └── templates #папка с фронтендом(html)
    ├── data #папка с настойкми nginx
    |   ├── nginx
    |       └──app.conf #файл с настойкми nginx
    ├── .env #файл с секретными переменными (создается при деплое sudo nano .env)
    └─  docker-compose.yml
## в папке templates  файл base.py в строчке заменяем в content на свой ключ который выдал гугл oauth . ссылка с примером как получить ключи https://developers.google.com/identity/sign-in/web/sign-in
<meta name="google-signin-client_id" content="286255588660-84eqn1m2rtfpmi4lu02epa63jg1ujt3l.apps.googleusercontent.com">

###  при локальной нужно создать файл .env с обязательными полями (если нужен фронтенд) ссылка с примером как получить ключи https://developers.google.com/identity/sign-in/web/sign-in
    ```
    # Environment settings for local development.
        id_client_google
        secret_key_google_auth
    ```
### перед разворачиванием локально не забываем создать баззу данных postgres локально или на стороннем сервисе . прописав путь в переменную URL_DATA_BASE в папке config файл database.py
### перед деплоем 
 0. В файле init-letsencrypt.sh в переменной domains вводим свое доменное имя example.ru www.example.ru
 1.  В папке data/nginx после значения server_name прописываем свое доменное имя и каждом месте где стоит example.com также заменяем на свое
 2. ### В папке static файл script js р
       ### //закоментировать при деплое -  раскоментироватьпри локальной разработке
       2. // const debug_path = 'http://localhost:8000' //при локальной разработке
       3. // const socket_debug = 'ws' //при локальной разработке
       4. // let wshost = 'localhost:8000' //при локальной разработке


      ### //раскоментировать при деплое - закоментировать при локальной разработке прописать свой домен
      1. const socket_debug = 'wss'
      2. let wshost = 'api-booking.ru'
      3. const debug_path  = 'https://api-booking.ru'

 3. В папке service файл pictures в переменную hosts = 'http://localhost:8000' 
 прописать имя домена https://example.com
### comands deploy
 0. https://console.cloud.yandex.ru/ нажимаем  compute cloud и затем  создать bm
 01. даем имя проекту 1.Выбор образа/загрузочного диска ставим Ubuntu 2. в поле логин вводим любое   имя , можно просто -admin
 
 1. В вашем компьютере в консоли вводим ssh-keygen -t rsa -b 2048 генерация ключа для яндекс клайуд
  попросит придумать кодовое слово - это будет ваш пароль для доступа
  и попросит повторить

 2. Вводим в консоли cat /home/gleb/.ssh/id_rsa(у вас будет свой путь для сохранения описаный в консоли после выполнения первой команды)  скопировать ключ ssh
 3. копируем ключ из результата команды номер 2 и вставляем в поле  SSH-ключ на странице яндекс клауд
 4. Нажимаем создать bm и после отображения кликаем на наш проект (дожидаемся status -  Running)
 5. Идем в консоль своего компьютера и вводим  ssh (наш логин и пункта 0.2)@(Публичный IPv4-он отображается на странице яндекс клайд нашего bm   ю
 )
  пример - ssh admin@84.201.179.68
 5. попросит ввести кодовое слово для этого аккаунта (вести кодовое слово из пункта 1)
 6. Если в пункте 5 все удачно - вы через консоль зашли в аккаунт яндекс клауд вашего bm 
 7. Вводим команду в консоли sudo apt get install git docker docker-compose -y  нажимаем enter
 8. Вводим команду git clone https://github.com/gleb89/pictures.git или вашу ссылку на репозиторий гит-хаб \нажимаем enter
 9. Вводим команду  cd pictures/ нажимаем enter
 10. Вводим команду  sudo nano .env
  откроется окно 
  ### вставить туда переменные со своими значениями(что связанно с POSTGRES пишем произвольные значения,можно оставить как есть)
     1. id_client_google и secret_key_google_auth это ваши ключи google auth
     2. POSTGRES_USER=glebhleb
     3. POSTGRES_PASSWORD=glebhleb2
     4. POSTGRES_DB=glebhleb
     ## пример 

      - id_client_google=286255588660-rgio676kjntofk12u3b1kg7ok61fkbdo.apps.googleusercontent.com
      - secret_key_google_auth=fDLe97luPpQhjE0nIjEmZKkk

11. Вводим команду chmod +x init-letsencrypt.sh нажимаем enter  для получения ssl сертификата
12. Вводим команду chmod ./init-letsencrypt.sh нажимаем enter для получения ssl сертификата
13. Вводим команду sudo docker-compose  up -d --build нажимаем enter 
14. Переходим в браузер и проверяем работу сайта






