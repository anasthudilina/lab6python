# Lab 06 - Automated Testing (Pytest)

Лабораторна робота №6. Варіант 4 — Система банківських рахунків.

## Тестування
Всі тести написані з використанням `pytest`, `pytest-cov` та `pytest-asyncio`.

## Запуск тестів та перевірка покриття
```bash
pytest -v --cov=bank_app --cov-branch --cov-report=term-missing