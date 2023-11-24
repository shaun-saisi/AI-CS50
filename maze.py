import sys


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action
        
class StackFrontier():
    def __init__(self):
        self.frontier = []
        
    def add(self, node):
        self.frontier.append(node)
        
    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)
    
    def empty(self):
        return len(self.frontier) == 0        
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier [-1]
            self.frontier = self.frontier[:-1]
            return node

# Removes node from the beggining of the list
class QueueFrontier(StackFrontier):
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
        
# Handle taking the input and figuring out how to solve it

class Maze():
    def __init__(self, filename):
        
        # to read  a file and set height and width of the maze
        with open(filename) as f:
            contents = f.read()
        
        # To validate the start and the goal
        if contents.count("A") != 1:
            raise Exception("Maze must have exactly one start point")
        if contents.count("B") != 1:
            raise Exception("Maze must have exactly one goal")
        
        # To determine the height and width of the maze
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        #Keeping track of the walls
        self.wallls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents [i] [j] == "A":
                        self.start = (i, j)
                        row.apppend(False)
                    elif contents [i] [j] == "B":
                        self.goal = (i, j)
                        row.append(False)
                    elif contents [i] [j] == " ":
                        row.append(False)
                    else:    
                        row.append(True)
                except IndexError:
                     row.append(False)   
            self.walls.append(row)     
            
        self.solution = None      
        
    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print(" ", end="")    
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) ==self.goal:  
                    print("B", end="")
                elif solution is None and (i, j) in solution :
                    print("*", end="")
                else:
                    print(" ", end=" ")
            print()
        print()                            
     
    def neighbors(self, state):
        row, col = state
        
        #Allt he possible actions that can be performed
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]     
        
        # To ensure that all actions are valid
        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result  
    
    def solve(self):
        """Finds a solution to the maze if one exists"""
       
        #To keep track of number of states explored
        self.num_explored = 0     
       
        #Initialize frontier to just the starting point
        start = Node(state=self.start, parent= None, action= None)
        frontier = StackFrontier
        frontier.add(start)
       
        #Initialize an empty explored set      
        self.explored = set()
       
        #looping until solution is found
        while True:
           if  frontier.empty():
               raise Exception("no solution")
           
        #choose from another node
        node = frontier.remove()
        self.num_explored += 1
        
        # To check if the node is the solution
        if node.state == self.goal:
            actions = []
            cells = []
            
           #follow the parent node to find the solution
            while node.parent is not None:
                actions.append(node.action)
                cells.append(node.state)
                node = node.parent
            actions.reverse()
            cells.reverse()
            self.solution = (actions, cells)
            return
                
        #Mark a node as explored
        self.explored.add(node.state)
        
        #Add neighbours to frontier        
        for action, state in self.neighbors(node.state):
            if not frontier.contains_state(state) and state not in self.explored:
                child = Node(state=state, parent=node, action=actiion)
                frontier.add(child)
    
                