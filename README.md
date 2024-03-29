
# Проект  Поварская книга сладостей
Проект  Поварская книга сладостей хранит рецепты вкусностей.


### Содержание:
- [Проект  Поварская книга сладостей](#проект--поварская-книга-сладостей)
    - [Содержание:](#содержание)
    - [Реализованы возможности](#реализованы-возможности)
    - [Как запустить проект](#как-запустить-проект)
    - [Примеры запросов](#примеры-запросов)
      - [Добавение к рецепту продукт с указанным весом](#добавение-к-рецепту-продукт-с-указанным-весом)
      - [Увеличение на единицу количества приготовленных блюд для каждого продукта, входящего в указанный рецепт](#увеличение-на-единицу-количества-приготовленных-блюд-для-каждого-продукта-входящего-в-указанный-рецепт)
      - [Увеличение](#увеличение)
    - [Автор:](#автор)


### Реализованы возможности
* add_product_to_recipe с параметрами recipe_id, product_id, weight. Функция добавляет к указанному рецепту указанный продукт с указанным весом. Если в рецепте уже есть такой продукт, то функция должна поменять его вес в этом рецепте на указанный.
*  cook_recipe c параметром recipe_id. Функция увеличивает на единицу количество приготовленных блюд для каждого продукта, входящего в указанный рецепт.
*   show_recipes_without_product с параметром product_id. Функция возвращает HTML страницу, на которой размещена таблица. В таблице отображены id и названия всех рецептов, в которых указанный продукт отсутствует, или присутствует в количестве меньше 10 грамм.
*   админка, где пользователь сможет управлять входящими в базу данных продуктами и рецептами. Для рецептов должна быть возможность редактировать входящие в их состав продукты и их вес в граммах.


### Как запустить проект

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Esperansa08/dj_cookbook.git
```
```
cd dj_cookbook
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```
```
Для Windows:
env/Scripts/activate

Для Linux или macos
source env/bin/activate
```
```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Выполнить миграции:
```
python3 manage.py migrate
```

Запустить проект:
```
python3 manage.py runserver
```


### Примеры запросов

#### Добавение к рецепту продукт с указанным весом

Request: [GET] http://127.0.0.1:8000/add_product_to_recipe/?product_id=7&weight=5&recipe_id=1

Response:

```
У рецепта Сырник ингредиент Сода - 5г
```

#### Увеличение на единицу количества приготовленных блюд для каждого продукта, входящего в указанный рецепт

Request: [GET] http://127.0.0.1:8000/cook_recipe/2/

Response:

```
В рецепте Драники увеличено на 1 количества
приготовленных блюд из: [({'Яйцо'}, {6}), ({'Картофель'}, {5}), ({'Соль'}, {6}), ({'Мука'}, {3})]
```
#### Увеличение

Request: [GET] http://127.0.0.1:8000/show_recipes_without_product/5/

Response:

HTML страница, на которой размещена таблица
```
Поварская книга сладостей
Таблица рецептов
id	назвние рецепта
3	Блины
2	Драники
© 2024 Copyright Савельева Анастасия

```

### Автор:
 * Савельева Анастасия ([Почта](Visteria09@yandex.ru), [Github](https://github.com/Esperansa08))
