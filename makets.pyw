#!/usr/bin/python3
import os
import shutil
import pathlib
from tkinter import *
from tkinter import messagebox
import configparser

"""
Копирование файлов из локальной временной директории (диск Х:) на сервер
(диск N:). Три файла: сам скрип makets.py и файлов, констант makets.ini и
иконка maket.ico
"""

configfile = 'maket.ini'
parser = configparser.ConfigParser()
parser.read(configfile)

PATH_X = pathlib.Path(parser['Pathes']['path_x'])
PATH_N = pathlib.Path(parser['Pathes']['path_n'])

def create_dirs():
	dirs = {}
	cdrs = pathlib.Path('CDRS') / parser['Num']['year'] / parser['Num']['numer']
	web = pathlib.Path('web') / parser['Num']['year']
	for i in parser['Dirs']:
		if i == 'web':
			dirs[i] = web
		else:
			dirs[i] = cdrs / i
	return dirs

DIRS = create_dirs()

def save_dirs():
	year = e_year.get()
	numer = e_num.get()
	parser.set('Num', 'year', year)
	parser.set('Num', 'numer', numer)
	
	with open(configfile, 'w') as f:
			parser.write(f)
	DIRS = create_dirs()
	messagebox.showinfo("Данные устарели", "Перезапустите скрипт")

	
class makets:
	dir_path = DIRS['_others']
		
	def open(self, disk, path='', file_name=''):
		self.path = pathlib.Path(path)
		self.file_name = pathlib.Path(file_name)
		try:
			os.startfile(disk / self.path / self.file_name)
		except FileNotFoundError:
			messagebox.showerror("ОШИБКА", "Не найден путь")

	def copy_fl(self, file_names):
		self.fl = pathlib.Path(file_names)
		pathlib.Path(PATH_N / self.dir_path).mkdir(parents=True, exist_ok=True)
		if not pathlib.Path.exists( PATH_N / self.dir_path / self.fl):
			shutil.copy(PATH_X / self.fl, PATH_N / self.dir_path / self.fl)
		else:
			messagebox.showerror("ОШИБКА", f"Файл {self.fl} существует")
		
	def clean_x(self):
		file_names = self.spisok(PATH_X)
		for fl in file_names:
			self.fl = pathlib.Path(fl)
			try:
				os.remove(PATH_X / self.fl)
			except PermissionError:
				messagebox.showerror("ОШИБКА", f"Файл {self.fl} блокирован")
		lbox_x.delete(0, END)
	
	def spisok(self, path):
		file_names = []
		spisok = os.listdir(path)
		for fl in spisok:
			if pathlib.Path.is_file(path / fl):
				file_names.append(fl)
		return file_names
		
	def __del__(self):
		print('убит')


def add_list(path, lbox, dir_path=''):
	for fl in maket.spisok(path / dir_path):
		lbox.insert(END, fl)

def copy_selected():
	for i in lbox_x.curselection():
		maket.copy_fl(lbox_x.get(i))
	
def copy_path():
	selected =lbox_x.curselection()
	if selected:
		e_path.delete(0, END)
		for i in selected:
			papka = pathlib.Path(maket.dir_path)
			imia = pathlib.Path(lbox_x.get(i))
			e_path.insert(END, '{} '.format(papka / imia))
	else:
		e_path.delete(0, END)
		e_path.insert(0, 'Не выбран файл')
		
def print_path(event):
	print(maket.dir_path)

def select_path(event):
	selected = lbox_dir.curselection()
	try:
		catalog = DIRS[lbox_dir.get(selected)]
	except:
		catalog = maket.dir_path
	maket.dir_path = catalog
	btn_dir['text'] = maket.dir_path
	lbox_n.delete(0, END)
	try:
		add_list(PATH_N, lbox_n, maket.dir_path)
	except FileNotFoundError:
		pass

def ref_x():
	lbox_x.delete(0, END)
	add_list(PATH_X, lbox_x)

maket = makets()

window = Tk()
window.title('Makets')
window.iconbitmap('Maket.ico')
f_top = Frame(window)
e_year = Entry(f_top, width=5)
e_year.insert(0, parser['Num']['year'])
e_year.pack(side=LEFT)

btn_num = Button(f_top, text='Записать номер', command=save_dirs)
btn_num.pack(side=RIGHT)

e_num = Entry(f_top, width=5)
e_num.insert(0, parser['Num']['numer'])
e_num.pack(side=RIGHT)
f_top.pack()

f_mid = LabelFrame(window, text='dirs')
lbox_dir = Listbox(f_mid, width=35, height=4)
lbox_dir.pack(side=RIGHT)
for key in DIRS:
	lbox_dir.insert(END, key)
lbox_dir.select_set(0)
lbox_dir.bind('<<ListboxSelect>>', select_path)
btn_dir = Button(f_mid, text=maket.dir_path, command=lambda:(maket.open(PATH_N, maket.dir_path)))
btn_dir.pack(side=TOP)
e_path = Entry(f_mid, width=40)
e_path.pack(side=LEFT)
btn_path = Button(f_mid, text='Путь файла', command = copy_path)
btn_path.pack(side=LEFT)
f_mid.pack(fill=X)

lbox_x = Listbox(width=35, height=10, selectmode=EXTENDED)
lbox_x.pack(side=LEFT)
add_list(PATH_X, lbox_x)

lbox_n = Listbox(width=35, height=10)
lbox_n.pack(side=RIGHT)

btn_test = Button(text='Обновить Х', command=ref_x)
btn_test.pack()
btn_copy = Button(text='Копировать файлы', command=copy_selected)
btn_copy.pack()
btn_clear = Button(text='Очистить Х:', command=maket.clean_x)
btn_clear.pack(side=BOTTOM)
window.mainloop()
