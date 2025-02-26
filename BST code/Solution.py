import pytest
from random import randint

class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        tree_node = TreeNode(value)

        def recurse(ptr, node):
            if not ptr:
                return node

            if node.value < ptr.value:
                ptr.left = recurse(ptr.left, node)
            else:
                ptr.right = recurse(ptr.right, node)

            return ptr

        self.root = recurse(self.root, tree_node)

    def inorder(self):
        inorder_list = []

        def recurse(ptr):
            if not ptr:
                return
            recurse(ptr.left)
            inorder_list.append(ptr.value)
            recurse(ptr.right)

        recurse(self.root)
        return inorder_list

# Test cases for the BST class
def test_empty_bst():
    bst = BST()
    assert bst.inorder() == []

def test_single_element():
    bst = BST()
    bst.insert(10)
    assert bst.inorder() == [10]

def test_multiple_elements():
    bst = BST()
    elements = [5, 3, 7, 2, 4, 6, 8]
    for el in elements:
        bst.insert(el)
    assert bst.inorder() == sorted(elements)

def test_sorted_insertion():
    bst = BST()
    for i in range(1, 11):  # Sorted elements
        bst.insert(i)
    assert bst.inorder() == list(range(1, 11))

def test_reverse_sorted_insertion():
    bst = BST()
    for i in range(10, 0, -1):  # Reverse sorted elements
        bst.insert(i)
    assert bst.inorder() == list(range(1, 11))

def test_random_insertion():
    bst = BST()
    random_elements = [randint(1, 100) for _ in range(10)]
    for el in random_elements:
        bst.insert(el)
    assert bst.inorder() == sorted(random_elements)

def test_duplicate_insertion():
    bst = BST()
    elements = [5, 3, 7, 3, 5, 7]  # Duplicates
    for el in elements:
        bst.insert(el)
    assert bst.inorder() == sorted(elements)

if __name__ == "__main__":
    pytest.main()