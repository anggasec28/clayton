import requests
import json
import os

class Color:
    BROWN = "\033[0;33m"
    CYAN = "\033[0;36m"
    RED = "\033[0;31m"
    YELLOW = "\033[93m"
    GREEN = "\033[0;32m"
    END = "\033[0m"

def read_init_data(file_path):
    """Reads the init-data from the specified file."""
    with open(file_path, 'r') as file:
        return file.read().strip()

def get_headers(init_data, content_type="application/json"):
    """Constructs headers for API requests."""
    return {
        "accept": "application/json, text/plain, */*",
        "init-data": init_data,
        "content-type": content_type,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0"
    }

def authenticate(init_data):
    """Authenticates using the given init-data and returns user info."""
    url = "https://tonclayton.fun/api/user/auth"
    headers = get_headers(init_data, content_type="text/plain")
    
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        print(Color.GREEN + "LOGIN BERHASIL" + Color.END)
        return response.json()
    except requests.RequestException as e:
        print(Color.RED + f"GAGAL LOGIN : [ Query ada yang salah ]{e}" + Color.END)
        return None

def fetch_tasks(init_data, urls):
    """Fetches tasks from the given URLs."""
    headers = get_headers(init_data)
    all_tasks = []
    
    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            tasks = response.json()
            all_tasks.extend(tasks)
            print(Color.GREEN + "Task Sukses" + Color.END)
        except requests.RequestException as e:
            print(Color.RED + f"Task Gagal: {e}" + Color.END)
    
    return all_tasks

def complete_task(task_id, init_data):
    """Marks a given task as complete."""
    url = "https://tonclayton.fun/api/tasks/complete"
    payload = {"task_id": task_id}
    headers = get_headers(init_data)
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(Color.GREEN + "Task Sukses" + Color.END)
        return response.json()
    except requests.RequestException as e:
        print(Color.RED + f"Task Gagal {e}" + Color.END)
        return None

def claim_task(task_id, init_data):
    """Claims the reward for a given task."""
    url = "https://tonclayton.fun/api/tasks/claim"
    payload = {"task_id": task_id}
    headers = get_headers(init_data)

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        print(Color.GREEN + "Claim Sukses" + Color.END)
        return response.json()
    except requests.RequestException as e:
        print(Color.RED + f"Claim Gagal: {e}" + Color.END)
        return None

def print_welcome_message():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Color.GREEN + "=" * 60 + Color.END)
    print(Color.CYAN + "Clayton BOT | ASC AIRDROP\n" + Color.END)
    print(Color.RED + "Telegram: @airdropasc" + Color.END)
    print(Color.YELLOW + "Gunakan dengan bijak dan jangan lupa join telegram!" + Color.END)
    print(Color.GREEN + "=" * 60 + Color.END)

def main():
    print_welcome_message()
    
    init_data = read_init_data('query.txt')  # Assuming this file exists
    urls = [
        "https://tonclayton.fun/api/tasks/daily-tasks",
        "https://tonclayton.fun/api/tasks/default-tasks",
        "https://tonclayton.fun/api/tasks/partner-tasks"
    ]
    
    auth_response = authenticate(init_data)
    if auth_response:
        print(Color.RED + f"Login Sukses" + Color.END)
        tasks = fetch_tasks(init_data, urls)
        
        for task_item in tasks:
            task = task_item.get('task', {})
            task_id = task_item.get('task_id')
            title = task.get('title', 'No Title')
            if task_id:
                print(f"Completing Task: {title} (ID: {task_id})")
                complete_task(task_id, init_data)
                claim_task(task_id, init_data)

if __name__ == "__main__":
    main()
