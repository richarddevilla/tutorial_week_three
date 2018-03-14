from bronze import *
import mysqltest
import time
from tkinter import StringVar, Tk, Toplevel, ttk
from tkinter import messagebox as msg

def createWindow():
    main_window = Tk()
    main_window.geometry("300x300")
    main_window.title('Contact List')
    return main_window

def create_search_win():
    search_frame = ttk.LabelFrame(main_window)
    search_entry = ttk.Entry(search_frame,
                             textvariable=search_var)
    search_entry.pack()
    search_button = ttk.Button(search_frame,
                               text='Search SQLite3',
                               command=lambda:create_search_result())
    mysqlsearch_button = ttk.Button(search_frame,
                               text='Search MySQL',
                               command=lambda: create_mysqlsearch_result())
    search_button.pack()
    mysqlsearch_button.pack()
    search_frame.pack(fill="none", expand=True)

def create_search_result():
    search_result_window = Toplevel(main_window)
    search_result_window.grab_set()
    search_result = ttk.Treeview(search_result_window,
                                 columns=['Name',
                                          'Mobile #',
                                          'Phone #',
                                          'Date of Birth',
                                          'Address']
                                )
    search_result.heading('Name',text='Name')
    search_result.heading('Mobile #', text='Mobile #')
    search_result.heading('Phone #', text='Phone #')
    search_result.heading('Date of Birth', text='Date of Birth')
    search_result.heading('Address', text='Address')
    search_result['show']= 'headings'
    search_result.pack()
    start_search = time.clock()
    result = search_data(search_var.get())
    end_search = time.clock()-start_search
    for each in result:
        search_result.insert('','end',values=each)
    msg.showinfo('Search Complete','Total time to search DataBase is {} seconds'.format(end_search))
    search_result.bind("<Double-1>", lambda e:on_click())

    def on_click():
        profile_window = Toplevel(search_result_window)
        profile_window.grab_set()
        profile_frame = ttk.LabelFrame(profile_window)
        profile_frame.pack()
        profile_selected = search_result.item(search_result.focus())
        widget=0
        label_counter = 0
        label={}
        profile_labels = ['Name',
                   'Mobile #',
                   'Phone #',
                   'Date of Birth',
                   'Address']
        for each in profile_selected['values']:
            label[widget]=ttk.Label(
                profile_frame,
                text=each)
            label[widget].grid(column=1,row=widget,sticky='W')
            label[label_counter] = ttk.Label(
                profile_frame,
                text=profile_labels[label_counter]+': ')
            label[label_counter].grid(column=0, row=label_counter,sticky='E')
            widget+=1
            label_counter+=1

def create_mysqlsearch_result():
    search_result_window = Toplevel(main_window)
    search_result_window.grab_set()
    search_result = ttk.Treeview(search_result_window,
                                 columns=['Name',
                                          'Mobile #',
                                          'Phone #',
                                          'Date of Birth',
                                          'Address']
                                )
    search_result.heading('Name',text='Name')
    search_result.heading('Mobile #', text='Mobile #')
    search_result.heading('Phone #', text='Phone #')
    search_result.heading('Date of Birth', text='Date of Birth')
    search_result.heading('Address', text='Address')
    search_result['show']= 'headings'
    search_result.pack()
    start_search = time.clock()
    result = mysqltest.mysqlsearch_data(search_var.get())
    end_search = time.clock()-start_search
    for each in result:
        search_result.insert('','end',values=each)
    msg.showinfo('Search Complete','Total time to search DataBase is {} seconds'.format(end_search))
    search_result.bind("<Double-1>", lambda e: on_click())

    def on_click():
        profile_window = Toplevel(search_result_window)
        profile_window.grab_set()
        profile_frame = ttk.LabelFrame(profile_window)
        profile_frame.pack()
        profile_selected = search_result.item(search_result.focus())
        widget=0
        label_counter = 0
        label={}
        profile_labels = ['Name',
                   'Mobile #',
                   'Phone #',
                   'Date of Birth',
                   'Address']
        for each in profile_selected['values']:
            label[widget]=ttk.Label(
                profile_frame,
                text=each)
            label[widget].grid(column=1,row=widget,sticky='W')
            label[label_counter] = ttk.Label(
                profile_frame,
                text=profile_labels[label_counter]+': ')
            label[label_counter].grid(column=0, row=label_counter,sticky='E')
            widget+=1
            label_counter+=1


if __name__ == '__main__':
    main_window = createWindow()
    search_var = StringVar(value='')
    create_search_win()
    main_window.mainloop()