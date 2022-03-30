import os
from time import sleep
from copy import deepcopy

# Dimensions of fields
_LENGTH: int = 40;
_HEIGHT: int = 30;

# Quality of Life
_SHOW_EMOJIS: bool = True  # Won't show emojis if running windows
_AUTOSTOP: bool = True
_AUTOPLAY: bool = True
_REST_IN_SECONDS: float = 1


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

    # Preset Glider Gun
    game_map[5][2] = True
    game_map[5][3] = True
    game_map[6][2] = True
    game_map[6][3] = True

    game_map[3][36] = True
    game_map[3][37] = True
    game_map[4][36] = True
    game_map[4][37] = True
    
    game_map[1][26] = True
    game_map[2][26] = True
    game_map[6][26] = True
    game_map[7][26] = True
    game_map[2][24] = True
    game_map[6][24] = True
    game_map[3][23] = True
    game_map[4][23] = True
    game_map[5][23] = True
    game_map[3][22] = True
    game_map[4][22] = True
    game_map[5][22] = True
    
    game_map[6][19] = True
    game_map[5][18] = True
    game_map[6][18] = True
    game_map[7][18] = True
    game_map[4][17] = True
    game_map[8][17] = True
    game_map[6][16] = True
    game_map[3][15] = True
    game_map[9][15] = True
    game_map[3][14] = True
    game_map[9][14] = True
    game_map[4][13] = True
    game_map[8][13] = True
    game_map[5][12] = True
    game_map[6][12] = True
    game_map[7][12] = True
    
    
    if _AUTOSTOP:
        game_history: list[list[list[bool]]] = [deepcopy(game_map)]  # Stores all maps during this simulation
    end_message: str
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(strmap(game_map))
        game_map = next_round(game_map)
        
        if _AUTOSTOP: 
            if game_map in game_history:  # If specific map has already occurred, it will loop
                end_message = "Game reached stable loop"
                break
            game_history.append(deepcopy(game_map))
        if _AUTOPLAY:
            sleep(_REST_IN_SECONDS)
        elif input():
            end_message = "Player Halted"
            break  # Stops if user inputs something
    
    print("Game Over\nReason:", end_message)
    return None
    

if __name__ == "__main__":
    main()
    exit(0)
