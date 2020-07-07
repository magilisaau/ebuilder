									Minecraft Build Assistant Document

​                                                                                      Magi, magilisaau@gmail.com, 2020.5.24

## Introduction

This is a source code written in JavaScript and Python which runs on Microsoft Minecraft EE(education edition), the initial purpose to start the project is to help my kids to build house more efficiently, thus they can pay more attention on the design of house rather than the building work.

Minecraft is one of the most popular game among kids around the world, it can run on PC, IPAD and xbox360.  In 2016, Microsoft released the education edition called Minecraft EE. Minecraft EE is not only a  game, but also an integrated development environment(IDE).  it can run  python, JavaScript and block language. 

 Minecraft EE 1.12.60(the latest version till now ) supports only a small subset of the python syntax called static python. variables must be initialized before used, classes can only be used as  data structure. it allows concurrency, but does NOT implement Lock or Semaphore. 

## Idea

When building a house,  players have to pile up the bricks one by one. for example, to build a wall of 20*10, they need to click the mouse 200 times.   and  some parts of a building are similar, it's a waste of time to build again.  Also sometimes we only want change the material or color other than tear down and rebuild.

Some senior players may use command-block to accelerate the building process,  but the command block are very unfriendly, see below

```
summon FallingSand ~ ~1 ~ {Time:1,Block:redstone_block,Riding:{id:FallingSand,Time:1,Block:command_block,TileEntityData:{Command:fill ~-1 ~-
```

*why are these commands not so friendly?*    1. too complex  2. do too much things in one command 

 In this project, I implement **three different user interface**:

1. **command line** , each command is designed with no parameter or at most one simple parameter.
2. **a graphical user interface**, you can use mouse only to do all the work
3. **a block language extension**, named *ebuilder*, for the kids who want to learn block language.

the relationship between them are 

![software structure](.\pic\soft_structure.png)



let's look at several concepts in the code first.

**block:**  blocks are the smallest unit of building, every type of block is represented by a number, for example, 0 represents for air, 1: stone, 2:  grass block, 9: water,  for detail please refer to  https://github.com/magilisaau/minecraft_buildAssistant/blob/master/blockid.py

**mark**: mark is a position on the map in game which you have marked for later use. Thinking about building a wall. First step, mark a place. Then, mark another place. At last, build a wall between two marks. in this project, <u>*mark is used to select a building or a space.*</u>

**enclosure**: in 2-D map, enclosure is the minimum bounding rectangle that contains all the marks, in 3-D map, enclosure is the minimum bounding cuboid that contains all the marks. 

## Features

```
mark a position on the map
remove a mark
pick a block for building
build wall 
let the wall higher
let the wall lower
build lines 
build cube
build hollow cube 
clone a space
replace old blocks to new blocks
show a ruler on the map
hide rulers
plant trees on the ground
```

## Files

---- custom.ts ,   the code in JavaScript to implement the extension/plugin of ebuilder

---- main.py,  	the code in python to implement command line and graphical user interface

---- main.ts,  	the code in JavaScript to implement command line and graphical user interface

---- block.py, 	to help user to look up the id of blocks, not included in the project compile.

---- buildAssistant.py,  the early python version of the project,  when python code exceed 400 line,  the prepare time will be very long, so it is abandoned and no longer maintained.  but it has been tested and can be used alone without custom.ts.  

## Import the code to your Minecraft game

As mentioned before, the code can only be used on Minecraft EE,   you can get the game from https://education.minecraft.net/get-started/download/ , after logging in the game, press C key on your keyboard to open the coder builder, then follow the steps below.

1. open your Code Builder in the Minecraft game, click import 

<img src=".\pic\import.png" style="zoom: 67%;" />



2. click Import URL

<img src=".\pic\import_url1.png" style="zoom:50%;" />

3. paste https://github.com/magilisaau/minecraft_buildAssistant 

<img src=".\pic\import_url2.png" style="zoom:50%;" />

4. if import code successfully, you will see a new extension called EBUILDER, if no, check your network.

<img src=".\pic\extension.png" style="zoom: 80%;" />

5. run the game

   <img src=".\pic\run.png" style="zoom:50%;" />

   6. you will see a group of special block to use to build house

      <img src=".\pic\run_successful.png" style="zoom:67%;" />



### Command Line Interface

to use command line, run the game and open the chat window (press T key on your keyboard), then input the command.  you can type "help" command to show the command list,  type "help mark" to show the detail of the mark command. all the command are as follows.

    ["mark","mark the position where the player standing"],
    ["mark2","compared with the mark cmd, it sticky to a block near the player"],
    ["umark","remove the last mark"],
    ["reset","hide and clear all marks"],
    ["wall","build walls between each two marks"],
    ["increase","increase n, increase n floors"],
    ["decrease","decrease n, decrease n floors"],
    ["line","build lines between each two marks"],
    ["clone","clone 0/1,clone the space enclosed by all marks to where the player stands,1:align 0: not align"],
    ["clear","clear the space enclosed by all marks"],
    ["replace","replace the old blocks enclosed by all marks to new blocks"],        
    ["setblock","setblock [id]: choose block [id] as building material"],
    ["setalign","setalign [0|1]: when setalign 1, the target position to clone into will align automatically"],
    ["blkmap","show a block map"],
    ["dbg","show all marks info"],
    ["cube","build a solid cube from marks"],
    ["hollowcube","build a hollow cube from marks"],
    ["plant","plant [tree] [interval]: plant trees on the ground, with intervals"],
    ["ruler","show ruler in the area enclosed by all marks"],
    ["hideruler","hide ruler in the area enclosed by all marks"],
    ["demo","run a demo"]



### Graphical User Interface

![](.\pic\ui2.png)

```
GOLDEN BOOTS: 	add a mark
DIAMOND_BOOTS: 	add a sticky mark
IRON BOOTS: 	umark/decrease a wall
GOLDEN SWORD:	 build a wall/ increase a wall
GOLDEN CARROT: 	choose a block
GOLDEN TORCH:	 replace
GOLDEN APPLE: 	clone
GOLDEN SHOVEL: 	clear
MELON: 			show ruler
GLISTERING MELON: hide ruler
GOLDEN_LEGGINGS: reset
```

**Pick a building block**:  before build a wall, you must choose what block to be used,  there are two ways to pick a block.  for example, if we use stone to build a wall, you can do as follows

```
way 1:  step 1) type T to open command box  
        step 2) input setblock 1 (note: 1 represents for the blockid of stone)         

way 2:  step 1) place a stone block on the ground
        step 2) stand on the stone         
        step 3) right-click the golden carrot
```

 

### Examples

**Build a wall:**  

```
way 1
step 1) input command "setblock 3"
step 2) input command "mark", then let the player move to another position
step 3) input command "mark"
step 4) input command "wall"
```

```
way 2
step 1) right-click the golden carrot to pick a block
step 2) add a mark by right-click golden boots
step 3) move to other position and add the second mark by right-click golden boots 
step 4) right-click the golden sword
```



**Clone a wall:**

```
1. right-click the golden boots to add the first mark, and move to a new place
2. right-click the golden boots to add the second mark, then move to the place
3. right-click the golden apple to clone the wall to the new place
```

**Replace a type of block to another on a wall**

```
1. pick a new block by right-click golden boots
2. move to the front of the wall
3. put a torch to one of the block to replace in front of you
```



### Co-development

if you are interested in the project and would like to develop new features, please send email to magilisaau@gmail.com and tell me your github account , I will add your account to the project. 



### 