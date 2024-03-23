import threading
import State as ST
import AgentSnake as AS
import tkinter
import time
import View as V


class Main:
    def __init__(self, State, AgentSnake, title, SnakeSpeed=30):
        self.State = State
        self.AgentSnake = AgentSnake
        self.View = V.SnakeViewer(self.State, title, SnakeSpeed)

    def setDirection(self, k):
        if (k == 0):
            self.State.snake.HeadDirection.X = 0
            self.State.snake.HeadDirection.Y = -1
        elif (k == 6):
            self.State.snake.HeadDirection.X = 0
            self.State.snake.HeadDirection.Y = 1
        elif (k == 3):
            self.State.snake.HeadDirection.X = 1
            self.State.snake.HeadDirection.Y = 0
        elif (k == 9):
            self.State.snake.HeadDirection.X = -1
            self.State.snake.HeadDirection.Y = 0

    def ExecutePlan(self, Plan):
        for k in Plan:
            self.setDirection(k)
            self.State.snake.moveSnake(self.State)
            if (self.State.snake.isAlive == False):
                break
            time.sleep(1/self.View.SPEED)
            self.View.UpdateView()

    def StartSnake(self):
        if(self.State.snake.isAlive == False):
            return
        PlanIsGood = True
        Message = "Game Over"
        while(self.State.snake.isAlive and PlanIsGood):
            ScoreBefore = self.State.snake.score
            Plan = self.AgentSnake.SearchSolution(self.State)
            self.ExecutePlan(Plan)
			
            ScoreAfter = self.State.snake.score
			
            if(ScoreAfter == ScoreBefore):
                self.View.AddFood(self.State.FoodPosition)
                PlanIsGood = False
                
            self.State.generateFood()
            if not self.State.snake.isAlive:
                self.View.AddFood(self.State.FoodPosition)
            # time.sleep(1/2)

        if(self.State.snake.isAlive):
            Message = Message + "  HAS A BAD PLAN"
        else:
            Message = Message + " HAS HIT A WALL"
        self.View.ShowGameOverMessage(Message)

    def Play(self):
        thread = threading.Thread(target=self.StartSnake)
        thread.start()
        return thread


def deployAgent(state, instance, windowTitle):
    return {'state': state, 'instance': instance, 'windowTitle': windowTitle}


def runGameAgents(agents: tuple):
    root = tkinter.Tk()
    root.title('Snake Search with Multiple Agents')
    root.withdraw()  # Hiding the root window

    # Fueling and running each game agent
    for agent in agents:
        engine = Main(agent['state'], agent['instance'], agent['windowTitle'])
        engine.Play()

    # Running the Main Tkinter Loop
    root.mainloop()


if __name__ == '__main__':
    runGameAgents(agents=(
        # A Star Search
        deployAgent(state=ST.SnakeState('orange', 10, 10, 0, 1, "hurdlesMaze.txt"),
                    instance=AS.AStarSearch(), windowTitle='A* Search'),

        # # Greedy Best First Search
        # deployAgent(state=ST.SnakeState('red', 10, 10, 0, 1, "hurdlesMaze.txt"),
        #             instance=AS.GreedyBestFirstSearch(), windowTitle='GBFS Search'),

        # # Unifrom Cost Search
        # deployAgent(state=ST.SnakeState('pink', 10, 10, 0, 1, "hurdlesMaze.txt"),
        #             instance=AS.UniformCostSearch(), windowTitle='UCS Search'),
    ))
