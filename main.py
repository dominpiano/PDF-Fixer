#Importing libraries for GUI, manipulating PDFs and time.
import tkinter as tk
from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog as fd
from pathlib import Path
from PyPDF2 import PdfFileReader
from PyPDF2 import PdfFileWriter
import time

pages = []
pagesInfo = []
isAllSel = False;

#Label describing which page is modified at any given moment and what modifier is performed
def updateLabel():
    s = "Modyfikowane strony: "
    s += str(pagesInfo)
    pgInfo.set(s)
    if not pagesInfo:
        pgInfo.set("Modyfikowane strony: ")

#Function for creating button
def createButton():
    clear_frame()
    buttonOpen = tk.Button(frame, text = "Otwórz plik do modyfikacji",
                           command = openfile,
                           width = "30",
                           height = "1",
                           font = ('bodoni MT', 20),
                           bg="#9cc472",
                           border="0")
    buttonOpen.pack(pady="10")

#Main function for modifying PDF
def modify():

    # actually rotating specific pages
    for n in range(pdf_reader.getNumPages()):
        page = pdf_reader.getPage(n)
        for m in pages:
            if int(m.split(";")[0]) - 1 == n:
                if(m.split(";")[1] == "90"):
                    page.rotateClockwise(90)
                elif(m.split(";")[1] == "-90"):
                    page.rotateClockwise(-90)
                elif (m.split(";")[1] == "180"):
                    page.rotateClockwise(180)
        pdf_writer.addPage(page)

    with Path(path / pdf_name).open(mode='wb') as output_file:
        pdf_writer.write(output_file)

    pages.clear()
    pagesInfo.clear()
    pgInfoLabel.destroy()
    time.sleep(1)
    createButton()

#Select All
def selectAll():
    entry.insert(0, "All")
    global isAllSel
    isAllSel = True

#Rotate right
def pgRight():
    if isAllSel:
        pagesNum = pdf_reader.getNumPages()
        pagesInfo.append(entry.get())
        updateLabel()
        for i in range(pagesNum + 1):
            pages.append(str(i) + ";90")

    else:
        pages.append(entry.get() + ";90")
        pagesInfo.append(entry.get())
        updateLabel()
        entry.delete(0, 'end')

#Rotate left
def pgLeft():
    if isAllSel:
        pagesNum = pdf_reader.getNumPages()
        pagesInfo.append(entry.get())
        updateLabel()
        for i in range(pagesNum + 1):
            pages.append(str(i) + ";-90")

    else:
        pages.append(entry.get() + ";-90")
        pagesInfo.append(entry.get())
        updateLabel()
        entry.delete(0, 'end')

#Rotate 180 degrees
def pgFull():
    if isAllSel:
        pagesNum = pdf_reader.getNumPages()
        pagesInfo.append(entry.get())
        updateLabel()
        for i in range(pagesNum + 1):
            pages.append(str(i) + ";180")

    else:
        pages.append(entry.get() + ";180")
        pagesInfo.append(entry.get())
        updateLabel()
        entry.delete(0, 'end')

#Delete last modified page
def undo():
    try:
        pages.pop(len(pages)-1)
        pagesInfo.pop(len(pagesInfo) - 1)
        updateLabel()
    except:
        pass

#Destroy all widgets
def clear_frame():
   for widgets in frame.winfo_children():
      widgets.destroy()

#Function for opening files
def openfile():
    clear_frame()
    global pdf_writer
    pdf_writer = PdfFileWriter()

    buttonOpen = tk.Button(frame, text="Otwórz plik do modyfikacji",
                           command=openfile,
                           width="30",
                           height="1",
                           font=('bodoni MT', 20),
                           bg="#9cc472",
                           border="0")
    buttonOpen.pack(pady="10")

    #opening file and specifying its path
    pdf_path = fd.askopenfilename()
    global path
    path = Path(pdf_path)


    # manipulating file name
    global pdf_name
    pdf_name = path.name
    pdf_name = pdf_name.replace(".pdf", "_obrocone.pdf")

    #getting one directory up
    path = path.parent

    #some objects
    global pdf_reader
    pdf_reader = PdfFileReader(str(pdf_path))

    info = tk.Label(frame, text="Po kolei wpisuj strony i klikaj ich obrócenie", font=('helvetica', 14, 'bold'), bg="white")
    info.pack(pady="10")

    # Button "All"
    btnRight = tk.Button(frame, command=selectAll, text="WSZYSTKIE", font=('bodoni MT', 14))
    btnRight.place(x=200, y=138)

    global entry
    entry = tk.Entry(frame, width="3", font=('helvetica', 26))
    entry.pack(pady="15")

    #Creating buttons
    btnRight = tk.Button(frame, command = pgRight, text="↻", font=('bodoni MT', 20, "bold"))
    btnRight.place(x=450, y=129)

    btnLeft = tk.Button(frame, command = pgLeft, text="↺", font=('bodoni MT', 20, "bold"))
    btnLeft.place(x=510, y=129)

    btnFull = tk.Button(frame, command = pgFull, text="⇅", font=('bodoni MT', 20, "bold"))
    btnFull.place(x=570, y=129)


    global pgInfo
    pgInfo = tk.StringVar()
    pgInfo.set("Modyfikowane strony: ")
    global pgInfoLabel
    pgInfoLabel = tk.Label(frame, textvariable = pgInfo, font=('helvetica', 14, 'bold'),
                      bg="white")
    pgInfoLabel.pack(pady="10")


    btnFull = tk.Button(frame, command=undo, text="Cofnij ostanią stronę", font=('helvetica', 16))
    btnFull.pack()

    buttonModify = tk.Button(frame, text="Działaj!",
                             command = modify,
                             width="40",
                             height="2",
                             font=('bodoni MT', 20),
                             bg="#9cc472",
                             border="0")
    buttonModify.pack(pady="20")


root = tk.Tk()
root.title('PDF FIXER')
root.iconbitmap("pdf.ico")
root.geometry("800x400")
root.resizable(False, False)


#Appearance - frame and background
frame = tk.Canvas(root)
frame.pack(side="top", expand=True, fill="both")
bg = tk.PhotoImage(file = "bg.png")
frame.background = bg
img = frame.create_image(0, 0, anchor=tk.NW, image=bg)

createButton()

root.mainloop()