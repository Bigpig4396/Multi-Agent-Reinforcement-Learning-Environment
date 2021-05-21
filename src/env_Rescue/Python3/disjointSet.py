#! /usr/bin/env python3
'''
Disjoint Set Class that provides basic functionality. 
Implemented according the functionality provided here:
	https://en.wikipedia.org/wiki/Disjoint-set_data_structure
@author: Paul Miller (github.com/138paulmiller)
'''
class DisjointSet:
	'''
	Disjoint Set : Utility class that helps implement Kruskal MST algorithm
		Allows to check whether to keys belong to the same set and to union
		sets together
	'''
	class Element:
		def __init__(self, key):
			self.key = key
			self.parent = self
			self.rank = 0
		
		def __eq__(self, other):
			return self.key ==  other.key
		def __ne__(self, other):
			return self.key != other.key
 
	def __init__(self):
		'''
		Tree = element map where each node is a (key, parent, rank) 
		Sets are represented as subtrees whose root is identified with
		a self referential parent
		'''
		self.tree = {}
	
	def make_set(self, key):
		'''
		Creates a new singleton set.
		@params 
			key : id of the element
		@return
			None
		'''
		# Create and add a new element to the tree
		e = self.Element(key)
		if not key in self.tree.keys():
			self.tree[key] = e

			
	def find(self, key):
		'''
		Finds a given element in the tree by the key.
		@params 
			key(hashable) : id of the element
		@return
			Element : root of the set which contains element with the key
		'''
		if key in self.tree.keys():
			element = self.tree[key]
			# root is element with itself as parent
			# if not root continue
			if element.parent != element:
				element.parent  = self.find(element.parent.key)
			return element.parent

	
	def union(self, element_a, element_b):
		'''
		Creates a new set that contains all elements in both element_a and element_b's sets
		Pass into union the Elements returned by the find operation
		@params 
			element_a(Element) : Element or key of set a
			element_b(Element) : Element of set b
		@return
			None
		''' 
		root_a = self.find(element_a.key)
		root_b = self.find(element_b.key)
		# if not in the same subtree (set)
		if root_a != root_b:
			#merge the sets
			if root_a.rank < root_b.rank:
				root_a.parent = root_b
			elif root_a.rank > root_b.rank:
				root_b.parent = root_a
			else:
				# same rank, set and increment arbitrary root as parent
				root_b.parent = root_a
				root_a.rank+=1

