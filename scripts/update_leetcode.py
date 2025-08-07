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
    
    try:
        response = requests.post("https://leetcode.com/graphql", json={"query": query}, headers={"Content-Type": "application/json"})
        response.raise_for_status()
        data = response.json()
        
        if "errors" in data:
            raise ValueError(f"LeetCode API error: {data['errors'][0]['message']}")
            
        solved = data["data"]["matchedUser"]["submitStatsGlobal"]["acSubmissionNum"]
        ranking = data["data"]["matchedUser"]["profile"]["ranking"]
        
        return {
            "total": sum(item["count"] for item in solved),
            "easy": solved[0]["count"],
            "medium": solved[1]["count"],
            "hard": solved[2]["count"],
            "ranking": ranking
        }
        
    except Exception as e:
        print(f"Error fetching LeetCode stats: {e}")
        return None

def update_readme(stats):
    if not stats:
        return False

    mermaid_diagram = f"""
```mermaid
pie title LeetCode (Всего: {stats['total']})
    "Easy" : {stats['easy']}
    "Medium" : {stats['medium']}
    "Hard" : {stats['hard']}
```
"""

    leetcode_profile = f"""
[![LeetCode](https://img.shields.io/badge/LeetCode-Профиль-FFA116?style=flat&logo=leetcode)](https://leetcode.com/{username}/)
**Ранг**: {stats['ranking']:,} (топ {max(1, int(stats['ranking']/10000))}%) 
"""

    timestamp = datetime.now().strftime('%d.%m.%Y %H:%M')

    try:
        with open("README.md", "r", encoding="utf-8") as f:
            content = f.read()

        new_content = content.replace(
            "<!-- LEETCODE_STATS -->", 
            f"<!-- LEETCODE_STATS -->\n{mermaid_diagram}\n{leetcode_profile}\n*Обновлено: {timestamp}*"
        )

        with open("README.md", "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return True
        
    except Exception as e:
        print(f"Error updating README: {e}")
        return False

if __name__ == "__main__":
    username = "Ilia_Kurdyukov"
    stats = get_leetcode_stats(username)
    
    if stats:
        success = update_readme(stats)
        if success:
            print("README updated successfully!")
        else:
            print("Failed to update README")
    else:
        print("Failed to fetch LeetCode stats")
