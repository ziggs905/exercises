# AIppetite

AIppetite is a Django web application that acts as a personal chef and dietitian. Users enter their body metrics and goals, and the app calculates nutritional targets and uses an AI provider to generate recipes with balanced macronutrients, then helps organize those recipes into weekly meal plans and shopping lists.

Features:
- User profiles with body metrics, activity level, and dietary preferences
- AI-generated recipes matched to personal calorie and macro targets
- A tagged recipe library with search, filtering, favorites, ratings, and notes
- BMI, TDEE, and macro split calculators
- Automatic weekly meal plan generation with per-day calorie targets
- Weight progress tracking with charts and meal plan adherence
- Shopping list generation with ingredient aggregation from a meal plan

The project is built with Python and Django, using SQLite as the database. The frontend uses Django Templates with a hand-written CSS file and vanilla JavaScript for AJAX calls, plus Chart.js for progress charts. AI recipe generation sits behind a provider interface, with the Anthropic Claude API as the eventual backing provider.
