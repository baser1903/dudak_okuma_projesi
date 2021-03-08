import tkinter as tk
from tkinter import filedialog, Text, Canvas
import os
from tkinter.ttk import Frame
from PIL import Image, ImageTk
import cv2
from main import prediction

if os.environ.get('DISPLAY','') == '':
    print('Ekran Bulundu. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')


root = tk.Tk()
maxWidth = 850
maxHeight = 600
root.geometry('%dx%d+%d+%d' % (maxWidth,maxHeight,0,0))

#var = tk.StringVar()

def close_window():
	root.destroy()
	exit()

def click():
	output.delete(0.0, tk.END)
	input_var = prediction(var)
	output.insert(tk.END, input_var)


def playVideo(path):
	
	#Capture video frames
	mainFrame = Frame(root)
	mainFrame.place(x=20, y=430)
	lmain = tk.Label(mainFrame)
	lmain.grid(row=0, column=0)

	cap = cv2.VideoCapture(path)

	def show_frame():
		try:
			ret, frame = cap.read()
			dim = (350, 250)
			frame = cv2.resize(frame, dim, interpolation = cv2.INTER_AREA)

			cv2image   = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

			img   = Image.fromarray(cv2image)
			imgtk = ImageTk.PhotoImage(image = img)
			lmain.imgtk = imgtk
			lmain.configure(image=imgtk)
			lmain.after(10, show_frame)
		except:
			pass

	show_frame()



def addVideo():
	global var
	root.filename = filedialog.askopenfilename(initialdir="./", title="Select File", filetypes=(("MP4","*.mp4"),("All Files","*.*")))
	my_label = tk.Label(root, text=root.filename, font="none 10")
	my_label.place(x=120, y=375)
	var = root.filename
		
	play = tk.Button(root, text="Videoyu Oynat", padx=10, pady=5, fg="white", bg="#263D42", command=lambda: playVideo(var))
	play.place(x=80, y=400)


	
#canvas = tk.Canvas(root, height=600, width=700, bg="#263D42")
#canvas.pack()




root.title("Bitirme Projesi")

canvas_width = 800
canvas_height = 10
w = Canvas(root, 
           width=canvas_width,
           height=canvas_height)
w.pack()

y = int(canvas_height / 2)
w.create_line(0, y, canvas_width, y, fill="#476042")

head_label = tk.Label(root, text="Dudak Okuma Projesi", font="none 40 bold")
head_label.pack()


canvas_width = 800
canvas_height = 10
w = Canvas(root, 
           width=canvas_width,
           height=canvas_height)
w.pack()

y = int(canvas_height / 2)
w.create_line(0, y, canvas_width, y, fill="#476042")

load = Image.open("./resim.jpg")
render = ImageTk.PhotoImage(load)
img = tk.Label(root, image=render)
img.image = render
img.place(x=250, y=100)


w = Canvas(root, width=10, height=230)
w.place(x=570, y=75)

w.create_line(0, 0, 800, 0, fill="#476042", width=3)

head1_label = tk.Label(root, text="Video Dosyası Seçiniz.", font="none 15 bold")
head1_label.place(x=20, y=310)

openFile = tk.Button(root, text="Dosya Aç", padx=10, pady=5, fg="white", bg="#263D42", command=addVideo)
openFile.place(x=80, y=340)

head2_label = tk.Label(root, text="Seçili Dosya: ", font="none 10")
head2_label.place(x=10, y=375)

head3_label = tk.Label(root, text="Video Konumu:", font="none 15 bold")
head3_label.place(x=550, y=310)

convert = tk.Button(root, text="Dönüştür", padx=30, pady=15, fg="white", bg="#263D42", command=click)
convert.place(x=380, y=450)

output = Text(root, width=40, height=10)
output.place(x=500, y=420)

root.mainloop()
