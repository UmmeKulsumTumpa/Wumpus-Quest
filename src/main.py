from WumpusQuestGame import WumpusQuestGame

if __name__ == "__main__":
    game = WumpusQuestGame(10)
    # game.initialize_game_random()
    game.initialize_game_from_file("input4.txt")
    game.print_world()
    score, has_gold, is_alive = game.run_game()

    f = open("output.txt", "a")
    f.write(f"\nGame finished! Score: {score}, Has Gold: {has_gold}, Agent Alive: {is_alive}")