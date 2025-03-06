"""
Keywords
-- zavrit do class all of the below
-- canvas
-- slider (potahovatko)
-- policko s tlacitky doleva doprava
    - kdyz cislo ok, kdyz necislo tak ignoruj
    - doprava zvetsi o 1, doleva zmensi o 1, spravne cislo zobraz v policku
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
        name_label = Label(self.root, text = 'Username', font=('calibre',10, 'bold'))
        name_label.pack()

        # creating a entry for input name using widget Entry
        self.frame_number = IntVar()
        name_entry = Entry(self.root, textvariable = self.frame_number, font=('calibre',10,'normal'))
        name_entry.pack()

        # creating a button using the widget Button that will call the submit function 
        sub_btn = Button(self.root, text = 'Submit', command = self.submit_frame_number) 
        sub_btn.pack()

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

        # function that will get the name and print it on the screen
    def submit_frame_number(self): # on this level it has to have self

        number = self.frame_number.get()
        print(f"Frame is : {number}")
        self.frame_number.set(number)

if __name__ == "__main__":
    p = Program()
