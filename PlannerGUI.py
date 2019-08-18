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

	def load_item_list(self):
		with open("shoplist.txt","r+") as file:
			content = file.readlines()
			# you may also want to remove whitespace characters like `\n` at the end of each line
			content = [x.strip() for x in content]

	def save_item_list(self):
		with open("shoplist.txt","a+") as file:
			for x in content:
				file.write(x + "\n")

	def create_left_frame(self):
		# loads all stored assignments

		self.left_frame = Frame(self.master)
		self.left_frame.pack(side=LEFT, anchor=N, padx=50, pady=30)
		self.left_frame['borderwidth'] = 2

		self.assignment_label = TitleLabel(self.master, self.left_frame, "Assignments:")
		
		self.separator = Frame(self.left_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

	def create_center_frame(self):
		self.center_frame = Frame(self.master)
		self.center_frame.pack(side=LEFT, anchor=N, padx=50, pady=30)
		self.center_frame['borderwidth'] = 2

		self.completed_title_label = TitleLabel(self.master, self.center_frame, "Completed:")

		self.separator = Frame(self.center_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

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
		self.label_font = ('times', 20, 'bold')
		self.title_label.config(font=self.label_font)

class Assignments:
	def __init__(self, master, assignment_class, assignment_description, index_num):
		self.master = master
		self.assignment_class = assignment_class
		self.assignment_description = assignment_description

		self.label_1 = Label(PlannerApp.left_frame, text=self.assignment_class, font='Helvetica 13 bold')
		self.label_1.pack(anchor=W)

		self.label_2 = Label(PlannerApp.left_frame, text="   " + self.assignment_description)
		self.label_2.pack(anchor=W)

		self.index_num = index_num

		self.delete_assignment_button = Button(PlannerApp.left_frame, text="Delete", command=self.delete_assignment)
		self.delete_assignment_button.pack()

		self.complete_assignment_button = Button(PlannerApp.left_frame, text="Complete", command=self.complete_assignment)
		self.complete_assignment_button.pack()

		self.separator = Frame(PlannerApp.left_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(anchor=W, fill=X, padx=5, pady=5)

		#adds new assignment obj to list_of_assignment_objs
		global assignment_objs_list
		assignment_objs_list.append(self)

		fix()

	def delete_assignment(self):
		self.label_1.pack_forget()
		self.label_2.pack_forget()
		self.delete_assignment_button.pack_forget()
		self.complete_assignment_button.pack_forget()
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

		self.label_1 = Label(PlannerApp.center_frame, text=self.assignment_class, font='Helvetica 13 bold')
		self.label_1.pack(anchor=W)

		self.label_2 = Label(PlannerApp.center_frame, text="   " + self.assignment_description)
		self.label_2.pack(anchor=W)

		self.index_num = index_num

		self.separator = Frame(PlannerApp.center_frame, width=200, height=2, bd=1, relief=SUNKEN)
		self.separator.pack(fill=X, padx=5, pady=5)

	def delete_assignment(self):
		self.label_1.pack_forget()
		self.label_2.pack_forget()
		self.delete_assignment_button.pack_forget()
		self.complete_assignment_button.pack_forget()
		self.separator.pack_forget()

		# 'delete' assignment from memory
		split_array = re.split(r"\,", assignments_list[self.index_num]) #removes ',' and splits
		split_array[3] = "deleted=true"

		assignments_list[self.index_num] = split_array[0] + "," + split_array[1] + "," + split_array[2] + "," + split_array[3]

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



