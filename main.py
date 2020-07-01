'''
Author: Magi
Contact: magilisaau@gmail.com
CreateTime: 2020/04/20
ModifyTime: 2020/6/28
Description: the project is to help kids build house more efficiently and easily in the game minecraft
'''
'''
    This project include TWO important files, and each have two sections
    ---custom.ts: written by javascript, this an extension which can be installed into Code Builder
                  this can be used seperately
    ---main.py: written by python, implement a command list interface(CLI) and the graphical user interface(UI)
    
'''
class setting:
    buildblock =GRASS

###########   section THREE, command list interface by Magi 2020 #########
def on_mark_handle():
    ebuilder.acquire()
    ebuilder.mark(player.position())
    ebuilder.release()
player.on_chat("mark", on_mark_handle)

def on_mark2_handle():
    checkpos =[ pos(-1,0,0),pos(1,0,0),
                pos(0,0,-1),pos(0,0,1),
            ]
    curpos =None
    ebuilder.acquire()
    for x in checkpos:
        if not blocks.test_for_block(AIR,x) and not blocks.test_for_block(WATER,x):
            curpos =x
            break
    if curpos: 
        ebuilder.mark(curpos,True)
        #blocks.place(TOP_SNOW,pos(0,0,0))
    ebuilder.release()
player.on_chat("mark2", on_mark2_handle)

def on_unmark_handle():
    ebuilder.acquire()
    ebuilder.unmark()
    ebuilder.release()
player.on_chat("unmark", on_unmark_handle)

def on_build_wall_handle():
    ebuilder.acquire()
    ebuilder.build_wall(setting.buildblock)
    ebuilder.release()
player.on_chat("wall", on_build_wall_handle)

def on_build_line_handle():
    ebuilder.acquire()
    ebuilder.build_line(setting.buildblock)
    ebuilder.release()
player.on_chat("line", on_build_line_handle)

def on_build_cube_handle(high: int = 0):
    ebuilder.acquire()
    ebuilder.build_cube(setting.buildblock)
    ebuilder.release()
player.on_chat("cube", on_build_cube_handle)

def on_build_hollow_cube_handle(high: int = 0):
    ebuilder.acquire()
    ebuilder.build_hollow_cube(setting.buildblock)
    ebuilder.release()
player.on_chat("hollowcube", on_build_hollow_cube_handle)

def on_reset_marks_handle():
    ebuilder.acquire()
    ebuilder.reset_marks()
    ebuilder.release()
player.on_chat("reset", on_reset_marks_handle)

def on_increase_wall_handle(cnt:number):
    if cnt==0: cnt=1
    ebuilder.acquire()
    ebuilder.increase_wall(setting.buildblock,cnt)
    ebuilder.release()
player.on_chat("increase", on_increase_wall_handle)

def on_decrease_wall_handle(cnt:number):
    if cnt==0: cnt=1
    ebuilder.acquire()
    ebuilder.decrease_wall(cnt)
    ebuilder.release()
player.on_chat("decrease", on_decrease_wall_handle)

def on_ruler():
    ebuilder.acquire()
    ebuilder.show_ruler(pos(0,0,0))
    ebuilder.release()
player.on_chat("ruler", on_ruler)

def on_remove_ruler():
    ebuilder.acquire()
    ebuilder.hide_ruler()
    ebuilder.release()
player.on_chat("hideruler", on_remove_ruler)

# clone 0/1
def on_clone_handle(align:int):
    ebuilder.acquire()
    if align==0:
        ebuilder.clone(player.position(),False)
    else:
        ebuilder.clone(player.position(),True)
    ebuilder.release()
player.on_chat("clone", on_clone_handle)

def on_clear_handle():
    ebuilder.acquire()
    ebuilder.clear()
    ebuilder.release()
player.on_chat("clear", on_clear_handle)

#replace oldblk newblk or replace oldblk
def on_replace_handle(oldblk:int,newblk:int):
    ebuilder.acquire()
    arg0 = player.get_chat_arg(0)
    arg1 = player.get_chat_arg(1)
    if arg1==None: newblk=setting.buildblock
    if arg0!=None:
        ebuilder.replace(oldblk,newblk)
    else:
        player.say("invalid cmd, use replace oldblock newblock")
    ebuilder.release()
player.on_chat("replace", on_replace_handle)

def on_plant_handle(tree,interval):
    if tree==0: tree=ACACIA_SAPLING
    if interval==0: interval=4
    ebuilder.acquire()
    ebuilder.plant(tree,interval)
    ebuilder.release()
player.on_chat("plant", on_plant_handle)

# config the type of block to build
def on_set_blk(blk:int):
    setting.buildblock=blk
    player.say("set building block to " + str(blk))
player.on_chat("setblock", on_set_blk)

#show marks
def on_debug():
    ebuilder.show_marks()
player.on_chat("dbg", on_debug)

def on_show_block_map():
    start = pos(0, 0, 0).to_world()
    for i in range(15):
        for j in range(1, 11):
            blocks.place(i * 10 + j, start.add(pos(2 * i + 2 * i // 10, -1, 2 * j)))
player.on_chat("blkmap", on_show_block_map)

###########   section FOUR, user interface by Magi 2020 #########
class ui_setting:
    buildmode =True
# check build mode
def check_build_mode():
    return True if ui_setting.buildmode else False
#config build mode on/off
def on_set_build_mode(mode: int):
    if mode==1: ui_setting.buildmode = True
    else: ui_setting.buildmode =False
    if ui_setting.buildmode:
        player.say("build mode on")
    else:
        player.say("build mode off ")
player.on_chat("setbuildmode", on_set_build_mode)

def on_item_interacted_mark():
    if not check_build_mode(): return
    ebuilder.acquire()
    ebuilder.mark(player.position())
    ebuilder.release()
player.on_item_interacted(GOLDEN_BOOTS, on_item_interacted_mark)

def on_item_interacted_unmark():
    if not check_build_mode(): return
    ebuilder.acquire()
    if ebuilder.mark_num():
        ebuilder.unmark()
    else:
        ebuilder.decrease_wall(1)
    ebuilder.release()
player.on_item_interacted(IRON_BOOTS, on_item_interacted_unmark)

def on_item_interacted_clear():
    if not check_build_mode(): return
    ebuilder.acquire()
    ebuilder.clear()
    ebuilder.release()
player.on_item_interacted(GOLDEN_SHOVEL, on_item_interacted_clear)

def on_item_interacted_wall():
    if not check_build_mode(): return
    ebuilder.acquire()
    if ebuilder.mark_num():
        if ebuilder.mark_num()>=2:
            ebuilder.build_wall(setting.buildblock)
    else:
        ebuilder.increase_wall(setting.buildblock,1)
    ebuilder.release()
    #player.say("wall build")
player.on_item_interacted(GOLDEN_SWORD, on_item_interacted_wall)


def on_item_interacted_reset():
    if not check_build_mode(): return
    ebuilder.acquire()
    ebuilder.reset_marks()
    ebuilder.release()
    #player.say("all marks reset")
player.on_item_interacted(GOLDEN_LEGGINGS, on_item_interacted_reset)


def on_item_interacted_clone():
    if not check_build_mode(): return
    ebuilder.acquire()
    ebuilder.clone(player.position())
    ebuilder.release()
    #player.say("clone")
player.on_item_interacted(GOLDEN_APPLE, on_item_interacted_clone)

def on_item_interacted_pick_block():
    curpos =player.position()
    footpos =curpos.add(pos(0,-1,0))
    setting.buildblock =ebuilder.detect_block_at_pos(footpos)
    player.say("set building block: "+str(setting.buildblock))
player.on_item_interacted(GOLDEN_CARROT, on_item_interacted_pick_block)

def on_item_interacted_melon():
    if not check_build_mode(): return
    ebuilder.acquire()
    ebuilder.show_ruler()
    ebuilder.release()
player.on_item_interacted(MELON, on_item_interacted_melon)

def on_item_interacted_glistering_melon():
    if not check_build_mode(): return
    ebuilder.acquire()
    ebuilder.hide_ruler()
    ebuilder.release()  
player.on_item_interacted(GLISTERING_MELON, on_item_interacted_glistering_melon)

def detect_and_replace(curpos:Position,block:number):
    x1 =0;x2 =0;y1 =0;y2 =0;z1 =0;z2 =0
    #player.say("block=")
    #player.say(block)
    while blocks.test_for_block(block, curpos.add(pos(x1,0,0))): x1 -=1
    while blocks.test_for_block(block, curpos.add(pos(x2,0,0))): x2 +=1
    while blocks.test_for_block(block, curpos.add(pos(0,y1,0))): y1 -=1
    while blocks.test_for_block(block, curpos.add(pos(0,y2,0))): y2 +=1
    while blocks.test_for_block(block, curpos.add(pos(0,0,z1))): z1 -=1
    while blocks.test_for_block(block, curpos.add(pos(0,0,z2))): z2 +=1        
    x1+=1; x2-=1; y1+=1; y2-=1; z1+=1; z2-=1;
    cnt =(y2-y1+1)//10
    reminder = (y2-y1+1)%10
    for i in range(cnt):
        start =curpos.add(pos(x1,y1+10*i,z1))
        end =curpos.add(pos(x2,y1+10*i+10,z2))
        blocks.replace(setting.buildblock, block,start,end)
    if reminder:
        start =curpos.add(pos(x1,y1+cnt*10,z1))
        end =curpos.add(pos(x2,y2,z2))
        player.say(start)
        player.say(end)
        blocks.replace(setting.buildblock, block,start,end)

def do_replace(checkpos, checkTorch, newTorch, relativePos):
    for x in checkpos:
        x1 =x.to_world()
        if blocks.test_for_block(checkTorch,x):
            blocks.place(newTorch,x)
            x2 =x1.add(relativePos)
            replacedblock =ebuilder.detect_block_at_pos(x2)
            ebuilder.acquire()
            if ebuilder.mark_num()==0:
                detect_and_replace(x2,replacedblock)
            else:
                ebuilder.replace(replacedblock,setting.buildblock)
            ebuilder.release()
            break
def on_block_placed_west():
    checkpos =[ pos(0,1,0),
                pos(-1,1,0),pos(-1,0,0),
                pos(-2,1,0),pos(-2,0,0),
                pos(-3,1,0),pos(-3,0,0),
            ]
    do_replace(checkpos,0x10032,0x1004c,pos(-1,0,0))
blocks.on_block_placed(0x10032, on_block_placed_west)

def on_block_placed_east():
    checkpos =[ pos(0,1,0),
                pos(1,1,0),pos(1,0,0),
                pos(2,1,0),pos(2,0,0),
                pos(3,1,0),pos(3,0,0),
            ]
    do_replace(checkpos,0x20032,0x2004c,pos(1,0,0))
blocks.on_block_placed(0x20032, on_block_placed_east)

def on_block_placed_north():
    checkpos =[ pos(0,1,0),
                pos(0,1,-1),pos(0,0,-1),
                pos(0,1,-2),pos(0,0,-2),
                pos(0,1,-3),pos(0,0,-3)
                ]
    do_replace(checkpos,0x30032,0x3004c,pos(0,0,-1))
blocks.on_block_placed(0x30032, on_block_placed_north)

def on_block_placed_south():
    checkpos =[ pos(0,1,0),
                pos(0,1,1),pos(0,0,1),
                pos(0,1,2),pos(0,0,2),
                pos(0,1,3),pos(0,0,3),
                ]
    do_replace(checkpos,0x40032,0x4004c,pos(0,0,1))
blocks.on_block_placed(0x40032, on_block_placed_south)

def on_help():
    cmd_all=["ui","mark","mark2","umark","reset","wall","increase","decrease","clone","clear","setblock","setalign","blkmap","dbg","cube","hollowcube","plant","demo"]
    cmd_detail=[
        ["mark","mark the position where the player standing"],
        ["mark2","compared with the mark cmd, it can mark the solid position near the player"],
        ["umark","remove the last mark"],
        ["reset","hide and clear all marks"],
        ["wall","build walls between each two marks"],
        ["increase","increase n, increase n floors"],
        ["decrease","decrease n, decrease n floors"],
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
    ]
    arg = player.get_chat_arg(0)
    if arg==None:
        player.say("---cmd list---")
        cmdlist=""
        for x in cmd_all:
            cmdlist+=x
            cmdlist+=' '
        player.say(cmdlist)
        player.say("---type help [cmd] for cmd detail---")
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

def help_ui():
    player.say("* right-click the block below to use *")
    player.say("GOLDEN BOOTS: mark")
    player.say("IRON BOOTS: umark")
    player.say("GOLDEN SWORD: wall")
    player.say("GOLDEN CARROT: choose a block")
    player.say("GOLDEN TORCH: replace")
    player.say("GOLDEN APPLE: clone")
    player.say("GOLDEN SHOVEL: clear")
    player.say("MELON: show ruler")
    player.say("GLISTERING MELON: hide ruler")

# on stat,here
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS),IRON_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_SWORD, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_SHOVEL, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_CARROT, 1)
mobs.give(mobs.target(ALL_PLAYERS),TORCH, 1)
mobs.give(mobs.target(ALL_PLAYERS),GOLDEN_APPLE, 1)
mobs.give(mobs.target(ALL_PLAYERS),MELON, 1)
mobs.give(mobs.target(ALL_PLAYERS),GLISTERING_MELON, 1)
