#! /usr/bin/python2.6

''' 
My attempt at creating an implementation of Conway's Game of Life in
python. This file constitutes the cell and grid classes for the game.
'''

class Cell:
    '''
    basic instance of a cell. Basically, it is either dead or alive, 
    and has no other characteristics.
    '''
    
    def __init__(self, al = False):
        self.alive = al
    
class Grid:
    
    def __init__(self, dims, start_grid = {}):
        '''
        Gets passed in a tuple of x and y dimensions. Makes a dictionary
        with coordinates as keys and each individual cell as the value
        '''
        
        self._grid = start_grid.copy()
        self._newgrid = {}
        self._width = dims[0]
        self._height = dims[1]
        
        for x in range(self._width):
            for y in range(self._height):
                #use for side effect of populating the grid
                self._grid.setdefault((x,y), Cell())
                
                
    def step(self):
        ''' 
        Applies Conway's Game of life rules in order to calculate
        what the grid will look like at the next time step. 
        
        Side Effects: updates the _grid, and clears the _newgrid
        
        TODO: look into using a more efficient algorithm for calculating the 
        next state of the board
        '''
        
        updated = {}
        for x in range(self._width):
            for y in range(self._height):
            
                current_pos = (x,y)
                current_cell = self._grid[current_pos] 
                new_cell = self._newgrid.setdefault(current_pos,Cell())
                neighbors = self.__neighbor_count(current_pos)
                
                #The next bit is marks whether the current cell will change
                #state in the next time step
                
                mark_to_die = True if (neighbors > 3 or neighbors < 2) and \
                              current_cell.alive else False
                                
                mark_to_live = True if neighbors == 3 and not \
                               current_cell.alive else False
                               
                #apply the actual logic now.
                if mark_to_die:
                    self.kill(new_cell)
                    updated[x,y] = Cell()
                    
                elif mark_to_live:
                    self.live(new_cell)
                    updated[x,y] = Cell(True)
                    
                else:
                    self._newgrid.setdefault(current_pos, Cell()).alive = \
                    self._grid[current_pos].alive
        
        #have to copy because python passes by refs
        self._grid = self._newgrid.copy()
        self._newgrid = {}
        return updated
                           
    def __neighbor_count(self, cell_loc):
        '''
        Calculates the number of living neighbors of any cell.
        
        
        returns int
        '''
    
        x = cell_loc[0]
        y = cell_loc[1]
        #The next logic block ensures that the grid will
        #behave as if it were toroidal
        inc_x  = x + 1 if x + 1 < self._width else 0
        inc_y = y + 1 if y + 1 < self._height else 0
        dec_x = x - 1 if x - 1  >= 0 else self._width - 1
        dec_y = y - 1 if y - 1  >= 0 else self._height - 1
        
        #Next, taking advantage of the fact the True evaluates as 1 and False
        #evals as 0, return how many living neighbors a cell has.
        
        return self._grid[x, dec_y].alive + \
               self._grid[x, inc_y].alive + \
               self._grid[dec_x, y].alive + \
               self._grid[inc_x, y].alive + \
               self._grid[inc_x, inc_y].alive + \
               self._grid[dec_x, dec_y].alive + \
               self._grid[dec_x, inc_y].alive + \
               self._grid[inc_x, dec_y].alive
                
    def live(self, cell):
        cell.alive = True
        
    def kill(self, cell):
        cell.alive = False
        
    def __str__(self):
        '''
        included for debugging purposes. returns a visual representation
        of the grid, with 0's and 1' representing dead and live cells, 
        respectively.
        '''
    
        width = self._width
        height = self._height
        cols = range(width)
        rows = range(height)
        
        #list comp is a bit hard to read but I really hate that I've
        #already used two double-nested loops
        prt = ["%d " % (self._grid[x,y].alive) for y in rows for x in cols]
        [prt.insert(i, "\n") for i in range(len(prt)) if i % (width+1) == 0]
        
        return "".join(prt)
        
    

if __name__ == "__main__":
    g = Grid((32, 64))
    g.live((11,24))
    
    print g._grid[11,24].alive
    g.kill((11,24))
    print g._grid[12,24].alive
