#backtracking algorithm to solve a sudoku puzzle
import math
from re import X
from tkinter import Y
import numpy as np
import pygame as pg

#define a class for board and square and functions for guessing values and checking validity
class Square:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.v = value
        self.next = None
        self.prev = None
        self.lock = False

    def printSquare(self):
        print(self.x, self.y, self.v)
        return True

class Tile:
    def __init__(self,X, Y, xpos, ypos):
        self.x = X
        self.y = Y
        self.xpos = xpos
        self.ypos = ypos
        

class Board:
    def __init__(self, length=9, width=9):
        self.length = length
        self.width = width
        self.x = []
        self.m = np.zeros((9,9))
        pg.init()
        self.s = pg.display.set_mode((900,900))
        self.WHITE = (255,255,255)
        self.BLACK = (0,0,0)
        self.s.fill(self.WHITE)
        self.font = pg.font.SysFont(None,100)
        #self.img = self.font.render('0',True, self.BLACK)
        #self.s.blit(self.img,(20,20))
        pg.display.update()



    def buildtiles(self):
        for i in range(0,9):
            for j in range(0,9):
                pg.draw.rect(self.s, self.BLACK,(i*100,j*100,100, 100),5)
        pg.display.update()

    def upBoard(self):
        c = ''
        for i in range(0,9):
            for j in range(0,9):
                #clear previous value from cell and replace with new value
                pg.draw.rect(self.s, self.WHITE,(i*100+5,j*100+5,90, 90))
                #determine what c is based upon given matrix x
                c = str(math.trunc(self.m[j][i]))
                mg = self.font.render(c, True, self.BLACK)
                self.s.blit(mg,(i*100 + 30, j*100 + 20))
        pg.display.update()

    def prefill(self, x):
        #where x is a matrix of predetermined values
        #currently uses code filled board, will adjust to replace with user input via GUI
        #utilize linked list structure for simplicity
        for i in range(0,self.length):
            for j in range(0,self.width):
                #print(x[i][j])
                
                self.x.append(Square(j,i,x[i][j]))
                self.m[i][j] = self.x[-1].v
                temp = self.transf(j,i)
                #locking statement
                if self.x[temp].v != 0:
                    self.x[temp].lock = True
                    #prevents solver from modifying user input values
                
                if i == 0 and j == 1:
                    self.x[temp-1].next = self.x[temp]
                    self.x[temp-1].prev = None
                elif i == 0 and j == 0:
                    #do nothing here
                    pass
                elif i == 8 and j == 8:
                    self.x[temp].next = None
                    self.x[temp].prev = self.x[temp-1]
                    self.x[temp-1].next = self.x[temp]
                else:
                    #print(temp)
                    self.x[temp-1].next = self.x[temp]
                    self.x[temp].prev = self.x[temp-1]
                
                

        #add check validity statement
        return True

    def printBoard(self):
        print(self.m)
        print('\n')
        return True

    def transf(self, x, y):
        #method to transform linear list of squares to a matrix output via coordinates
        #returns self.x indice for reference
        temp = (y*9) + x
        return temp

    def solveBoard(self):
        #backtracking algorithm to solve any sudoku board in real time
        #check if any zeroes present
        
        if self.checkBoard() == True:
            #check for board initially full
            return True
        else:
            #define function find next cell
            sq = self.findCell()
            s = self.x[0]
            #print(sq.lock)
            b = False
            while self.checkBoard() == False:
                #backtracking algorithm
                #find first empty square
                #modify value to 1
                if sq.lock == False and sq.v == 0:
                    sq.v = 1
                    self.m[sq.y][sq.x] = sq.v
                elif sq.lock == True:
                    sq = sq.next
                
                

                
                
                while self.testBoard(sq) == False:
                    
                    #increment value if value < 9
                    #self.printBoard()
                    if sq.v < 9:
                        if sq.lock == False:
                            sq.v += 1
                            self.m[sq.y][sq.x] = sq.v
                        elif self.testBoard(sq) == True and sq.v != 0:
                            self.m[sq.y][sq.x] = sq.v
                            sq = sq.next
                        elif self.testBoard(sq) == False and sq.lock == True:
                            sq = self.backtrack(sq)
                    elif sq.v == 9 and self.testBoard(sq) == False:
                        #backtrack
                        if sq.lock == True:
                            sq = self.checklock(sq)
                            sq = self.backtrack(sq)    
                        else:
                            sq = self.backtrack(sq)

                    if self.testBoard(sq) == True and sq.v != 0:
                        self.m[sq.y][sq.x] = sq.v
                        sq = sq.next
                    if sq.prev.v == 0 and sq.prev.lock == False:
                        sq = self.backtrack(sq)
                    #self.printBoard()
                    self.upBoard()
                if sq.v != 0: 
                    self.m[sq.y][sq.x] = sq.v
                    sq = sq.next    
                
                
                
        return True

    def checkBoard(self):
        for i in self.m:
            for j in i:
                if j == 0:
                    #print("working")
                    return False
        return True

    def checklock(self, sq):
        if sq.lock == True:
            self.m[sq.y][sq.x] = sq.v
            sq = sq.prev
            self.checklock(sq)
        sq.v = 0
        return sq

    def backtrack(self, sq):
        if sq.prev != None:
            if sq.lock == False:
                if sq.v < 9:
                    sq.v+=1
                    self.m[sq.y][sq.x] = sq.v
                    if self.testBoard(sq) == False:
                        sq = self.backtrack(sq)
                else:
                    sq.v = 0
                    self.m[sq.y][sq.x] = sq.v
                    sq = sq.prev
                    sq = self.backtrack(sq)
            else:
                sq = sq.prev
                sq = self.backtrack(sq)

        return sq


    def findCell(self):
        #function for finding next open cell
        for i in self.x:
            if i.v == 0:
                return i

    def testBoard(self, sq):
        #determine if board passes all rules
        value = sq.v
        if sq.v == 0:
            return False
        #test each value in each square
        i = self.m[sq.y]
        for k in range(self.length):
            #print(i[k])
            if i[k] == value and k != sq.x:
                return False #tests all values in row
        
            temp = np.transpose(self.m)
        i = temp[sq.x]

        for k in range(self.length):
             if i[k] == value and k != sq.y:
                 return False #tests all values in columns via transposing

        #test for square
        sq1 = self.findSquare(sq.x, sq.y)
        sq_X1 = sq1[0]
        sq_X2 = sq1[1]
        sq_Y1 = sq1[2]
        sq_Y2 = sq1[3]
        
        for i in range(sq_X1,sq_X2):
            for j in range(sq_Y1,sq_Y2):
                if value == self.m[j][i] and i != sq.x and j != sq.y :
                    return False
                #print("true")

        
        return True #if no issues are found
    
    def findSquare(self, index_X, index_Y):
        #method to find the subsquare based upon the x and y coordinates of a box
        sq = []
        if index_X < 3:
            if index_Y < 3:
                sq = [0,2,0,2]
            elif index_Y < 6:
                sq = [0,2,3,5]
            else:
                sq = [0,2,6,8]
        elif index_X < 6:
            if index_Y < 3:
                sq = [3,5,0,2]
            elif index_Y < 6:
                sq = [3,5,3,5]
            else:
                sq = [3,5,6,8]
        else:
            if index_Y < 3:
                sq = [6,8,0,2]
            elif index_Y < 6:
                sq = [6,8,3,5]
            else:
                sq = [6,8,6,8]
        if sq != None:
            return sq
        return False



#define board in main
def main():
    b = Board(length = 9, width = 9)

    b.prefill([[5,3,4,6,7,8,9,1,2],
               [6,0,0,1,9,5,0,0,0],
               [0,9,8,0,0,0,0,6,0],
               [8,0,0,0,6,0,0,0,3],
               [4,0,0,8,0,3,0,0,1],
               [7,0,0,0,2,0,0,0,6],
               [0,6,0,0,0,0,2,8,0],
               [0,0,0,4,1,9,0,0,5],
               [0,0,0,0,8,0,0,7,9]])


    b.upBoard()
    b.buildtiles()

    running = True
    while running:
        b.solveBoard()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

    pg.quit()

if __name__ == '__main__':
    main()

#print(b.testBoard(0,4))
#print(b.testBoard(0,5))
