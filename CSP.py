digits =  cols = "123456789"  
rows = "ABCDEFGHI"  

def cross(A, B):
	return [a + b for a in A for b in B]

squares = cross(rows, cols)     

class csp:
	
	def __init__ (self, domain = digits, grid = ""):
		self.variables = squares
		self.domain = self.getDict(grid)
		self.values = self.getDict(grid)
		self.unitlist = ([cross(rows, col) for col in cols] +   
            			 [cross(row, cols) for row in rows] +    
            			 [cross(rows, cols) for rows in ('ABC','DEF','GHI') for cols in ('123','456','789')])
		self.units = dict((s, [u for u in self.unitlist if s in u]) for s in squares)
		self.peers = dict((s, set(sum(self.units[s],[]))-set([s])) for s in squares)     
		self.constraints = {(variable, peer) for variable in self.variables for peer in self.peers[variable]}
	
	def getDict(self, grid=""):
		i = 0
		values = dict()
		for cell in self.variables:
			if grid[i]!='0':
				values[cell] = grid[i]
			else:
				values[cell] = digits
			i = i + 1
		return values