import sys, os
from tkinter import *
import tkinter.filedialog
from PIL import Image, ImageTk  

class MainWindow():
    def __init__(self, main):
        self.B1 = Button(main, text="開く")
        self.B1.bind("<Button-1>", self.DeleteEntryValue)  
        self.B1.pack()
        self.B2 = Button(main, text="保存", command=self.test)
        self.B2.pack()
        self.B3 = Button(main, text="階調補正", command=self.test)
        self.B3.pack()
        self.B4 = Button(main, text="２値化処理", command=self.test)
        self.B4.pack()
        self.B5 = Button(main, text="Hello cancel", command=self.test)
        self.B5.pack()
        self.B6 = Button(main, text="周波数フィルタリング", command=self.test)
        self.B6.pack()

    def test(self):
        print("a")

    def DeleteEntryValue(self, event):  
        self.root = Tk()  
        self.root.withdraw()  
        self.filetype = [("", "*.jpg")]
        self.dirpath = os.path.abspath(os.path.dirname(__file__))
        # 選択したファイルのパスを取得
        self.filepath = tkinter.filedialog.askopenfilename(filetypes = self.filetype, initialdir = self.dirpath) 
        print(self.filepath)  
        self.root.destroy()  
        self.root = Tk()  
        self.photo = ImageTk.PhotoImage(Image.open(self.filepath))  
        self.labimg = Label(self.root, image = self.photo)  
        self.labimg.image = self.photo  
        self.labimg.pack()  

if __name__ == "__main__":
    top = Tk()
    MainWindow(top)
    top.mainloop()  