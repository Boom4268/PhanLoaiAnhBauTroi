from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import ImageTk, Image
from FeatureExtraction import *
from KNN import *
import cv2 as cv

fileName = 'data.csv'
WIDTH = 255
HEIGHT = 160

# tiền sử lý ảnh
def image_proccess(image):
    new_image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    new_image = cv.resize(new_image, dsize=(WIDTH, HEIGHT))
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

        self.lbl_image = Label(root)
        self.lbl_image.pack()

        frame = Frame(root)
        frame.pack(side=BOTTOM, padx=15, pady=15)

        inforFrame = Frame(root)
        inforFrame.pack(side=LEFT, padx=15, pady=15)

        # self.lbl_featureNumber = Label(inforFrame, textvariable=self.stringVar)
        # self.lbl_featureNumber.pack()

        self.tbl = ttk.Treeview(inforFrame, columns=(1, 2, 3, 4), show="headings", height="3")
        self.tbl.pack();
        self.tbl.heading(1, text="Thông số ảnh")
        self.tbl.column(1, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.tbl.heading(2, text="Mean")
        self.tbl.column(2, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.tbl.heading(3, text="Std Deviation")
        self.tbl.column(3, minwidth=0, width=115, stretch=NO, anchor=CENTER)
        self.tbl.heading(4, text="Skewness")
        self.tbl.column(4, minwidth=0, width=115, stretch=NO, anchor=CENTER)

        btn_next = Button(frame, text='Choose Image', command=self.show_image).pack(side=LEFT, padx=10)
        btn_next = Button(frame, text='Find', command=self.find).pack(side=LEFT, padx=10)
        btn_exit = Button(frame, text='Exit', command=self.exit_app,).pack(side=LEFT)

    def show_image(self):
        fileName = filedialog.askopenfilename()
        image = cv.imread(fileName)
        self.image_query = image
        image_display = image_proccess(image)
        image_display = imageCV_to_imageTk(image_display)
        self.lbl_image.configure(image=image_display)
        self.lbl_image.image = image_display

        #Hiện thị thông số ảnh
        self.ponit = color_moment(image_proccess(self.image_query))
        self.tbl.delete(*self.tbl.get_children())
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

    def find(self):
        if(self.image_query is None):
            print("Image is None")
        else:
            data = read_data(fileName='data.csv')
            res = KNN(data, self.ponit, 5)
            label = mostLabel(res)
            f = Toplevel(self.root)
            f.title("Kết quả truy vấn")
            res_frame = Frame(f, relief=GROOVE, borderwidth=5)
            res_frame.grid(column=0, row=0, pady=10, padx=10)
            Label(res_frame, text='Kết quả phân loại ảnh: '+str(label)).grid(row=0, column=0)

            # image_frame = Frame(f)
            # image_frame.grid(column=0, row=1, pady=10, padx=10)

            for i in range(5):
                image = cv.imread(res[i]['path'])
                image = cv.resize(image, dsize=(150, 100))
                image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
                image = imageCV_to_imageTk(image)

                frame = Frame(f)
                frame.grid(column=i, row=1, padx=10, pady=10)
                Label(frame, text='Label: ' + res[i]['label']).grid(row=0, column=0)
                Label(frame, text='Distance: ' + str(res[i]['dist'])).grid(row=1, column=0)
                lable = Label(frame, image=image).grid(row=2, column=0)