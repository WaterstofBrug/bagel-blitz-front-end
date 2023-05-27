from enumerators import Color
from piece import PieceLogic

"""
Game class stores and handles all the game state data.
"""


class Game:
    def __init__(self, history):
        self.color_to_move = Color.WHITE
        self.pieces = []
        self.history = history

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

    def get_piece_from_square(self, square):  # returns the piece at the square given
        for piece in self.pieces:
            if piece.x == square.x and piece.y == square.y:
                return piece
        return None

    def square_is_empty(self, selected_square):  # returns true iff there is no piece occupying the square
        for piecelogic in self.pieces:
            if piecelogic.x == selected_square.x and piecelogic.y == selected_square.y:
                return False
        return True

    def is_valid_move(self, from_square, to_square):  # returns true iff the move requested is allowed
        def get_opponents_color():  # returns the first letter of the color of the team who is not to move.
            return "B" if self.color_to_move == Color.WHITE else "W"

        def get_piececode_given_square(x, y):  # returns the piece code given the pieces location,
            # if no piece is at the location it returns "EMPTY"
            for piecelogic in self.pieces:
                if piecelogic.x == x and piecelogic.y == y:
                    return piecelogic.code
            return "EMPTY"

        def contains_given_piece(x, y, piece_code):
            return get_piececode_given_square(x, y) == piece_code

        def contains_given_pieces(x, y, piece_codes):
            for piece_code in piece_codes:
                if contains_given_piece(x, y, piece_code):
                    return True
            return False

        def square_is_not_attacked(square):  # returns true if the given square is not under attack, false otherwise
            # vertical line above given square
            opponents_color = get_opponents_color()
            for y in range(square.y, 8):
                if not contains_given_pieces(square.x, y, [opponents_color + "R", opponents_color + "Q"]):
                    if not contains_given_piece(square.x, y, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # vertical line under given square
            for y in range(square.y, -1, -1):
                if not contains_given_pieces(square.x, y, [opponents_color + "R", opponents_color + "Q"]):
                    if not contains_given_piece(square.x, y, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # horizontal line to the right of the given square
            for x in range(square.x, 8):
                if not contains_given_pieces(x, square.y, [opponents_color + "R", opponents_color + "Q"]):
                    if not contains_given_piece(x, square.y, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # horizontal line to the left of the given square
            for x in range(square.x, -1, -1):
                if not contains_given_pieces(x, square.y, [opponents_color + "R", opponents_color + "Q"]):
                    if not contains_given_piece(x, square.y, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # diagonal line upper right
            for step in range(max(square.x, square.y), 8):
                if not contains_given_pieces(square.x + step - max(square.x, square.y),
                                             square.y + step - max(square.x, square.y),
                                             [opponents_color + "B", opponents_color + "Q"]):
                    if not contains_given_piece(square.x + step - max(square.x, square.y),
                                                square.y + step - max(square.x, square.y), "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # diagonal line lower right
            for step in range(0, min(7 - square.x, square.y) + 1):
                if not contains_given_pieces(square.x + step, square.y - step,
                                             [opponents_color + "B", opponents_color + "Q"]):
                    if not contains_given_piece(square.x + step, square.y - step, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # diagonal line upper left
            for step in range(0, min(square.x, 7 - square.y) + 1):
                if not contains_given_pieces(square.x - step, square.y + step,
                                             [opponents_color + "B", opponents_color + "Q"]):
                    if not contains_given_piece(square.x - step, square.y + step, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # diagonal line lower left
            for step in range(0, min(square.x, square.y) + 1):
                if not contains_given_pieces(square.x - step, square.y - step,
                                             [opponents_color + "B", opponents_color + "Q"]):
                    if not contains_given_piece(square.x - step, square.y - step, "EMPTY"):
                        break
                    else:
                        continue
                else:
                    return False

            # check for attacks of the horsies:
            # if everything is clear, return true:
            return True

        def move_puts_king_in_check():  # returns true if the given move indeed puts the king in check.
            # STILL NEED TO CHECK FOR MOVING THORUGH PIECES.
            king_code = "WK" if self.color_to_move == Color.WHITE else "BK"
            kingpiece = self.pieces[0]
            for piecelogic in self.pieces:
                if piecelogic.code == king_code:
                    kingpiece = piecelogic
                    break

            # check if the moving piece is the king:
            if kingpiece.x == from_square.x and kingpiece.y == from_square.y:
                return not square_is_not_attacked(to_square)

            # checking for when the moving piece is not the king itself
            else:
                # cases where the moving piece and the king are aligned row wise or column wise.
                if from_square.x == kingpiece.x:
                    # if the piece remains in the same x it should be fine:
                    if to_square.x == from_square.x:
                        return False
                    else:
                        # checking when the moving piece is above the king.
                        if from_square.y > kingpiece.y:
                            for y in range(from_square.y, 7):
                                if get_piececode_given_square(from_square.x, y) == get_opponents_color() + "R" or \
                                        get_piececode_given_square(from_square.x, y) == get_opponents_color() + "Q":
                                    return True
                            return False
                        else:
                            for y in range(0, from_square.y):
                                if get_piececode_given_square(from_square.x, y) == get_opponents_color() + "R" or \
                                        get_piececode_given_square(from_square.x, y) == get_opponents_color() + "Q":
                                    return True
                            return False
                elif from_square.y == kingpiece.y:
                    # if piece remains in the same y it should be fine:
                    if to_square.y == from_square.y:
                        return False
                    else:
                        # checking when the moving piece is below the king.
                        if from_square.x > kingpiece.x:
                            for x in range(from_square.x, 7):
                                if get_piececode_given_square(x, from_square.y) == get_opponents_color() + "R" or \
                                        get_piececode_given_square(x, from_square.y) == get_opponents_color() + "Q":
                                    return True
                            return False
                        else:
                            for x in range(0, from_square.x):
                                if get_piececode_given_square(x, from_square.y) == get_opponents_color() + "R" or \
                                        get_piececode_given_square(x, from_square.y) == get_opponents_color() + "Q":
                                    return True
                            return False

                # case where the moving piece was aligned diagonally with the king.
                if abs(from_square.x - kingpiece.x) == abs(from_square.y - kingpiece.y):
                    # if the piece remains in the same diagonal it should be fine
                    if abs(from_square.x - kingpiece.x) == abs(to_square.x - from_square.x) == abs(
                            to_square.y - from_square.y):
                        return False
                    else:
                        # split into the four cases where the moving piece can be upper right, lower right, upper left, or lower left
                        # moving piece is to the upper right of the king:
                        if from_square.x > kingpiece.x and from_square.y > kingpiece.y:
                            for x in range(from_square.x, 7):
                                if from_square.y + x - from_square.x > 7:
                                    return False
                                if get_piececode_given_square(x,
                                                              from_square.y + x - from_square.x) == get_opponents_color() + "B" or \
                                        get_piececode_given_square(x,
                                                                   from_square.y + x - from_square.x) == get_opponents_color() + "Q":
                                    return True
                            return False

                        # moving piece is to the lower right of the king:
                        if from_square.x > kingpiece.x and from_square.y < kingpiece.y:
                            for x in range(from_square.x, 7):
                                if from_square.y + x - from_square.x < 0:
                                    return False
                                if get_piececode_given_square(x, from_square.y - (
                                        x - from_square.x)) == get_opponents_color() + "B" or \
                                        get_piececode_given_square(x, from_square.y - (
                                                x - from_square.x)) == get_opponents_color() + "Q":
                                    return True
                            return False

                        # moving piece is to the upper left of the king:
                        if from_square.x < kingpiece.x and from_square.y > kingpiece.y:
                            for y in range(from_square.y, 7):
                                if from_square.x - (y - from_square.y) < 0:
                                    return False
                                if get_piececode_given_square(from_square.x - (y - from_square.y),
                                                              y) == get_opponents_color() + "B" or \
                                        get_piececode_given_square(from_square.x - (y - from_square.y),
                                                                   y) == get_opponents_color() + "Q":
                                    return True
                            return False

                        # moving piece is to the lower left of the king:
                        else:
                            for y in range(from_square.y, 0, -1):
                                if from_square.x - (from_square.y - y) < 0:
                                    return False
                                if get_piececode_given_square(from_square.x - (from_square.y - y),
                                                              y) == get_opponents_color() + "B" or \
                                        get_piececode_given_square(from_square.x - (from_square.y - y),
                                                                   y) == get_opponents_color() + "W":
                                    return True
                            return False

        def basic_move_restriction():  # enforces basic move restrictions as playing with right the right color and staying in the board
            return 0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and not move_puts_king_in_check() \
                and self.color_to_move == piece.get_color()

        piece = self.get_piece_from_square(from_square)
        piecetype = piece.code[1:]

        match piecetype:
            case "B":  # bishop
                if abs(to_square.x - from_square.x) == abs(to_square.y - from_square.y):
                    return basic_move_restriction()
                return False
            case "K":  # king
                # TODO: CASTLING STILL HAS TO BE IMPLEMENTED
                if abs(to_square.x - from_square.x) <= 1 and abs(to_square.y - from_square.y) <= 1:
                    return basic_move_restriction()
                return False
            case "N":  # Knight
                if (abs(to_square.x - from_square.x) == 1 and abs(to_square.y - from_square.y) == 2) or \
                        (abs(to_square.x - from_square.x) == 2 and abs(to_square.y - from_square.y) == 1):
                    return basic_move_restriction()
                return False
            case "P":  # Pawn
                # TODO: EN PASSENT STILL HAS TO BE IMPLEMENTED
                def basic_pawn_move_check():
                    pawn_takes = abs(from_square.x - to_square.x) == 1 and not self.square_is_empty(to_square) and \
                                 get_piececode_given_square(to_square.x, to_square.y)[0] == get_opponents_color()
                    pawn_goes_straight = from_square.x == to_square.x
                    return (pawn_goes_straight and self.square_is_empty(to_square)) or pawn_takes

                if piece.get_color() == Color.WHITE:
                    if to_square.y - from_square.y == 1 and basic_pawn_move_check() or \
                            (to_square.y - from_square.y == 2 and from_square.y == 1 and from_square.x == to_square.x
                             and self.square_is_empty(to_square)):
                        return basic_move_restriction()
                else:
                    if to_square.y - from_square.y == -1 and basic_pawn_move_check() or \
                            (to_square.y - from_square.y == -2 and from_square.y == 6 and from_square.x == to_square.x
                             and self.square_is_empty(to_square)):
                        return basic_move_restriction()
                return False
            case "Q":  # TODO: Queen
                if (to_square.y == from_square.y or to_square.x == from_square.x) or \
                        abs(to_square.x - from_square.x) == abs(to_square.y - from_square.y):
                    return basic_move_restriction()
                return False
            case "R":  # Rook
                if to_square.y == from_square.y or to_square.x == from_square.x:
                    return basic_move_restriction()
                return False

    def move(self, from_square, to_square):  # moves a piece from from_square to to_square
        if not self.is_valid_move(from_square, to_square):
            raise Exception("you requested an invalid move")

        self.history.append(self.pieces)

        if not self.square_is_empty(to_square):
            self.take_on(to_square)
        for piece in self.pieces:
            if piece.x == from_square.x and piece.y == from_square.y:
                piece.x, piece.y = to_square.x, to_square.y
                break
        self.swap_color_to_move()

    def swap_color_to_move(self):  # swaps the color of the to move
        if self.color_to_move == Color.WHITE:
            self.color_to_move = Color.BLACK
        else:
            self.color_to_move = Color.WHITE

    def take_on(self, square):
        piece = self.get_piece_from_square(square)
        self.pieces.remove(piece)
