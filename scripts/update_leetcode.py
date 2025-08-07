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
    solved = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
    ranking = data["data"]["matchedUser"]["profile"]["ranking"]
    return {
        "total": sum(item["count"] for item in solved),
        "easy": solved[0]["count"],
        "medium": solved[1]["count"],
        "hard": solved[2]["count"],
        "ranking": ranking
    }

stats = get_leetcode_stats("Ilia_Kurdyukov")

mermaid_diagram = f"""
```mermaid
pie title LeetCode (Всего: {stats['total']})
    "Easy" : {stats['easy']}
    "Medium" : {stats['medium']}
    "Hard" : {stats['hard']}
```
"""

leetcode_link = f"""
[![LeetCode Profile](https://img.shields.io/badge/LeetCode-Профиль-FFA116?style=flat&logo=leetcode)](https://leetcode.com/Ilia_Kurdyukov/)
**Ранг**: {stats['ranking']:,} (топ {int(stats['ranking']/10000)}%) 
"""

with open("README.md", "r") as f:
    content = f.read()

new_content = content.replace(
    "<!-- LEETCODE_STATS -->", 
    f"<!-- LEETCODE_STATS -->\n{mermaid_diagram}\n{leetcode_link}\n*Обновлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}*"
)

with open("README.md", "w") as f:
    f.write(new_content)
