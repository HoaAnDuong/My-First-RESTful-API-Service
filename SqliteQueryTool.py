import tkinter
import sqlite3

#just a simp Query Tool using Tkinter

#sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


#Tkinter
window = tkinter.Tk()
window.title("Python Sqlite Query Tool")
window.geometry("1300x800")

canvas = tkinter.Canvas(window)
canvas.pack(side="left",fill = "both",expand=True)



title = tkinter.Label(canvas,text="Python Sqlite Query Tool",font=("Calibri","20"))
title.pack(padx=5,pady=5)


frame_1 = tkinter.Frame(canvas,width=500,height=300, background="white")
frame_1.pack(padx=5,pady=5)

option = tkinter.IntVar()

v_scrollbar_1 = tkinter.Scrollbar(frame_1,orient='vertical')
v_scrollbar_1.pack(side="right",fill="y")
h_scrollbar_1 = tkinter.Scrollbar(frame_1,orient='horizontal')
h_scrollbar_1.pack(side="bottom",fill="x")

radio_button_1 = tkinter.Radiobutton(canvas,text = "One statement at a time",variable=option, value=0)
radio_button_1.pack()
radio_button_2 = tkinter.Radiobutton(canvas,text = "More than One statement at a time",variable=option, value=1)
radio_button_2.pack()

query_text = tkinter.Text(frame_1,font=("Cascadia Code","12"),xscrollcommand=h_scrollbar_1.set,yscrollcommand=v_scrollbar_1.set)
v_scrollbar_1.config(command=query_text.yview)
h_scrollbar_1.config(command=query_text.xview)
query_text.pack()

def querry():
    try:
        if option.get()==0:
            cursor.execute(query_text.get("1.0", "end-1c"))
            query_out.insert("end", f"\n{cursor.fetchall()}")
        elif option.get()==1:
            for statement in query_text.get("1.0", "end-1c").split(";"):
                cursor.execute(statement)
                query_out.insert("end", f"\n{cursor.fetchall()}")
    except Exception as e:
        print(f"{type(e)}:{e}")
        query_out.insert("end", f"\n{type(e)}:{e}")

button = tkinter.Button(canvas,text="Execute!!!",font=("Calibri","20"),command =querry)

button.pack(padx=5,pady=5)

canvas_2 = tkinter.Canvas(window)
canvas_2.pack(side = "right",fill="both",expand=True)

title_2 = tkinter.Label(canvas_2,text="Output",font=("Calibri","20"))
title_2.pack(padx=5,pady=5)

frame_2 = tkinter.Frame(canvas_2,width=500,height=300,background="black",highlightcolor="white")
frame_2.pack(padx=5,pady=5)

v_scrollbar_2 = tkinter.Scrollbar(frame_2,orient='vertical')
v_scrollbar_2.pack(side="right",fill="y")
h_scrollbar_2 = tkinter.Scrollbar(frame_2,orient='horizontal')
h_scrollbar_2.pack(side="bottom",fill="x")

query_out = tkinter.Text(frame_2,font=("Cascadia Code","12"),foreground="white",background="black",xscrollcommand=h_scrollbar_2.set,yscrollcommand=v_scrollbar_2.set)
v_scrollbar_2.config(command=query_out.yview)
h_scrollbar_2.config(command=query_text.yview)
query_out.pack()

def delete():
    query_out.delete("1.0","end")

delete_button = tkinter.Button(canvas_2,text="Delete",font=("Calibri","20"),command = delete)
delete_button.pack()

window.mainloop()





