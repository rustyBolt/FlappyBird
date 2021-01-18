if __name__ == "__main__":
    import src.Game as Game

    game = Game.Game(400, 800)
    e = Game.Event()
    e.events.addSubscriber(game, "collision")
    e.events.addSubscriber(game, "new")
    e.events.addSubscriber(game, "end")
    game.loop(e)
