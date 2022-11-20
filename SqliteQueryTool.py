import tkinter
import sqlite3

#just a simp Query Tool using Tkinter

#sqlite3

connection = sqlite3.connect("database.db")
cursor = connection.cursor()


#Tkinter
class SqliteQueryTool:
    def __init__(self):

        self.window = tkinter.Tk()
        self.window.title("Python Sqlite Query Tool")
        self.window.geometry("1300x800")

        self.canvas = tkinter.Canvas(self.window)
        self.canvas.pack(side="left",fill = "both",expand=True)



        self.title = tkinter.Label(self.canvas,text="Python Sqlite Query Tool",font=("Calibri","20"))
        self.title.pack(padx=5,pady=5)

        self.frame_1 = tkinter.Frame(self.canvas,width=500,height=300, background="white")
        self.frame_1.pack(padx=5,pady=5)

        self.option = tkinter.IntVar()

        self.v_scrollbar_1 = tkinter.Scrollbar(self.frame_1,orient='vertical')
        self.v_scrollbar_1.pack(side="right",fill="y")
        self.h_scrollbar_1 = tkinter.Scrollbar(self.frame_1,orient='horizontal')
        self.h_scrollbar_1.pack(side="bottom",fill="x")

        self.radio_button_1 = tkinter.Radiobutton(self.canvas,text = "One statement at a time",variable=self.option, value=0)
        self.radio_button_1.pack()
        self.radio_button_2 = tkinter.Radiobutton(self.canvas,text = "More than One statement at a time",variable=self.option, value=1)
        self.radio_button_2.pack()

        self.query_text = tkinter.Text(self.frame_1,font=("Cascadia Code","12"),xscrollcommand=self.h_scrollbar_1.set,yscrollcommand=self.v_scrollbar_1.set)
        self.v_scrollbar_1.config(command=self.query_text.yview)
        self.h_scrollbar_1.config(command=self.query_text.xview)
        self.query_text.pack()



        self.button = tkinter.Button(self.canvas,text="Execute!!!",font=("Calibri","20"),command =self.querry)

        self.button.pack(padx=5,pady=5)

        self.canvas_2 = tkinter.Canvas(self.window)
        self.canvas_2.pack(side = "right",fill="both",expand=True)

        self.title_2 = tkinter.Label(self.canvas_2,text="Output",font=("Calibri","20"))
        self.title_2.pack(padx=5,pady=5)

        self.frame_2 = tkinter.Frame(self.canvas_2,width=500,height=300,background="black",highlightcolor="white")
        self.frame_2.pack(padx=5,pady=5)

        self.v_scrollbar_2 = tkinter.Scrollbar(self.frame_2,orient='vertical')
        self.v_scrollbar_2.pack(side="right",fill="y")
        self.h_scrollbar_2 = tkinter.Scrollbar(self.frame_2,orient='horizontal')
        self.h_scrollbar_2.pack(side="bottom",fill="x")

        self.query_out = tkinter.Text(self.frame_2,font=("Cascadia Code","12"),foreground="white",background="black",xscrollcommand=self.h_scrollbar_2.set,yscrollcommand=self.v_scrollbar_2.set)
        self.v_scrollbar_2.config(command=self.query_out.yview)
        self.h_scrollbar_2.config(command=self.query_text.yview)
        self.query_out.pack()
        self.delete_button = tkinter.Button(self.canvas_2, text="Delete", font=("Calibri", "20"), command=self.delete)
        self.delete_button.pack()
    def querry(self):
        try:
            if self.option.get()==0:
                cursor.execute(self.query_text.get("1.0", "end-1c"))
                self.query_out.insert("end", f"\n{cursor.fetchall()}")
            elif self.option.get()==1:
                for statement in self.query_text.get("1.0", "end-1c").split(";"):
                    cursor.execute(statement)
                    self.query_out.insert("end", f"\n{cursor.fetchall()}")
        except Exception as e:
            print(f"{type(e)}:{e}")
            self.query_out.insert("end", f"\n{type(e)}:{e}")
    def delete(self):
        self.query_out.delete("1.0","end")
    def mainloop(self):
        self.window.mainloop()
    def destroy(self):
        self.window.destroy()

sqlitetool1 = SqliteQueryTool()
sqlitetool1.mainloop()









