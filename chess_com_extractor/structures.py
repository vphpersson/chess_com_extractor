from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from pyutils.my_dataclasses import JsonDataclass
from chess import Move

from chess_com_extractor.tcn import decode_tcn


@dataclass
class ArchivedGameEntry:
    game_id: str
    game_type: str


@dataclass
class PGNInfo(JsonDataclass):
    name: str
    game_id: int
    start_date: datetime
    player1_name: str
    player2_name: str
    time_control: int
    tcn_moves: str
    move_timestamps: tuple[int]
    initial_setup: str
    variant: str
    player1_result_id: int
    player2_result_id: int
    round: str
    first_move_ply: int
    variant_id: int
    white_rating: int
    black_rating: int
    # NOTE: It appears this is always equivalent to `start_date`...
    end_time: datetime

    @property
    def moves(self) -> list[Move]:
        return decode_tcn(tcn_string=self.tcn_moves)

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> PGNInfo:
        json_object['start_date'] = datetime.fromtimestamp(json_object.pop('startDate')).astimezone(tz=timezone.utc)
        json_object['time_control'] = int(json_object.pop('timeControl'))
        json_object['move_timestamps'] = tuple(
            int(move_timestamp)
            for move_timestamp in json_object.pop('moveTimestamps').split(',')
        )

        json_object['end_time']: datetime = datetime.strptime(
            json_object.pop('endTime').split()[0],
            '%H:%M:%S'
        ).replace(
            year=json_object['start_date'].year,
            month=json_object['start_date'].month,
            day=json_object['start_date'].day,
            tzinfo=ZoneInfo('America/Los_Angeles')
        ).astimezone(tz=timezone.utc)

        if json_object['end_time'] < json_object['start_date']:
            latest_end_datetime: datetime = json_object['start_date'] + timedelta(seconds=json_object['time_control'])

            json_object['end_time'].replace(
                year=latest_end_datetime.year,
                month=latest_end_datetime.month,
                day=latest_end_datetime.day,

            )

        return super().from_json(json_object=json_object)
