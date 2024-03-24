import sys
import threading
import State as ST
import AgentSnake as AS
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
        if (self.State.snake.isAlive == False):
            return
        PlanIsGood = True
        Message = "Game Over"
        while (self.State.snake.isAlive and PlanIsGood):
            ScoreBefore = self.State.snake.score
            Plan = self.AgentSnake.SearchSolution(self.State)
            self.ExecutePlan(Plan)

            ScoreAfter = self.State.snake.score

            if (ScoreAfter == ScoreBefore):
                self.View.AddFood(self.State.FoodPosition)
                PlanIsGood = False

            self.State.generateFood()
            if not self.State.snake.isAlive:
                self.View.AddFood(self.State.FoodPosition)

            self.View.AddFood(self.State.FoodPosition)
            # time.sleep(1/2)

        if (self.State.snake.isAlive):
            Message = Message + " : Has a Bad Plan"
        else:
            Message = Message + " : Snake Hit Something"

        self.View.ShowGameOverMessage(Message)

    def Play(self):
        thread = threading.Thread(target=self.StartSnake)
        thread.start()
        self.View.top.mainloop()
        return thread


if __name__ == '__main__':
    arguments = sys.argv
    if len(arguments) < 5:
        print("Usage: python main.py <A*/GBFS/UCS> <COLOR> <MAZE.TXT> <WINDOW TITLE>")
        sys.exit(1)

    algo = arguments[1]
    color = arguments[2]
    maze = arguments[3]
    title = arguments[4]

    instance = AS.AStarSearch()
    if algo.lower() == 'GBFS'.lower():
        instance = AS.GreedyBestFirstSearch()

    if algo.lower() == 'UCS'.lower():
        instance = AS.UniformCostSearch()

    # A Star Search
    agent = {
        'state': ST.SnakeState(color, 10, 10, 0, 1, maze),
        'instance': instance,
        'windowTitle': title
    }

    engine = Main(agent['state'], agent['instance'], agent['windowTitle'])
    engine.Play()
