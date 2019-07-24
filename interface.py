import sys, os
from tkinter import *
import tkinter.filedialog, tkinter.ttk
from tkinter import messagebox
from PIL import Image, ImageTk  
import cv2
import numpy as np

class MainWindow():
    def __init__(self, main):
        self.B1 = Button(main, text="開く", command = self.ImgOpen) 
        self.B1.pack()
        self.B2 = Button(main, text="保存", command = self.ImgSave)
        self.B2.pack()
        self.B3 = Button(main, text="階調補正", command=self.Gamma)
        self.B3.pack()
        self.B4 = Button(main, text="２値化処理", command=self.binary)
        self.B4.pack()
        self.B5 = Button(main, text="空間フィルター", command=self.space)
        self.B5.pack()
        self.B6 = Button(main, text="周波数フィルタリング", command=self.freq)
        self.B6.pack()

        self.path = ""

    def ImgOpen(self):
        #select file type
        self.filetype = [("", "*")]
        self.dirpath = os.path.abspath(os.path.dirname(__file__))
        print(self.dirpath)
        # 選択したファイルのパスを取得
        self.filepath = tkinter.filedialog.askopenfilename(filetypes = self.filetype, initialdir = self.dirpath) 
        self.path = self.filepath

        #open a image
        self.img = Image.open(self.filepath)
        self.photo = ImageTk.PhotoImage(self.img)
        w, h = self.img.size
        #make sub_window
        self.sub_win = Toplevel()
        self.sub_win.geometry(str(h + 10) + "x" + str(w + 10))
        
        #画像表示
        self.labimg = Label(self.sub_win, image = self.photo)  
        self.labimg.image = self.photo  
        self.labimg.pack()

    def ImgSave(self):
        try:
            self.img = Image.open(self.path)
            print(os.path.join(self.dirpath, "dl"))
            self.img.show()
            self.img.save(os.path.join(self.dirpath, "dl", "pic.jpg"), quality=95)
        except:
            messagebox.showerror("error", "ファイルが存在しません")

    def Gamma(self):
        try:
            gamma = 1.8
            lookUpTable = np.zeros((256, 1), dtype = 'uint8')
            for i in range(256):
	            lookUpTable[i][0] = 255 * pow(float(i) / 255, 1.0 / gamma)
            img_src = cv2.imread(self.path, 1)
            img_gamma = cv2.LUT(img_src, lookUpTable)
            cv2.imwrite(os.path.join(self.dirpath, "dl", "ganma.jpg"), img_gamma)
        except:
            messagebox.showerror("error", "ファイルが存在しません")
    
    def binary(self):
        try:            
            border = 127
            gray = cv2.imread(self.path, 0)
            _, th2 = cv2.threshold(gray, border, 255, cv2.THRESH_BINARY)
            cv2.imwrite(os.path.join(self.dirpath, "dl", "bin.jpg"), th2)
        except:
            messagebox.showerror("error", "ファイルが存在しません")

    def space(self):
        try:
            # 入力画像の読み込み
            gray = cv2.imread(self.path, 0)
            kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
            dst = cv2.filter2D(gray, -1, kernel)
            cv2.imwrite(os.path.join(self.dirpath, "dl", "spase.jpg"), dst)
        except:
            messagebox.showerror("error", "ファイルが存在しません")
    
    def freq(self):
        try:   
            gray = cv2.imread(self.path, 0)
            himg = self.lowpass_filter(gray, 0.3)
            cv2.imwrite(os.path.join(self.dirpath, "dl", "freq.jpg"), himg)
        except:
            messagebox.showerror("error", "ファイルが存在しません")

    def lowpass_filter(self, src, a = 0.5):
        src = np.fft.fft2(src)
        # 画像サイズ
        h, w = src.shape
        # 画像の中心座標
        cy, cx =  int(h/2), int(w/2)
        # フィルタのサイズ(矩形の高さと幅)
        rh, rw = int(a*cy), int(a*cx)
        # 第1象限と第3象限、第1象限と第4象限を入れ替え
        fsrc =  np.fft.fftshift(src)
        # 入力画像と同じサイズで値0の配列を生成
        fdst = np.zeros(src.shape, dtype=complex)
        # 中心部分の値だけ代入（中心部分以外は0のまま）
        fdst[cy-rh:cy+rh, cx-rw:cx+rw] = fsrc[cy-rh:cy+rh, cx-rw:cx+rw]
        # 第1象限と第3象限、第1象限と第4象限を入れ替え(元に戻す)
        fdst =  np.fft.fftshift(fdst)
        # 高速逆フーリエ変換 
        dst = np.fft.ifft2(fdst)
        # 実部の値のみを取り出し、符号なし整数型に変換して返す
        return  np.uint8(dst.real)

if __name__ == "__main__":
    top = Tk()
    MainWindow(top)
    top.mainloop()  