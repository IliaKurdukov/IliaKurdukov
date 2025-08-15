import os
import requests
from datetime import datetime, timedelta

def get_leetcode_stats(username):
    query = """
    {
      matchedUser(username: "%s") {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
        profile {
          ranking
        }
      }
    }
    """ % username
    
    response = requests.post("https://leetcode.com/graphql", json={"query": query})
    data = response.json()
    solved = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"][1:]
    ranking = data["data"]["matchedUser"]["profile"]["ranking"]
    return {
        "total": sum(item["count"] for item in solved),
        "easy": solved[0]["count"],
        "medium": solved[1]["count"],
        "hard": solved[2]["count"],
        "ranking": ranking
    }

def calculate_experience(start_date):
    today = datetime.now()
    start = datetime.strptime(start_date, "%Y-%m")
    
    total_months = (today.year - start.year) * 12 + (today.month - start.month)
    years = total_months // 12
    months = total_months % 12
    
    # Склонение "год/года/лет"
    if years == 1:
        years_text = "год"
    elif 2 <= years % 10 <= 4 and (years % 100 < 10 or years % 100 >= 20):
        years_text = "года"
    else:
        years_text = "лет"
    
    # Склонение "месяц/месяца/месяцев"
    if months == 1:
        months_text = "месяц"
    elif 2 <= months % 10 <= 4 and (months % 100 < 10 or months % 100 >= 20):
        months_text = "месяца"
    else:
        months_text = "месяцев"
    
    # Формирование строки
    if years > 0 and months > 0:
        return f"{years} {years_text} {months} {months_text}"
    elif years > 0:
        return f"{years} {years_text}"
    elif months > 0:
        return f"{months} {months_text}"

stats = get_leetcode_stats("Ilia_Kurdyukov")

# Рассчет опыта работы
experience_text = calculate_experience("2024-05")
experience_block = f"- Опыт работы: {experience_text}"

mermaid_diagram = """
```mermaid
%%{{init: {{'theme': 'base', 'themeVariables': {{ 'pie1': '#1CBAC8', 'pie2': '#FEB700', 'pie3': '#F63737' }}, 'config': {{'width': 300, 'height': 200}}}}}}%%
pie title Решено задач: {total}
   "Easy" : {easy}
   "Medium" : {medium}
   "Hard" : {hard}
```
""".format(
   total=stats['total'],
   easy=stats['easy'],
   medium=stats['medium'],
   hard=stats['hard']
)

leetcode_link = f"""
[![LeetCode Profile](https://img.shields.io/badge/LeetCode-Профиль-FFA116?style=flat&logo=leetcode)](https://leetcode.com/Ilia_Kurdyukov/)
**Ранг**: {'{0:,}'.format(stats['ranking']).replace(',', ' ')} 
"""

with open("README.md", "r") as f:
    content = f.read()

# Разделяем содержимое на части
start_exp_marker = "<!-- EXPERIENCE_START -->"
end_exp_marker = "<!-- EXPERIENCE_END -->"
start_leetcode_marker = "<!-- LEETCODE_STATS -->"
end_leetcode_marker = "<!-- LEETCODE_STATS_END -->"

# Находим позиции маркеров
start_exp_pos = content.find(start_exp_marker)
end_exp_pos = content.find(end_exp_marker)
start_leetcode_pos = content.find(start_leetcode_marker)
end_leetcode_pos = content.find(end_leetcode_marker)

if start_exp_pos != -1 and end_exp_pos != -1 and start_leetcode_pos != -1 and end_leetcode_pos != -1:
    # Сохраняем части до и после блока статистики
    before_content = content[:start_exp_pos]
    middle_content = content[(end_exp_marker  + len(end_exp_marker):start_leetcode_pos]
    after_content = content[end_leetcode_pos + len(end_leetcode_marker):]
    
    # Собираем новое содержимое
    new_content = (
        before_content +
        start_exp_marker + "\n" +
        experience_block + "\n" +
        end_exp_marker +
        middle_content +
        start_leetcode_marker + "\n" +
        leetcode_link + "\n" +
        mermaid_diagram + "\n" +
        f"*Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}*\n" +
        end_leetcode_marker +
        after_content
    )
else:
    # Если маркеров нет, добавляем блоки в конец
    new_content = content + "\n" +
    start_exp_marker + "\n" +
    experience_block + "\n" +
    end_exp_marker + "\n\n" +
    start_leetcode_marker + "\n" +
    leetcode_link + "\n" +
    mermaid_diagram + "\n" +
    f"Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n" +
    end_leetcode_marker

with open("README.md", "w") as f:
    f.write(new_content)
