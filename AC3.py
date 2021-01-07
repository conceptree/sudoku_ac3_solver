import queue    
from CSP import *  

class AC3:

	def applyAC3(self, csp):        
		q = queue.Queue()        
		for arc in csp.constraints:    
			q.put(arc)
		i = 0
		while not q.empty():  
			(Xi, Xj) = q.get()   
			i = i + 1  
			if self.revise(csp, Xi, Xj):  
				if len(csp.values[Xi]) == 0:  
					return False
				for Xk in (csp.peers[Xi] - set(Xj)): 
					q.put((Xk, Xi))  
		return True 

	def revise(self, csp, Xi, Xj):  
		revised = False    
		values = set(csp.values[Xi])   
		for x in values:          
			if not self.isconsistent(csp, x, Xi, Xj):   
				csp.values[Xi] = csp.values[Xi].replace(x, '')   
				revised = True                   
		return revised    

	def isconsistent(self, csp, x, Xi, Xj):    
		for y in csp.values[Xj]:
			if Xj in csp.peers[Xi] and y!=x:  
				return True                  
		return False   

	def isComplete(self, csp):
		for variable in squares:   
			if len(csp.values[variable])>1:      
				return False
		return True

	def write(self, values):
		output = ""    
		for variable in squares:   
			output = output + values[variable]   
		return output