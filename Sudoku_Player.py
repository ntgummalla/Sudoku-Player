import pygame # for computer graphics and sound libraries used in Python
import requests # to make requests to API


WIDTH = 550
background_color = (251,247,245)
original_grid_elem_color = (52, 31, 151)
buffer = 5 # to ensure the boundary line is noot disappeared when we super-impose the bckgrnd color on the text.

# API call:
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
grid = response.json()['board'] # board is the parameter being searched inside json response. Now we have the board in the grid.
# since we're manipulating the 'grid' var, we created another var to store the original grid
# so that it doesn't get modified everytime we manuplate our grid.
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))] 

def insert(win, position): # ('window' in which we are drawing, 'position' of the block)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    i,j = position[1], position[0] # as there will be an iversion of values when updating them int he database.

    while True:
        for event in pygame.event.get(): # to check for an event in pygame window
            if event.type == pygame.QUIT: # if the user is quiting the game
                return
            if event.type == pygame.KEYDOWN: # if the user is clicking a box.
                if(grid_original[i-1][j-1] != 0): #  if the original_grid_elem is not empty, so blank elems are denoted by 0
                    return
                if(event.key == 48): # if the field is being untuched touched it's associate with 0 (0 is indicated by 48 in ASCII)
                    grid[i-1][j-1] = event.key - 48 # to update the value/assign the value
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    # to make the field blank (we're super-imposing the bckgrnd color on the text to make it blank)
                    pygame.display.update()
                    return
                if(0 < event.key - 48 <10): # checking for a valid input
                    pygame.draw.rect(win, background_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0)) # (0,0,0) is the color black as the text is black
                    win.blit(value, (position[0]*50 +15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return

def main():    
    pygame.init() #intialising pygame
    win = pygame.display.set_mode((WIDTH, WIDTH)) #creating a window
    pygame.display.set_caption("Sudoku")
    win.fill(background_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)

    for i in range(0,10): # as a sudoku grid is a 9*9 grid so we need 10 vertical and horizontal lines
         # vertical line: 1st parameter is colour, 2nd is starting point(the x-coordinate for each line is at a distance of 
         # 50 units from the previous line and the y-coordinate 50 is the starting point for a specific line), 
         # 3rd is end co-ordinate(the y-coordinate here is the ending point for that specific line), 4th is the width of the line

        if(i%3 == 0): # as the grid contains some bold lines to indicate the partitions(boxes). We increase the width to 4 to make them bold.
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i ,500 ), 4 )
            pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 4 )

        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2)
        pygame.draw.line(win, (0,0,0), (50, 50 + 50*i), (500, 50 + 50*i), 2) # horizontal line
    pygame.display.update()

    # to populate the grid:
    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_elem_color) # we first render the text we want to add.
                win.blit(value, ((j+1)*50 + 15, (i+1)*50 )) # now we add the text to the screen using 'blit' func.
                # the 2nd parameter is where we are blitting the value. Here '15' is the off-set for x-coordinate.
    pygame.display.update()
        
    while True: 
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1: # event.button == 1 indicates left click
                pos = pygame.mouse.get_pos() # to get the position of the mouse
                insert(win, (pos[0]//50, pos[1]//50)) # we divide 'pos' by 50 to get the grid number(index) instead of getting the position.
            if event.type == pygame.QUIT: #if we press the 'QUIT' button, the window quits.
                pygame.quit()
                return
   
main()

