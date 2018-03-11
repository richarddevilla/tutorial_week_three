from bronze import *
import time
from tkinter import StringVar, Tk, Toplevel, ttk
from tkinter import messagebox as msg

def createWindow():
    main_window = Tk()
    main_window.title('Contact List')
    search_button = ttk.Button(main_window,
                               command=create_search_win,
                               text='Search Contact List')
    search_button.pack()
    return main_window


def create_search_win():
    search_window = Toplevel(main_window)
    search_window.grab_set()
    search_entry = ttk.Entry(search_window,
                             textvariable=search_var)
    search_entry.pack()
    search_button = ttk.Button(search_window,
                               text='Search',
                               command=lambda:create_search_result())
    search_button.pack()

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

if __name__ == '__main__':
    main_window = createWindow()
    search_var = StringVar(value='')
    main_window.mainloop()