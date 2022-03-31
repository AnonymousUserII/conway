import os
from time import sleep
from copy import deepcopy

# Dimensions of fields
_HEIGHT: int = 30;
_LENGTH: int = 30;

# Quality of Life
_USE_EMOJIS: bool = True  # Won't show emojis if running windows
_AUTOSTOP: bool = True
_AUTOPLAY: bool = True
_REST_IN_SECONDS: float = 0.1

_GENERATION: int = 0


def strmap(map: list[list[bool]]) -> str:
    output: str = ""
    for x in map:
        for y in x:
            if y:
                output += '# ' if os.name == "nt" or not _USE_EMOJIS else '⬛️'
            else:
                output += '. ' if os.name == "nt" or not _USE_EMOJIS else '⬜️'
        output += '\n'
    
    return output


def will_be_alive(x: int, y: int, map: list[list[bool]]) -> True:
    alive_neighbours: int = 0
    x_bounds: set[int] = {-1 if x > 0 else 0, 0, 1 if (x < _HEIGHT - 1) else 0}
    y_bounds: set[int] = {-1 if y > 0 else 0, 0, 1 if (y < _LENGTH - 1) else 0}
    
    # Check for neighbours
    
    for x_offset in x_bounds:
        for y_offset in y_bounds:
            if map[x + x_offset][y + y_offset]:
                alive_neighbours += 1
    
    if map[x][y]:  # If tile is alive
        return alive_neighbours - 1 in [2, 3]  # Account for itself
    else:
        return alive_neighbours == 3


def next_round(map: list[list[bool]]) -> list[list[bool]]:
    old_map: list[list[bool]] = deepcopy(map)
    for x in range(_HEIGHT):
        for y in range(_LENGTH):
            map[x][y] = will_be_alive(x, y, old_map)
    global _GENERATION
    _GENERATION += 1
    return map


def starting_pattern() -> list[list[bool]]:
    """
    Put your customizations in here
    """
    # All cells are initially dead
    map = [[False for _ in range(_LENGTH)] for _ in range(_HEIGHT)]
    
    # Preset Glider
    map[5][3] = True
    map[5][4] = True
    map[5][5] = True
    map[4][5] = True
    map[3][4] = True
    
    return map


def main() -> None: 
    # Create starting map
    game_map: list[list[bool]] = starting_pattern()
    
    end_message: str
    if _AUTOSTOP:
        game_gens: list[list[list[bool]]] = [deepcopy(game_map)]  # Stores all maps during this simulation
    
    running: bool = True
    while running:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"Generation: {_GENERATION}")
        print(strmap(game_map))
        game_map = next_round(game_map)
        
        if _AUTOSTOP: 
            if game_map in game_gens:  # If specific map has already occurred, it will loop
                game_gens.append(deepcopy(game_map))
                print(strmap(game_map))
                end_message = "Game reached stable loop"
                running = False
            game_gens.append(deepcopy(game_map))
        if _AUTOPLAY:
            try:
                sleep(_REST_IN_SECONDS)
            except KeyboardInterrupt:
                end_message = "Player Suspended Process"
                running = False
        elif input():
            end_message = "Player Halted"
            running = False  # Stops if user inputs something to console
    
    print("Game Over\nReason:", end_message, "\nGeneration:", _GENERATION - 1)
    return None
    

if __name__ == "__main__":
    main()
    exit(0)
