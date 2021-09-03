#Implementation is based on the RBT chapter from "Introduction to Algorithms, Third Edition" book by T. Cormen

class Node:
    def __init__(self, val=None, process=None, color = 1):
        self.val=val
        self.process=process
        self.color = color #red by default
        self.parent = None
        self.left = None
        self.right = None


class RBT:
    def __init__(self):
        self.nil = Node() #the empty node, represents all references to leafs 
        
        self.nil.parent = self.nil
        self.nil.right = self.nil
        self.nil.left = self.nil
        
        self.nil.color = 0
        
        self.root = self.nil #at the begining, the root is an empty node
        self.n_elements = 0 #keep track of the number of elements in the tree
        
    def get_leftmost(self):
        y = self.nil
        x = self.root
        
        while x is not self.nil:
            y = x
            x = x.left
        return y
    
    def search(self, val, process): #the function to search for any node by val and proces. Actually is not used, since we always need the leftmost node, and it has another function.
        search = self.root
        z = self.nil
        
        while search is not self.nil:
            if search.val == val and search.process == process:
                z = search
                break
            elif val<search.val:
                search = search.left
            else:
                search = search.right
        
        return z
    
    def insert(self, node):
        
        self.n_elements+=1
        
        z = node
        
        y = self.nil
        x = self.root
        
        #find the suitable parent

        while x is not self.nil:
            y = x
            if z.val < x.val:
                x = x.left
            else:
                x = x.right
        
        z.parent = y

        #if parent is still None, it means that the inserted node is a new root 
        if y is self.nil:
            self.root = z
        #in not, then determine left or right child
        elif z.val<y.val:
            y.left = z
        else:
            y.right = z
        
        
        #set children of the new process as empty nodes
        z.left = self.nil
        z.right = self.nil
        
        #restore RBT properties
        self.fix_insert(z)
        
    def delete(self, node):
        
        self.n_elements-=1
      
        z = node
        
        #if node has a single child, then just assign the parent of that child to grandaprent of the node, bypassing the deleted one
        if z.left is self.nil or z.right is self.nil:
            y = z
        else:
            #if both children exist, determine the successor of the deleted node
            y = self.tree_successor(z)
        #standard procedure of deletion in binary tree    
        if y.left is not self.nil:
            x = y.left
        else:
            x = y.right
            
        x.parent = y.parent
        
        if y.parent is self.nil:
            self.root = x
        elif y is y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x
            
        if y is not z:
            z.val = y.val
            z.process = y.process
        #if successor is red, it doesn't violate any properties since the black height did not change and no two red nodes are adjacent    
        if y.color == 0:
            self.fix_delete(x)
    
    
    def tree_successor(self, z):
        #successor in the binary tree is the smallest key with the value greater than that of the deleted node
        #it is minimum that is greater, so go to the right child and from there then to the left till the end.  
        if z.right is not self.nil:
            x = z.right
            while x.left is not self.nil:
                x = x.left
            return x
        
        #if no right child, then go up and check there by the same logic, until found
        y = z.parent
        
        while y is not self.nil and z is y.right:
            z = y
            y = y.parent
        return y
            
    def fix_insert(self, z):
        #since the new node is always red, it does not violate properties about the number of black nodes.
        #two properties that might be violated are: if new node is the root and is red, and if parent of new node is red
        while z.parent.color == 1:
            #property of no two reds in a row is violated only if the parent is red
            if z.parent is z.parent.parent.left:
                #if parent is left child of grandparent, then uncle y is the right child
                y = z.parent.parent.right
                if y.color == 1:
                    #case 1: uncle is red: set both parent and uncle to black, set grandparent to red
                    #it may also violate the properties of RBT, by the same logic, so set grandparent as new z, and repeat in the next iteration
                    z.parent.color=0
                    y.color = 0
                    z.parent.parent.color=1
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        #case 2: uncle is black, z is right child
                        #in this case we need to left-rotate on the parent
                        z = z.parent
                        self.leftrotate(z)
                    #case 3: uncle is black, z is left child
                    #the same logic, but right-rotate
                    z.parent.color = 0
                    z.parent.parent.color = 1
                    self.rightrotate(z.parent.parent)
            else:
                #symmetrical
                y = z.parent.parent.left
                if y.color == 1:
                    z.parent.color=0
                    y.color = 0
                    z.parent.parent.color=1
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.rightrotate(z)
                    z.parent.color = 0
                    z.parent.parent.color = 1
                    self.leftrotate(z.parent.parent)
        #if new node is the root, it changed root's color, so set the root to black
        self.root.color = 0
    
    def fix_delete(self, x):
        while (x is not self.nil) and (x.color==0):
            if x is x.parent.left:
                # w is sibling
                w = x.parent.right
                
                if w.color == 1:
                    #case 1: sibling is red
                    #switch colors of w and its parent, then leftrotate
                    w.color = 0
                    x.parent.color = 1
                    self.leftrotate(x.parent)
                    #x color is now black, while terminates
                    #place w as x sibling
                    w = x.parent.right
                
                if w.left.color == 0 and w.right.color == 0:
                    #case 2: w is black, both children are black
                    #set w to red. It might violate the properties of RBT, so set x to its parent and the fix will be repeated on next iter.
                    w.color = 1
                    x = x.parent
                else:
                    if w.right.color == 0:
                        #case 3: w is black, left child is red, right child is black
                        #set left child to black, w itself to red and right rotate
                        w.left.color = 0
                        w.color = 1
                        self.rightrotate(w)
                        #place w back as x sibling
                        w = x.parent.right
                    #case 4: w is black, left child is black, right child is red
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.right.color = 0
                    self.leftrotate(x.parent)
                    x = self.root
            
            else:
                #symmetrical
                w = x.parent.left
                if w.color == 1:
                    w.color = 0
                    x.parent.color = 1
                    self.rightrotate(x.parent)
                    w = x.parent.left
                
                if w.left.color == 0 and w.right.color == 0:
                    w.color = 1
                    x = x.parent
                else:
                    if w.left.color == 0:
                        w.right.color = 0
                        w.color = 1
                        self.leftrotate(w)
                        w = x.parent.left
                    
                    w.color = x.parent.color
                    x.parent.color = 0
                    w.left.color = 0
                    self.rightrotate(x.parent)
                    x = self.root
        x.color = 0
    
    def leftrotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not self.nil:
            y.left.parent = x
        
        y.parent = x.parent
        
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.left = x
        x.parent = y
    
    def rightrotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not self.nil:
            y.right.parent = x
        
        y.parent = x.parent
        
        if x.parent is self.nil:
            self.root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
            
        y.right = x
        x.parent = y