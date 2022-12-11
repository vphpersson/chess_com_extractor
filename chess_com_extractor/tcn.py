from string import ascii_lowercase, ascii_uppercase, digits

from chess import Move, PieceType, PIECE_SYMBOLS


TCN_INDEX_STRING = ascii_lowercase + ascii_uppercase + digits + '!?{~}(^)[_]@#$,./&-*++='
TCN_PIECE_INDEX_STRING = 'qnrkbp'


def decode_tcn(tcn_string: str) -> list[Move]:

    moves: list[Move] = []

    for i in range(0, len(tcn_string), 2):
        from_value_index: int = TCN_INDEX_STRING.index(tcn_string[i])
        to_value_index: int = TCN_INDEX_STRING.index(tcn_string[i+1])

        promotion: PieceType | None = None
        drop: PieceType | None = None

        if to_value_index > 63:
            promotion = PIECE_SYMBOLS.index(TCN_PIECE_INDEX_STRING[(to_value_index - 64) // 3])
            to_value_index = from_value_index + (-8 if from_value_index < 16 else 8) + (to_value_index - 1) % 3 - 1

        if from_value_index > 75:
            drop = PIECE_SYMBOLS.index(TCN_PIECE_INDEX_STRING[from_value_index - 79])

        moves.append(
            Move(
                from_square=from_value_index,
                to_square=to_value_index,
                promotion=promotion,
                drop=drop
            )
        )

    return moves
