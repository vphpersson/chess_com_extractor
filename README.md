# chess_com_extractor

Extract information from Chess.com.

## extract_archived_games.py

### Usage

```
$ ./extract_archived_games.py --help
usage: extract_archived_games.py [-h] [--player-name PLAYER_NAME] username password

Extract archived games of a player from Chess.com.

positional arguments:
  username              The username with which to authenticate.
  password              The password with which to authenticate.

optional arguments:
  -h, --help            show this help message and exit
  --player-name PLAYER_NAME
                        The name of the player whose games to extract. Defaults to the logged-in user.
```

#### Example

```shell
$ ./extract_archived_games.py 'USERNAME' 'PASSWORD' --player-name 'virrevvv' | jq '.'
```

**Output:**

```javascript
[
  {
    "name": "Live Chess",
    "gameId": 13026220933,
    "startDate": 1619287458,
    "player1Name": "virrevvv",
    "player2Name": "kattsaros",
    "timeControl": "600",
    "tcnMoves": "mC0Kbs5QfH9ziq",
    "moveTimestamps": "5998,5970,5975,5864,5908,5789,5806,5369",
    "initialSetup": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
    "variant": "Standard Chess",
    "player1ResultID": 1,
    "player2ResultID": 6,
    "round": "-",
    "firstMovePly": 1,
    "variantId": 1,
    "whiteRating": 982,
    "blackRating": 779,
    "endTime": "11:04:18 PDT"
  },
  ...
]
```

You can also parse the `tcnMoves` field into `python-chess` `Move`s using the `decode_tcn` included in this library.

:thumbsup:

## Implementation references

- [jschessengine.min.5ea1f76f.js](https://www.chess.com/bundles/app/js/vendor/jschessengine/jschessengine.min.5ea1f76f.js) - The JavaScript file that includes the original TCN decoder function, `decodeTCN`, that I ported.
