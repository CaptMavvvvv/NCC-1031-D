class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data)
        if self.right:
            self.right.PrintTree()

    def find_min(self):
        current = self
        while current.left is not None:
            current = current.left
        return current

    def delete(self, data):
        if data < self.data:
            if self.left:
                self.left = self.left.delete(data)
            return self
        elif data > self.data:
            if self.right:
                self.right = self.right.delete(data)
            return self
        else:
            if self.left is None:
                return self.right
            elif self.right is None:
                return self.left
            else:
                min_node = self.right.find_min()
                self.data = min_node.data
                self.right = self.right.delete(min_node.data)
                return self
            
    def findval(self, lkpval):
        if lkpval < self.data:
            if self.left is None:
                return str(lkpval)+" Not Found"
            return self.left.findval(lkpval)
        elif lkpval > self.data:
            if self.right is None:
                return str(lkpval)+" Not Found"
            return self.right.findval(lkpval)
        else:
            print(str(self.data) + ' is found')

    def inorderTraversal(self, root):
        res = []
        if root:
            res = self.inorderTraversal(root.left)
            res.append(root.data)
            res = res + self.inorderTraversal(root.right)
        return res
    
    def preorderTraversal(self, root):
        res = []
        if root:
            res.append(root.data)
            res = res + self.preorderTraversal(root.left)
            res = res + self.preorderTraversal(root.right)
        return res
    
    def postorderTraversal(self, root):
        res = []
        if root:
            res = self.postorderTraversal(root.left)
            res = res + self.postorderTraversal(root.right)
            res.append(root.data)
        return res

root = Node(10)
root.insert(30)
root.insert(40)
root.insert(35)
root.insert(20)
root.insert(47)
root.insert(5)
print(root.findval(7))
print(root.findval(35))
print(root.inorderTraversal(root))
print(root.preorderTraversal(root))
print(root.postorderTraversal(root))

print("Tree before deletion:")
root.PrintTree()

root = root.delete(30)
print("\nTree after deleting 30:")
root.PrintTree()

root = root.delete(10)
print("\nTree after deleting 10:")
root.PrintTree()

root = root.delete(47)
print("\nTree after deleting 47:")
root.PrintTree()