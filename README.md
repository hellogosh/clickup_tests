# Проект автоматизации тестирования ClickUp

Автотесты для платформы ClickUp, покрывающие API и UI.  
Проект написан на Python с использованием Pytest, Playwright и Allure.

---

##  Стек технологий

- **Python** 3.12+
- **Pytest** — фреймворк для тестирования
- **Requests** — HTTP-клиент для API
- **Playwright** — автоматизация браузера
- **Allure** — отчёты
- **Faker** — генерация тестовых данных
- **Ruff** — линтинг и форматирование

---

##  Структура проекта
clickup_tests/
├── api/ # API-слой
│ ├── api_manager.py # менеджер API
│ └── tasks_api.py # методы работы с задачами
├── custom_requester/ # базовый класс с логированием запросов
├── data/ # тестовые данные (негативные сценарии)
├── enums/ # перечисления (браузеры, хосты)
├── tests/ # тесты
│ ├── ui/ # UI-тесты
│ ├── test_tasks.py # API-тесты задач
│ └── conftest.py # фикстуры
├── utils/ # утилиты
│ ├── browser_setup.py # настройка Playwright
│ ├── datagenerator.py # генерация данных (Faker)
│ └── helpers.py # переменные окружения
├── .env # конфиденциальные данные (не в Git)
├── .gitignore
├── requirements.txt
├── pytest.ini
└── README.md

---

## Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/hellogosh/clickup_tests.git
```
```bash
cd clickup_tests
```
### 2. Настройка виртуального окружения
```bash
python -m venv .venv
```
```bash
source .venv/bin/activate        # macOS/Linux

# .venv\Scripts\activate          # Windows
```
```bash
pip install -r requirements.txt
```
### 3. Переменные окружения (.env)
Создайте файл .env в корне и заполните:

CLICKUP_API_KEY=pk_...

CLICKUP_EMAIL=your_email@example.com

CLICKUP_PASSWORD=your_password

LIST_ID=901521528654

TEAM_ID=90152324458

### 4. Установка Allure (для отчётов)

Установите Java (требуется для Allure) 

Скачайте Allure CLI с GitHub releases (файл .tgz)

Распакуйте архив, например, в ~/allure и добавьте в PATH:


```bash
echo 'export PATH="$HOME/allure/bin:$PATH"' >> ~/.zshrc
```
```bash
source ~/.zshrc
```
Установите allure-pytest:

```bash
pip install allure-pytest
``` 
### Запуск тестов

API-тесты

```bash
pytest tests/test_tasks.py -v
```
UI-тесты

```bash
pytest tests/ui/ -v
```
Все тесты с Allure

```bash
pytest --alluredir=./allure-results
```
```bash
allure serve ./allure-results
```
### Покрытие тестами

API (8 тестов)

✅ Создание задачи

✅ Получение задачи

✅ Обновление задачи

✅ Удаление задачи

✅ Параметризованный негативный тест создания (невалидные данные)

✅ Негативные тесты для Get / Update / Delete (несуществующий ID → 401)


UI (3 теста)

✅ Успешная авторизация

✅ Неуспешная авторизация (неверный пароль)

✅ Удаление задачи через интерфейс


Все подготовительные действия (создание задачи) и очистка (удаление) выполняются через API-фикстуры.



