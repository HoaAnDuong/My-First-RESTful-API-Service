import tkinter
from tkinter import font

window = tkinter.Tk()
window.geometry("800x500")

def onFrameConfigure(canvas):
   canvas.configure(scrollregion=canvas.bbox("all"))

canvas = tkinter.Canvas(window,bd=1, background="white")
frame = tkinter.Frame(canvas,background = "white")
scroll_y = tkinter.Scrollbar(window, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")
canvas.pack(side="top",expand=1, fill="both")
canvas.create_window((5,4), window=frame, anchor="n")
frame.bind("<Configure>", lambda e, canvas=canvas: onFrameConfigure(canvas))

font_labels = []

for i,e in enumerate(list(font.families())):
    font_labels.append(tkinter.Label(frame,text = f"{e}",font = (f"{e}","20"),background="white"))
    font_labels[i].pack(pady=5)
window.mainloop()