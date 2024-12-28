# Game Controller
from WumpusWorld import WumpusWorld
from Agent import Agent
from EntityType import EntityType
from Position import Position

class WumpusQuestGame:
    def __init__(self, size: int = 10):
        self.world = WumpusWorld(size)
        self.agent = Agent(self.world)

    def initialize_game(self):
        self.world.initialize_random_world()
        print("Game initialized with random world")

    def run_game(self, max_steps: int = 1000):
        step = 0
        while step < max_steps and self.world.agent_alive and not self.world.has_gold:
            self.agent.perceive_current_location()
            
            # Check if we found gold
            current_cell = self.world.grid[self.world.agent_pos.x][self.world.agent_pos.y]
            if EntityType.GOLD in current_cell.entities:
                self.world.has_gold = True
                self.world.score += 1000
                print("Gold found! Game won!")
                break

            # Make move
            move = self.agent.make_move()
            if move:
                new_pos = self.world.agent_pos + move.value
                self.world.agent_pos = new_pos
                self.agent.path_history.append(self.world.agent_pos)
                
                # Check if we died
                current_cell = self.world.grid[new_pos.x][new_pos.y]
                if EntityType.WUMPUS in current_cell.entities or EntityType.PIT in current_cell.entities:
                    self.world.agent_alive = False
                    self.world.score -= 1000
                    print("Agent died!")
                    break
                
                self.world.score -= 1  # Cost for each move
            else:
                print("No safe moves available!")
                break
            
            step += 1
        
        return self.world.score, self.world.has_gold, self.world.agent_alive
