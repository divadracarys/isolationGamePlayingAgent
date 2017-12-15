"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # Checking if we have won the game
    if game.is_winner(player):
        return float("inf")
    # Checking if we have lost the game
    if game.is_loser(player):
        return float("-inf")
    # improving readability of the code
    p_moves = game.get_legal_moves(player)
    o_moves = game.get_legal_moves(game.get_opponent(player))
    score = len(p_moves) - 2*len(o_moves)
    return float(score)



def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("inf")
    # Checking if we have lost the game
    if game.is_loser(player):
        return float("-inf")
    # improving readability of the code
    p_moves = game.get_legal_moves(player)
    o_moves = game.get_legal_moves(game.get_opponent(player))
    score = len(p_moves) - len(o_moves)
    return float(score)


def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if game.is_winner(player):
        return float("inf")
    # Checking if we have lost the game
    if game.is_loser(player):
        return float("-inf")
    # improving readability of the code
    p_moves = game.get_legal_moves(player)
    score = len(p_moves)
    return float(score)


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=20.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout
        

class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return best_move
    
    def terminal_test(self, game, depth):
        """
        True = game over for active player
        False = otherwise
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        """
        #Copying the timer check into the helper function
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if len(game.get_legal_moves()) == 0 or depth == 0:
            return True
        else: 
            return False
        
        
    def min_value(self, game, depth):
        """
        Return the value for a win (+1) if the game is over
        otherwise,
        Returns the min val over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game, depth):
            return self.score(game, self)
        bestScore = float("inf")
        for move in game.get_legal_moves():
            bestScore = min(bestScore, self.max_value(game.forecast_move(move), depth-1))
        return bestScore
    
    def max_value(self, game, depth):
        """
        Return the value for a loss (-1) if the game is over
        otherwise,
        Returns the max value over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game, depth):
            return self.score(game, self)
        bestScore = float("-inf")
        for move in game.get_legal_moves():
            bestScore = max(bestScore, self.min_value(game.forecast_move(move), depth-1))
        return bestScore
    
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # Implementation w/o depth limited search
        #return max(game.get_legal_moves(), key = lambda m: self.min_value(game.forecast_move(m)))
        bestScore = float('-inf') 
        availablemoves = game.get_legal_moves()
        bestMove = availablemoves[0] # if there are no legal moves
        if self.terminal_test(game, depth):
            return (-1, -1)
        for move in game.get_legal_moves():  
            v = self.min_value(game.forecast_move(move), depth-1)
            if v > bestScore:
                bestScore = v
                bestMove = move
        return bestMove
            
            


class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        bestMove = (-1, -1)
#        try:
#            # The try/except block will automatically catch the exception
#            # raised when the timer is about to expire.
#            return self.alphabeta(game, self.search_depth)
#
#        except SearchTimeout:
#            pass  # Handle any actions required after timeout as needed
#
#        # Return the best move from the last completed search iteration
#        return best_move


        depth = 1
        if len(game.get_legal_moves()) == 0:
            return bestMove
        try:
            # The search method call (alpha beta or minimax) should happen in
            # here in order to avoid timeout. The try/except block will
            # automatically catch the exception raised by the search method
            # when the timer gets close to expiring
            while True:
                bestMove = self.alphabeta(game, depth)
                depth += 1
            return bestMove

        except SearchTimeout:
            pass  # Handle any actions required after timeout as needed

        # Return the best move from the last completed search iteration
        return bestMove
        
    def terminal_test(self, game, depth):
        """
        True = game over for active player
        False = otherwise
        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).
        """
        #Copying the timer check into the helper function
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if len(game.get_legal_moves()) == 0 or depth == 0:
            return True
        else: 
            return False
        
        
    def min_value(self, game, alpha, beta, depth):
        """
        Return the value for a win (+1) if the game is over
        otherwise,
        Returns the min val over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game, depth):
            return self.score(game, self)
        bestScore = float("inf")
        for move in game.get_legal_moves():
            bestScore = min(bestScore, self.max_value(game.forecast_move(move), alpha, beta, depth-1))
            if bestScore <= alpha:
                return bestScore
            beta = min(beta, bestScore)
        return bestScore
    
    def max_value(self, game, alpha, beta, depth):
        """
        Return the value for a loss (-1) if the game is over
        otherwise,
        Returns the max value over all legal child nodes
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        if self.terminal_test(game, depth):
            return self.score(game, self)
        bestScore = float("-inf")
        for move in game.get_legal_moves():
            bestScore = max(bestScore, self.min_value(game.forecast_move(move), alpha, beta, depth-1))
            if bestScore >= beta:
                return bestScore
            alpha = max(alpha, bestScore)
        return bestScore
        
    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        # defining the helper functios for the above situation
        # Implementation w/o depth-limited search
        # return max(game.get_legal_moves(), key = lambda m: self.min_value(game.forecast_move(m), alpha, beta))
        bestScore = float('-inf') 
        availablemoves = game.get_legal_moves()
        bestMove = availablemoves[0] # if there are no legal moves
        if self.terminal_test(game, depth):
            return (-1, -1)
        for move in game.get_legal_moves():  
            v = self.min_value(game.forecast_move(move), alpha, beta, depth-1)
            if v > bestScore:
                bestScore = v
                bestMove = move
            # updating alpha
            alpha = max(alpha, bestScore)
        return bestMove
