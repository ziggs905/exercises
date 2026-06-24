"""
[Title/Звание]

AIppetite - AI-задвижван персонален готвач и диетолог


[Description/Обрисовка]

Това е web приложение, разработено с Django, което играе ролята на персонален
диетолог и готвач. Потребителят въвежда базовите си показатели и описва целите си,
след което приложението използва AI (API) за генериране на персонализирани 
рецепти с точно балансирани хранителни стойности. Приложението включва интелигентна 
система за категоризиране на рецепти с тагове, основни хранителни калкулатори, 
автоматично генериране на shopping списъци и проследяване на прогреса чрез графики.


[Functionalities/Надарености]

1. Потребителски профили и автентикация:
   - Регистрация, login с валидиране на данни (име, имейл, парола).
   - Личен профил с метрики (тегло, ръст, възраст, пол, ниво на активност).
   - Дефиниране на цели и хранителни предпочитания (vegan, gluten-free, allergies).

2. AI-генериране на рецепти:
   - Изчисляване на BMR и TDEE с калориен корекция спрямо целта.
   - Определяне на оптимални пропорции макронутриенти спрямо целта.
   - Генериране на структурирани промптове и изпращане към Claude API.
   - Parsing на AI отговорите в JSON формат и съхранение като Recipe обекти.
   - Възможност за генериране на отделни рецепти или седмични meal plans.

3. Управление на рецепти с тагове:
   - Основна тагове система: dietary (vegan, vegetarian, gluten-free), practical 
     (quick-meals, budget-friendly), nutritional (high-protein, low-carb).
   - Търсене и филтриране по тагове, макроси, съставки.
   - Запазване, маркиране като любими и оценяване на рецепти (1-5 звезди).
   - Лична рецептурна библиотека с възможност за бележки.
   - Recipe collections / cook books

4. Хранителни калкулатори:
   - BMI калкулатор с интерпретация на резултатите.
   - TDEE калкулатор за различни нива на активност.
   - Macro Calculator - разпределение P/C/F спрямо целта.

5. Meal Planning:
   - Генериране на седмични meal plans с автоматично разпределение на калории.
   - Комбиниране на рецепти за постигане на дневните макро цели.
   - Възможност за редактиране и персонализиране на планове.

6. Проследяване на прогрес:
   - Въвеждане и проследяване на тегло във времето с графика.
   - Tracking на спазване на meal plans - процент изпълнение.
   - Преизчисляване на хранителни нужди при промяна на тегло/цел.

7. Shopping Lists:
   - Автоматично генериране на shopping lists от избрани meal plans.
   - Групиране и агрегиране на еднакви съставки.
   - Възможност за редактиране на генерирания списък.


[Milestones/Възлови точки]

- Django setup - models за User, Recipe, Tag, WeeklyPlan, WeightEntry.
- User authentication модул - регистрация, login, profile management.
- Хранителни калкулации модул - BMR, TDEE, macro distribution.
- AI интеграция модул - prompt generation, Claude API, JSON parsing.
- Recipe management модул - CRUD, favorites, ratings, search/filtering.
- Tagging система - Tag model, recipe categorization, filtering logic.
- Meal planning модул - weekly plans, calorie distribution между recipes.
- Progress tracking модул - weight entries, графики (Chart.js).
- Shopping list модул - ingredient aggregation, editing functionality.
- Calculator pages - BMI, TDEE, macro калкулатори като отделни форми.
- Frontend templates - dashboard, recipe pages, meal plans, calculators.
- Testing модул - unit tests за калкулации, mocked AI integration tests.


[Estimate in man-hours/Времеоценка в човекочасове]

- Django setup и базови models (8-12 часа)
- User authentication и profiles (8-12 часа)
- Хранителни калкулации и AI интеграция (15-20 часа)
- Recipe CRUD с тагове (10-15 часа)
- Meal planning functionality (8-12 часа)
- Progress tracking и графики (8-12 часа)
- Calculator pages (5-8 часа)
- Shopping list функционалност (5-8 часа)
- Frontend templates и styling (10-15 часа)
- Testing и debugging (8-12 часа)

Общо: 85-126 часа???


[Usage of technologies/Потребление на технологии]

- Web framework - Django
- База данни - SQLite 
- AI комуникация - Anthropic Claude API (anthropic library)
- Frontend - Django Templates + Bootstrap/CSS?
- Графики - Chart.js за weight progress visualization
- JSON handling - Python json library за AI response parsing
- Version control - Git/GitHub
"""
