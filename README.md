# NL2SQL Telegram bot

## Запуск

### Предустановки

- Python, uv
- Docker
- Postgres

### Как получить токен бота и openrouter
Для получения токена бота, необходимо написать в телеграмме @BotFather, открыть мини-приложение, нажать кнопку "создать нового бота" и следовать инструкции
<br/>

Для получения токена openrouter, необходимо зарегистрироваться на сайте https://openrouter.ai/, после справа сверху навестить на иконку пользователя и выбрать Keys, далее создать ключ 

### Без использования docker

1. Скопируйте репозиторий
```
git clone https://github.com/JaxckR/testTask_RTL.git
```
2. Установите все зависимости и активируйте вирутальное окружение
```
cd testTask_RTL
uv sync --all-groups
.\.venv\Scripts\activate
```
3. Заполните .env.dist файл и переименуйте его в .env
4. Примените миграции и запустите приложение
```
uv run --env-file .env alembic upgrade head
uv run --env-file .env python -m app.main
```

**Чтобы загрузить свои данные воспользуйтесь следующей командой**
```
uv run --env-file .env scripts/load_videos.py *path_to_file*
```
<br/>

### С использованием docker
1. Скопируйте репозиторий
```
git clone https://github.com/JaxckR/testTask_RTL.git
```
2. Заполните .env.dist файл и переименуйте его в .env
3. Запустите приложение
```
docker compose up --build
```
**Чтобы загрузить свои данные воспользуйтесь следующими командами**
```
docker exec -it *container_name* bash
python -m load_videos.py *path_to_file*
```

## Об архитектуре
В проекте используется реализация чистой архитектуры. 
Запросы к llm происходят через LLMGateway(реализация - OpenRouterGateway). 
Промпт находится в файле llm_prompt.txt на самом верхнем уровне. 
Промпт отправляется при каждом запросе, а возвращается SQL-запрос, который далее исполняется sqlalchemy и возвращается ответ