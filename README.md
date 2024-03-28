There are 2 main methods I have created for implementation in a chess sense:
1. Alpha-Beta Pruning + Minimax algorithms, these work based on the valuations of the chess pieces and you can change how deep the algorithm searches
Making it 1 move is relatively weak, and the higher the algorithm searches the higher the elo rating, 4 plays at around 1000 elo, the higher it is the more the elo would be
2. Deep Q Learning, these work based on the number of games you play with it, so initially the moves are essentially random, but as the AI learns and starts to gain accuracy it plays moves
trained on the past games rather than playing random moves. This is more useful than method 1, when we have enough training. So as we are able to train this more and more,
the gameplay becomes better with the chess AI playing better. In the future, I hope to implement this algorithm into Lichess as a bot to play against, so other people/bots can be ran against
the bot to create mass training of the bot, making it drastically better than the method 1. I have attached both algorithms for you to use/analyze for whatever purposes. I will update this file
when the lichess code is done and the bot is available to play on lichess.
