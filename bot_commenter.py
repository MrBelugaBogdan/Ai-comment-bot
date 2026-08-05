import os
import random
from github import Github
from groq import Groq

# Отримання ключів з налаштувань (Secrets)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
BOT_GITHUB_TOKEN = os.getenv("BOT_GITHUB_TOKEN")

g = Github(BOT_GITHUB_TOKEN)
client = Groq(api_key=GROQ_API_KEY)

# Публічні репозиторії, де бот може писати коментарі
TARGET_REPOSITORIES = [
    "vinta/awesome-python",
    "public-apis/public-apis",
    "octocat/Spoon-Knife",
    "donnemartin/system-design-primer"
]

def generate_developer_comment(topic_context):
    prompt = f"""
    Ти — досвідчений айтішник з іронічним гумором. 
    Тобі треба прокоментувати тему на GitHub: "{topic_context}".
    
    Напиши короткий (2-3 речення) коментар англійською чи українською мовою з айті-сленгом.
    Без мета-фраз, без образ та без тегів @.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_bot():
    print("🤖 Бот заступає на зміну...")
    repo_name = random.choice(TARGET_REPOSITORIES)
    print(f"🔍 Обираємо репозиторій: {repo_name}")
    
    try:
        repo = g.get_repo(repo_name)
        issues = list(repo.get_issues(state="open"))
        
        if issues:
            target_issue = random.choice(issues[:10])
            print(f"💬 Знайшли тему: '{target_issue.title}'")
            
            comment = generate_developer_comment(target_issue.title)
            target_issue.create_comment(comment)
            
            print(f"✅ Коментар успішно залишено: {target_issue.html_url}")
            print(f"📝 Текст: {comment}")
        else:
            print("😴 Немає відкритих тем у цьому репозиторії.")
            
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == "__main__":
    run_bot()
