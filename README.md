# QA Automation Framework

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Allure](https://img.shields.io/badge/Allure_Report-FF7F00?style=for-the-badge&logo=allure&logoColor=white)
![CI/CD](https://img.shields.io/badge/CI%2FCD-2C2C2C?style=for-the-badge&logo=git&logoColor=white)

Фреймворк автоматизированного тестирования (UI + API), демонстрирующий современные практики разработки тестов на Python.

## Особенности архитектуры

*   **Page Object Model (POM):** Модульная структура для UI тестов, обеспечивающая переиспользуемость кода и легкость поддержки.
*   **API Client Wrapper:** Обертка над `requests` с автоматическим логированием и управлением сессиями.
*   **Allure Reporting:** Подробные отчеты с шагами, логами и скриншотами.
*   **Cross-browser Testing:** Поддержка Chrome и Firefox (включая Headless режим).
*   **Parallel Execution:** Ускорение тестов с помощью `pytest-xdist`.
*   **CI/CD Integration:** Настроенный workflow для платформ GitHub, GitLab, etc.

## Требования

*   **Python 3.10+** Для запуска тестов.
*   **[Node.js & NPM](https://nodejs.org/en/download)** Для работы с отчетами Allure.

## Установка и настройка

Проект содержит скрипты для автоматической настройки окружения.

### Linux / macOS

Установка зависимостей: `chmod +x setup.sh && ./setup.sh`

Активация окружения: `source venv/bin/activate`

### Windows

Установка зависимостей: `setup.bat`

Активация окружения: `venv\Scripts\activate`

## Запуск тестов

Тесты запускаются через `pytest`. Конфигурация по умолчанию находится в `pytest.ini`.

| Задача | Команда |
| :--- | :--- |
| **Все тесты** | `pytest` |
| **Только UI** | `pytest tests/ui` |
| **Только API** | `pytest tests/api` |
| **Выбор браузера** | `pytest --browser=firefox` |
| **Параллельный запуск** | `pytest -n auto` |
| **Headless режим** | **Linux/Mac**: `HEADLESS=true pytest` <br> **Windows**: `set "HEADLESS=true" && pytest` |

## Отчетность

После выполнения тестов сырые данные попадают в `allure-results`. На их основе автоматически генерируется HTML-отчет.

### Просмотр отчета:

Прямой запуск: открыть `index.html` из папки `allure-report`.

Рекомендуемый способ: выполнить `npm run allure:open` для запуска через локальный сервер.

*Примечание: запуск через локальный сервер гарантирует корректное отображение данных, которые могут блокироваться браузером при прямом открытии файла.*

## Структура проекта

*   `api/` — Клиент для API тестов.
*   `pages/` — Page Objects.
*   `tests/` — Тестовые сценарии.
*   `config.py` — Конфигурация проекта.
*   `conftest.py` — Фикстуры Pytest.
*   `pytest.ini` — Настройки тестового раннера.
*   `.env.example` — Шаблон переменных окружения.
*   `.github/workflows/tests.yml` — CI/CD конфигурация.

## Контакты

Если у вас возникли вопросы по работе фреймворка или вы хотите обсудить сотрудничество:

**Моё [резюме](https://hh.ru/resume/feef596fff06469df60039ed1f67574941366f)** на hh.ru

---

## Лицензия

Этот проект распространяется на условиях лицензии **MIT**. Подробности в файле [LICENSE](LICENSE).

