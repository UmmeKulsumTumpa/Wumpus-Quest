# # Game Controller
# from WumpusWorld import WumpusWorld
# from Agent import Agent
# from EntityType import EntityType
# from Position import Position

# class WumpusQuestGame:
#     def __init__(self, size: int = 10):
#         self.world = WumpusWorld(size)
#         self.agent = Agent(self.world)

#     def initialize_game(self):
#         self.world.initialize_random_world()
#         print("Game initialized with random world")

#     def run_game(self, max_steps: int = 1000):
#         step = 0
#         while step < max_steps and self.world.agent_alive and not self.world.has_gold:
#             self.agent.perceive_current_location()
            
#             # Check if we found gold
#             current_cell = self.world.grid[self.world.agent_pos.x][self.world.agent_pos.y]
#             if EntityType.GOLD in current_cell.entities:
#                 self.world.has_gold = True
#                 self.world.score += 1000
#                 print("Gold found! Game won!")
#                 break

#             # Make move
#             move = self.agent.make_move()
#             if move:
#                 new_pos = self.world.agent_pos + move.value
#                 self.world.agent_pos = new_pos
#                 self.agent.path_history.append(self.world.agent_pos)
                
#                 # Check if we died
#                 current_cell = self.world.grid[new_pos.x][new_pos.y]
#                 if EntityType.WUMPUS in current_cell.entities or EntityType.PIT in current_cell.entities:
#                     self.world.agent_alive = False
#                     self.world.score -= 1000
#                     print("Agent died!")
#                     break
                
#                 self.world.score -= 1  # Cost for each move
#             else:
#                 print("No safe moves available!")
#                 break
            
#             step += 1
        
#         return self.world.score, self.world.has_gold, self.world.agent_alive

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

<<<<<<< HEAD
    def print_world(self):
        print("\n=== Current World ===")
        for row in self.world.grid:
            for cell in row:
                if EntityType.PIT in cell.entities:
                    print("P", end=" ")
                elif EntityType.WUMPUS in cell.entities:
                    print("W", end=" ")
                elif EntityType.GOLD in cell.entities:
                    print("G", end=" ")
                else:
                    print("-", end=" ")
            print()

    def run_game(self, max_steps: int = 1000):
        step = 0
        f = open("output.txt", "w")

        f.write("\n=== Starting Game ===")

        while step < max_steps and self.world.agent_alive and not self.world.has_gold:
            f.write(f"\n\nStep {step + 1}:")
            f.write(f"\nAgent Position: ({self.world.agent_pos.x + 1}, {self.world.agent_pos.y + 1})")
            
            self.agent.perceive_current_location()
            current_cell = self.world.grid[self.world.agent_pos.x][self.world.agent_pos.y]
            
            # f.writete current perceptions
            perceptions = current_cell.entities
            if perceptions:
                f.write("\nAgent perceives: " + ", ".join([p.name for p in perceptions]))
            else:
                f.write("\nAgent perceives: Nothing")
            
            # Check if we found gold
            if EntityType.GOLD in current_cell.entities:
                self.world.has_gold = True
                self.world.score += 1000
                f.write("\n\nHurrah! Gold found! Game won!")
                break
=======
    def run_game(self):
        step = 0
        while not self.is_game_over():
            print(f"Step {step}:")
            print(f"Agent Position: {self.agent.position}")
            perceptions = self.world.get_perceptions(self.agent.position)
            print(f"Perceptions: {perceptions}")
            
            self.agent.update_knowledge(perceptions)
            print(f"Knowledge Base: {self.agent.knowledge_base}")
>>>>>>> f296204eef1607c279dffc35d0d61117133b94a7

            move = self.agent.make_move()
<<<<<<< HEAD
            if move:
                f.write(f"\nAgent moves: {move.name}")
                new_pos = self.world.agent_pos + move.value
                self.world.agent_pos = new_pos
                self.agent.path_history.append(self.world.agent_pos)
                
                # Check if we died
                current_cell = self.world.grid[new_pos.x][new_pos.y]
                if EntityType.WUMPUS in current_cell.entities or EntityType.PIT in current_cell.entities:
                    self.world.agent_alive = False
                    self.world.score -= 1000
                    f.write("\n\nOhh no! Agent died!")
                    break
                
                self.world.score -= 1  # Cost for each move
            else:
                f.write("\n\nAlas! No safe moves available!")
                break
=======
            print(f"Agent Move: {move}")
>>>>>>> f296204eef1607c279dffc35d0d61117133b94a7
            
            self.agent.move(move)
            step += 1
<<<<<<< HEAD
        
        f.write("\n\n=== Game Over ===")
        f.write(f"\nTotal Steps: {step}")
        f.write(f"\nFinal Score: {self.world.score}")
        f.write(f"\nHas Gold: {self.world.has_gold}")
        f.write(f"\nAgent Alive: {self.world.agent_alive}")
        return self.world.score, self.world.has_gold, self.world.agent_alive
=======
            print("-" * 20)

        print("Game Over")
        print(f"Final Score: {self.calculate_score()}")
        print(f"Agent Alive: {self.agent.is_alive}")
        print(f"Gold Found: {self.agent.has_gold}")

>>>>>>> f296204eef1607c279dffc35d0d61117133b94a7
