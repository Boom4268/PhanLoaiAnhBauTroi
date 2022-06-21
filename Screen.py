from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from setuptools import sic

from FeatureExtraction import *
from KNN import *
import cv2 as cv

fileName = 'data.csv'
WIDTH = 255
HEIGHT = 160
k=5

# tiền xử lý ảnh
def image_proccess(image, width=255, height=160):
    new_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    new_image = cv.resize(new_image, dsize=(width, height))
    return new_image

# Chuyển kiểu ảnh để hiển thị trên tkinter
def imageCV_to_imageTk(image):
    new_image = Image.fromarray(image)
    new_image = ImageTk.PhotoImage(new_image)
    return new_image

class App:
    def __init__(self, root):
        #declare var for app
        self.image_query = None
        self.root = root
        self.ponit = None
        self.stringVar = StringVar();

        topFrame = Frame(root)
        topFrame.pack(side=TOP, padx=15, pady=15)
        self.lbl_image = Label(topFrame)
        self.lbl_image.pack(side=LEFT)

        resultFrame = Frame(root)
        resultFrame.pack(side=TOP, padx=15, pady=15)
        self.resultText = StringVar()
        Label(resultFrame, textvariable=self.resultText).pack(side=LEFT)

        bottomFrame = Frame(root)
        bottomFrame.pack(side=BOTTOM, padx=15, pady=15)

        leftFrame = Frame(root)
        leftFrame.pack(side=LEFT, padx=15, pady=15)
        self.labels = []
        for i in range(k):
            lbl_img = Label(leftFrame)
            lbl_img.pack(side=LEFT)
            self.labels.append(lbl_img)

        self.tbl = ttk.Treeview(topFrame, columns=(1, 2, 3, 4), show="headings", height="3")

        Button(bottomFrame, text='Choose Image', command=self.show_image).pack(side=LEFT, padx=10)
        Button(bottomFrame, text='Find', command=self.find).pack(side=LEFT, padx=10)
        Button(bottomFrame, text='Refresh', command=self.refresh_app, ).pack(side=LEFT, padx=10)
        Button(bottomFrame, text='Exit', command=self.exit_app,).pack(side=LEFT)

    def show_image(self):
        fileName = filedialog.askopenfilename()
        image = cv.imread(fileName)
        self.refresh_app()
        self.image_query = image
        image_display = image_proccess(image)
        image_display = imageCV_to_imageTk(image_display)
        self.lbl_image.configure(image=image_display)
        self.lbl_image.image = image_display

        #Hiện thị thông số ảnh
        self.tbl.pack(side=BOTTOM, padx=15, pady=15);
        self.tbl.heading(1, text="Thông số ảnh")
        self.tbl.column(1, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.tbl.heading(2, text="Mean")
        self.tbl.column(2, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.tbl.heading(3, text="Std Deviation")
        self.tbl.column(3, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.tbl.heading(4, text="Skewness")
        self.tbl.column(4, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.ponit = color_moment(image_proccess(self.image_query))
        chanel1 = ["R"]
        chanel1.extend(self.ponit[0:3])
        self.tbl.insert(parent='', index='end', iid=0, text='', values=chanel1)
        chanel2 = ["G"];
        chanel2.extend(self.ponit[3:6]);
        self.tbl.insert(parent='', index='end', iid=1, text='', values=chanel2)
        chanel3 = ["B"];
        chanel3.extend(self.ponit[6:9]);
        self.tbl.insert(parent='', index='end', iid=2, text='', values=chanel3)

    def exit_app(self):
        return exit()

    def refresh_app(self):
        self.ponit = None
        self.tbl.delete(*self.tbl.get_children())
        self.lbl_image.configure(image=None)
        self.lbl_image.image = None
        self.resultText.set("")
        for i in range(k):
            self.labels[i].configure(image=None)
            self.labels[i].image = None

    def find(self):
        if(self.image_query is None):
            print("Image is None")
            f = Toplevel(self.root)
            f.title("Cảnh báo")
            f.geometry("300x50")
            Label(f, text="Bạn chưa chọn ảnh để tìm kiếm").pack(side=LEFT, padx=30)
            return
        else:
            data = read_data(fileName='data.csv')
            res = KNN(data, self.ponit, k)
            label = mostLabel(res)

            self.resultText.set('Kết quả phân loại ảnh: '+str(label))
            for i in range(k):
                image = cv.imread(res[i]['path'])
                image = image_proccess(image, 180, 110)
                image = imageCV_to_imageTk(image)
                self.labels[i].configure(image=image)
                self.labels[i].image = image
