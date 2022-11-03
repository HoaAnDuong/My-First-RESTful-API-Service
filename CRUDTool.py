import tkinter
import sqlite3



def Destroy(i):
    try:
        if(isinstance(i,dict)):
            for item in i.values():
                Destroy(item)
        else:
            i.destroy()
    except Exception as e:
        print(e)

class CRUDTool:
    def __init__(self):
        self.connection = sqlite3.connect("database.db")
        self.cursor = self.connection.cursor()



        self.window = tkinter.Tk()
        self.window.title("CRUDTool")
        self.window.geometry("1300x800")

        self.table_manager = {}
        self.table_displayer = {}

        self.table_manager["canvas_1"] = tkinter.Canvas(self.window,width=500,height=800)
        self.table_manager["canvas_1"].pack(side="left",fill="both")
        self.table_manager["frame_1"] = tkinter.Frame(self.table_manager["canvas_1"],width=300,height=800,background="white",highlightbackground="black",highlightthickness=1)
        self.table_manager["frame_1"].pack(side="left",fill="both")
        self.table_manager["table_option"] = {}

        self.showTableOption()

        self.table_displayer["canvas_2"] = tkinter.Canvas(self.window, width=800, height=800)
        self.table_displayer["canvas_2"].pack(side="left", fill="both")
        self.table_displayer["frame_2"] = tkinter.Frame(self.table_displayer["canvas_2"], width=800, height=800, background="white",highlightbackground="black",highlightthickness=1)
        self.table_displayer["frame_2"].pack(side="left",fill="both")
        self.table_displayer["table"] = tkinter.Label(self.table_displayer["frame_2"])
        self.table_displayer["table"].pack()

    def showTableOption(self):
        try:
            Destroy(self.table_manager["table_option"])
        except Exception as e:
            print(e)
        table_list = self.getTableName()
        for item in table_list:
            print(item)
            self.table_manager["table_option"][item] = tkinter.Button(self.table_manager["frame_1"], text=item,
                                                                      font=("Calibri", "12"),
                                                                      command=lambda: self.displayTable(self.table_manager["table_option"][item]["text"]))
            self.table_manager["table_option"][item].pack(padx=20, pady=20)
    def displayTable(self,table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name})")
        print(table_name,self.cursor.fetchall())
        self.table_displayer["table"].config(text = self.cursor.fetchall())
    def getTableName(self):
        self.cursor.execute("select name from sqlite_schema where type='table'")
        table_name = self.cursor.fetchall()
        table_name = [i[0] for i in table_name]
        return table_name
    def destroy(self):
        Destroy(self.__dict__)
    def mainloop(self):
        self.window.mainloop()






c1 = CRUDTool()
c1.mainloop()


