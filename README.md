									Minecraft Build Assistant Document

​                                                                                      magilisaau@gmail.com, 2020.5.24

## Introduction

This is a source code written in python running on Minecraft EE, the initial purpose is to help my kids to build block-house in the game more efficiently, thus they can pay more attention on the design of house rather than the building work.

Minecraft is one of the most popular game among kids around the world, it can runs on PC, mobile devices, and xbox360.  In 2016, Microsoft released the education edition called Minecraft EE. Minecraft EE is not only a  game, but also an integrated development environment for kids to learn computer programming. it can run  python, javascript and Graphical blocks language. 

 Minecraft EE 1.12.60(the latest version till now ) supports only a small subset of the python syntax called static python. variables must be initialized before used, classes can only be used as  data structure. it allows concurrency, but does NOT implement Lock or Semaphore. I guess the reason is to provide the same language features as the blocks language.  I expect Minecraft to provide more features of the language in the future. 

## BuildAssitant

before start, let's look at several concepts in the code

**block:**  blocks are the smallest unit of building, every type of block is represented by a number, for example, 0 represents for air, 1: stone, 2:  grass block, 9: water,  for detail please refer to  https://github.com/magilisaau/minecraft_buildAssistant/blob/master/blockid.py

**mark**: mark is a position on the map in game which you have marked for later use. Thinking about building a wall. First step, mark a place. Then, mark another place. At last, build a wall between two marks.

**enclosure**: in 2-D map, enclosure is the minimum bounding rectangle that contains all the marks, in 3-D map, enclosure is the minimum bounding cuboid that contains all the marks.

## How to use

As mentioned before, the code can only be used on Minecraft EE,   you can get it from https://education.minecraft.net/get-started/download/ , after logging in the game, press C key on your keyboard to open the coder builder,  create a new project , switch to python,  copy the content of  https://github.com/magilisaau/minecraft_buildAssistant/blob/master/buildAssistant.py , then click the run button.

There are two ways to use this tool, the command line interface, and the graphical user interface

### command line interface

to use command line, run the game and open the chat window (press T key on your keyboard), then input the command.  you can type "help" command to show the command list,  type "help mark" to show the detail of the mark command. all the command are as follows.

    ["mark","mark the position where the player is standing"],
    ["umark","remove the last mark"],
    ["wall","build walls between every two adjacent marks"],
    ["addfloor [n]","add n floors on the wall, used after the cmd "wall" "],
    ["delfloor [n]","remove n floors of the wall"  ],
    ["clone","clone the cubic space enclosed by marks into place where the player standing"],
    ["clear","clear the cubic space enclosed by marks"],
    ["replace","replace the old blocks enclosed by marks to new blocks"],     
    ["reset","commit changes and clear marks"],
    ["cube","build a solid cube from marks"],
    ["hollowcube","build a hollow cube from marks"],
    ["plant [tree] [interval]","plant trees on the groud with interval between trees"],
    ["setblock [id]",set block [id] as the building block"],
    ["setnewblock [id]", set block [id] as the new block in cmd "replace"]
    ["setalign [0|1]"," when setalign 1, the position to clone will align automatically"],
    ["blkmap","show a block map"],
    ["dbg","show the marks"],
    ["demo","run a demo to build a wall"]


Example1:  





The code consists of three sections:

- ​	section 1: basic function, they are independent and can be reused in other project easily. 
- ​	section 2: a command line interface, which can be used in your own script
- ​	section 3: a graphical user interface, this is for the players, with the aid of this, they can accelerate the   building process using mouse, and don't care about the code.

### 





