"""
Elevator Maintenance
====================

You've been assigned the onerous task of elevator maintenance - ugh! It wouldn't be so bad, except that all the elevator documentation has been lying in a disorganized pile at the bottom of a filing cabinet for years, and you don't even know what elevator version numbers you'll be working on. 

Elevator versions are represented by a series of numbers, divided up into major, minor and revision integers. New versions of an elevator increase the major number, e.g. 1, 2, 3, and so on. When new features are added to an elevator without being a complete new version, a second number named "minor" can be used to represent those new additions, e.g. 1.0, 1.1, 1.2, etc. Small fixes or maintenance work can be represented by a third number named "revision", e.g. 1.1.1, 1.1.2, 1.2.0, and so on. The number zero can be used as a major for pre-release versions of elevators, e.g. 0.1, 0.5, 0.9.2, etc (Commander Lambda is careful to always beta test her new technology, with her loyal henchmen as subjects!).

Given a list of elevator versions represented as strings, write a function answer(l) that returns the same list sorted in ascending order by major, minor, and revision number so that you can identify the current elevator version. The versions in list l will always contain major numbers, but minor and revision numbers are optional. If the version contains a revision number, then it will also have a minor number.

For example, given the list l as ["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"], the function answer(l) would return the list ["1.0", "1.0.2", "1.0.12", "1.1.2", "1.3.3"]. If two or more versions are equivalent but one version contains more numbers than the others, then these versions must be sorted ascending based on how many numbers they have, e.g ["1", "1.0", "1.0.0"]. The number of elements in the list l will be at least 1 and will not exceed 100.

Languages
=========

To provide a Python solution, edit solution.py
To provide a Java solution, edit solution.java

Test cases
==========

Inputs:
    (string list) l = ["1.1.2", "1.0", "1.3.3", "1.0.12", "1.0.2"]
Output:
    (string list) ["1.0", "1.0.2", "1.0.12", "1.1.2", "1.3.3"]

Inputs:
    (string list) l = ["1.11", "2.0.0", "1.2", "2", "0.1", "1.2.1", "1.1.1", "2.0"]
Output:
    (string list) ["0.1", "1.1.1", "1.2", "1.2.1", "1.11", "2", "2.0", "2.0.0"]


"""

class node:
    left = None
    right = None
    father = None
    value = ''
    def __init__(self, v, father):
        self.value = v
        self.father = father
        
    def isBefore(self, n):
        lc = self.value.split('.')
        ln = n.split('.')
        for i in range(0, min(len(lc), len(ln))):
            if int(lc[i]) == int(ln[i]):
                continue
            if int(lc[i]) > int(ln[i]):
                return False
            if int(lc[i]) < int(ln[i]):
                return True          
        if len(lc) < len(ln):
            return True
        else:
            return False
            
    def printSub(self):
        result = []
        if self.left is not None:
            result = result + self.left.printSub()
        result = result + [self.value]
        if self.right is not None:
            result = result + self.right.printSub()
        return result
    
class Tree:
    root = None
    
    def insert(self, v):
        
        if self.root == None:
            self.root = node(v, None)
            print('insert root: ' +v)
            return
            
        current = self.root
        while True:
            if current is None:
                current = node(v, current)
                return
            if current.isBefore(v):
                if current.right is None:
                    current.right = node(v, current)
                    return
                else:    
                    current = current.right
            else:
                if current.left is None:
                    current.left = node(v, current)
                    return
                else:
                    current = current.left
                
    def printTree(self):
        if self.root is None:
            return None
        else:
            return self.root.printSub()
    
def answer(l):
    # your code here
    myTree = Tree()
    for v in l:
        myTree.insert(v)
    return myTree.printTree()
