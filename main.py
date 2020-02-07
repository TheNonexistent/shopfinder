from tkinter import *
import pprint
from os import path, remove

from lib import *

#####Config#####
print("Reading Config...")
config = open("config.cfg",'r')
KEY = config.read().splitlines()[0]
config.close()

if os.path.exists("temp.txt"):
  os.remove("temp.txt")

buff = []

###Window###

root = Tk()
root.resizable(0, 0)
root.title("Shop Finder")
###StringVars###

statusvar = StringVar()

ltln = [0, 0]

inp = ['out.xlsx']

###Funcs###

def read():
    print("[-]Fetching Place Ids:")
    places = []
    (place, rescode, status, next_page_token) = read_id(KEY, "Search Word", ltln[0].get(), ltln[1].get(), False)
    print("STAT:" + status)
    if status == "OVER_QUERY_LIMIT":
        print("API Key Maxed, Either change it or keep trying.")
        statusvar.set("API Key Maxed, Either change it or keep trying.")
        return
    elif status == "OK":
        places.append(place)
    timeout = 1
    while next_page_token != False or status == "OVER_QUERY_LIMIT":
        time.sleep(2)
        (place, rescode, status, next_page_token) = read_id(KEY, "Search Word", ltln[0].get(), ltln[1].get(), next_page_token)
        print("STAT:" + status)
        if status == "OVER_QUERY_LIMIT" and timeout <= 15:
            print("Timeout: " + str(timeout) + "/15")
            timeout += 1
            continue
        timeout = 1 
        if status == "OVER_QUERY_LIMIT" and timeout > 15:
            print("API Key Maxed, Either change it or keep trying.")
            statusvar.set("API Key Maxed, Either change it or keep trying.")
            return
        if status == "OK":
            places.append(place)
    print("[+]" + str(len(places)) + " Pages Indexed.")
    print("[-]Saving Place IDs For Later Use.")
    for value in places:
        save_id(value, 'temp.txt')
    statusvar.set("Done. " + str(len(places)) + " Page Of Place IDs Fetched.")
    print()
    print("[-]Done.")
    log = open('log.txt', 'a')
    log.write(pprint.pformat(places))
    log.close()

def generate():
    if not path.exists('temp.txt'):
        statusvar.set("No Fetched Data Found. Fetch Place IDs Before Generating.")
        return
    done = []
    plid_file = open('temp.txt', 'r')
    plids = plid_file.read().splitlines()
    count_all = len(plids)
    for index, plid in enumerate(plids):
        (data, status) = read_data(KEY, plid)
        print("STAT:" + status)
        if status == "OK":
            buff.append(data)
            done.append(index)
    plid_file.close()
    plid_file = open('temp.txt', 'w')
    for index,val in enumerate(plids):
        if index not in done:
            plid_file.write(val + "\n")
    plid_file.close()
    statusvar.set("Done. Generated " + str(len(done)) + "/" + str(len(plids)) + "Name, Phone Pairs.")

def save():
    print("Buffer:")
    print(buff)
    filename = inp[0].get() + ".xlsx"
    if filename == ".xlsx":
        filename = "out.xlsx"    
    
    generate_xlsx(buff, filename)



###GUI###

statusvar.set("Idle")

#Creating
title = Label(root, text="Shop Finder", font=('DejaVu Sans', 15))
lstatus = Label(root, text="Status:")
status = Label(root, textvariable=statusvar, fg='grey')
lapikey = Label(root, text="API Key:")
apikey = Entry(root, width=25)
apikey.insert(END, KEY)
def api_change():
    global KEY
    KEY = apikey.get()
    print("New API Key:" + apikey.get())
apikeybtn = Button(root, text="Change", padx= 10, pady=1, command=api_change)
llat = Label(root, text="Latitude:")
llng = Label(root, text="Longitude:")
ltln[0] = Entry(root, width=12)
ltln[1] = Entry(root, width=12)
linp = Label(root, text="Filename:")
inp[0] = Entry(root, width=22)
fetchbtn = Button(root, text="Fetch", padx=30, pady=6, command=read)
generatebtn = Button(root, text="Generate", padx=19, pady=6, command=generate)
savebtn = Button(root, text="Save", padx=30, pady=6, command=save)



#Deploying
title.grid(row=0, column=1)
lstatus.grid(row=1, column=0, sticky='W')
status.grid(row=1, column=1, sticky='W')
lapikey.grid(row=2, column=0, sticky='W')
apikey.grid(row=2, column=1, sticky='W')
apikeybtn.grid(row=2, column=2, sticky='W')
llat.grid(row=3, column=0, sticky='W')
ltln[0].grid(row=3, column=1, sticky='W')
llng.grid(row=4, column=0, sticky='W')
ltln[1].grid(row=4, column=1, sticky='W')
linp.grid(row=5, column=0, sticky='W')
inp[0].grid(row=5, column=1, sticky='W')
fetchbtn.grid(row=3, column=3)
generatebtn.grid(row=4, column=3)
savebtn.grid(row=5, column=3)


root.mainloop()
