from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkcalendar import *
import os
import pymongo
from pymongo import MongoClient
from datetime import datetime
import gridfs
import io
from PIL import Image
from PIL import ImageTk
from PIL.ExifTags import TAGS
import time
import sys

root = Tk()
root.rowconfigure(0,weight=1)
root.columnconfigure(0,weight=1)
root.title('DBMS Image Project')
root.geometry("700x700")
imagelist = []
cluster = MongoClient(sys.argv[1])
db = cluster["SelfStudy"]
fs = gridfs.GridFS(db)
fsfiles = db["fs.files"]
test = db["test"]
selecttext = 'Select Camera Model'#drop down mnenu default value

def colinit():
	#this function is just a utility function to set initial values
	#for empty db. Not called otherwise
	test.insert_one({"_id":1})
	test.update_one({"_id":1},{"$addToSet":{"models":selecttext}})

def goback():
		start_frame.tkraise()

def display(images):
	# Clear Main Frame and add stuff again
	for widget in main_frame.winfo_children():
		widget.destroy()
	
	main_frame.tkraise()
	# Create A Canvas
	my_canvas = Canvas(main_frame)
	my_canvas.pack(side=LEFT, fill=BOTH, expand=1)

	# Add A Scrollbar To The Canvas
	my_scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=my_canvas.yview)
	my_scrollbar.pack(side=RIGHT, fill=Y)
	# Configure The Canvas
	my_canvas.configure(yscrollcommand=my_scrollbar.set)
	my_canvas.bind('<Configure>', lambda e: my_canvas.configure(scrollregion = my_canvas.bbox("all")))
	# Create ANOTHER Frame INSIDE the Canvas
	second_frame = Frame(my_canvas)
	# Add that New frame To a Window In The Canvas
	my_canvas.create_window((0,0), window=second_frame, anchor="nw")
	
	imagelist.clear()
	rowcount = 0
	for result in images:
		data = fs.get(result["_id"]).read()
		ba = bytearray(data)
		pic = Image.open(io.BytesIO(ba))
		resized = pic.resize((300,225),Image.ANTIALIAS)
		imageeg = ImageTk.PhotoImage(resized)
		imagelist.append(imageeg)
		Label(second_frame,image=imagelist[rowcount],bg="white").grid(row=rowcount,column=0,sticky=W,padx=10,pady=10)
		opdate = result['metadata']['ogdate']
		op = datetime.strftime(opdate,'%B %e, %Y')
		Label(second_frame,text=('Date: '+op+'\nModel: '+result['metadata']['model']),bg="white").grid(row=rowcount,column=1,sticky=W,padx=10,pady=10)
		#Label(second_frame,image=imagelist[rowcount],bg="white").grid(row=rowcount,column=1,sticky=W,padx=10,pady=10)
		rowcount+=1

	back_button = Button(second_frame,text="Go Back",command=goback)
	back_button.grid(row=rowcount+1,column=0,sticky=W,padx=10,pady=10)
def upload():
	global drop
	filenames = filedialog.askopenfilenames(initialdir="C:",title="Select a file",filetypes=[("jpg files","*.jpg")])
	for filename in filenames:
		try:
			file = open(filename,"rb")
			a = fs.put(file)
			image = Image.open(filename)
			exif = {}
			for tag, value in image._getexif().items():
				if tag in TAGS:
					exif[TAGS[tag]] = value
			dt = datetime.strptime(exif['DateTimeOriginal'],"%Y:%m:%d %H:%M:%S")
			model = exif['Model']
			fsfiles.update_one({"_id":a},{"$set":{"metadata.ogdate":dt}})
			fsfiles.update_one({"_id":a},{"$set":{"metadata.model":model}})
			test.update_one({"_id":1},{"$addToSet":{"models":model}})
			
			
		except Exception as e:
			print("Upload unsuccesful")
			print(e)
			
		else:
			print("Upload Successful")
			
		

	r = (test.find_one({"_id":1}))(test.find_one({"_id":1}))['models']
	clicked=StringVar()
	clicked.set(r[0])
	drop.destroy()
	drop = OptionMenu(start_frame, clicked, *r)
	drop.grid(row=4,column=2,sticky=W,padx=10,pady=10)

def search():
	sample = start_date.get_date()
	dt = datetime.combine(sample, datetime.min.time())

	sample2 = end_date.get_date()
	dt2 = datetime.combine(sample2, datetime.min.time())

	#cameramodel is the string that needs to take the input
	cameramodel = clicked.get()
	print(cameramodel)
	if cameramodel == selecttext:
		print('1st condition inside')
		imagesfound=fsfiles.find({"metadata.ogdate":{"$gte":dt,"$lt":dt2}})
		display(imagesfound)

	else:
		print('2nd condition inside')
		imagesfoundcam=fsfiles.find({"metadata.ogdate":{"$gte":dt,"$lt":dt2},"metadata.model":cameramodel})
		display(imagesfoundcam)


start_frame = Frame(root)
main_frame = Frame(root)
start_frame.grid(row=0,column=0,sticky='nsew')
main_frame.grid(row=0,column=0,sticky='nsew')


start_frame.tkraise()
#images = fsfiles.find({"length":{"$gt":25}})
#display()

#ROW 0
label1 = Label(start_frame,text="Upload image(s) to the database:-",font=("Helvetica",18),bd=1)
label1.grid(row=0,column=0,sticky=W,padx=10,pady=10)

#ROW 1
upload_btn = Button(start_frame,text="Choose file",command=upload)
upload_btn.grid(row=1,column=0,sticky=W,padx=10,pady=10)

#ROW 2
label2 = Label(start_frame,text="Search for image:-",font=("Helvetica",18),bd=1)
label2.grid(row=2,column=0,sticky=W,padx=10,pady=10)

#ROW 3
start_label = Label(start_frame,text="From:-",font=("Helvetica",14))
start_label.grid(row=3,column=0,sticky=W,padx=10,pady=10)

end_label = Label(start_frame,text="Till:-",font=("Helvetica",14))
end_label.grid(row=3,column=1,sticky=W,padx=10,pady=10)


cam_label = Label(start_frame,text="Camera:-",font=("Helvetica",14))
cam_label.grid(row=3,column=2,sticky=W,padx=10,pady=10)

#ROW 4
start_date = DateEntry(start_frame, selectmode='day', year=2020, month=11, day=22)
start_date.grid(row=4,column=0,sticky=W,padx=10,pady=10)

end_date = DateEntry(start_frame, selectmode='day', year=2020, month=11, day=22)
end_date.grid(row=4,column=1,sticky=W,padx=10,pady=10)


res = (test.find_one({"_id":1}))['models']
clicked=StringVar()
clicked.set(res[0])
drop = OptionMenu(start_frame, clicked, *res)
drop.grid(row=4,column=2,sticky=W,padx=10,pady=10)

#ROW 5
search_btn = Button(start_frame,text='Search',command=search)
search_btn.grid(row=5,column=0,sticky=W,padx=10,pady=10)

#ROW 6
exit_btn = Button(start_frame,text='Exit',command=lambda:root.destroy())
exit_btn.grid(row=6,column=0,sticky=W,padx=10,pady=10)

root.mainloop()
