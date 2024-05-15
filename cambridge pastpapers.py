import subprocess
import requests
import os
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askdirectory

selectfolder=False
if selectfolder==True:
    path=""

def select():
    global selectfolder,path
    selectfolder=True
    path=askdirectory()
def download_file(url, directory):
    local_filename = os.path.join(str(path), url.split('/')[-1])
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def download_past_papers(urls):
    desktop_dir = str(path)
    os.makedirs(desktop_dir, exist_ok=True)
    for url in urls:
        try:
            filename = download_file(url, desktop_dir)
            status_var.set(f"Downloaded {filename}")
        except Exception as e:
            status_var.set(f"Failed to download {url}: {e}")

def generate_past_paper_urls():
    year = year_var.get()
    subject = subject_var.get().lower()
    varient = varient_var.get()
    paper = paper_var.get()
    season = season_var.get().lower()


    if subject == "computer science" and int(year) < 21:
        code = "9608"
    elif subject == "computer science":
        code="9618"
    elif subject=="egp":
        code="8021"
    elif subject == "physics":
        code="9702"
    elif subject == "further mathematics":
        code="9231"
    elif subject == "chemistry":
        code="9701"
    elif subject=="mathematics":
        code="9709"
    elif subject=="accounts":
        code="9706"
#Add more subjects here.
    #elif subject == "":
        #code="

    type = "s" if season == "summer" else "w" if season == "winter" else None

    url = f"https://pastpapers.papacambridge.com/directories/CAIE/CAIE-pastpapers/upload/{code}_{type}{year}_{paper}_{varient}.pdf"
    download_past_papers([url])

    location = path + "/"+str(code) + "_" + str(type) + str(year) + "_" + str(paper) + "_" + str(varient) + ".pdf"
    subprocess.Popen([location],shell=True)

def main():
    root = tk.Tk()
    root.title("Past Paper Downloader")

    frame = ttk.Frame(root, padding="30")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

    ttk.Label(frame, text="YEAR:").grid(row=0, column=0, sticky=tk.SE ,pady=10 , padx =10 )
    ttk.Label(frame, text="SUBJECT:").grid(row=1, column=0, sticky=tk.SE,pady=10, padx =10)
    ttk.Label(frame, text="VARIENT:").grid(row=2, column=0, sticky=tk.SE ,pady=10 , padx =10)
    ttk.Label(frame, text="TYPE:").grid(row=3, column=0, sticky=tk.SE,pady=10 , padx =10)
    ttk.Label(frame, text="SEASON:").grid(row=4, column=0, sticky=tk.SE,pady=10 , padx =10)

    global year_var, subject_var, varient_var, paper_var, season_var, status_var


    year_var = tk.StringVar()
    subject_var = tk.StringVar()
    varient_var = tk.StringVar()
    paper_var = tk.StringVar()
    season_var = tk.StringVar()
    status_var = tk.StringVar()

    ttk.Combobox(frame, textvariable=year_var, values=["07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23"]).grid(row=0, column=1, sticky=tk.W)
    ttk.Combobox(frame, textvariable=subject_var, values=["Mathematics", "EGP", "Physics", "Chemistry", "Further Mathematics", "Computer Science", "Accounts",]).grid(row=1, column=1, sticky=tk.W)
    ttk.Combobox(frame, textvariable=varient_var,values=["11","12","13","21","22","23","31","32","33","41","42","42","43","51","52","53","61","62","63"]).grid(row=2, column=1, sticky=tk.W)
    ttk.Combobox(frame, textvariable=paper_var, values=["ms", "qp","in"]).grid(row=3, column=1, sticky=tk.W)
    ttk.Combobox(frame, textvariable=season_var, values=["Summer", "Winter"]).grid(row=4, column=1, sticky=tk.W)
    ttk.Button(frame, text="Download", command=generate_past_paper_urls).grid(row=5, column=0, columnspan=2, pady=10)
    ttk.Button(frame, text="select folder", command=select).grid(row=6, column=0, columnspan=2, pady=10)
    ttk.Label(frame, textvariable=status_var).grid(row=7, column=0, columnspan=2)

    root.mainloop()

if __name__ == "__main__":
    main()
