import requests
from bs4 import BeautifulSoup
import json

# Функция для получения информации о вакансии
def get_vacancy_info(vacancy):
    vacancy_info = {}
    title = vacancy.find('span', class_='g-user-content').text.strip()
    salary = vacancy.find('div', class_='vacancy-serp-item__compensation')
    company = vacancy.find('a', class_='bloko-link')
    city = vacancy.find('span', class_='vacancy-serp-item__meta-info').text.split(",")[0].strip()
    link = vacancy.find('a', class_='bloko-link')['href']
    if salary:
        salary_text = salary.text.strip()
    else:
        salary_text = 'Не указана'
    vacancy_info['title'] = title
    vacancy_info['salary'] = salary_text
    vacancy_info['company'] = company.text.strip() if company else 'Не указана'
    vacancy_info['city'] = city
    vacancy_info['link'] = link
    return vacancy_info

# Отправляем запрос к странице с вакансиями на HeadHunter
url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
response = requests.get(url)

# Создаем объект BeautifulSoup для парсинга HTML
soup = BeautifulSoup(response.text, 'html.parser')

# Находим все блоки с информацией о вакансиях
vacancies = soup.find_all('div', class_='vacancy-serp-item')

# Создаем список для хранения информации о вакансиях
vacancies_info = []

# Проходимся по найденным блокам и извлекаем информацию о вакансиях
for vacancy in vacancies:
    vacancy_info = get_vacancy_info(vacancy)
    # Проверяем, содержат ли вакансии ключевые слова "Django" и "Flask"
    if 'Django' in vacancy_info['title'] or 'Flask' in vacancy_info['title']:
        vacancies_info.append(vacancy_info)

# Сохраняем информацию о вакансиях в JSON файл
with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies_info, f, ensure_ascii=False, indent=4)

print("Информация о вакансиях сохранена в файле vacancies.json")
