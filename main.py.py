'''
Author: Magi
Contact: magilisaau@gmail.com
CreateTime: 2020/04/20
ModifyTime: 2020/5/10
Description: the project is to help kids build house more efficiently and easily in the game minecraft

Author: Magi
Contact: magilisaau@gmail.com
ModifyTime: 2020/5/17
Description: bug fix, clear marks after clear/cube/hollowcube
'''
#help info
def help_ui():
    player.say("---right-click the block below to build---")
    player.say("GOLDEN BOOTS:   add a mark")
    player.say("IRON BOOTS:  remove last mark or del one floor")
    player.say("GOLDEN SWORD:   build wall or add one floor")
    player.say("GOLDEN LEGGINGS: reset all marks")
    player.say("GOLDEN CARROT:  choose the block under the player's feet")
    player.say("GOLDEN APPLE:   replace the old block to the new one under the player's feet")
    player.say("GOLDEN CHESTPLATE: clone to the place where the player is standing")
    player.say("GOLDEN SHOVEL: clear the cubic space enclosed by all marks")
def on_help():
    cmd_all=["mark","umark","reset","wall","addfloor","delfloor","clone","clear","setblock","setalign","blkmap","dbg","cube","hollowcube","plant","demo"]
    cmd_detail=[
        ["mark","mark the position where the player is standing"],
        ["umark","remove the last mark"],
        ["reset","commit changes and clear all marks"],
        ["wall","build walls between every two adjacent marks"],
        ["addfloor","addfloor n, add n floors on the wall"],
        ["delfloor","delfloor n, del n floors of the wall"],
        ["clone","clone the cube space enclosed by all marks into the position where the player stands"],
        ["clear","clear the cube space enclosed by all marks"],
        ["replace","replace the blocks enclosed by all marks to new blocks"],        
        ["setblock","setblock [id]: choose block [id] as building material"],
        ["setalign","setalign [0|1]: when setalign 1, the target position to clone into will align automatically"],
        ["blkmap","show a block map"],
        ["dbg","show all marks"],
        ["cube","build solid cube from marks"],
        ["hollowcube","build hollow cube from marks"],
        ["plant","plant [tree] [interval]: plant trees on the groud from marks, interval between trees"],
        ["demo","run a demo to build a wall"]
    ]
    arg = player.get_chat_arg(0)
    if arg==None:
        player.say("--- cmd list, type T to open chat window---")
        for x in cmd_all:
            player.say(x)
        player.say("---type help [cmd] for cmd detail---")
        player.say("---type help ui for user interface---")
    elif arg=="ui":
        help_ui()
    else:
        for i in range(len(cmd_detail)):
            if cmd_detail[i][0]==arg:
                player.say(cmd_detail[i][1])
                return
        player.say("invalid cmd")
    pass
player.on_chat("help", on_help)
################################ section one: lib #################################################
'''
section one are fundermental lib for process marks
the functions in section one can only be called by section two and section three
the functions in section one can NOT call the functions in section two and section three
'''
'''
**NOTE: microsoft minecraft python doesn't support python class well till now, so we have to use functions
        and minecraft python only support static python syntax, not all python2.x/python3.x syntax can be used

detect_block_at_pos(marks,pos)      :get the id of the block at the position of pos
add_build_line(marks,pos)           :build a auxiliary line at the position of pos
del_build_line(marks,pos)           :del the auxiliary line at the position of pos
get_enclosure_from_marks(marks)     :get the cube area enclosed by the marks which previous added
def get_relative_pos(marks,orient,origin,dir): given the origin position and the orientation, get the coordinate in the direction of LEFT/RIGHT/FORWARD/BACK/UP/DOWN
push_mark(marks,pos)                :add a new mark
pop_mark(marks)                     :remove the last added mark
clear_marks(marks)                  :clear all marks previous added
build_wall_from_marks(marks,block)  :build walls according to the previously marks,using block as materials
clone_from_marks(marks,into,align)  :clone the cube space enclosed by the marks [into] a new place, if align is True, it will align automaticlly with the origin area
replace_from_marks(marks,newblk, oldblk):replace the old block to new block in the cube space enclosed by the marks 
clear_from_marks(marks)             :clear the cube space enclosed by the marks 
build_cube_from_marks(marks)        :build a solid cube according to the previously marks
build_hollow_cube_from_marks(marks) :like build_cube_from_marks() do, but a hollow cube
plant_trees_from_marks(marks,tree,interval):plant [trees] in the projective region of the marks on the ground, every [interval] distance
'''

def detect_block_at_pos(position:Position):
    agent.teleport(position.add(pos(0,1,0)),WEST)
    what=agent.inspect(AgentInspection.BLOCK, DOWN)
    for i in range(1,16):
        detail=65536*i+what
        if blocks.test_for_block(detail,pos(0,-1,0)):
            return detail
    return what

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
    x1 = mark.get_value(Axis.X); y1 = mark.get_value(Axis.Y); z1 = mark.get_value(Axis.Z)
    x2 = x1; y2 = y1; z2 = z1
    for x in marks:
        mark = x
        if mark.get_value(Axis.X) < x1: x1 = mark.get_value(Axis.X)
        if mark.get_value(Axis.X) > x2: x2 = mark.get_value(Axis.X)
        if mark.get_value(Axis.Y) < y1: y1 = mark.get_value(Axis.Y)
        if mark.get_value(Axis.Y) > y2: y2 = mark.get_value(Axis.Y)
        if mark.get_value(Axis.Z) < z1: z1 = mark.get_value(Axis.Z)
        if mark.get_value(Axis.Z) > z2: z2 = mark.get_value(Axis.Z)
    return [world(x1, y1, z1), world(x2, y2, z2)]

#place a flag on the top of the cubic space enclosed by the marks, which is useful when clone to a new place
def place_on_enclosure_top(marks=[pos(0,0,0)]):
    closure = get_enclosure_from_marks(marks)
    start =pos(0,0,0)
    end =pos(0,0,0)
    start = closure[0]
    end = closure[1]
    x1 = start.get_value(Axis.X)
    y1 = start.get_value(Axis.Y); y2 = end.get_value(Axis.Y)
    z1 = start.get_value(Axis.Z)
    newstart =world(x1,y1,z1).add(pos(0,y2-y1+1,0))
    blocks.place(TOP_SNOW,positions.ground_position(newstart))


# add mark
def push_mark(marks=[pos(0,0,0)],curpos:Position=player.position(),mark_blk=TOP_SNOW):
    marks.append(curpos)
    if setting.buildline: add_build_line(curpos)
    blocks.place(mark_blk, curpos)

# undo last added mark
def pop_mark(marks=[pos(0, 0, 0)]):
    size = len(marks)
    if size == 0: return
    prepos = None #pos(0, 0, 0)
    curpos = marks[size - 1]
    if setting.buildline: del_build_line(curpos)
    blocks.place(AIR, curpos)
    if size >= 2:
        prepos = marks[size - 2]
        if setting.buildline: add_build_line(prepos)
    marks.pop()

# build wall from a serial of adjacent marks
def build_wall_from_marks(marks=[pos(0, 0, 0)], block=GRASS):
    size = len(marks)
    if size < 2: return False
    start = marks[0]
    for i in range(1, size):
        end = marks[i]
        blocks.fill(block, start, end)
        start = marks[i]
    for x in marks:
        if setting.buildline:del_build_line(x)
    return True

# clear all marks
def clear_marks(marks=[pos(0, 0, 0)]):    
    while (len(marks)):
        marks.pop()

def copy_marks(dst=[pos(0, 0, 0)],src=[pos(0, 0, 0)]):
    clear_marks(dst)
    for x in src:  
        dst.append(x)
#get mark num
def marks_num(marks=[pos(0, 0, 0)]):
    return len(marks)
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
    if align:
        xin=False; zin=False
        if x >= x1 and x <= x2: xin = True
        if z >= z1 and z <= z2: zin = True
        if xin and zin: 
            x =x1; z=z1
        if xin and not zin:
            #dz =0
            dz =z2-z1
            _into_z =0 # I don't know why _into_z must asigned to 0 first, or else there will be a compile error, a stupid python compiler
            _into_z =z+dz
            if _into_z >= z1 and _into_z <= z2: z-=dz
            x =x1
        if not xin and zin:
            #dx =0
            dx =x2-x1
            _into_x =0 
            _into_x = x+dx
            if _into_x >=x1 and _into_x <= x2: x-=dx
            z=z1
    _into =world(x,y,z)
    blocks.clone(start, end,_into, CloneMask.REPLACE, CloneMode.NORMAL)
    copy_marks(marks,[_into,world(x+x2-x1,y+y2-y1,z+z2-z1)])
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

def plant_trees_from_marks(marks=[],tree:number=ACACIA_SAPLING,interval:number=2):
    if len(marks) < 2: return
    closure = get_enclosure_from_marks(marks)
    start=pos(0,0,0)
    end=pos(0,0,0)
    start = closure[0]
    end = closure[1]
    x1 = start.get_value(Axis.X); x2 = end.get_value(Axis.X)
    y1 = start.get_value(Axis.Y); y2 = end.get_value(Axis.Y)
    z1 = start.get_value(Axis.Z); z2 = end.get_value(Axis.Z)
    for x in range(x1,x2+1,interval):
        for z in range(z1,z2+1,interval):
            where = positions.ground_position(world(x,y2,z))
            blocks.place(tree,where)
################################ section two, command line interface ##############################################
'''
on_mark()->void                 :add the position where the player stands as a new mark
on_unmark()->void               :del the last added mark
on_build_wall()->void           :build wall according to the marks previously added, a wall each two adjacent marks
on_build_cube()->void           :build a solid cube according to the marks previously added
on_build__hollow_cube()->void   :build a hollow cube according to the marks previously added
on_reset()->void                :clear all marks previous added
on_add_floor(n)->void           :if current marksqueue not empty, build n new floors just on the current wall
on_del_floor(n)->void           :del n floors of wall
on_clone()->void                :clone the cube space enclosed bye the marks to a new place where the player stands
on_clear()->void                :clear the cube space enclosed bye the marks to a new place where the player stands
on_replace()->void              :replace the old blocks in the cube enclosed bye the marks to new blocks
on_plant()->void                :plant trees or weeds in the ground area which is enclosed by the marks
on_setblk(int)->void            :set the building block type
'''

# 05-17,magi??because minecraft doesn't provide threading.Lock, we need to simulate one, maybe sometime it will failed,but can go in most cases
class TestBit:
    lock=0
def acquire():
    while(TestBit.lock): loops.pause(50)
    TestBit.lock=1
def release():
    TestBit.lock=0

def on_mark():
    acquire()
    if BuildState.buildstate==BuildState.DONE: 
        release()
        on_reset()    
        acquire()     
    push_mark(buildmarks,player.position())
    #2020-05-18 Magi
    mobs.apply_effect(Effect.HASTE, mobs.target(LOCAL_PLAYER),600)
    release()
def on_mark_handle():
    on_mark()
player.on_chat("mark", on_mark_handle)

#
def on_unmark():
    acquire()
    if BuildState.buildstate==BuildState.READY:
        marks = buildmarks
        pop_mark(marks)
        if(len(marks)==0): 
            #2020-05-18,Magi
            mobs.clear_effect(mobs.target(LOCAL_PLAYER))
        release()
    if BuildState.buildstate==BuildState.DONE:
        release()
        on_del_floor()
    

def on_unmark_handle():
    on_unmark()
player.on_chat("unmark", on_unmark_handle)

#
def on_build_wall():
    acquire()
    if BuildState.buildstate==BuildState.READY:
        marks = buildmarks
        if len(marks)>=2: 
            build_wall_from_marks(marks, setting.buildblock)
            place_on_enclosure_top(marks)
            BuildState.buildstate=BuildState.DONE
        release()
    elif BuildState.buildstate==BuildState.DONE:
        release()#because acquire will be called also in on_add_floor,so release here
        on_add_floor()

def on_build_wall_handle():
    on_build_wall()
player.on_chat("wall", on_build_wall_handle)

def on_build_cube():
    acquire()
    marks = buildmarks
    if len(marks)>=2: build_cube_from_marks(marks,setting.buildblock)
    release()
    on_reset()
def on_build_cube_handle(high: int = 0):
    on_build_cube()
player.on_chat("cube", on_build_cube_handle)

def on_build__hollow_cube():
    acquire()
    marks = buildmarks
    if len(marks)>=2: build_hollow_cube_from_marks(marks,setting.buildblock)
    release()
    on_reset()
def on_build__hollow_cube_handle(high: int = 0):
    on_build__hollow_cube()
player.on_chat("hollowcube", on_build__hollow_cube_handle)

#
def on_reset():
    acquire()
    if BuildState.buildstate==BuildState.READY:
        if setting.buildline:
            for p in buildmarks: del_build_line(p)
    clear_marks(buildmarks)
    BuildState.buildstate=BuildState.READY
    mobs.clear_effect(mobs.target(LOCAL_PLAYER))
    release()
def on_reset_handle():
    on_reset()
player.on_chat("reset", on_reset_handle)
#
def on_show_block():
    player.say("building block:"+str(setting.buildblock))
    player.say("replace  block:"+str(setting.replaceblock))
player.on_chat("showblock", on_show_block)

# process add one level cmd
def on_add_floor():
    global buildmarks
    acquire()
    marks = buildmarks
    if len(marks) < 2: 
        release()
        return
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
    clear_marks(buildmarks)
    buildmarks =newmarks
    build_wall_from_marks(buildmarks,setting.buildblock)
    release()
def on_add_floor_handle(times:number):
    if times==0:  times=1
    for i in range(times):
        on_add_floor()
player.on_chat("addfloor", on_add_floor_handle)

#process del one level cmd
def on_del_floor():
    global buildmarks
    acquire()
    marks = buildmarks
    if len(marks) < 2: 
        release()
        return
    floor = pos(0, 0, 0)
    ceil = pos(0, 0, 0)
    closure = get_enclosure_from_marks(marks)
    floor = closure[0]
    ceil = closure[1]
    dy = ceil.get_value(Axis.Y) - floor.get_value(Axis.Y) + 1
    newmarks = [pos(0, 0, 0)]
    newmarks.pop()
    for x in marks:
        newmarks.append(x.add(pos(0, -dy, 0)))
    build_wall_from_marks(buildmarks,AIR)
    clear_marks(buildmarks)
    buildmarks =newmarks
    release()
    
def on_del_floor_handle(times:number):
    if times==0: times=1
    for x in range(times):
        on_del_floor()
player.on_chat("delfloor", on_del_floor_handle)

#process clone from marks cmd
def on_clone():
    acquire()
    marks= buildmarks
    if marks_num(marks):
        copy_marks(clonemarks,marks)
        release()
        on_reset()
        acquire()
    if marks_num(clonemarks):
        newpos =clone_from_marks(clonemarks,player.position(),setting.clonealign)
        if newpos: player.teleport(newpos)
    player.say("clone")
    release()

def on_clone_handle():
    on_clone()
player.on_chat("clone", on_clone_handle)

def on_unclone():
    clear_from_marks(clonemarks)
    player.say("unclone")

def on_unclone_handle():
    on_unclone()
player.on_chat("unclone", on_unclone_handle)


#process clone from marks cmd
def on_clear():
    acquire()
    clear_from_marks(buildmarks)
    release()
    on_reset()#remove marks after clear done    

def on_clear_handle():
    on_clear()
player.on_chat("clear", on_clear_handle)


def on_replace():
    acquire()
    marks = buildmarks
    if len(marks) >=2: 
        replace_from_marks(marks,setting.replaceblock, setting.buildblock)
        #block=newblk, removed 2020-05024
    release()
    on_reset()

def on_replace_handle():
        on_replace()
player.on_chat("replace", on_replace_handle)

def on_teleport(position):
    loops.pause(50)
    acquire()
    player.teleport(position)
    release()
'''

'''
#plant_from_marks
def on_plant(tree,interval):
    acquire()
    plant_trees_from_marks(buildmarks,tree,interval)
    release()
    on_reset()
    pass
def on_plant_handle(tree,interval):
    if tree==0: tree=ACACIA_SAPLING
    if interval==0: interval=4
    on_plant(tree,interval)
player.on_chat("plant", on_plant_handle)

# config the type of block to build
def on_set_blk(blk:int):
    setting.buildblock=blk
    player.say("set building block to " + str(blk))
player.on_chat("setblock", on_set_blk)


def on_set_replace_blk(blk:int):
    setting.replaceblock=blk
    player.say("replace old block to " + str(blk))
player.on_chat("setnewblock", on_set_replace_blk)

#config build mode on/off
def on_set_build_mode(mode: int):
    if mode==1: setting.buildmode = True
    else: setting.buildmode =False
    if setting.buildmode:
        player.say("build mode on")
    else:
        player.say("build mode off ")
player.on_chat("setbuildmode", on_set_build_mode)
#config clone alignment 
def on_set_clone_alignment(align: int):
    if align==1: 
        setting.clonealign = True
    else: 
        setting.clonealign =False
    if setting.clonealign:
        player.say("clone alignment on")
    else:
        player.say("clone alignment off ")
player.on_chat("setalign", on_set_clone_alignment)

# check build mode
def check_build_mode():
    return True if setting.buildmode else False
    
#show marks
def on_debug():
    strr=""
    for x in buildmarks: strr+="("+str(x)+")"
    player.say(strr)
    pass   
player.on_chat("dbg", on_debug)

def on_show_block_map():
    start = pos(0, 0, 0).to_world()
    for i in range(15):
        for j in range(1, 11):
            blocks.place(i * 10 + j, start.add(pos(2 * i + 2 * i // 10, -1, 2 * j)))
player.on_chat("blkmap", on_show_block_map)

class BuildState:
    buildstate=0
    READY=0
    DONE=1

class setting:
    buildblock =GRASS
    replaceblock =GRASS
    buildmode =True
    buildline =True
    clonealign =True

# on stat,here
buildmarks = [pos(0, 0, 0)]
clonemarks = [pos(0,0,0)]
buildmarks.pop()
clonemarks.pop()
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS),IRON_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_SWORD, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_SHOVEL, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_CARROT, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_APPLE, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_CHESTPLATE, 1)
######################################### section three, user interface ##################################################
'''
section three can call functions in section one and section two, but can NOT be called by section one and section two
'''
def on_item_interacted_mark():
    if not check_build_mode(): return
    on_mark()
    #player.run_chat_command("mark")
    #player.say("marked")
player.on_item_interacted(GOLDEN_BOOTS, on_item_interacted_mark)

def on_item_interacted_unmark2():
    if not check_build_mode(): return
    on_unmark()    

player.on_item_interacted(IRON_BOOTS, on_item_interacted_unmark2)

def on_item_interacted_clear():
    if not check_build_mode(): return
    on_clear()
    
player.on_item_interacted(GOLDEN_SHOVEL, on_item_interacted_clear)

def on_item_interacted_wall():
    if not check_build_mode(): return
    on_build_wall()
    #player.run_chat_command("build")
    player.say("wall build")
player.on_item_interacted(GOLDEN_SWORD, on_item_interacted_wall)


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
    curpos =player.position()
    footpos =curpos.add(pos(0,-1,0))
    footposdown =footpos.add(pos(0,-1,0))
    setting.replaceblock =detect_block_at_pos(footposdown)
    setting.buildblock =detect_block_at_pos(footpos)
    player.say("set building block: "+str(setting.buildblock))
    player.say("set replace block:  "+str(setting.replaceblock))

player.on_item_interacted(GOLDEN_CARROT, on_item_interacted_pick_block)


def on_item_interacted_replace():
    on_replace()
    player.say("replace")
player.on_item_interacted(GOLDEN_APPLE, on_item_interacted_replace)

######################  section four, a demo to build house using chat command ##############################
def demo():
    player.run_chat_command("setblock 155")
    player.run_chat_command("mark")
    on_teleport(pos(48,0,0)) 
    player.run_chat_command("mark")
    on_teleport(pos(0,1,0))   
    player.run_chat_command("wall")
    on_teleport(pos(0,1,0))   
    player.run_chat_command("addfloor")  
    on_teleport(pos(0,1,0))   
    player.run_chat_command("addfloor")  
    on_teleport(pos(0,1,0))   
    player.run_chat_command("addfloor")     
    on_teleport(pos(0,1,0))  
    player.run_chat_command("addfloor")  
    player.run_chat_command("reset") 
    player.run_chat_command("mark") 
    for i in range(6):
        on_teleport(pos(0,1,0))
        player.run_chat_command("mark")
        on_teleport(pos(-4,0,0))
        player.run_chat_command("mark")
        on_teleport(pos(0,-1,0))  
        player.run_chat_command("mark")
        on_teleport(pos(-4,0,0))  
        player.run_chat_command("mark")
    player.run_chat_command("wall")
    player.run_chat_command("reset")

def on_demo():
    demo()
player.on_chat("demo",on_demo)

 