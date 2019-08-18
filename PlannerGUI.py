from Tkinter import *
import os

assignments_list = []
assignment_objs_list = []

# At some point assign each assignment a unique ID number,
# which would help assignments_list stay organized.

class Planner:
	def __init__(self, master):
		file1 = open("assignments.txt","a")

		self.master = master
		master.title("Planner")
		master.geometry('900x600+200+100')

		self.create_left_frame()
		self.create_center_frame()
		self.create_right_frame()

	def commit_assignments_to_memory(self):
		# below is a fix for problem with pyinstaller
		filename = "assignments.txt"
		#filename = "/Users/oscarluthje/Desktop/PythonPrograms/Planner/assignments.txt"
		#if '_MEIPASS2' in os.environ:
   		#	filename = os.path.join(os.environ['_MEIPASS2'], filename)

		with open(filename,"w+") as file:
			for assignment in assignments_list:
				file.write(assignment + "\n")
	#(self, master, assignment_class, assignment_description)
	def load_assignments_from_memory(self):
		global assignments_list
		# below is a fix for problem with pyinstaller
		filename = "assignments.txt"
		#filename = "/Users/oscarluthje/Desktop/PythonPrograms/Planner/assignments.txt"
		#if '_MEIPASS2' in os.environ:
   		#	filename = os.path.join(os.environ['_MEIPASS2'], filename)

		with open(filename,"r+") as file:
			assignments_list = file.readlines()
			# remove whitespace characters like `\n` at the end of each line
			assignments_list = [item.strip() for item in assignments_list]

		# load all assignments from memory into application for display
		for index, item in enumerate(assignments_list):
			# removes ',' from each item in list and seperates each item into 3
			split_array = re.split(r"\,", item)
			if split_array[2] == "completed=true" and split_array[3] == "deleted=false":
				self.completed_assignment_label = CompletedAssignments(self.master, split_array[0], split_array[1], index)
			if split_array[2] == "completed=false" and split_array[3] == "deleted=false":
				self.assignment_label = Assignments(self.master, split_array[0], split_array[1], index)

	def create_left_frame(self):
		self.left_frame = Frame(self.master, relief=GROOVE, bd=1)
		self.left_frame.pack(side=LEFT, anchor=NW, padx=25, pady=25)
		self.left_frame['borderwidth'] = 2

		self.assignment_label = TitleLabel(self.master, self.left_frame, "Assignments:")
		
		self.separator = Frame(self.left_frame, width=200, height=2, bd=1, relief=GROOVE)
		self.separator.pack(fill=X, padx=5, pady=5)

		# scroll enabling
		self.left_canvas=Canvas(self.left_frame, width=200, height=500)
		self.scroll_frame=Frame(self.left_canvas)
		self.left_scrollbar=Scrollbar(self.left_frame,orient="vertical",command=self.left_canvas.yview)
		self.left_canvas.configure(yscrollcommand=self.left_scrollbar.set)

		def configure_scroll(event):
			self.left_canvas.configure(scrollregion=self.left_canvas.bbox("all"))

		self.left_scrollbar.pack(side="right",fill="y")
		self.left_canvas.pack(side="left", fill="both", expand=True)
		self.left_canvas.create_window((0,0),window=self.scroll_frame,anchor='nw')
		self.scroll_frame.bind("<Configure>", configure_scroll)

	def create_center_frame(self):
		self.center_frame = Frame(self.master, relief=GROOVE, bd=1)
		self.center_frame.pack(side=LEFT, anchor=N, padx=25, pady=25)
		self.center_frame['borderwidth'] = 2

		self.completed_title_label = TitleLabel(self.master, self.center_frame, "Completed:")

		self.separator = Frame(self.center_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

		# scroll enabling
		self.center_canvas=Canvas(self.center_frame, width=200, height=500)
		self.center_scroll_frame=Frame(self.center_canvas)
		self.center_scrollbar=Scrollbar(self.center_frame,orient="vertical",command=self.center_canvas.yview)
		self.center_canvas.configure(yscrollcommand=self.center_scrollbar.set)

		def configure_scroll(event):
			self.center_canvas.configure(scrollregion=self.center_canvas.bbox("all"))

		self.center_scrollbar.pack(side="right",fill="y")
		self.center_canvas.pack(side="left")
		self.center_canvas.create_window((0,0),window=self.center_scroll_frame,anchor='nw')
		self.center_scroll_frame.bind("<Configure>", configure_scroll)

	def create_right_frame(self):
		self.right_frame = Frame(self.master)
		self.right_frame.pack(side=RIGHT, anchor=N, padx=50, pady=30)
		self.right_frame['borderwidth'] = 2

		self.assignment_title_label = TitleLabel(self.master, self.right_frame, "Add Assignment:")
		
		self.separator = Frame(self.right_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

		self.entry_1_label = Label(self.right_frame, text="Class ")
		self.entry_1_label.pack(anchor=W)
		self.entry_1 = Entry(self.right_frame)
		self.entry_1.pack()

		self.entry_2_label = Label(self.right_frame, text="Assignment: ")
		self.entry_2_label.pack(anchor=W)
		self.entry_2 = Entry(self.right_frame)
		self.entry_2.pack()

		self.button_1 = Button(self.right_frame, text="Add Asignment", command=self.add_new_assignment)
		self.button_1.pack()

		self.button_clear_assignments = Button(self.right_frame, text="Clear Planner", command=self.clear_assignments)
		self.button_clear_assignments.pack()

		self.separator = Frame(self.right_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

	def clear_assignments(self):
		global assignment_objs_list
		for obj in assignment_objs_list:
			obj.delete_assignment()

		global assignments_list
		assignments_list = []
		self.commit_assignments_to_memory()

	def add_new_assignment(self):
		if self.entry_1.get() != "":
			global assignments_list

			# adds assignment to assignments_list
			assignments_list.append(self.entry_1.get().replace(',', '') + "," + self.entry_2.get().replace(',', '') + "," + "completed=false" + "," + "deleted=false")

			# creates new assignment object which displays assignment
			index_num = len(assignments_list) - 1
			self.assignment_label = Assignments(self.master, self.entry_1.get(), self.entry_2.get(), index_num)

			self.commit_assignments_to_memory()
			# resets entry text
			self.set_entry_text("", "")

	def set_entry_text(self, text, text2):
		self.entry_1.delete(0, END)
		self.entry_1.insert(0, text)
		self.entry_2.delete(0, END)
		self.entry_2.insert(0, text2)

class TitleLabel:
	def __init__(self, master, frame, label_name):
		self.frame = frame
		self.title_label = Label(self.frame, text=label_name)
		self.title_label.pack(anchor=W)
		self.label_font = ('Helvetica', 20, 'bold')
		self.title_label.config(font=self.label_font)

class Assignments:
	def __init__(self, master, assignment_class, assignment_description, index_num):
		self.master = master
		self.assignment_class = assignment_class
		self.assignment_description = assignment_description

		self.label_1 = Label(PlannerApp.scroll_frame, text=self.assignment_class, font='Helvetica 13 bold')
		self.label_1.pack(anchor=W)

		self.label_2 = Label(PlannerApp.scroll_frame, text="   " + self.assignment_description)
		self.label_2.pack(anchor=W)

		self.index_num = index_num

		# creates frame for two buttons
		self.button_frame = Frame(PlannerApp.scroll_frame)
		self.button_frame.pack()

		self.x_mark_photo = PhotoImage(file = r"redxmark.gif")
		self.delete_assignment_button = Button(self.button_frame, command=self.delete_assignment, image=self.x_mark_photo, height=20, width=20)
		self.delete_assignment_button.pack(side=LEFT)

		self.check_mark_photo = PhotoImage(file = r"greencheckmark.gif")
		self.complete_assignment_button = Button(self.button_frame, command=self.complete_assignment, image=self.check_mark_photo, height=20, width=20)
		self.complete_assignment_button.pack(side=RIGHT)

		self.separator = Frame(PlannerApp.scroll_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(side=TOP, anchor=N, fill=X, padx=5, pady=5)

		#adds new assignment obj to list_of_assignment_objs
		global assignment_objs_list
		assignment_objs_list.append(self)

		fix()

	def delete_assignment(self):
		self.label_1.pack_forget()
		self.label_2.pack_forget()
		self.delete_assignment_button.pack_forget()
		self.complete_assignment_button.pack_forget()
		self.button_frame.pack_forget()
		self.separator.pack_forget()

		# 'delete' assignment from memory
		split_array = re.split(r"\,", assignments_list[self.index_num]) #removes ',' and splits
		split_array[3] = "deleted=true"

		assignments_list[self.index_num] = split_array[0] + "," + split_array[1] + "," + split_array[2] + "," + split_array[3]

		PlannerApp.commit_assignments_to_memory()


	def complete_assignment(self):
		# removes assignment from left_frame
		self.label_1.pack_forget()
		self.label_2.pack_forget()
		self.delete_assignment_button.pack_forget()
		self.complete_assignment_button.pack_forget()
		self.button_frame.pack_forget()
		self.separator.pack_forget()

		self.completed_assignment_label = CompletedAssignments(self.master, self.assignment_class, self.assignment_description, self.index_num)

		# complete assignment and apply to memory
		split_array = re.split(r"\,", assignments_list[self.index_num]) #removes ',' and splits
		split_array[2] = "completed=true"

		assignments_list[self.index_num] = split_array[0] + "," + split_array[1] + "," + split_array[2] + "," + split_array[3]

		PlannerApp.commit_assignments_to_memory()

class CompletedAssignments:
	def __init__(self, master, assignment_class, assignment_description, index_num):
		self.master = master
		self.assignment_class = assignment_class
		self.assignment_description = assignment_description

		self.label_1 = Label(PlannerApp.center_scroll_frame, text=self.assignment_class, font='Helvetica 13 bold')
		self.label_1.pack(anchor=W)

		self.label_2 = Label(PlannerApp.center_scroll_frame, text="   " + self.assignment_description)
		self.label_2.pack(anchor=W)

		self.index_num = index_num

		self.separator = Frame(PlannerApp.center_scroll_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

		#adds new assignment obj to list_of_assignment_objs
		global assignment_objs_list
		assignment_objs_list.append(self)

	def delete_assignment(self):
		self.label_1.pack_forget()
		self.label_2.pack_forget()
		self.separator.pack_forget()
		PlannerApp.commit_assignments_to_memory()

def fast_fix():
	a = root.winfo_geometry().split('+')[0]
	b = a.split('x')
	w = int(b[0])
	h = int(b[1])
	root.geometry('%dx%d' % (w+1,h+1))

def fix():
	root.update()
	root.after(0, fast_fix)

root = Tk()
PlannerApp = Planner(root)
PlannerApp.load_assignments_from_memory()
fix()
root.mainloop()


# How to create executable with pyinstaller:

# type: pyinstaller --onefile --windowed --noconsole PlannerGUI.py
# then type: pyinstaller --add-data 'assignments.txt:.' PlannerGUI.py



