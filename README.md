
## CSBK - Code Assessment
## About The Project
The project is basically a simple game writen in python language.
the game consist of a 2d graph which the coordinates are starting from the top left
and (y,x) coordinates instead of (x,y), players and items.
although this project has'nt reached to the graphing point but will explore any libraries that we can feed our data so we can visualize it better,
libraries like matplotlib etc.

### Built With

list of external and standard libraries used
* uuid - standard
* typing - standard
* fileinput - standard

<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

* python2 or python3
* virtualenv or system python environment .

_but its better to use virtualenv incase project is getting bigger_

### Instruction

create movement file with instructions

  ```sh
  
  
    GAME-START
    <Player>:<Direction>
    <Player>:<Direction>
    <Player>:<Direction>
    .
    .
    .
    GAME-END
  ```
example 

  ```sh
    GAME-START
    R:S
    R:S
    B:E
    G:N
    Y:N
    GAME-END
  ```
run
``` sh
    python main.py file.txt
```
