'''
Author: Magi
Contact: magilisaau@gmail.com
ModifyTime: 2020/5/10
Description: 
'''


################################ section one #################################################
'''
section one are fundermental lib for process one-level marks
the functions in section one can only be called by section two and section three
the functions in section one can NOT call the functions in section two and section three
'''
def detect_block_on_foot():
    agent.teleport_to_player()
    what=agent.inspect(AgentInspection.BLOCK, DOWN)
    for i in range(1,16):
        detail=65536*i+what
        if blocks.test_for_block(detail,pos(0,-1,0)):
            return detail
    return what

def detect_block_at_pos(position:Position):
    agent.teleport(position.add(pos(0,1,0)),WEST)
    what=agent.inspect(AgentInspection.BLOCK, DOWN)
    for i in range(1,16):
        detail=65536*i+what
        if blocks.test_for_block(detail,pos(0,-1,0)):
            return detail
    return what
# build_line: some auxiliary lines which help to locate
#line_blk=REDSTONE_TORCH
mark_blk=TOP_SNOW
#linesize=5
def add_build_line(curpos=pos(0, 0, 0),line_blk=REDSTONE_TORCH, linesize=5):
    if blocks.test_for_block(AIR, curpos.add(pos(0, -1, 0))): return
    blocks.replace(line_blk, AIR, curpos.add(pos(-linesize, 0, 0)), curpos.add(pos(linesize, 0, 0)))
    blocks.replace(line_blk, AIR, curpos.add(pos(0, 0, -linesize)), curpos.add(pos(0, 0, linesize)))


def del_build_line(curpos=pos(0, 0, 0),line_blk=REDSTONE_TORCH,linesize=5):
    if blocks.test_for_block(AIR, curpos.add(pos(0, -1, 0))): return
    blocks.replace(AIR, line_blk, curpos.add(pos(-linesize, 0, 0)), curpos.add(pos(linesize, 0, 0)))
    blocks.replace(AIR, line_blk, curpos.add(pos(0, 0, -linesize)), curpos.add(pos(0, 0, linesize)))
# caculate the cube space the marks occupy
def get_enclosure_from_marks(marks):
    mark = pos(0, 0, 0)
    mark = marks[0]
    x1 = mark.get_value(Axis.X);
    y1 = mark.get_value(Axis.Y);
    z1 = mark.get_value(Axis.Z)
    x2 = x1;
    y2 = y1;
    z2 = z1
    for x in marks:
        mark = x
        if mark.get_value(Axis.X) < x1:
            x1 = mark.get_value(Axis.X)
        if mark.get_value(Axis.X) > x2:
            x2 = mark.get_value(Axis.X)

        if mark.get_value(Axis.Y) < y1:
            y1 = mark.get_value(Axis.Y)
        if mark.get_value(Axis.Y) > y2:
            y2 = mark.get_value(Axis.Y)

        if mark.get_value(Axis.Z) < z1:
            z1 = mark.get_value(Axis.Z)
        if mark.get_value(Axis.Z) > z2:
            z2 = mark.get_value(Axis.Z)
    return [world(x1, y1, z1), world(x2, y2, z2)]

# add mark
def push_mark(marks=[pos(0, 0, 0)]):
    curpos = player.position()
    marks.append(curpos)
    add_build_line(curpos)
    blocks.place(mark_blk, curpos)

# undo last added mark
def pop_mark(marks=[pos(0, 0, 0)]):
    size = len(marks)
    if size == 0: return
    #curpos = pos(0, 0, 0)
    prepos = None #pos(0, 0, 0)
    curpos = marks[size - 1]
    del_build_line(curpos)
    if size >= 2:
        prepos = marks[size - 2]
        blocks.fill(AIR, marks[size - 1], marks[size - 2])
        add_build_line(prepos)
        blocks.place(mark_blk, marks[size - 2])
    elif size == 1:
        blocks.place(AIR, marks[size - 1])
    marks.pop()

# build wall from a serial of adjacent marks
def build_wall_from_marks(marks=[pos(0, 0, 0)], block=GRASS, high: int = 0):
    size = len(marks)
    if size < 2: return False
    start = marks[0]
    for i in range(1, size):
        end = marks[i]
        blocks.fill(block, start, end)
        start = marks[i]
    for x in marks:
        del_build_line(x)
    return True

# clear all marks of all levels
def clear_marks(marks=[pos(0, 0, 0)]):    
    while (len(marks)):
        marks.pop()

# clone from the cube space enclosed by all marks
def clone_from_marks(marks=[],into:Position=player.position(),align:bool=True):
    if len(marks) < 2: return None
    closure = get_enclosure_from_marks(marks)
    start = closure[0]
    end = closure[1]
    x1 = start.get_value(Axis.X); x2 = end.get_value(Axis.X)
    y1 = start.get_value(Axis.Y); y2 = end.get_value(Axis.Y)
    z1 = start.get_value(Axis.Z); z2 = end.get_value(Axis.Z)
    x = into.get_value(Axis.X); y = into.get_value(Axis.Y); z = into.get_value(Axis.Z)
    _into = into
    if align:
        xin=False; zin=False
        if x >= x1 and x <= x2:
            xin = True
        if z >= z1 and z <= z2:
            zin = True
        if xin and zin:
            _into = world(x1,y,z1)
        if xin and not zin:
            _into = world(x1,y,z)
        if not xin and zin:
            _into = world(x,y,z1)
    blocks.clone(start, end,_into, CloneMask.REPLACE, CloneMode.NORMAL)
    return _into.add(pos(0,y2-y1+1,0))

def replace_from_marks(marks=[],newblk:int=GRASS, oldblk:int=GRASS):
    if len(marks) < 2: return
    closure = get_enclosure_from_marks(marks)
    start = closure[0]
    end = closure[1]
    blocks.replace(newblk, oldblk, start, end)

def clear_from_marks(marks=[]):
    if len(marks) < 2: return
    closure = get_enclosure_from_marks(marks)
    start = closure[0]
    end = closure[1]
    blocks.fill(AIR,start, end)   

def get_relative_pos(orientation:number,origin:Position,direction:number):
    newpos:Position = None
    real_orient:int = orientation
    if direction == UP:
        newpos=origin.add(pos(0,1,0))
        return newpos
    if direction == DOWN:
        newpos=origin.add(pos(0,-1,0))
        return newpos
    if direction == BACK:
        real_orient += 180
    elif direction == LEFT:
        real_orient += -90
    elif direction == RIGHT:
        real_orient += 90
    #revise
    if 180 == real_orient:
        real_orient = -180
    elif 270 == real_orient:
        real_orient = -90
    elif -270 == real_orient:
        real_orient = 90
    #
    if real_orient == 0:
        newpos=origin.add(pos(0,0,1))
    elif real_orient == -180:
        newpos=origin.add(pos(0,0,-1))
    elif real_orient == -90:
        newpos=origin.add(pos(1,0,0))
    elif real_orient == 90:
        newpos=origin.add(pos(-1,0,0))
    return newpos
#
def build_cube_from_marks(marks,block:number):
    if len(marks) < 2: return
    closure = get_enclosure_from_marks(marks)
    start = closure[0]
    end = closure[1]
    blocks.fill(block, start, end)    
    pass
#
def build_hollow_cube_from_marks(marks,block:number):
    if len(marks) < 2: return
    closure = get_enclosure_from_marks(marks)
    start = closure[0]
    end = closure[1]
    blocks.fill(block, start, end,FillOperation.HOLLOW)
    pass
################################ section two ###################################################
def on_mark():
    if BuildState.buildstate==BuildState.DONE: 
        on_reset()         
    push_mark(marksarray[len(marksarray) - 1])
def on_mark_handle():
    on_mark()
player.on_chat("mark", on_mark_handle)

#
def on_unmark():
    if BuildState.buildstate==BuildState.READY:
        pop_mark(marksarray[len(marksarray) - 1])
    if BuildState.buildstate==BuildState.DONE:
        on_del_one_level(1)

def on_unmark_handle():
    on_unmark()
player.on_chat("unmark", on_unmark_handle)

#
def on_build_wall(high: int = 1):
    if BuildState.buildstate==BuildState.READY:
        size = len(marksarray)
        marks = marksarray[size - 1]
        if len(marks)<2: return
        build_wall_from_marks(marks, block, high)
        BuildState.buildstate=BuildState.DONE
    elif BuildState.buildstate==BuildState.DONE:
        on_add_one_level()

def on_build_wall_handle(high: int = 0):
    on_build_wall(high)
player.on_chat("wall", on_build_wall_handle)

def on_build_cube():
    size = len(marksarray)
    marks = marksarray[size - 1]
    if len(marks)<2: return 
    build_cube_from_marks(marks,block)
def on_build_cube_handle(high: int = 0):
    on_build_cube()
player.on_chat("cube", on_build_cube_handle)

def on_build__hollow_cube():
    size = len(marksarray)
    marks = marksarray[size - 1]
    if len(marks)<2: return 
    build_hollow_cube_from_marks(marks,block)
def on_build__hollow_cube_handle(high: int = 0):
    on_build__hollow_cube()
player.on_chat("hollowcube", on_build__hollow_cube_handle)

#
def on_reset():
    global marksarray
    if BuildState.buildstate==BuildState.READY:
        marks=marksarray[len(marksarray)-1]
        for x in marks: del_build_line(x)
    marksarray = [[pos(0, 0, 0), ], ]
    #stupid code below by magi,2020.5.10
    temp = [pos(0, 0, 0)]
    temp = marksarray[0]
    temp.pop()
    BuildState.buildstate=BuildState.READY
def on_reset_handle():
    on_reset()
player.on_chat("reset", on_reset_handle)
#
def on_show_block():
    player.say("block="+str(block))
player.on_chat("showblock", on_show_block)

# process add one level cmd
def on_add_one_level():
    marks = marksarray[len(marksarray) - 1]
    if len(marks)==0: return
    floor = pos(0, 0, 0)
    ceil = pos(0, 0, 0)
    closure = get_enclosure_from_marks(marks)
    floor = closure[0]
    ceil = closure[1]
    dy = ceil.get_value(Axis.Y) - floor.get_value(Axis.Y) + 1
    newmarks = [pos(0, 0, 0)]
    newmarks.pop()
    for x in marks:
        newmarks.append(x.add(pos(0, dy, 0)))
    marksarray.append(newmarks)
    build_wall_from_marks(newmarks,block,1)

def on_add_one_level_handle():
    on_add_one_level()
player.on_chat("addlevel", on_add_one_level_handle)

#process del one level cmd
def on_del_one_level(high: int = 0):
    marks= marksarray[len(marksarray) - 1]
    build_wall_from_marks(marks,AIR,1)
    if len(marksarray) >1:
        marksarray.pop()
    else:
        clear_marks(marks)
def on_del_one_level_handle():
    on_del_one_level()
player.on_chat("dellevel", on_del_one_level_handle)

#process clone from marks cmd
def on_clone():
    newpos =clone_from_marks(marksarray[len(marksarray) - 1])
    if newpos: player.teleport(newpos)
    player.say("clone")

def on_clone_handle():
    on_clone()
player.on_chat("clone", on_clone_handle)

# config the type of block to build
def on_set_blk(blk:int):
    global block
    #strblk=""
    block=blk
    player.say("set block to " + str(blk))
player.on_chat("setblock", on_set_blk)

#config build mode on/off
def on_set_build_mode(mode: int):
    global buildmode
    buildmode = mode
    if buildmode == 0:
        player.say("build mode off")
    else:
        player.say("build mode on ")
player.on_chat("buildmode", on_set_build_mode)

# check build mode
def check_build_mode():
    global buildmode
    return True if buildmode == 1 else False
    
#show marks,print each level of marks
def on_debug():
    for marks in marksarray:
        strr=""
        for mark in marks:
            strr+="("+str(mark)+")"
        player.say(strr)    
player.on_chat("dbg", on_debug)

def on_show_block_map():
    start = pos(0, 0, 0).to_world()
    for i in range(15):
        for j in range(1, 11):
            blocks.place(i * 10 + j, start.add(pos(2 * i + 2 * i // 10, -1, 2 * j)))
player.on_chat("blkmap", on_show_block_map)

#help info
def on_help():
    player.say("----------use chat command to build-------------")
    player.say("buildmode [0/1]: OFF/ON")
    player.say("mark: mark a position to build")
    player.say("umark: unmark the last position")
    player.say("reset: commit changes and clear all marks")
    player.say("wall: build wall between adjacent marks")
    player.say("clone: clone everything enclosed by all marks")
    player.say("setblock [id]: choose block [id] as building material")
    player.say("addlevel: build one more level of floor from marks ")
    player.say("dellevel: del one level of floor from marks ")   
    player.say("blkmap: show a block map ") 
    player.say("dbg: show all marks of different level ")
    player.say("cube: build solid cube from marks")
    player.say("hollowcube: build hollow cube from marks")
    
    if check_build_mode():
        player.say("----------interacte with block to build -------------")
        player.say("use [GOLDEN      BOOTS] to mark")
        player.say("use [GOLDEN     SHOVEL] to unmark")
        player.say("use [GOLDEN      SWORD] to build wall")
        player.say("use [DIAMOND  LEGGINGS] to reset all marks")
        player.say("use [GOLDEN CHESTPLATE] to clone everything enclosed by all marks")
    player.say("--- by Magi, magilisaau@gmail.com, 2020 ---")

player.on_chat("help", on_help)

class BuildState:
    buildstate=0
    READY=0
    DONE=1

# on stat,here
# curlevel=0
marksarray = [[pos(0, 0, 0), ], ]
block = GRASS
buildmode = 1 
# I don't why can't use marksarray[0].pop(), so I wrote such stupid code below
temp = [pos(0, 0, 0)]
temp = marksarray[0]
temp.pop()
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_SWORD, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_SHOVEL, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_CARROT, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_APPLE, 1)

######################################### section three ################################################################
'''
    section three can call functions in section one and section two, but can NOT be called by section one and section two
'''
def on_item_interacted_mark():
    if not check_build_mode(): return
    on_mark()
    #player.run_chat_command("mark")
    #player.say("marked")
player.on_item_interacted(GOLDEN_BOOTS, on_item_interacted_mark)


def on_item_interacted_undo():
    if not check_build_mode(): return
    on_unmark()
    #player.run_chat_command("unmark")
    #player.say("undo last mark")
player.on_item_interacted(GOLDEN_SHOVEL, on_item_interacted_undo)

def on_item_interacted_wall():
    if not check_build_mode(): return
    on_build_wall()
    #player.run_chat_command("build")
    player.say("wall build")
player.on_item_interacted(GOLDEN_SWORD, on_item_interacted_wall)

def on_item_interacted_destroy():
    if not check_build_mode(): return
    on_del_one_level(1)
    #player.run_chat_command("dellevel")
    player.say("wall destroyed")
player.on_item_interacted(DIAMOND_SHOVEL, on_item_interacted_destroy)


def on_item_interacted_reset():
    if not check_build_mode(): return
    on_reset()
    #player.run_chat_command("reset")
    player.say("all marks reset")
player.on_item_interacted(GOLDEN_LEGGINGS, on_item_interacted_reset)


def on_item_interacted_clone():
    if not check_build_mode(): return
    on_clone()
    #player.run_chat_command("clone")
    player.say("clone")
player.on_item_interacted(GOLDEN_CHESTPLATE, on_item_interacted_clone)


def on_item_interacted_pick_block():
    global block
    block =detect_block_on_foot()
    player.say("set block to "+str(block))
player.on_item_interacted(GOLDEN_CARROT, on_item_interacted_pick_block)


def on_item_interacted_replace():
    global block
    newblk =detect_block_on_foot()
    marks = marksarray[len(marksarray) - 1]
    if len(marks)<2: return
    replace_from_marks(marks,newblk,block)
    player.say("replace block:"+str(block))
    block=newblk
player.on_item_interacted(GOLDEN_APPLE, on_item_interacted_replace)

######################  section four, a demo to build house using chat command ##############################
def demo():
    player.run_chat_command("setblock 155")
    player.run_chat_command("mark")
    loops.pause(500)
    player.teleport(pos(48,0,0))
    loops.pause(100)
    player.run_chat_command("mark")
    loops.pause(500)
    player.teleport(pos(0,1,0))
    player.run_chat_command("wall")
    loops.pause(500)
    player.teleport(pos(0,1,0))
    loops.pause(100)
    player.run_chat_command("addlevel")    
    loops.pause(500)  
    player.teleport(pos(0,1,0))
    loops.pause(100)
    player.run_chat_command("addlevel")  
    loops.pause(500)  
    player.teleport(pos(0,1,0))
    loops.pause(100)
    player.run_chat_command("addlevel")       
    loops.pause(500)      
    player.teleport(pos(0,1,0))
    loops.pause(100)
    player.run_chat_command("addlevel") 
    loops.pause(500)  
    player.run_chat_command("reset") 
    loops.pause(500)
    player.run_chat_command("mark")
    loops.pause(500)
    for i in range(6):
        player.teleport(pos(0,1,0))
        loops.pause(100)
        player.run_chat_command("mark")
        loops.pause(500)

        player.teleport(pos(-4,0,0))
        loops.pause(100)
        player.run_chat_command("mark")
        loops.pause(500)

        player.teleport(pos(0,-1,0))
        loops.pause(100)
        player.run_chat_command("mark")
        loops.pause(500)

        player.teleport(pos(-4,0,0))
        loops.pause(100)
        player.run_chat_command("mark")
        loops.pause(500)
    player.run_chat_command("wall")
    loops.pause(1000)
    player.run_chat_command("reset")

def on_demo():
    demo()
player.on_chat("demo",on_demo)
