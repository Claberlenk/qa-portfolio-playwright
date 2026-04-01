# Путеводитель по проекту: QA Automation Portfolio

Этот файл объясняет **зачем** нужна каждая часть проекта, как всё связано между собой, и с чего начать изучение.

---

## Зачем вообще нужна структура?

Автотест — это обычная программа. Если писать всё в одном файле, через месяц никто не поймёт что происходит, а любое изменение на сайте (например, сменился CSS-класс кнопки) сломает 50 тестов вместо одного.

Структура проекта решает эту проблему.

---

## Карта проекта и роль каждой части

```
qa-portfolio-playwright/
│
├── pages/          ← "ЧТО есть на странице и КАК с ней взаимодействовать"
├── tests/
│   ├── ui/         ← "ЧТО проверяем в браузере"
│   └── api/        ← "ЧТО проверяем в HTTP-запросах"
├── utils/          ← "Общие инструменты — не тест, не страница, а помощники"
├── conftest.py     ← "Общие фикстуры для всех тестов"
├── pytest.ini      ← "Настройки Pytest — как и что запускать"
├── requirements.txt ← "Список зависимостей"
├── Dockerfile      ← "Как запустить проект в контейнере"
└── Jenkinsfile     ← "Как запускать тесты в CI/CD пайплайне"
```

---

## 1. `pages/` — Page Object Model (POM)

**Идея:** каждая страница сайта = отдельный Python-класс.

```python
# pages/login_page.py

class LoginPage:
    def __init__(self, page: Page) -> None:
        self.username_input = page.locator("#user-name")  # ← где элемент
        self.login_button   = page.locator("#login-button")

    def login(self, username, password):           # ← что можно сделать
        self.username_input.fill(username)
        self.login_button.click()
```

**Зачем POM?**
Если завтра кнопка сменит id с `#login-button` на `#btn-login` — правишь **одно место** (`login_page.py`), а не 20 тестов.

> Правило: тест говорит **что проверить**, страница знает **как это сделать**.

---

## 2. `tests/ui/` — UI-тесты (Playwright)

Тест **использует** классы из `pages/` и **проверяет** результат.

```python
# tests/ui/test_login.py

def test_successful_login(self, page: Page) -> None:
    lp = LoginPage(page)      # создаём объект страницы
    lp.navigate()             # открываем браузер
    lp.login("standard_user", "secret_sauce")  # действие
    expect(page).to_have_url("...inventory.html")  # проверка (assertion)
```

Структура каждого теста — **AAA**:
- **Arrange** — подготовка (открыть страницу, залогиниться)
- **Act** — действие (нажать кнопку, заполнить форму)
- **Assert** — проверка (что URL изменился, что появилась ошибка)

---

## 3. `tests/api/` — API-тесты (Requests)

Браузер не нужен. Отправляем HTTP-запрос — проверяем ответ.

```python
# tests/api/test_users.py

def test_get_single_user_returns_200(self) -> None:
    r = api_get("/users/2")        # GET https://reqres.in/api/users/2
    assert r.status_code == 200    # проверяем код ответа

def test_get_single_user_schema(self) -> None:
    r = api_get("/users/2")
    user = r.json()["data"]
    assert "id" in user            # проверяем структуру JSON
    assert "email" in user
```

API-тесты быстрее UI-тестов в 10–50 раз и не зависят от браузера.

---

## 4. `utils/helpers.py` — Помощники

Функции которые используются везде — не тест и не страница.

```python
BASE_API_URL = "https://reqres.in/api"

def api_get(path, **kwargs):
    return requests.get(f"{BASE_API_URL}{path}", timeout=10, **kwargs)
```

**Зачем выносить в utils?** Если поменяется базовый URL — меняешь в одном месте.

---

## 5. `conftest.py` — Фикстуры

Фикстура — это **подготовка условий** для теста. Pytest запускает её автоматически.

```python
# conftest.py

@pytest.fixture
def logged_in(page: Page) -> Page:
    lp = LoginPage(page)
    lp.navigate()
    lp.login("standard_user", "secret_sauce")
    return page  # тест получает уже залогиненный браузер
```

В тесте:
```python
def test_inventory_has_items(self, logged_in: Page) -> None:
    # браузер уже залогинен — не надо писать логин в каждом тесте
    inv = InventoryPage(logged_in)
    assert inv.inventory_items.count() == 6
```

> Правило: если 5+ тестов делают одно и то же в начале — это фикстура.

---

## 6. `pytest.ini` — Конфигурация Pytest

```ini
markers =
    ui: UI tests
    api: API tests
    smoke: Smoke tests
```

Маркеры позволяют запускать только нужные тесты:

```bash
pytest -m api      # только API
pytest -m ui       # только UI
pytest -m smoke    # только самые важные
```

---

## 7. `Dockerfile` — Контейнеризация

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.50.0-jammy
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["pytest"]
```

**Зачем Docker?** На твоей машине тесты работают. На машине коллеги — нет (другая OS, другой Python). Docker упаковывает всё окружение — тесты работают везде одинаково.

---

## 8. `Jenkinsfile` — CI/CD пайплайн

Jenkins автоматически запускает тесты при каждом коммите в git.

```
Push в git → Jenkins видит изменение → запускает Jenkinsfile →
  Stage 1: pip install
  Stage 2: pytest -m api
  Stage 3: pytest -m ui
→ Публикует отчёт
```

---

## Схема зависимостей

```
tests/ui/test_login.py
    └── uses → pages/login_page.py        (POM)
    └── uses → conftest.py fixture        (logged_in)

tests/api/test_users.py
    └── uses → utils/helpers.py           (api_get, api_post...)

conftest.py
    └── imports → pages/*.py

pytest.ini   → настраивает → pytest
Dockerfile   → запускает   → pytest
Jenkinsfile  → оркестрирует → Dockerfile
```

---

## С чего начать учиться

Рекомендуемый порядок:

1. **Запусти API тесты** — `pytest -m api -v` (быстро, без браузера, легко читать)
2. **Разбери один тест** в `tests/api/test_users.py` — что отправляется, что проверяется
3. **Добавь свой тест** — например, проверь что `GET /users?page=2` возвращает 6 элементов
4. **Запусти UI тесты** — `pytest -m ui --headed` (увидишь браузер)
5. **Разбери POM** — прочитай `pages/login_page.py` и `tests/ui/test_login.py` рядом
6. **Добавь свою страницу** — например, страницу деталей товара
