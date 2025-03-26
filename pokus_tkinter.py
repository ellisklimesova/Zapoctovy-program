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
import random

class Game: #self.dim_x, self.dim_y stored here
    def __init__(self, file_name=None):
        if file_name is not None:
            pole = self.load_file(file_name)
        else: 
            pole = self.default_array()
        self.history_of_sweeps = [pole] # save into history the initial setting

    def print_sweep(self, number=0):
        for row in self.get_sweep(number):
            print(*map(lambda x: f"{x: 4}",row),sep="")
            
    def load_file(self, file_name):
        with open(file_name, mode="r") as file:
            lines = file.readlines()
        strange_cells = [] # cells that are not "value=5" at t=0 (coordinate_x, coordinate_y, value)
        for line in lines:
            if ":" in line:
                key, value = line.split(":")
                if "dimensions" in key:
                    self.dimensions = list(map(int, value.split()))
                if "square" in key:
                    self.size_square = int(value)
            else:
                strange_cells.append(list(map(int, line.split())))
        array = list(list(5 for dim_y in range(self.dimensions[1])) 
                     for dim_x in range(self.dimensions[0]))

        for x, y, value in strange_cells: # rewrite initially "5" cells to initially non-5 values
            array[x][y] = value

        return array

    # TODO: Is this alright? Added 21.3.25
    def default_array(self, dim_x=20, dim_y=20):
        array = list(list(5 for dim_y in range(dim_y) 
                    for dim_x in range(dim_x)))
        array[0][0] = -5
        array[-1][-1] = -5
        
    def return_dimensions(self):
        self.dim_x = len(self.history_of_sweeps[0])
        self.dim_y = len(self.history_of_sweeps[0][0])

        return self.dim_x, self.dim_y

    """
    -- dimensions (2 numbers)
    -- intially, every cell is green, i.e. valued 5, unless stated otherwise
    -- list of cells that are not 5: 
        -- coordinates (2 numbers) + value (1 number)
    """
    def evolve_cell_value(self, array, x, y):
        # returns new value of the cells due to its neighbors
        actual_value = array[x][y]
        # differences = [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]
        neighbors = []
        for diff_x in range(-1,2):
            for diff_y in range(-1,2):
                if (diff_x == diff_y == 0):
                    continue
                neighbor_x = x + diff_x
                neighbor_y = y + diff_y

                if (0 <= neighbor_y < len(array[0])) and (0 <= neighbor_x < len(array)): 
                    neighbors.append(array[neighbor_x][neighbor_y])    # write it into neighbors
                    
        return self.apply_rules_on_cell(neighbors, actual_value)

    def apply_rules_on_cell(self, neighbors_values, actual_value)->int: # returns value   
        
        # A) BLACK (carbonized) cell remains black for 5 sweeps. 
        #    values of black cell: 100, 101, 102, 103, 104, 105 --> assign value 1
        if actual_value >= 100:
            actual_value += 1
            if actual_value == 105: # after the fifth sweep it becomes greenish
                return 1
            else: 
                return actual_value

        # B) GREEN cell not in fire = [1,2,3,4,5] 
        if actual_value > 0:
            # 1. No neighbors on fire
            # is_in_range = []
            # for value in neighbors_values:
            #     if value >= 0: # neighboring black cells (100,..,104) do not set the green cell on fire
            #         is_in_range.append(True)
            #     else:
            #         is_in_range.append(False)
            # if all(is_in_range): 
            #     actual_value += 1 # regenerate slowly
            #     return actual_value
            
            # 2. Some neighbors on fire
            negative_neighbors = []
            for value in neighbors_values:
                if value < 0:
                    negative_neighbors.append(value)

            # The cell is set on fire, if enough fire around it
            # This condition also takes into account that a greener cell is set on fire more easily
            # while less green cell needs more fire around it.
            if sum(negative_neighbors) <= actual_value - 6:
                return -5   # kazda zacne horet hodne
            return min(actual_value + 1, 5) # 5 doesn't regenerate anymore

        # C) RED cells on fire = [-5,-4,-3,-2,-1]
        if actual_value < 0:
            # cell on fire always gets better, no matter the neighbors
            actual_value += 1
            if actual_value == 0:
                return 100 # start the 1st of 5 regenerating cycles
            return actual_value 

    def perform_one_sweep(self, array):  
        new_array = list(list(None for dim_y in range(len(array[0]))) 
                     for dim_x in range(len(array)))

        for x in range(len(array)):
            for y in range(len(array[x])):
                new_value = self.evolve_cell_value(array, x, y)
                new_array[x][y] = new_value
        
        return new_array

    def get_sweep(self, number=0): # returns sweep of the given number
        while number >= len(self.history_of_sweeps):
            a = self.perform_one_sweep(self.history_of_sweeps[-1])
            self.history_of_sweeps.append(a)

        return self.history_of_sweeps[number]
    



class Program(): # Tk()
    def __init__(self, file_name):
        self.root = Tk()
        self.game = Game(file_name) # TODO: je TOTO SPRAVNE????
        self.set_window()
        self.frame_number = 0
        if file_name is not None:
            self.dim_x, self.dim_y = self.load_dimensions(file_name)
            self.size_square = self.load_size_square(file_name)
        else:
            self.dim_x, self.dim_y = 10, 15
            self.size_square = 5
        self.height_canv, self.width_canv = self.dim_x * self.size_square, self.dim_y * self.size_square
        self.set_field() # must be performed after setting self.height_canv, self.width_canv
        self.display_sweep()

        self.root.mainloop()

    def load_size_square(self, file_name):

        with open(file_name, mode="r") as file:
            lines = file.readlines()

        for line in lines:
            if ":" in line:
                key, value = line.split(":")
                if "square" in key:
                    self.size_square = int(value)

        return self.size_square
    
    def load_dimensions(self, file_name):
        
        with open(file_name, mode="r") as file:
            lines = file.readlines()
        
        for line in lines:
            if ":" in line:
                key, value = line.split(":")
                if "dimensions" in key:
                    self.dimensions = list(map(int, value.split()))

        return self.dimensions

    def set_window(self):
        # setting the windows size
        self.root.geometry("1100x750")
        Label(self.root, text='NO STRESS NO PROBLEM').pack()
        # button STOP
        self.root.title('Run until I stop you.')
        Button(self.root, text='Stop', 
                        width=20, command=self.root.destroy).pack(side=BOTTOM)

        # creating a label for name using widget Label
        name_label = Label(self.root, text = 'Frame number', font=('calibre',10, 'bold'))
        name_label.pack()

        # creating a entry for input using widget Entry
        self.num_entry = Entry(self.root, font=('calibre',10,'normal'))
        self.num_entry.pack()
        self.num_entry.bind("<KeyRelease>", self.submit_frame_number)

        subframe = Frame(self.root)
        subframe.pack(  )

        # simple slider - it will change speed of the evolution
        s = Scale(subframe, from_=0, to=10, orient=HORIZONTAL).pack( side = RIGHT )
        # button that increases the number       
        Button(subframe, text = '+1', command = self.increase_frame_number).pack(side=LEFT)
        Button(subframe, text = '-1', command = lambda: self.increase_frame_number(False)).pack(side=LEFT)

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
        if int(number_str) + 1 == number:
            print(f"Increased by 1: {number}")
        else:
            print(f"Decreased by 1: {number}")
        
    def set_field(self):
        # creating canvas
        # TODO: check whether any initial elements in "initial.txt" are beyond the boundary? 
        self.c = Canvas(self.root, bg="gray", width=self.width_canv, height=self.height_canv)
        self.c.pack()

        """ Colors see here: https://cs111.wellesley.edu/archive/cs111_fall14/public_html/labs/lab12/tkintercolor.html """
        color = {-5: "red4",
            -4: "red3",
            -3: "red2",
            -2: "darkorange",
            -1: "orange",
            100: "black",
            101: "black",
            102: "black",
            103: "black",
            104: "black",
            0: "black",
            1: "DarkOliveGreen1",
            2: "DarkOliveGreen2",
            3: "DarkOliveGreen3",
            4: "chartreuse3",
            5: "green"} 
        rect1 = Square(1,1 , color[-5],  self.size_square).draw(self.c)
        rect2 = Square(1,5 , color[-4],  self.size_square).draw(self.c)
        rect3 = Square(2,3 , color[-3],  self.size_square).draw(self.c)
        rect4 = Square(0,3 , color[-2],  self.size_square).draw(self.c)
        rect5 = Square(0,3 , color[-1],  self.size_square).draw(self.c)
        rect5 = Square(0,2 , color[100], self.size_square).draw(self.c)
        rect6 = Square(0,4 , color[1],  self.size_square).draw(self.c)
        rect7 = Square(2,5 , color[2],  self.size_square).draw(self.c)
        rect8 = Square(1,2 , color[3],  self.size_square).draw(self.c)
        rect9 = Square(4,4 , color[4],  self.size_square).draw(self.c)
        rect10 = Square(3,5 , color[5],  self.size_square).draw(self.c)

    def nahodna_barva(self):
        return f"#{random.randint(0, 0xFFFFFF):06x}"

    def display_sweep(self, sweep_number=0):  # will show the new canvas
        color = {-5: "red4",
            -4: "red3",
            -3: "red2",
            -2: "darkorange",
            -1: "orange",
            100: "black",
            101: "black",
            102: "black",
            103: "black",
            104: "black",
            0: "black",
            1: "DarkOliveGreen1",
            2: "DarkOliveGreen2",
            3: "DarkOliveGreen3",
            4: "chartreuse3",
            5: "green"} 
        actual_sweep = self.game.get_sweep()
        dim_x, dim_y = self.dim_x, self.dim_y
        for x in range(dim_x): 
            for y in range(dim_y):
                x1 = x * self.size_square 
                y1 = y * self.size_square
                x2 = x1 + self.size_square
                y2 = y1 + self.size_square
                actual_color = color[actual_sweep[x][y]]
                Square(x,y,color=actual_color,size_square=self.size_square).draw(self.c)
                # barva = self.nahodna_barva()
                # self.c.create_rectangle(x1, y1, x2, y2, fill=barva, outline="black")
        
class Square(): 
    
    def __init__(self, field_coord_x, field_coord_y, color, size_square):
        self.field_coord_x, self.field_coord_y = field_coord_x, field_coord_y
        self.color = color
        self.coord_x1 = ( field_coord_x ) * size_square 
        self.coord_y1 = ( field_coord_y ) * size_square 
        self.coord_x2 = self.coord_x1  + size_square
        self.coord_y2 = self.coord_y1  + size_square
        self.coords = [self.coord_x1, self.coord_y1, self.coord_x2, self.coord_y2]

    def draw(self, canvas):
        # coordinates of the square are two numbers (position of value of the cell in the field).
        canvas.create_rectangle(*self.coords, fill=self.color)
        canvas_width  = int(canvas.__getitem__('width'))
        canvas_height = int(canvas.__getitem__('height'))           
        

if __name__ == "__main__":
    # g = Game("initial.txt")
    p = Program("initial.txt")


    # print(g.get_sweep(10))
    # for i in range(15):
    #     g.print_sweep(i)
    #     print("--------------")




