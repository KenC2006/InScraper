from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import tkinter as tk
from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from collections import Counter
import threading
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import os


chrome_options = Options()
chrome_options.add_argument("--headless") 
chrome_options.add_argument("--window-size=1920,1080") 
chrome_options.add_argument("--no-sandbox")  
chrome_options.add_argument("--disable-dev-shm-usage")

base_dir = os.path.abspath(os.getcwd())  
chromedriver_path = os.path.join(base_dir, "chromedriver.exe")  
service = Service(executable_path=chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.instagram.com/")
user=""
access=""
logged_in=False

def login(username, password):
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")

    username_field.send_keys(Keys.CONTROL + "a")  
    username_field.send_keys(Keys.BACKSPACE)     
    password_field.send_keys(Keys.CONTROL + "a")  
    password_field.send_keys(Keys.BACKSPACE)     

    username_field.send_keys(username)
    password_field.send_keys(password)
    log_in_button = driver.find_element(By.XPATH, "//div[normalize-space() = 'Log in']")
    log_in_button.click()

def scroll_data(element):
    last_height = driver.execute_script("return arguments[0].scrollHeight;", element)
    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", element)
        try:
            WebDriverWait(driver, 5).until(lambda driver: driver.execute_script("return arguments[0].scrollHeight;", element) > last_height)
            new_height = driver.execute_script("return arguments[0].scrollHeight;", element)
            if new_height == last_height:  
                break
            last_height = new_height
        except TimeoutException:
            break

    data = element.find_elements(By.TAG_NAME, "a")
    data_links = [link.get_attribute("href") for link in data]
    for i in range(len(data_links)):
        data_links[i] = data_links[i][26:len(data_links[i])-1]
    data_links = list(dict.fromkeys(data_links))
    return data_links

def start_login():
    global user
    username = username_entry.get()
    password = password_entry.get()
    
    if not username or not password:
        messagebox.showerror("Error", "Please enter both username and password")
        return

    login_button.config(text="Attempting login", state=tk.DISABLED)

    try:
        login(username, password)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Save info']"))
        )
        messagebox.showinfo("Success", "Login successful")
        login_button.config(text="Obtaining follow data...", state=tk.DISABLED)
        user = username
        fetch_data()
    except Exception as e:
        messagebox.showerror("Error", f"Login failed")
    finally:
        login_button.config(text="Login", state=tk.NORMAL)

def update_ui(names):
    for widget in root.winfo_children():
        widget.destroy()

    tk.Label(root, text="Select an account:").pack(pady=10)
    
    combobox = ttk.Combobox(root, values=names, state="readonly")
    combobox.pack(pady=10)
    combobox.set("Select an account")
    def on_select(event):
        global user
        user = combobox.get()
        messagebox.showinfo(user+" Selected", "Obtaining data")
        fetch_data()

    combobox.bind("<<ComboboxSelected>>", on_select)

def fetch_data():
    driver.get("https://www.instagram.com/"+user+"/")
    followersLink= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "followers")))
    followersLink.click()
    followerList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))
    followers=scroll_data(followerList)

    driver.get("https://www.instagram.com/"+user+"/")
    followingList= WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "following")))
    followingList.click()
    followingList = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//div[@class='xyi19xy x1ccrb07 xtf3nb5 x1pc53ja x1lliihq x1iyjqo2 xs83m0k xz65tgg x1rife3k x1n2onr6']")))   
    following=scroll_data(followingList)

    v1 = Counter(following)
    v2 = Counter(followers)
    diff = v1 - v2

    unfollowed_accounts = list(diff.elements())
    result_message = (f"Followers: {len(followers)}\nFollowing: {len(following)}\n\n"f"Accounts that are followed but do not follow back:\n{unfollowed_accounts}")
    messagebox.showinfo("Results", result_message)
    global logged_in
    if (logged_in==False):
        update_ui(following)
        logged_in=True

root = tk.Tk()
root.title("Instagram Login")
frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

tk.Label(frame, text="Username:").grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Password:").grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)

login_button = tk.Button(frame, text="Login", command=lambda: threading.Thread(target=start_login).start())
login_button.grid(row=2, columnspan=2, pady=10)

root.mainloop()

