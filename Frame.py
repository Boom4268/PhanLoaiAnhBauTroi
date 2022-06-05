import cv2 as cv
from PIL import ImageTk
from PIL import Image as Img
from tkinter import *

# chuyển đổi kiểu ảnh để hiển thị
def imageCV_to_imageTk(image):
    new_image = Img.fromarray(image)
    new_image = ImageTk.PhotoImage(new_image)
    return new_image
root = Tk();

# image1 = cv.imread('test/Am_u/am_u (38).jpg')
# image1 = cv.resize(image1, dsize=(150, 100))
# image1 = cv.cvtColor(image1, cv.COLOR_BGR2RGB)
# image1 = imageCV_to_imageTk(image1)

res_frame = Frame(root, relief=GROOVE, borderwidth=5)
res_frame.grid(column=0, row=0, pady=10, padx=10)
Label(res_frame, text='Phan loai anh thuoc: ').grid(row=0, column=0)
main_frame = Frame(root)
main_frame.grid(column=0, row=1, pady=10, padx=10)

top = Toplevel(root)

# for i in range(5):
#     frame1 = Frame(main_frame)
#     frame1.grid(column=i, row=0, padx=10, pady=10)
#     Label(frame1, text='This Frame 1').grid(row=0, column=0)
#     Label(frame1, image=image1).grid(row=1, column=0)
#
# for i in range(5):
#     frame1 = Frame(top)
#     frame1.grid(column=i, row=0, padx=10, pady=10)
#     Label(frame1, text='This Frame 1').grid(row=0, column=0)
#     Label(frame1, image=image1).grid(row=1, column=0)

root.title("Display result")
root.mainloop()