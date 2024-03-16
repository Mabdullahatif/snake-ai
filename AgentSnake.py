
class Agent(object):
	def SearchSolution(self, state):
		return []
		
class AgentSnake(Agent):    
	def SearchSolution(self, state):
		FoodX = state.FoodPosition.X
		FoodY = state.FoodPosition.Y

		HeadX = state.snake.HeadPosition.X #L
		HeadY = state.snake.HeadPosition.Y #T
		
		DR = FoodY - HeadY
		DC = FoodX - HeadX
		
		plan = []
		
		F = -1
		if(DR == 0 and state.snake.HeadDirection.X*DC < 0):
			plan.append(0)
			F = 6
			
		if(state.snake.HeadDirection.Y*DR < 0):
			plan.append(3)
			if(DC == 0):
				F = 9
			else:
				DC = DC - 1
		Di = 6
		if(DR < 0):
			Di = 0
			DR = -DR
		for i in range(0,int(DR)):
			plan.append(Di)
		Di = 3
		if(DC < 0):
			Di = 9
			DC = -DC
		for i in range(0,int(DC)):
			plan.append(Di)
		if(F > 0):
			plan.append(F)
			F = -1
			
		return plan
	
	def showAgent():
		print("A Snake Solver By MB")
		
# You code of agent goes here
# You must create three agents one using A*, second using greedy best first search and third using an uninformed algo of your choice to make a plan

 
	