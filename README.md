# Голосовой Ассистент на Langchain (OpenAI)

## Описание проекта

Этот проект представляет собой голосового ассистента, разработанного в рамках дипломного проекта для Яндекс.Практикума.
Ассистент основан на технологиях OpenAI и предназначен для поиска информации о фильмах в нашем сервисе кинотеатра.

## Что удалось реализовать?

###

- Организация кодовой базы по [шаблону DDD](https://github.com/yp-middle-python-24/python-service-example/)
- Speech To Text на базе [Whisper](https://openai.com/research/whisper) от OpenAI
- LLM:
  - Получение embeddings для фильмов в векторную базу данных pgvector
  - Поиск фильмов по embeddings
  - Получение информации о конкретном фильме по embeddings
  - Сохранение истории диалогов с ассистентом
- Text to speech на базе [Yanex SpeechKit](https://cloud.yandex.ru/services/speechkit) и [ElevenLabs](https://elevenlabs.io/)
- Клиент для работы с сервисом на базе Telegram-бота

## Команда:

- [Артем](https://github.com/ijaric/python-monorepo/commits?author=ijaric)
- [Александр](https://github.com/ksieuk)
- [Алексей](https://github.com/grucshetskyaleksei)

## Как запустить проект?

1. Скачать [файл базы данных](https://disk.yandex.ru/d/ZAKDDg8lP9DHBQ) с `embeddings` и поместить её по пути `src/assistant/data/dump.sql`.

2. В файл `.env.example` переименовать в `.env` и заполнить переменные окружения.
   Пример заполнения переменных окружения:

```
POSTGRES_DRIVER=postgresql+asyncpg # Драйвер для работы с базой данных
POSTGRES_HOST=db # Хост базы данных
POSTGRES_PORT=5432 # Порт базы данных
POSTGRES_USER=app # Пользователь базы данных
POSTGRES_PASSWORD=123qwe # Пароль пользователя базы данных
POSTGRES_DB_NAME=movies_database # Название базы данных

NGINX_PORT=80 # Порт nginx
API_HOST=0.0.0.0 # Хост API
API_PORT=8000 # Порт API

JWT_SECRET_KEY=secret # Секретный ключ для JWT
JWT_ALGORITHM=HS256 # Алгоритм шифрования JWT

APP_RELOAD=True # Автоматическая перезагрузка приложения

VOICE_AVAILABLE_FORMATS=mp3,ogg,wav,oga # Доступные форматы аудиофайлов
VOICE_MAX_INPUT_SIZE=5120 # Максимальный размер входного аудиофайла в килобайтах
VOICE_MAX_INPUT_SECONDS=30 # Максимальная длительность входного аудиофайла в секундах

OPENAI_API_KEY=sk-1234567890 # API-ключ OpenAI
OPENAI_STT_MODEL=whisper-1 # Модель для распознавания речи

PROXY_HOST=123.123.123.123 # Хост прокси
PROXY_PORT=1234 # Порт прокси
PROXY_USER=proxy_user # Пользователь прокси
PROXY_PASSWORD=proxy_password # Пароль прокси
PROXY_ENABLE=True # Включить прокси

TTS_YANDEX_API_KEY=1234567890 # API-ключ Yandex SpeechKit
TTS_YANDEX_AUDIO_FORMAT=oggopus # Формат аудиофайла
TTS_YANDEX_SAMPLE_RATE_HERTZ=48000 # Частота дискретизации аудиофайла

TTS_ELEVEN_LABS_API_KEY=1234567890 # API-ключ ElevenLabs
TTS_ELEVEN_LABS_DEFAULT_VOICE_ID=EXAVITQu4vr4xnSDxMaL # ID голоса по умолчанию

BOT_CONTAINER_NAME=bot_container_name # Название контейнера
BOT_IMAGE_NAME=botimage_name # Название образа
BOT_NAME=mybotname # Название бота
BOT_TOKEN=1234567890:ABCdefghIJKlmnopQRStuVWXYz # Токен бота
BOT_ADMINS=1234567890,9876543210 # ID администраторов бота через запятую

API_PROTOCOL=http # Протокол API
API_URL=api# URL API
API_PORT=8000 # Порт API

REDIS_HOST=redis # Хост Redis
REDIS_PORT=6379 # Порт Redis
```

3. Запустить проект командой `docker-compose up -d`

### Важно!

Для работы с Telegram-ботом необходимо предварительно начать с ним диалог и отключить в параметрах конфиденциальности
вашего аккаунта запрет на голосовые сообщения.
