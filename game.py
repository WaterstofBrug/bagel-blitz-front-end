from enumerators import Color
from piece import PieceLogic
from board import Board
from copy import copy

"""
Game class stores and handles all the game state data.
"""


class Game:
    def __init__(self, history):
        self.color_to_move = Color.WHITE
        self.pieces = []
        self.history = history
        self.pieces_moved = {"WK": False, "BK": False, "WR-King-Side": False, "WR-Queen-Side": False,
                             "BR-King-Side": False, "BR-Queen-Side": False}
        self.win_state = "None"

    def add_pieces(self):
        pawns = [PieceLogic("WP", i, 1) for i in range(0, 8)] + [PieceLogic("BP", i, 6) for i in range(0, 8)]
        bischops = [PieceLogic("WB", 2, 0), PieceLogic("WB", 5, 0), PieceLogic("BB", 2, 7), PieceLogic("BB", 5, 7)]
        rooks = [PieceLogic("WR", 0, 0), PieceLogic("WR", 7, 0), PieceLogic("BR", 0, 7), PieceLogic("BR", 7, 7)]
        knights = [PieceLogic("WN", 1, 0), PieceLogic("WN", 6, 0), PieceLogic("BN", 1, 7), PieceLogic("BN", 6, 7)]
        kings = [PieceLogic("WK", 3, 0), PieceLogic("BK", 3, 7)]
        queens = [PieceLogic("WQ", 4, 0), PieceLogic("BQ", 4, 7)]


        self.pieces = pawns + bischops + rooks + knights + kings + queens

    def restart(self):
        self.history = []
        self.add_pieces()
        self.color_to_move = Color.WHITE
        for key in self.pieces_moved:
            self.pieces_moved[key] = False
        self.win_state = "None"

    def get_piece_from_square(self, square):  # returns the piece at the square given
        for piece in self.pieces:
            if piece.x == square.x and piece.y == square.y:
                return piece
        return None

    def square_is_empty(self, x, y):  # returns true iff there is no piece occupying the square
        for piecelogic in self.pieces:
            if piecelogic.x == x and piecelogic.y == y:
                return False
        return True

    def is_valid_location(self, x, y):
        return 0 <= x <= 7 and 0 <= y <= 7

    def get_piececode_given_square(self, x, y):  # returns the piece code given the pieces location,
        # if no piece is at the location it returns "EMPTY"
        for piece in self.pieces:
            if piece.x == x and piece.y == y:
                return piece.code
        return "EMPTY"

    def contains_given_piece(self, x, y, piece_code):
        return self.get_piececode_given_square(x, y) == piece_code

    def contains_given_pieces(self, x, y, piece_codes):
        for piece_code in piece_codes:
            if self.contains_given_piece(x, y, piece_code):
                return True
        return False

    def get_opponents_color(self):  # returns the first letter of the color of the team who is not to move.
        return "B" if self.color_to_move == Color.WHITE else "W"

    def get_players_color(self):
        return "W" if self.color_to_move == Color.WHITE else "B"

    def square_is_not_attacked(self, square_x, square_y):  # returns true if the given square is not under attack,
        # false otherwise

        # vertical line above given square
        opponents_color = self.get_opponents_color()
        players_color = self.get_players_color()

        if players_color == Color.WHITE:
            if self.contains_given_piece(square_x - 1, square_y + 1,opponents_color + "P") \
                    or self.contains_given_piece(square_x + 1, square_y + 1,opponents_color + "P"):
                return False
        else:
            if self.contains_given_piece(square_x - 1, square_y - 1,opponents_color + "P") \
                    or self.contains_given_piece(square_x + 1, square_y - 1,opponents_color + "P"):
                return False

        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0) and self.is_valid_location(square_x + i, square_y + j):
                    if self.contains_given_piece(square_x + i, square_y + j, opponents_color + "K"):
                        return False

        for y in range(square_y, 8):
            if not self.contains_given_pieces(square_x, y, [opponents_color + "R", opponents_color + "Q"]):
                if not self.contains_given_pieces(square_x, y, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # vertical line under given square
        for y in range(square_y, -1, -1):
            if not self.contains_given_pieces(square_x, y, [opponents_color + "R", opponents_color + "Q"]):
                if not self.contains_given_pieces(square_x, y, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # horizontal line to the right of the given square
        for x in range(square_x, 8):
            if not self.contains_given_pieces(x, square_y, [opponents_color + "R", opponents_color + "Q"]):
                if not self.contains_given_pieces(x, square_y, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # horizontal line to the left of the given square
        for x in range(square_x, -1, -1):
            if not self.contains_given_pieces(x, square_y, [opponents_color + "R", opponents_color + "Q"]):
                if not self.contains_given_pieces(x, square_y, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # diagonal line upper right
        for step in range(max(square_x, square_y), 8):
            if not self.contains_given_pieces(square_x + step - max(square_x, square_y),
                                              square_y + step - max(square_x, square_y),
                                              [opponents_color + "B", opponents_color + "Q"]):
                if not self.contains_given_pieces(square_x + step - max(square_x, square_y),
                                                  square_y + step - max(square_x, square_y),
                                                  ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # diagonal line lower right
        for step in range(0, min(7 - square_x, square_y) + 1):
            if not self.contains_given_pieces(square_x + step, square_y - step,
                                              [opponents_color + "B", opponents_color + "Q"]):
                if not self.contains_given_pieces(square_x + step, square_y - step, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # diagonal line upper left
        for step in range(0, min(square_x, 7 - square_y) + 1):
            if not self.contains_given_pieces(square_x - step, square_y + step,
                                              [opponents_color + "B", opponents_color + "Q"]):
                if not self.contains_given_pieces(square_x - step, square_y + step, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # diagonal line lower left
        for step in range(0, min(square_x, square_y) + 1):
            if not self.contains_given_pieces(square_x - step, square_y - step,
                                              [opponents_color + "B", opponents_color + "Q"]):
                if not self.contains_given_pieces(square_x - step, square_y - step, ["EMPTY", players_color + "K"]):
                    break
            else:
                return False

        # check for attacks of the horsies:
        if (self.is_valid_location(square_x + 2, square_y + 1) and  # possible location for horsie: +2, +1
            self.get_piececode_given_square(square_x + 2, square_y + 1) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x - 2, square_y + 1) and  # -2, +1
                    self.get_piececode_given_square(square_x - 2, square_y + 1) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x + 2, square_y - 1) and  # +2, -1
                    self.get_piececode_given_square(square_x + 2, square_y - 1) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x - 2, square_y - 1) and  # -2, -1
                    self.get_piececode_given_square(square_x - 2, square_y - 1) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x + 1, square_y + 2) and  # +1, +2
                    self.get_piececode_given_square(square_x + 1, square_y + 2) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x + 1, square_y - 2) and  # +1, -2
                    self.get_piececode_given_square(square_x + 1, square_y - 2) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x - 1, square_y + 2) and  # -1, +2
                    self.get_piececode_given_square(square_x - 1, square_y + 2) == self.get_opponents_color() + "N") \
                or (self.is_valid_location(square_x - 1, square_y - 2) and  # -1, -2
                    self.get_piececode_given_square(square_x - 1, square_y - 2) == self.get_opponents_color() + "N"):
            return False
        # if everything is clear, return true:
        return True

    def king_is_in_check(self):  # TODO: use this function to determine legal moves. (if you are in check you must
        # make a move such that you get out of check.
        king_code = "WK" if self.color_to_move == Color.WHITE else "BK"
        kingpiece = self.pieces[0]
        for piecelogic in self.pieces:
            if piecelogic.code == king_code:
                kingpiece = piecelogic
                break
        return not self.square_is_not_attacked(kingpiece.x, kingpiece.y)

    def passes_through_pieces(self, piecetype, from_square,
                              to_square):  # returns true if the move passes through pieces
        opponents_color = self.get_opponents_color()

        match piecetype:
            case "B":
                step_x = int((to_square.x - from_square.x) / abs(to_square.x - from_square.x))
                step_y = int((to_square.y - from_square.y) / abs(to_square.y - from_square.y))

                x = from_square.x
                y = from_square.y

                for step in range(0, abs(to_square.x - from_square.x) - 1):
                    x += step_x
                    y += step_y
                    if not self.square_is_empty(x, y):
                        return True
                return False
            case "R":
                if to_square.x - from_square.x == 0:  # horizontal movement
                    step_y = int((to_square.y - from_square.y) / abs(to_square.y - from_square.y))
                    for y in range(from_square.y + step_y, to_square.y, step_y):
                        if not self.square_is_empty(from_square.x, y):
                            return True
                else:  # vertical movement
                    step_x = int((to_square.x - from_square.x) / abs(to_square.x - from_square.x))
                    for x in range(from_square.x + step_x, to_square.x, step_x):
                        if not self.square_is_empty(x, from_square.y):
                            return True
                return False
            case "Q":
                if to_square.x - from_square.x == 0 or to_square.y - from_square.y == 0:  # rook-movement
                    return self.passes_through_pieces("R", from_square, to_square)
                else:  # bishop-movement
                    return self.passes_through_pieces("B", from_square, to_square)
            case "P":
                return self.passes_through_pieces("R", from_square, to_square)
            case _:
                return False

    def after_move_king_in_check(self, from_square, to_square):  # returns true if the king will be in check
        future_game = Game([])
        for piece_ in self.pieces:
            future_game.pieces.append(copy(piece_))
        future_game.color_to_move = self.color_to_move

        from_piece = self.get_piece_from_square(from_square)
        index_from_piece = self.pieces.index(from_piece)
        to_piece = self.get_piece_from_square(to_square)

        if to_piece is not None:
            index_to_piece = self.pieces.index(to_piece)
            if index_to_piece < index_from_piece:
                index_from_piece -= 1
            future_game.pieces.pop(index_to_piece)

        future_game.pieces[index_from_piece].x = to_square.x
        future_game.pieces[index_from_piece].y = to_square.y

        return future_game.king_is_in_check()

    def valid_castle(self, from_square, to_square, board):
        players_color = self.get_players_color()
        if not self.pieces_moved[players_color + "K"]:
            if from_square.y == to_square.y:
                if to_square.x - from_square.x == -2:  # king-side
                    return not self.pieces_moved[players_color + "R-King-Side"] \
                           and not self.passes_through_pieces("R", from_square, to_square) \
                           and not self.after_move_king_in_check(from_square,
                                                                 board.get_square(from_square.x - 1, from_square.y))
                elif to_square.x - from_square.x == 2:
                    return not self.pieces_moved[players_color + "R-Queen-Side"] \
                           and not self.passes_through_pieces("R", from_square, to_square) \
                           and not self.after_move_king_in_check(from_square,
                                                                 board.get_square(from_square.x + 1, from_square.y))
        return False

    def is_valid_move(self, from_square, to_square, board):  # returns true iff the move requested is allowed
        def basic_move_restriction():  # enforces basic move restrictions as playing the right color,
            # staying in the board, and making sure you are not in check.
            return self.is_valid_location(to_square.x, to_square.y) and not self.after_move_king_in_check(from_square,
                                                                                                          to_square) \
                   and self.color_to_move == piece.get_color()

        piece = self.get_piece_from_square(from_square)
        piecetype = piece.code[1:]

        match piecetype:
            case "B":  # bishop
                if abs(to_square.x - from_square.x) == abs(to_square.y - from_square.y):
                    return basic_move_restriction() and not self.passes_through_pieces("B", from_square, to_square)
                return False
            case "K":  # king
                if abs(to_square.x - from_square.x) <= 1 and abs(to_square.y - from_square.y) <= 1 or self.valid_castle(
                        from_square, to_square, board):
                    return basic_move_restriction()
                return False
            case "N":  # Knight
                if (abs(to_square.x - from_square.x) == 1 and abs(to_square.y - from_square.y) == 2) or \
                        (abs(to_square.x - from_square.x) == 2 and abs(to_square.y - from_square.y) == 1):
                    return basic_move_restriction()
                return False
            case "P":  # Pawn
                # TODO: EN PASSANT STILL HAS TO BE IMPLEMENTED
                def basic_pawn_move_check():
                    pawn_takes = abs(from_square.x - to_square.x) == 1 and not self.square_is_empty(to_square.x,
                                                                                                    to_square.y) and \
                                 self.get_piececode_given_square(to_square.x, to_square.y)[
                                     0] == self.get_opponents_color()
                    pawn_goes_straight = from_square.x == to_square.x
                    return (pawn_goes_straight and self.square_is_empty(to_square.x, to_square.y)) or pawn_takes

                if piece.get_color() == Color.WHITE:
                    if to_square.y - from_square.y == 1 and basic_pawn_move_check() or \
                            (to_square.y - from_square.y == 2 and from_square.y == 1 and from_square.x == to_square.x
                             and self.square_is_empty(to_square.x, to_square.y)):
                        return basic_move_restriction() and not self.passes_through_pieces("P", from_square, to_square)
                else:
                    if to_square.y - from_square.y == -1 and basic_pawn_move_check() or \
                            (to_square.y - from_square.y == -2 and from_square.y == 6 and from_square.x == to_square.x
                             and self.square_is_empty(to_square.x, to_square.y)):
                        return basic_move_restriction()
                return False
            case "Q":  # TODO: Queen
                if (to_square.y == from_square.y or to_square.x == from_square.x) or \
                        abs(to_square.x - from_square.x) == abs(to_square.y - from_square.y):
                    return basic_move_restriction() and not self.passes_through_pieces("Q", from_square, to_square)
                return False
            case "R":  # Rook
                if to_square.y == from_square.y or to_square.x == from_square.x:
                    return basic_move_restriction() and not self.passes_through_pieces("R", from_square, to_square)
                return False

    def move(self, from_square, to_square, board, ghost_move=False):  # moves a piece from from_square to to_square
        if not ghost_move:  # a ghost move means a move like moving the rook in a castle
            self.history.append(self.pieces)  # update history with board before move

        if not self.square_is_empty(to_square.x, to_square.y):  # taking a piece if it is in the new spot
            self.take_on(to_square)

        piece = self.get_piece_from_square(from_square)

        if piece.code[1] == "K" and self.valid_castle(from_square, to_square, board):
            players_color = self.get_players_color()
            if to_square.x - from_square.x == -2:  # king-side
                self.move(board.get_square(0, from_square.y), board.get_square(2, from_square.y), board,
                          ghost_move=True)
                pieceGUI = board.get_piece(board.get_square(0, from_square.y))
                pieceGUI.move_to(2, from_square.y)
            else:  # queen-side
                self.move(board.get_square(7, from_square.y), board.get_square(4, from_square.y), board,
                          ghost_move=True)
                pieceGUI = board.get_piece(board.get_square(7, from_square.y))
                pieceGUI.move_to(4, from_square.y)

        # handle movement status of kings and rooks concerning castling
        if piece.code[1] == "K":
            self.pieces_moved[piece.code] = True
        elif piece.code[1] == "WR":
            if piece.x == 0 and piece.y == 0:
                self.pieces_moved["WR-King-Side"] = True
            elif piece.x == 7 and piece.y == 0:
                self.pieces_moved["WR-Queen-Side"] = True
        elif piece.code[1] == "BR":
            if piece.x == 0 and piece.y == 7:
                self.pieces_moved["BR-King-Side"] = True
            elif piece.x == 7 and piece.y == 7:
                self.pieces_moved["BR-Queen-Side"] = True

        if to_square.y in (0, 7) and piece.code[1] == "P":
            guipiece = board.get_piece(board.get_square(from_square.x, from_square.y))
            guipiece.code = guipiece.code[0] + "Q"
            piece.code = piece.code[0] + "Q"
            guipiece.sprite = guipiece.load()
        piece.x, piece.y = to_square.x, to_square.y  # move the piece
        if not ghost_move:
            self.swap_color_to_move()  # give move to other color

    def swap_color_to_move(self):  # swaps the color of the to move
        if self.color_to_move == Color.WHITE:
            self.color_to_move = Color.BLACK
        else:
            self.color_to_move = Color.WHITE

    def take_on(self, square):
        piece = self.get_piece_from_square(square)
        self.pieces.remove(piece)

    def get_possible_moves_raw_inputs(self, piece_code, piece_x, piece_y,
                                      board):  # returns a list of possible moves concerning piece type and pieces on the board
        possible_moves = []

        current_square = board.get_square(piece_x, piece_y)

        piece_type = piece_code[1]

        match piece_type:
            case "K":
                for i in [-1, 0, 1]:
                    for j in [-1, 0, 1]:
                        if not (i == 0 and j == 0) and self.is_valid_move(current_square,
                                                                          board.get_square(piece_x + i, piece_y + j),
                                                                          board) \
                                and self.get_piececode_given_square(piece_x + i, piece_y + j)[0] != piece_code[0]:
                            possible_moves.append(board.get_square(piece_x + i, piece_y + j))
            case "R":
                # vertical line above given square
                for y in range(piece_y + 1, 8):
                    if self.is_valid_location(piece_x, y) and self.is_valid_move(current_square,
                                                                                 board.get_square(piece_x, y), board) \
                            and self.get_piececode_given_square(piece_x, y)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(piece_x, y))

                # vertical line under given square
                for y in range(piece_y - 1, -1, -1):
                    if self.is_valid_location(piece_x, y) and self.is_valid_move(current_square,
                                                                                 board.get_square(piece_x, y), board) \
                            and self.get_piececode_given_square(piece_x, y)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(piece_x, y))

                # horizontal line to the right of the given square
                for x in range(piece_x + 1, 8):
                    if self.is_valid_location(x, piece_y) and self.is_valid_move(current_square,
                                                                                 board.get_square(x, piece_y), board) \
                            and self.get_piececode_given_square(x, piece_y)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(x, piece_y))

                # horizontal line to the left of the given square
                for x in range(piece_x - 1, -1, -1):
                    if self.is_valid_location(x, piece_y) and self.is_valid_move(current_square,
                                                                                 board.get_square(x, piece_y), board) \
                            and self.get_piececode_given_square(x, piece_y)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(x, piece_y))
            case "B":
                # diagonal line upper right TODO; fix deze
                for step in range(1, min(7 - piece_x, 7 - piece_y) + 1, 1):
                    if self.is_valid_move(current_square, board.get_square(piece_x + step, piece_y + step), board) \
                            and self.get_piececode_given_square(piece_x + step, piece_y + step)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(piece_x + step, piece_y + step))

                # diagonal line lower right
                for step in range(1, min(7 - piece_x, piece_y) + 1):
                    if self.is_valid_move(current_square, board.get_square(piece_x + step, piece_y - step), board) \
                            and self.get_piececode_given_square(piece_x + step, piece_y - step)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(piece_x + step, piece_y - step))

                # diagonal line upper left
                for step in range(1, min(piece_x, 7 - piece_y) + 1):
                    if self.is_valid_move(current_square, board.get_square(piece_x - step, piece_y + step), board) \
                            and self.get_piececode_given_square(piece_x - step, piece_y + step)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(piece_x - step, piece_y + step))

                # diagonal line lower left
                for step in range(1, min(piece_x, piece_y) + 1):
                    if self.is_valid_move(current_square, board.get_square(piece_x - step, piece_y - step), board) \
                            and self.get_piececode_given_square(piece_x - step, piece_y - step)[0] != piece_code[0]:
                        possible_moves.append(board.get_square(piece_x - step, piece_y - step))
            case "Q":
                possible_moves = self.get_possible_moves_raw_inputs(piece_code[0] + "R", piece_x, piece_y, board) \
                                 + self.get_possible_moves_raw_inputs(piece_code[0] + "B", piece_x, piece_y, board)
            case "P":
                if piece_code[0] == "W":
                    moves_to_check = [(0, 1), (0, 2), (-1, 1), (1, 1)]
                else:
                    moves_to_check = [(0, -1), (0, -2), (-1, -1), (1, -1)]

                for move in moves_to_check:
                    if self.is_valid_location(piece_x + move[0], piece_y + move[1]) \
                            and self.is_valid_move(current_square,
                                                   board.get_square(piece_x + move[0], piece_y + move[1]), board) \
                            and self.get_piececode_given_square(piece_x + move[0], piece_y + move[1])[0] != piece_code[
                        0]:
                        possible_moves.append(board.get_square(piece_x + move[0], piece_y + move[1]))
            case "N":
                for i in [-1, 1]:
                    for j in [-1, 1]:
                        if self.is_valid_location(piece_x + 1 * i, piece_y + 2 * j) \
                                and self.is_valid_move(current_square,
                                                       board.get_square(piece_x + 1 * i, piece_y + 2 * j), board) \
                                and self.get_piececode_given_square(piece_x + 1 * i, piece_y + 2 * j)[0] != piece_code[
                            0]:
                            possible_moves.append(board.get_square(piece_x + 1 * i, piece_y + 2 * j))
                        if self.is_valid_location(piece_x + 2 * i, piece_y + 1 * j) \
                                and self.is_valid_move(current_square,
                                                       board.get_square(piece_x + 2 * i, piece_y + 1 * j), board) \
                                and self.get_piececode_given_square(piece_x + 2 * i, piece_y + 1 * j)[0] != piece_code[
                            0]:
                            possible_moves.append(board.get_square(piece_x + 2 * i, piece_y + 1 * j))
        return possible_moves

    def get_possible_moves(self, piece, board):
        return self.get_possible_moves_raw_inputs(piece.code, piece.x, piece.y, board)

    def has_possible_moves(self, piece, board):  # returns true iff a piece has a possible move
        return len(self.get_possible_moves(piece, board)) > 0

    def color_has_possible_moves(self, color, board):  # for White set color to "W", for Black: "B"
        for piece in self.pieces:
            if piece.code[0] == color and self.has_possible_moves(piece, board):
                return True
        return False

    def is_pat(self, color, board):  # color managed to draw with a stalemate
        return not self.king_is_in_check() and not self.color_has_possible_moves(color, board)

    def is_mat(self, color, board):  # color lost to a check mate
        return self.king_is_in_check() and not self.color_has_possible_moves(color, board)

    def set_winner(self, color, GUI):
        if color == "B":
            GUI.dispatch_win("WHITE")
        else:
            GUI.dispatch_win("BLACK")
