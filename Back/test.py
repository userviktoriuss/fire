import json
import customtkinter as ctk
import ttkbootstrap as btrp

window = ctk.CTk()



params = {
    1: 1.5,
    2: 6
}

with open('strings.json', 'w') as f:
    json.dump(params, f)

with open('strings.json', 'r') as f:
    d = json.load(f)
    print(d)

window.mainloop()