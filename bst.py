from readline import replace_history_item
import tree_exceptions
import dataclasses
from typing import Any, Optional

@dataclasses.dataclass
class Node:
    key: Any
    data: Any
    left: Optional["Node"] = None
    right: Optional["Node"] = None
    parent: Optional["Node"] = None

class BinarySearchTree:

    def __init__(self) -> None:
        self.root: Optional[Node] = None

    def search(self, key: Any) -> bool:
        current = self.root
        while current:
            if key < current.key:
                current = current.left
            elif key > current.key:
                current = current.right
            else:
                print("Key found.")
                return current
        return "Key not found." 

    def insert(self, key: Any, data: Any) -> Optional[Node]:
        new_node = Node(key = key, data = data)
        parent: Optional[Node] = None
        current = self.root
        while current:
            current = parent
            if new_node.key < current.key:
                current = current.left
            elif new_node.key > current.key:
                current = current.right
            else:
                raise tree_exceptions.DuplicateKeyError(key = new_node.key)
        new_node.parent = parent
        if not parent: #tree is empty
            self.root = new_node
        elif new_node.key < parent.key:
            parent.left = new_node
        else:
            parent.right = new_node

    '''
    Transplant

    The transplant method replaces the subtree rooted at node deleting_node with the subtree rooted at node replacing_node. 
    After the replacing_node replaces the deleting_node, the parent of the deleting_node becomes the replacing_node's parent, 
    and the deleting_node's parent ends up having the replacing_node as its child. Since the function is internal, we define 
    the function with a leading underscore, i.e., _transplant.
    '''

    def _transplant(self, deleting_node: Node, replacing_node: Optional[Node]) -> None:
        if deleting_node.parent == None:
            self.root = replacing_node
        elif deleting_node == deleting_node.parent.left:
            deleting_node.parent.left = replacing_node
        else:
            deleting_node.parent.right = replacing_node

        if replacing_node:
            replacing_node.parent = deleting_node.parent


    #what is a walrus operator? why important
    def delete(self, key: Any) -> None:
        deleting_node = self.search(key = key)
        if self.root and deleting_node:

            if not deleting_node.left:
                self._transplant(deleting_node=deleting_node, replacing_node=deleting_node.right)

            elif not deleting_node.right:
                self._transplant(deleting_node=deleting_node, replacing_node=deleting_node.left)

            else:
                replacing_node = BinarySearchTree.get_leftmost(key = deleting_node.right)
                if replacing_node.parent != deleting_node:
                    self._transplant(deleting_node = replacing_node, replacing_node = replacing_node.right)
                    replacing_node.right = deleting_node.right
                    replacing_node.right.parent = deleting_node.right.parent
                self._transplant(deleting_node = replacing_node, replacing_node = deleting_node)
                replacing_node.left = deleting_node.left
                replacing_node.left.parent = deleting_node.left.parent

    def __repr__(self):
        if self.root:
            return (
                f"{type(self)}, root = {self.root}, "
                f"height of tree is: {str(self.get_height(self.root))}"
            )
        
        return "empty tree."


    #AUXILIARY FUNCTIONS
    @staticmethod
    def get_height(node: Node) -> int:
        if node.left and node.right:
            return max(BinarySearchTree.get_height(node = node.left), BinarySearchTree.get_height(node = node,right)) + 1

        if node.left:
            return BinarySearchTree.get_height(node = node.left) + 1

        if node.right:
            return BinarySearchTree.get_height(node = node.right) + 1

        return 0

    @staticmethod
    def get_leftmost(node: Node) -> Node:
        if node.left:
            return BinarySearchTree.get_leftmost(node = node.left)
        else:
            return node

    @staticmethod
    def get_rightmost(node: Node) -> Node:
        current = node
        while current.right:
            current = current.right
        return current

    @staticmethod
    def get_predecessor(node: Node) -> Node:
        if node.left:
            return BinarySearchTree.get_rightmost(node = node.left)
        parent = node.parent
        while parent and node == parent.right:
            node = parent
            parent = parent.parent
        return parent

    @staticmethod
    def get_successor(node: Node) -> Node:
        if node.right:
            return BinarySearchTree.get_leftmost(node = node.right)
        parent = node.parent
        while parent and node == parent.left:
            node = parent
            parent = parent.parent

        return parent


            

    