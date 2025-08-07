import os
import requests
from datetime import datetime

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

stats = get_leetcode_stats("Ilia_Kurdyukov")

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
**Ранг**: {stats['ranking']:,} (топ {int(stats['ranking']/10000)}%) 
"""

with open("README.md", "r") as f:
    content = f.read()

new_content = content.replace(
    "<!-- LEETCODE_STATS -->", 
    f"<!-- LEETCODE_STATS -->\n{leetcode_link}\n{mermaid_diagram}\n*Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}*"
)

with open("README.md", "w") as f:
    f.write(new_content)
