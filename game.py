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
        self.pieces.append(PieceLogic("WK", 2, 7))
        self.pieces.append(PieceLogic("BN", 3, 6))

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

        def move_puts_king_in_check():  # returns true if the given move indeed puts the king in check.
            king_code = "WK" if self.color_to_move == Color.WHITE else "BK"
            kingpiece = self.pieces[0]
            for piecelogic in self.pieces:
                if piecelogic.code == king_code:
                    kingpiece = piecelogic
                    break

            # check if the moving piece is the king:
            if kingpiece.x == from_square.x and kingpiece.y == from_square.y:
                # raise Exception(" TODO:not implemented yet ")
                return False

            # checking for when the moving piece is not the king itself
            else:
                # cases where the moving piece and the king are aligned row wise or column wise.
                if from_square.x == kingpiece.x:
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
                    # split into the four cases where the moving piece can be upper right, lower right, upper left, or lower left

                    # moving piece is to the upper right of the king:
                    if from_square.x > kingpiece.x and from_square.y > kingpiece.y:
                        for x in range(from_square.x, 7):
                            if from_square.y + x - from_square.x > 7:
                                return False
                            if get_piececode_given_square(x, from_square.y + x - from_square.x) == get_opponents_color() + "B" or \
                                get_piececode_given_square(x, from_square.y + x - from_square.x) == get_opponents_color() + "Q":
                                return True
                        return False

                    # moving piece is to the lower right of the king:
                    if from_square.x > kingpiece.x and from_square.y < kingpiece.y:
                        for x in range(from_square.x, 7):
                            if from_square.y + x - from_square.x < 0:
                                return False
                            if get_piececode_given_square(x, from_square.y - (x - from_square.x)) == get_opponents_color() + "B" or \
                                get_piececode_given_square(x, from_square.y - (x - from_square.x)) == get_opponents_color() + "Q":
                                return True
                        return False

                    # moving piece is to the upper left of the king:
                    if from_square.x < kingpiece.x and from_square.y > kingpiece.y:
                        for y in range(from_square.y, 7):
                            if from_square.x - (y - from_square.y) < 0:
                                return False
                            if get_piececode_given_square(from_square.x - (y - from_square.y), y) == get_opponents_color() + "B" or \
                                get_piececode_given_square(from_square.x - (y - from_square.y), y) == get_opponents_color() + "Q":
                                return True
                        return False

                    # moving piece is to the lower left of the king:
                    else:
                        for y in range(from_square.y, 0, -1):
                            if from_square.x - (from_square.y - y) < 0:
                                return False
                            if get_piececode_given_square(from_square.x - (from_square.y - y), y) == get_opponents_color() + "B" or \
                                get_piececode_given_square(from_square.x - (from_square.y - y), y) == get_opponents_color() + "W":
                                return True
                        return False

        piecetype = ""
        for piecelogic in self.pieces:
            if piecelogic.x == from_square.x and piecelogic.y == from_square.y:
                piecetype = piecelogic.code[1:]
                break

        match piecetype:
            case "B":  # bishop
                if abs(to_square.x - from_square.x) == abs(to_square.y - from_square.y) and \
                        0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and not move_puts_king_in_check():
                    return True
                return False
            case "K":  # king
                # TODO: CASTLING STILL HAS TO BE IMPLEMENTED
                if 0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and not move_puts_king_in_check() and \
                        abs(to_square.x - from_square.x) <= 1 and abs(to_square.y - from_square.y) <= 1:
                    return True
                return False
            case "N":  # Knight
                if 0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and \
                            ((abs(to_square.x - from_square.x) == 1 and abs(to_square.y - from_square.y) == 2) or
                             (abs(to_square.x - from_square.x) == 2 and abs(to_square.y - from_square.y) == 1)):
                    return True
                return False
            case "P":  # Pawn
                # EN PASSENT STILL HAS TO BE IMPLEMENTED
                if 0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and not move_puts_king_in_check() \
                        and abs(to_square.y - from_square.y) == 1 and not move_puts_king_in_check():
                    return True
                return False
            case "Q":  # Queen
                if 0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and not move_puts_king_in_check() and not move_puts_king_in_check():
                    return True
                return False
            case "R":  # Rook
                if 0 <= to_square.x <= 7 and 0 <= to_square.y <= 7 and (to_square.y == from_square.y ^ to_square.x == from_square.x) \
                        and not move_puts_king_in_check():
                    return True
                return False

    def move(self, from_square, to_square):  # moves a piece from from_square to to_square
        if not self.is_valid_move(from_square, to_square):
            raise Exception("you requested an invalid move")
        if not self.square_is_empty(to_square):
            self.take_on(to_square)
        for piece in self.pieces:
            if piece.x == from_square.x and piece.y == from_square.y:
                piece.x, piece.y = to_square.x, to_square.y
                break

    def take_on(self, square):
        piece = self.get_piece_from_square(square)
        self.pieces.remove(piece)
