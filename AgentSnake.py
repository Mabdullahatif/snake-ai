from collections import deque
import State as ST
from heapdict import heapdict
from State import Vector
import heapq


class Agent(object):
    def SearchSolution(self, state):
        return []

    def _GetMoveCoordinates(self, source: tuple, move: int):
        # X = Cols | Y = Rows
        col, row = source

        if move == 0:
            return (col, row - 1)
        if move == 6:
            return (col, row + 1)
        if move == 3:
            return (col + 1, row)
        if move == 9:
            return (col - 1, row)

    def GenerateMoves(self, state, source: tuple, visited: set, previousMove):
        # List of Potential Moves
        moves = [0, 6, 3, 9]

        # Remove those moves which are invalid
        if previousMove == 0:
            moves.remove(6)
        if previousMove == 6:
            moves.remove(0)
        if previousMove == 3:
            moves.remove(9)
        if previousMove == 9:
            moves.remove(3)

        return {move: self._GetMoveCoordinates(source, move) for move in moves if self.IsValidMove(self._GetMoveCoordinates(source, move), state, visited)}

    def IsValidMove(self, moveCoordinate, state, visited: set):
        # Checking if the move was already visited before
        if moveCoordinate in visited:
            return False

        # Checking if the move is within the maze
        if moveCoordinate[0] < 0 or moveCoordinate[0] >= state.maze.WIDTH:
            return False

        if moveCoordinate[1] < 0 or moveCoordinate[1] >= state.maze.HEIGHT:
            return False

        # Checking if the move does not lead to a wall
        col, row = moveCoordinate
        if state.maze.MAP[row][col] == -1:
            return False

        return True

    def GetPreviousMove(self, state):
        if state.snake.HeadDirection.X == 0 and state.snake.HeadDirection.Y == -1:
            return 0
        if state.snake.HeadDirection.X == 0 and state.snake.HeadDirection.Y == 1:
            return 6
        if state.snake.HeadDirection.X == 1 and state.snake.HeadDirection.Y == 0:
            return 3
        if state.snake.HeadDirection.X == -1 and state.snake.HeadDirection.Y == 0:
            return 9


class AgentSnake(Agent):
    def SearchSolution(self, state):
        FoodX = state.FoodPosition.X
        FoodY = state.FoodPosition.Y

        HeadX = state.snake.HeadPosition.X  # L
        HeadY = state.snake.HeadPosition.Y  # T

        DR = FoodY - HeadY
        DC = FoodX - HeadX

        plan = []

        # Moves
        # 0 = Top
        # 6 = Bottom
        # 9 = Left
        # 3 = Right

        F = -1
        if (DR == 0 and state.snake.HeadDirection.X*DC < 0):
            plan.append(0)
            F = 6

        if (state.snake.HeadDirection.Y*DR < 0):
            plan.append(3)
            if (DC == 0):
                F = 9
            else:
                DC = DC - 1
        Di = 6
        if (DR < 0):
            Di = 0
            DR = -DR
        for i in range(0, int(DR)):
            plan.append(Di)
        Di = 3
        if (DC < 0):
            Di = 9
            DC = -DC
        for i in range(0, int(DC)):
            plan.append(Di)
        if (F > 0):
            plan.append(F)
            F = -1

        return plan

    def showAgent():
        print("A Snake Solver By MB")

# You code of agent goes here
# You must create three agents one using A*, second using greedy best first search and third using an uninformed algo of your choice to make a plan


class AStarSearch(Agent):
    def SearchSolution(self, state: ST.SnakeState):
        source = state.snake.HeadPosition.getTuple()
        goal = state.FoodPosition.getTuple()

        plan = []
        visited = set()
        heap = heapdict()
        heap[source] = (0, 0, plan)  # TotalCost + SourceCost + Moves
        previousMove = self.GetPreviousMove(state)

        while heap:
            node, data = heap.popitem()
            totalCost, sourceCost, currentPlan = data
            visited.add(node)

            if node[0] == goal[0] and node[1] == goal[1]:
                plan = currentPlan
                break

            Moves = self.GenerateMoves(
                state, node, visited, previousMove if node == source else -1)

            for move, moveCoordinate in Moves.items():
                moveSourceCost = sourceCost + 1
                moveHeuristic = abs(moveCoordinate[0] - goal[0]) + \
                    abs(moveCoordinate[1] - goal[1])

                currentMoveCost = moveSourceCost + moveHeuristic
                previousMoveCost = heap.get(
                    moveCoordinate, (float('inf'), None, None))[0]

                if currentMoveCost < previousMoveCost:
                    heap[moveCoordinate] = (
                        currentMoveCost, moveSourceCost, [*currentPlan, move])

        return plan if len(plan) != 0 else [0]


class GreedyBestFirstSearch(Agent):
    def SearchSolution(self, state: ST.SnakeState):
        source = state.snake.HeadPosition.getTuple()
        goal = state.FoodPosition.getTuple()

        plan = []
        visited = set()
        queue = [(self.heuristic(state, source, goal), source, plan)]  # Heuristic + Node + Plan
        previousMove = self.GetPreviousMove(state)

        while queue:
            _, node, currentPlan = heapq.heappop(queue)
            visited.add(node)

            if node[0] == goal[0] and node[1] == goal[1]:
                plan = currentPlan
                break

            Moves = self.GenerateMoves(
                state, node, visited, previousMove if node == source else -1)

            for move, moveCoordinate in Moves.items():
                moveHeuristic = self.heuristic(state, moveCoordinate, goal)
                heapq.heappush(queue,(moveHeuristic, moveCoordinate, [*currentPlan, move]))

        return plan

    def heuristic(self, state, start, goal):
        maze = state.maze.MAP
        visited = set()
        queue = deque([(start, 0)])
        visited.add(start)

        while queue:
            node, distance = queue.popleft()

            if node == goal:
                return distance

            for move, moveCoordinate in self.GenerateMoves(state, node, visited, -1).items():
                visited.add(moveCoordinate)
                if maze[moveCoordinate[1]][moveCoordinate[0]] != -1:
                    queue.append((moveCoordinate, distance + 1))

        return float('inf')

class UniformCostSearch(Agent):
    def SearchSolution(self, state: ST.SnakeState):
        source = state.snake.HeadPosition.getTuple()
        goal = state.FoodPosition.getTuple()

        plan = []
        visited = set()
        cost = {source: 0}
        queue = [(0, source, plan)]  # Cost + Node + Plan
        previousMove = self.GetPreviousMove(state)

        while queue:
            currentCost, node, currentPlan = heapq.heappop(queue)
            visited.add(node)

            if node[0] == goal[0] and node[1] == goal[1]:
                plan = currentPlan
                break

            if currentCost > cost[node]:
                continue  # Skip if we have already found a cheaper path to this node

            Moves = self.GenerateMoves(
                state, node, visited, previousMove if node == source else -1)

            for move, moveCoordinate in Moves.items():
                moveCost = 1  # Uniform cost for each move
                totalCost = cost[node] + moveCost

                if moveCoordinate not in cost or totalCost < cost[moveCoordinate]:
                    cost[moveCoordinate] = totalCost
                    heapq.heappush(queue, (totalCost, moveCoordinate, [*currentPlan, move]))

        return plan

