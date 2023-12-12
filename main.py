
import requests
import base64
import io
import PIL.Image
from ttkthemes import ThemedTk
import json
import openai
from tkinter import *
from tkinter.filedialog import askopenfile
win = ThemedTk(theme="breeze")
win.title("open file")
win.minsize(400,400)
win.maxsize(800,900)
openai.api_key = api_key = "YOUR_API_KEY"

def file_retrieve():
    global win
    file = askopenfile(filetypes=[("images",".png .jpg .jpeg")])
    global newwin
    newwin = Toplevel(master=win)
    newwin.title("results")
    newwin.minsize(400,500)
    global buttony
    global brrr
    brrr = PhotoImage(PIL.Image.open(file.name))
    

    global carto
    carto = brrr.subsample(3,3)
    buttony = Button(image=carto, master=newwin)
    # else:
    #     buttony = Button(image=brrr, master=newwin)        

    buttony.grid(row=1, column=0)
    global image
    
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
            {"role": "user", "content": f"{la_lista} tell me the emmisions on average over a year for each described iten. "}
        ]
    )

    print(response.choices[0].message.content)
    global labela
    labela = Label(text=response.choices[0].message.content, font=("Arial", 16),master=newwin,wraplength=270)
    labela.grid(row=2,column=0)


giant = PhotoImage(file="image-icon (2).png")
button = Button(image=giant, command=file_retrieve)
button.grid(column=1,row=1)



win.mainloop()
