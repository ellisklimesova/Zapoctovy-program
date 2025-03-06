"""
Keywords

-- slider (potahovatko)
-- timer - spousti eventy 
"""
"""
On macos apriori one cannot change the buttom color.
Hence one shall use "Button" function from tkmacosx instead.  
Usage and instalation: https://pypi.org/project/tkmacosx/
"""

from tkinter import *

class Program:
    def __init__(self):
        self.root = Tk()
        self.set_window()
        self.frame_number = 0
        self.root.mainloop()

    def set_window(self):
        # setting the windows size
        self.root.geometry("600x400")

        # widgets
        Label(self.root, text='Interesting text').pack()
        # zmena
        # button STOP
        self.root.title('Run until I stop you.')
        Button(self.root, text='Stop', 
                        width=20, command=self.root.destroy).pack(side=BOTTOM)


        # creating a label for name using widget Label
        name_label = Label(self.root, text = 'Frame number', font=('calibre',10, 'bold'))
        name_label.pack()

        # creating a entry for input name using widget Entry
        # self.frame_number = IntVar()
        self.num_entry = Entry(self.root, font=('calibre',10,'normal'))
        self.num_entry.pack()
        self.num_entry.bind("<KeyRelease>", self.submit_frame_number)

        subframe = Frame().pack()
        # button that increases the number
        Button(subframe, text = '+1', command = self.increase_frame_number).pack(side=LEFT)
        Button(subframe, text = '-1', command = lambda: self.increase_frame_number(False)).pack(side=LEFT)

        # creating canvas
        c = Canvas(self.root, bg="gray", height=500, width=500)
        coor = 0,50,100,150
        arc = c.create_arc(coor, start=0, extent=100, fill="red")
        c.pack()

        # simple slider 
        s = Scale(self.root, from_=0, to=42)
        s.pack()
        # s = Scale(root, from_=0, to=200, orient=HORIZONTAL)
        # s.pack()


    def submit_frame_number(self, event=None): # on this level it has to have self

        number_str = self.num_entry.get()
        if number_str.isnumeric():                           
            number = int(number_str)       # No need to save (no self. ), as not used elsewhere                              
        else:     
            number = self.frame_number
            
        print(f"Number of frame: {number}")
        self.num_entry.delete(0,len(self.num_entry.get()))
        self.num_entry.insert(0, number)
        self.frame_number = number 

    def increase_frame_number(self, sign=True):
        number_str = self.num_entry.get()
        if number_str.isnumeric():                           
            number = int(number_str)            
        else:     
            number = self.frame_number
        number += 1 if sign else -1  
            
        self.num_entry.delete(0,len(self.num_entry.get()))
        self.num_entry.insert(0, number)
        self.frame_number = number 
        print(f"Increased by 1: {number}")

        # self.display_frame()  # will show the new canvas

if __name__ == "__main__":
    p = Program()
