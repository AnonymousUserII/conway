import os
from time import sleep
from copy import deepcopy

# Dimensions of fields
_LENGTH: int = 20;
_HEIGHT: int = 20;

# Quality of Life
_SHOW_EMOJIS: bool = True  # Won't show emojis if running windows
_AUTOPLAY: bool = True
_REST_IN_SECONDS: float = 0.3


def strmap(map: list[list[bool]]) -> str:
    output: str = ""
    for y in map:
        for x in y:
            if x:
                output += '#' if os.name == "nt" or not _SHOW_EMOJIS else '⬛️'
            else:
                output += '.' if os.name == "nt" or not _SHOW_EMOJIS else '⬜️'
        output += '\n'
    
    return output


def will_be_alive(x: int, y: int, map: list[list[bool]]) -> True:
    alive_neighbours: int = 0
    y_bounds: set[int] = {-1 if y > 0 else 0, 0, 1 if (y < _HEIGHT - 1) else 0}
    x_bounds: set[int] = {-1 if x > 0 else 0, 0, 1 if (x < _LENGTH - 1) else 0}
    
    # Check for neighbours
    for y_offset in y_bounds:
        for x_offset in x_bounds:
            if map[y + y_offset][x + x_offset]:
                alive_neighbours += 1
    
    if map[y][x]:  # If tile is alive
        return alive_neighbours - 1 in [2, 3]  # Account for itself
    else:
        return alive_neighbours == 3


def next_round(map: list[list[bool]]) -> list[list[bool]]:
    old_map: list[list[bool]] = deepcopy(map)
    for y in range(_HEIGHT):
        for x in range(_LENGTH):
            map[y][x] = will_be_alive(x, y, old_map)
            
    return map


def main() -> None: 
    # Set all initial tiles to dead
    game_map: list[list[bool]] = [[False for _ in range(_LENGTH)] for _ in range(_HEIGHT)]

    ## Presets
    # Glider 1
    game_map[7][8] = True
    game_map[8][6] = True
    game_map[8][8] = True
    game_map[9][7] = True
    game_map[9][8] = True
    
    # Glider 2
    game_map[12][8] = True
    game_map[13][6] = True
    game_map[13][8] = True
    game_map[14][7] = True
    game_map[14][8] = True
    
    # T-Piece
    game_map[4][5] = True
    game_map[5][3] = True
    game_map[5][4] = True
    game_map[5][5] = True
    
    game_history: list[list[list[bool]]] = [deepcopy(game_map)]  # Stores all maps during this simulation
    end_message: str
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(strmap(game_map))
        game_map = next_round(game_map)
        game_history.append(deepcopy(game_map))
        
        if game_map in game_history[:-1]:  # If specific map has already occurred, it will loop
            end_message = "Game reached stable loop"
            break
        elif _AUTOPLAY:
            sleep(_REST_IN_SECONDS)
        elif input():
            end_message = "Player Halted"
            break  # Stops if user inputs something
    
    print("Game Over\nReason:", end_message)
    return None
    

if __name__ == "__main__":
    main()
    exit(0)
