import os
from time import sleep
from copy import deepcopy

# Dimensions of fields
_LENGTH: int = 40;
_HEIGHT: int = 30;

# Quality of Life
_SHOW_EMOJIS: bool = True  # Won't show emojis if running windows
_AUTOSTOP: bool = False
_AUTOPLAY: bool = True
_REST_IN_SECONDS: float = 0.1


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
    game_map[4][0] = True
    game_map[4][1] = True
    game_map[5][0] = True
    game_map[5][1] = True
    
    game_map[2][34] = True
    game_map[2][35] = True
    game_map[3][34] = True
    game_map[3][35] = True
    
    game_map[0][24] = True
    game_map[1][24] = True
    game_map[5][24] = True
    game_map[6][24] = True
    game_map[1][22] = True
    game_map[5][22] = True
    game_map[2][21] = True
    game_map[3][21] = True
    game_map[4][21] = True
    game_map[2][20] = True
    game_map[3][20] = True
    game_map[4][20] = True
    
    game_map[5][17] = True
    game_map[4][16] = True
    game_map[5][16] = True
    game_map[6][16] = True
    game_map[3][15] = True
    game_map[7][15] = True
    game_map[5][14] = True
    game_map[2][13] = True
    game_map[8][13] = True
    game_map[2][12] = True
    game_map[8][12] = True
    game_map[3][11] = True
    game_map[7][11] = True
    game_map[4][10] = True
    game_map[5][10] = True
    game_map[6][10] = True
    
    
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
