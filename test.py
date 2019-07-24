import os, tkinter, tkinter.filedialog, tkinter.messagebox

root = tkinter.Tk()
root.withdraw()

# 選択候補を拡張子jpgに絞る（絞らない場合は *.jpg → *）
filetype = [("", "*.jpg")]

dirpath = os.path.abspath(os.path.dirname(__file__))
tkinter.messagebox.showinfo('テスト', 'ファイルを選択してください')

# 選択したファイルのパスを取得
filepath = tkinter.filedialog.askopenfilename(filetypes = filetype, initialdir = dirpath)

# 選択したファイル名を表示
tkinter.messagebox.showinfo('テスト', filepath)