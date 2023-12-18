
import requests
import base64
import io
import PIL.Image
from PIL import ImageTk
from ttkthemes import ThemedTk
import json
import openai
from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
import sv_ttk
win = Tk()
win.title("open file")
win.minsize(1,400)
win.config(padx=20,pady=20)
win.maxsize(800,900)
openai.api_key = api_key = "YOUR_API"

def file_retrieve():
    global win, newwin, buttony, brrr, br, image, buffered, base64_string, payload, api_url, response, json_data, la_lista, rhino
    file = askopenfile(filetypes=[("images",".png .jpg .jpeg")])

    newwin = Toplevel(master=win)
    newwin.title("results")
    newwin.minsize(400,500)

    brrr = PIL.Image.open(file.name)
    brrr = brrr.resize((100, 100))
    br= ImageTk.PhotoImage(brrr)
    



    buttony = Canvas(master=newwin,height=100,width=100,borderwidth=0,highlightthickness=0)

    rhino = buttony.create_image(50,50,image=br)
    
    # else:
    #     buttony = Button(image=brrr, master=newwin)        

    buttony.grid(row=1, column=1)

    
    image = PIL.Image.open(file.name).convert("RGB")
    # Convert to a JPEG Buffer
    global buffered
    buffered = io.BytesIO()
    image.save(buffered, quality=90, format="JPEG")
    # Base 64 Encode
    global base64_string
    base64_string = base64.b64encode(buffered.getvalue())
    base64_string = base64_string.decode("ascii")
    
    global payload
    global api_url
    global response
    global json_data
    global la_lista
    payload = { "base64str": base64_string, "model_id": '21af3472-6b14-4c84-9844-0eb8868a65ee', "conf_thresh": 0.4, "nms_thresh": 0.45 }
    api_url = 'https://apiv2.chooch.ai/predict?api_key=e27d9f14-e7ab-4a03-a501-3f4233b42c41'
    response = requests.put(api_url, data=json.dumps(payload))
    json_data = json.loads(response.content)
    la_lista = []

    for i in json_data["predictions"]:
        
        cat = f"I think there is a {i['class_title']} with certainty {i['score']} and/ or"    
        la_lista.append(cat)
    #     print(cat)

    response = openai.chat.completions.create(
        model = "gpt-4-1106-preview",

        messages = [
            {"role": "system", "content": "You are a carbon emmisions calculator. The user will give you a descriptions of 1 or more items and you will have to provide the emmisions for each item. Take into account that the words in between I think there are and and/or relate to a single item and are only describing it - they are not each individual items eg. chicken burger sandwich burger all mean the same. Only respond with a list format of each item - CO2 Emissions per annum in kg - eco alternative"},
            {"role": "user", "content": f"{la_lista} tell me the emmisions on average over a year for each described item and put it in a ordered list. "}
        ]
    )

    print(response.choices[0].message.content)
    global labela
    labela = ttk.Label(text=response.choices[0].message.content, font=("Arial", 8),master=newwin,wraplength=270)
    labela.grid(row=1,column=0)

    title = ttk.Label(text="Results",font=("Arial",40),master=newwin)
    title.grid(row=0,column=0)



giant = PhotoImage(file="image-icon (2).png")
button = ttk.Button(image=giant, command=file_retrieve)
button.grid(column=1,row=1)


sv_ttk.set_theme("light")
win.mainloop()
