from WumpusQuestGame import WumpusQuestGame

if __name__ == "__main__":
    game = WumpusQuestGame(10)
    game.initialize_game()
    score, has_gold, is_alive = game.run_game()

    f = open("output.txt", "a")
    f.write(f"Game finished! Score: {score}, Has Gold: {has_gold}, Agent Alive: {is_alive}")