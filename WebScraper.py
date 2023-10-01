import requests
import tkinter as tk
from tkinter import ttk, messagebox
from ttkbootstrap import Style

from bs4 import BeautifulSoup as bs

#Create the main window
root = tk.Tk()
root.title("Github Scraper App")
root.geometry("500x500")
style = Style(theme='solar')

#Configure the tab font to be bold
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))
style.configure("TNotebook", font=("TkDefaultFont", 25, "bold"))

#Create the notebook to hold the notes
notebook = ttk.Notebook(root, style="TNotebook")
notebook = ttk.Notebook(root)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
note_frame = ttk.Frame(notebook, padding=50)

notebook.add(note_frame, text="Add Github username")

#creates content label
content_label = ttk.Label(note_frame, text="Username:")
content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

#creates input box
content_entry = tk.Text(note_frame, width=40, height=1)
content_entry.grid(row=1,column=1,padx=10,pady=10)

content = ""

note_content = tk.Text(notebook, width = 40, height=10)
note_content.insert(tk.END, content)


def check_info():

    github_user = content_entry.get("1.0", tk.END)

    #gets url
    url = 'https://github.com/' + github_user.strip()

    #sends requests to url
    r = requests.get(url)

    #info from html page
    soup = bs(r.content, 'html.parser')

    person = []

    try:
        #locates specific info from html page
        profile_name = soup.find('span',{'itemprop': 'name'}).decode_contents()
        profile_userName = soup.find('span',{'itemprop': 'additionalName'}).decode_contents()
        profile_bio = soup.find('div',{'class': 'p-note user-profile-bio mb-3 js-user-profile-bio f4'})['data-bio-text']
        profile_location = soup.find('span',{'class': 'p-label'}).decode_contents()
    except :
        print("No username")
        pass

    #deletes current page and adds info page 
    notebook.forget(notebook.select())
    notebook.add(note_content, text="GitHub Info")
    try:
        note_content.insert(tk.END,"Name: "+ profile_name.strip()  + "\n")
        note_content.insert(tk.END, "Username: " + profile_userName.strip()  + "\n")
        note_content.insert(tk.END, "Bio: " + profile_bio.strip()  + "\n")
        note_content.insert(tk.END, "Located in: "+profile_location.strip()  + "\n")
    except:
        messagebox.showinfo(title="Error", message="Username not found.")
        pass

#submit button
submit_btn = ttk.Button(note_frame, text="Submit", command=check_info, style="scondary.TButton")
submit_btn.grid(row=2,column=1, padx=10, pady=10)

