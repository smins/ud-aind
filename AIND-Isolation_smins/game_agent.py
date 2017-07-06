"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import math


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
    # Minimize the combined distance between the center of the other board
    # The idea is to keep to the center, but do not let the other player wall
    # you in - stay close enough to your opponent that he can't box you out, 
    # but prefer moves that are farther from the corners to avoid traps
    
    # Check win/loss conditions
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Find the center of the board
    center_width = game.width/2.0
    center_height = game.height/2.0
    
    # Find the player's position
    player_height, player_width = game.get_player_location(player)
    
    # Find the opponent's position
    opp_height, opp_width = game.get_player_location(game.get_opponent(player))
    
    # Find the NEGATIVE Square Euclidean distance to the other player, as we want
    # to prefer positions closer to our opponents
    oppdist = -((opp_height - player_height)**2 + (opp_width - player_width)**2)
    
    # Find the NEGATIVE Square Euclidean Distance to the center of the board, 
    # as we want to prefer positions closer to center
    centdist = -((center_height - player_height)**2 + (center_width - player_width)**2)
    
    # Prefer center positions more
    return float(oppdist + 1.75*centdist)


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
    # Stay-centered heuristic - by avoiding the corners of the board, 
    # we keep our options open & hopefully avoid being trapped.
    # Minimize the Squared Euclidean distance between the player 
    # & the center of the board, while still preferring moves that keep 
    # open the most possible moves
    
    # Check win/loss conditions
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")
    
    # Find the center of the board
    center_width, center_height = game.width/2.0, game.height/2.0
    
    # Find the player's position
    player_height, player_width = game.get_player_location(player)
    
    # Get the number of open moves
    moves = len(game.get_legal_moves(player))
    
    # Return the # of number of moves minus the Square Euclidean Distance to 
    # the center of the board, as we want to prefer positions closer to center 
    # but also prefer ones that leave open more moves
    return float(1.5*moves - ((abs(center_height - player_height)) + abs((center_width - player_width)**2)))


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
    # Create a composite score that blends preferring the center, preferring
    # moves with more descendants, and staying close to the opponent
    
    # Minimize the combined distance between the center of the other board
    # The idea is to keep to the center, but do not let the other player wall
    # you in - stay close enough to your opponent that he can't box you out.
    # While doing this, prefer moves with more open possibilities.
    
    # Check win/loss conditions
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    # Find the center of the board
    center_width = game.width/2.0
    center_height = game.height/2.0
    
    # Find the player's position
    player_height, player_width = game.get_player_location(player)
    
    # Find the opponent's position
    opp_height, opp_width = game.get_player_location(game.get_opponent(player))
    
    # Find the NEGATIVE Square Euclidean distance to the other player, as we want
    # to prefer positions closer to our opponents
    opp_score = -((opp_height - player_height)**2 + (opp_width - player_width)**2)
    
    # Find the NEGATIVE Square Euclidean Distance to the center of the board, 
    # as we want to prefer positions closer to center
    center_score = -((center_height - player_height)**2 + (center_width - player_width)**2)
    
    # Find the number of open moves
    move_score = len(game.get_legal_moves(player))
    
    # Combined
    
    return (1.5*move_score + 1.75*center_score + 0.7*opp_score)

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
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
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

        # Get the current player's legal moves
        legal_moves = game.get_legal_moves()
        
        # No remaining legal moves - is this a forfeit?
        if not legal_moves:
            return (-1, -1)
        
        """
        Begin the minimax calculation by calling min_value as the max player
        Note the "1" while calling min_value
        Note best_move is intialized OOB by the constructor to (-1, -1)
        We pass this because from the root, this is the first level searched
        """
        # Discard the util value & keep the move part of the tuple
        _, move = max([(self.min_value(game.forecast_move(m), 1), m) for m in legal_moves])

        return move
    
    
    def max_value(self, game, curr_depth):
        """
        Finds the move with the highest utility value for the current state by
        traversing the entire game tree.
        
        Assumes the opponent is rational & playing to MINIMIZE utility
        """
        # To avoid timing out
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
                        
        # Get the legal moves for the current player
        legal_moves = game.get_legal_moves()
            
        # If max depth is this level or no legal moves remain, 
        # return the utility of the current state
        if curr_depth == self.search_depth or len(legal_moves) == 0:
            return self.score(game, self)
        
        else:
            # Assume that the current branch has the worst possible utility
            # For MAX, this is the minimum value possible, -inf
            util = float("-inf")
            
            # Find the move that returns the MAX utility AFTER 
            # the opponent has moved. Increase the depth as we move down
            util = max(util, 
                       max([self.min_value(game.forecast_move(m), curr_depth+1) for m in legal_moves])
                       )
        
        return util
            
    
    def min_value(self, game, curr_depth):
        """
        Finds the move with the lowest utility value for the current state by
        traversing the entire game tree.
        
        Assumes the opponent is rational & playing to MAXIMIZE utility
        """
        # To avoid timing out
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        # Get the legal moves for the current player
        legal_moves = game.get_legal_moves()
            
        # If max depth is at this level or no legal moves remain, 
        # return the utility of the current state
        if curr_depth == self.search_depth or len(legal_moves) == 0:
            return self.score(game, self)
        
        else:
            # Assume that the current branch has the worst possible utility
            # For MIN, this is the maximum value possible, +inf
            util = float("inf")
            
            # Find the move that returns the MIN utility AFTER 
            # the opponent has moved. Increase the depth as we move down
            util = min(util, 
                       min([self.max_value(game.forecast_move(m), curr_depth+1) for m in legal_moves])
                       )
        
        return util
            

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
        best_move = (-1, -1)
        
        # Initialize depth and begin iterative deepening
        depth = 1

        while True:
            try:
                # Let alphabeta return, then increase the depth and re-search
                best_move = self.alphabeta(game, depth)
                depth += 1

            # Time's up, break the loop and return the best move
            except SearchTimeout:
                return best_move

        # We searched the entire tree before time was up, so return
        return best_move

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

        # Get the current player's legal moves
        legal_moves = game.get_legal_moves()
        
        # No remaining legal moves - is this a forfeit?
        if not legal_moves:
            return (-1, -1)
        
        """
        Begin the alphabeta calculation by calling ab_max_value as the root
        Note: Alpha and beta are initialized by the constructor to -inf/+inf
        Note the "1" while calling ab_min_value
        We pass this because from the root, this is the first level searched
        """
        # Initalize OOB / Worst Case
        best_move = (-1, -1)
        
        # Examine every child of the root becase we need to see at least one
        # leaf node of every subtree before pruning
        for move in legal_moves:
            util = self.ab_min_value(game.forecast_move(move), 1, alpha, beta)
            
            # New best-choice detected, update the lower bound
            if util >= alpha:
                best_move = move
                alpha = util
                
        return best_move
                
        
    def ab_max_value(self, game, curr_depth, alpha, beta):
        """
        Finds the move with the highest utility value for the current state by
        traversing the entire game tree.
        
        Uses alpha-beta pruning to prune branches of the tree that do not 
        need to be considered.
        
        Assumes the opponent is rational & playing to MINIMIZE utility
        """
        # To avoid timing out
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
                        
        # Get the legal moves for the current player
        legal_moves = game.get_legal_moves()
            
        # If max depth is this level or no legal moves remain, 
        # return the utility of the current state
        if curr_depth == self.search_depth or len(legal_moves) == 0:
            return self.score(game, self)
        
        else:
            # Assume that the current branch has the worst possible utility
            # For MAX, this is the minimum value possible, -inf
            util = float("-inf")
            
            # Looking at our legal moves, find one that returns the MAX utility of:
                # 1) the worst case scenario
                # 2) Our utility after MIN plays
            for m in legal_moves:
                util = max(
                        util, 
                        self.ab_min_value(game.forecast_move(m), curr_depth+1, alpha, beta)
                           )
            
                # If we find a move that is better for MAX than our beta value 
                # (MIN's best move seen during MAX's search), 
                # prune the remaining moves & return immediately
                if util >= beta:
                    return util
                
                # Update alpha and continue
                alpha = max(alpha, util)
        
        return util
            
    
    def ab_min_value(self, game, curr_depth, alpha, beta):
        """
        Finds the move with the lowest utility value for the current state by
        traversing the entire game tree.
        
        Uses alpha-beta pruning to prune branches of the tree that do not 
        need to be considered.
        
        Assumes the opponent is rational & playing to MAXIMIZE utility
        """
        # To avoid timing out
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
            
        # Get the legal moves for the current player
        legal_moves = game.get_legal_moves()
            
        # If max depth is at this level or no legal moves remain, 
        # return the utility of the current state
        if curr_depth == self.search_depth or len(legal_moves) == 0:
            return self.score(game, self)
        
        else:
            # Assume that the current branch has the worst possible utility
            # For MIN, this is the maximum value possible, +inf
            util = float("inf")
            
            # Looking at our legal moves, find one that returns the MIN utility of:
                # 1) the worst case scenario
                # 2) Our utility after MAX plays
            for m in legal_moves:
                util = min(
                        util, 
                        self.ab_max_value(game.forecast_move(m), curr_depth+1, alpha, beta)
                           )
                
                # If we find a move that is better for MIN than our alpha value 
                # (MAX's best move seen during MIN's search), 
                # prune the remaining moves & return immediately
                if util <= alpha:
                    return util
                
                # Update beta and continue
                beta = min(beta, util)
        
        return util
