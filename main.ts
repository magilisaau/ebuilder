/** 
Author: Magi
Contact: magilisaau@gmail.com
CreateTime: 2020/04/20
ModifyTime: 2020/6/28
Description: the project is to help kids build house more efficiently and easily in the game minecraft

 */
/** 
    This sourcecode include TWO main files
    ---custom.ts: written in javascript, this is an extension which can be installed into Code Builder
    this can be used seperately
    ---main.py: written in python, implement a command list interface(CLI) and the graphical user interface(UI)
    
    ---buildAssistant.py: in python,this file has been obelete and no longer maintained, but it has been tested and can run seperately
                 , I use python in the begining,but later I found the extension for minecraft can only be written in javascript, So it was
                 devided into custom.ts and main.py.

 */
class setting {
    static buildblock = GRASS
}

player.onChat("help", function on_help() {
    let cmdlist: string;
    let cmd_all = ["ui", "mark", "mark2", "umark", "reset", "wall", "increase", "decrease", "clone", "clear", "setblock", "setalign", "blkmap", "dbg", "cube", "hollowcube", "plant", "demo"]
    let cmd_detail = [["mark", "mark the position where the player standing"], ["mark2", "compared with the mark cmd, it sticky to a block near the player"], ["umark", "remove the last mark"], ["reset", "hide and clear all marks"], ["wall", "build walls between each two marks"], ["line", "build lines between each two marks"], ["increase", "increase n, increase n floors"], ["decrease", "decrease n, decrease n floors"], ["clone", "clone 0/1,clone the space enclosed by all marks to where the player stands,1:align 0: not align"], ["clear", "clear the space enclosed by all marks"], ["replace", "replace the old blocks enclosed by all marks to new blocks"], ["setblock", "setblock [id]: choose block [id] as building material"], ["setalign", "setalign [0|1]: when setalign 1, the target position to clone into will align automatically"], ["blkmap", "show a block map"], ["dbg", "show all marks info"], ["cube", "build a solid cube from marks"], ["hollowcube", "build a hollow cube from marks"], ["plant", "plant [tree] [interval]: plant trees on the ground, with intervals"], ["ruler", "show ruler in the area enclosed by all marks"], ["hideruler", "hide ruler in the area enclosed by all marks"], ["demo", "run a demo"]]
    let arg = player.getChatArg(0)
    if (arg == undefined) {
        player.say("---cmd list---")
        cmdlist = ""
        for (let x of cmd_all) {
            cmdlist += x
            cmdlist += " "
        }
        player.say(cmdlist)
        player.say("---type help [cmd] for cmd detail---")
    } else if (arg == "ui") {
        help_ui()
    } else {
        for (let i = 0; i < cmd_detail.length; i++) {
            if (cmd_detail[i][0] == arg) {
                player.say(cmd_detail[i][1])
                return
            }
            
        }
        player.say("invalid cmd")
    }
    
    
})
function help_ui() {
    player.say("* right-click the block below to use *")
    player.say("GOLDEN BOOTS: add a mark")
    player.say("DIAMOND_BOOTS: add a sticky mark")
    player.say("IRON BOOTS: umark")
    player.say("GOLDEN SWORD: build wall")
    player.say("GOLDEN CARROT: choose a block")
    player.say("GOLDEN TORCH: replace")
    player.say("GOLDEN APPLE: clone")
    player.say("GOLDEN SHOVEL: clear")
    player.say("MELON: show ruler")
    player.say("GLISTERING MELON: hide ruler")
    player.say("GOLDEN_LEGGINGS: reset")
}

// ##########   section ONE, command list interface by Magi 2020 #########
player.onChat("mark", function on_mark_handle() {
    ebuilder.acquire()
    ebuilder.mark(player.position(), true)
    ebuilder.release()
})
player.onChat("mark2", function on_mark2_handle() {
    ebuilder.acquire()
    ebuilder.mark2(player.position(), true)
    ebuilder.release()
})
player.onChat("unmark", function on_unmark_handle() {
    ebuilder.acquire()
    ebuilder.unmark()
    ebuilder.release()
})
player.onChat("wall", function on_build_wall_handle() {
    ebuilder.acquire()
    ebuilder.build_wall(setting.buildblock)
    ebuilder.release()
})
player.onChat("line", function on_build_line_handle() {
    ebuilder.acquire()
    ebuilder.build_line(setting.buildblock)
    ebuilder.release()
})
player.onChat("cube", function on_build_cube_handle(high: number = 0) {
    ebuilder.acquire()
    ebuilder.build_cube(setting.buildblock)
    ebuilder.release()
})
player.onChat("hollowcube", function on_build_hollow_cube_handle(high: number = 0) {
    ebuilder.acquire()
    ebuilder.build_hollow_cube(setting.buildblock)
    ebuilder.release()
})
player.onChat("reset", function on_reset_marks_handle() {
    ebuilder.acquire()
    ebuilder.reset_marks()
    ebuilder.release()
})
player.onChat("increase", function on_increase_wall_handle(cnt: number) {
    if (cnt == 0) {
        cnt = 1
    }
    
    ebuilder.acquire()
    ebuilder.increase_wall(setting.buildblock, cnt)
    ebuilder.release()
})
player.onChat("decrease", function on_decrease_wall_handle(cnt: number) {
    if (cnt == 0) {
        cnt = 1
    }
    
    ebuilder.acquire()
    ebuilder.decrease_wall(cnt)
    ebuilder.release()
})
player.onChat("ruler", function on_ruler() {
    ebuilder.acquire()
    ebuilder.show_ruler(pos(0, 0, 0))
    ebuilder.release()
})
player.onChat("hideruler", function on_remove_ruler() {
    ebuilder.acquire()
    ebuilder.hide_ruler()
    ebuilder.release()
})
function float_to_surface() {
    let y = 0
    while (!blocks.testForBlock(AIR, pos(0, y, 0))) {
        y += 1
    }
    if (y > 0) {
        player.teleport(pos(0, y, 0))
    }
    
}

//  clone 0/1
player.onChat("clone", function on_clone_handle(align: any) {
    ebuilder.acquire()
    if (align == 0) {
        ebuilder.clone(player.position(), false)
    } else {
        ebuilder.clone(player.position(), true)
    }
    
    float_to_surface()
    ebuilder.release()
})
player.onChat("clear", function on_clear_handle() {
    ebuilder.acquire()
    ebuilder.clear()
    ebuilder.release()
})
// replace oldblk newblk or replace oldblk
player.onChat("replace", function on_replace_handle(oldblk: number, newblk: number) {
    ebuilder.acquire()
    let arg0 = player.getChatArg(0)
    let arg1 = player.getChatArg(1)
    if (arg1 == undefined) {
        newblk = setting.buildblock
    }
    
    if (arg0 != undefined) {
        ebuilder.replace(oldblk, newblk)
    } else {
        player.say("invalid cmd, use replace oldblock newblock")
    }
    
    ebuilder.release()
})
player.onChat("plant", function on_plant_handle(tree: number, interval: number) {
    if (tree == 0) {
        tree = ACACIA_SAPLING
    }
    
    if (interval == 0) {
        interval = 4
    }
    
    ebuilder.acquire()
    ebuilder.plant(tree, interval)
    ebuilder.release()
})
//  config the type of block to build
player.onChat("setblock", function on_set_blk(blk: number) {
    setting.buildblock = blk
    player.say("set building block to " + ("" + blk))
})
// show marks
player.onChat("dbg", function on_debug() {
    ebuilder.show_marks()
    player.say("buildblock=" + ("" + setting.buildblock))
    player.say("clone align=" + ("" + ui_setting.align))
})
player.onChat("blkmap", function on_show_block_map() {
    let start = pos(0, 0, 0).toWorld()
    for (let i = 0; i < 15; i++) {
        for (let j = 1; j < 11; j++) {
            blocks.place(i * 10 + j, start.add(pos(2 * i + Math.idiv(2 * i, 10), -1, 2 * j)))
        }
    }
})
// ##########   section TWO, user interface by Magi 2020 #########
class ui_setting {
    static buildmode = true
    static align = true
}

//  check build mode
function check_build_mode() {
    return ui_setting.buildmode ? true : false
}

// config build mode on/off
player.onChat("setbuildmode", function on_set_build_mode(mode: any) {
    if (mode == 1) {
        ui_setting.buildmode = true
    } else {
        ui_setting.buildmode = false
    }
    
    if (ui_setting.buildmode) {
        player.say("build mode on")
    } else {
        player.say("build mode off ")
    }
    
})
player.onChat("setalign", function on_set_align(flag: any) {
    if (flag == 0) {
        ui_setting.align = false
    } else {
        ui_setting.align = true
    }
    
    player.say("set clone align to " + ("" + ui_setting.align))
})
player.onItemInteracted(GOLDEN_BOOTS, function on_item_interacted_mark() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.mark(player.position(), true)
    ebuilder.release()
})
player.onItemInteracted(DIAMOND_BOOTS, function on_item_interacted_mark2() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.mark2(player.position(), true)
    ebuilder.release()
})
player.onItemInteracted(IRON_BOOTS, function on_item_interacted_unmark() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    if (ebuilder.mark_num()) {
        ebuilder.unmark()
    } else {
        ebuilder.decrease_wall(1)
    }
    
    ebuilder.release()
})
player.onItemInteracted(GOLDEN_SHOVEL, function on_item_interacted_clear() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.clear()
    ebuilder.release()
})
// player.say("wall build")
player.onItemInteracted(GOLDEN_SWORD, function on_item_interacted_wall() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    let num = ebuilder.mark_num()
    if (num >= 2) {
        ebuilder.build_wall(setting.buildblock)
    } else if (num > 0) {
        player.errorMessage("error,add at least two marks first")
    } else {
        ebuilder.increase_wall(setting.buildblock, 1)
    }
    
    ebuilder.release()
})
// player.say("all marks reset")
player.onItemInteracted(GOLDEN_LEGGINGS, function on_item_interacted_reset() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.reset_marks()
    ebuilder.release()
})
// player.say("clone")
player.onItemInteracted(GOLDEN_APPLE, function on_item_interacted_clone() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.clone(player.position(), ui_setting.align)
    float_to_surface()
    ebuilder.release()
})
player.onItemInteracted(GOLDEN_CARROT, function on_item_interacted_pick_block() {
    let curpos = player.position()
    let footpos = curpos.add(pos(0, -1, 0))
    setting.buildblock = ebuilder.detect_block_at_pos(footpos)
    player.say("set building block: " + ("" + setting.buildblock))
})
player.onItemInteracted(MELON, function on_item_interacted_melon() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.show_ruler(pos(0,0,0))
    ebuilder.release()
})
player.onItemInteracted(GLISTERING_MELON, function on_item_interacted_glistering_melon() {
    if (!check_build_mode()) {
        return
    }
    
    ebuilder.acquire()
    ebuilder.hide_ruler()
    ebuilder.release()
})
function detect_area(curpos: Position, block: number) {
    let x1 = 0
    let x2 = 0
    let y1 = 0
    let y2 = 0
    let z1 = 0
    let z2 = 0
    while (blocks.testForBlock(block, curpos.add(pos(x1, 0, 0)))) {
        x1 -= 1
    }
    while (blocks.testForBlock(block, curpos.add(pos(x2, 0, 0)))) {
        x2 += 1
    }
    while (blocks.testForBlock(block, curpos.add(pos(0, y1, 0)))) {
        y1 -= 1
    }
    while (blocks.testForBlock(block, curpos.add(pos(0, y2, 0)))) {
        y2 += 1
    }
    while (blocks.testForBlock(block, curpos.add(pos(0, 0, z1)))) {
        z1 -= 1
    }
    while (blocks.testForBlock(block, curpos.add(pos(0, 0, z2)))) {
        z2 += 1
    }
    x1 += 1
    x2 -= 1
    y1 += 1
    y2 -= 1
    z1 += 1
    z2 -= 1
    ebuilder.mark(curpos.add(pos(x1, y1, z1)), false)
    ebuilder.mark(curpos.add(pos(x2, y2, z2)), false)
}

function do_replace(checkpos: Position[], checkTorch: number, newTorch: number, relativePos: Position) {
    let x1: Position;
    let x2: Position;
    let replacedblock: number;
    for (let x of checkpos) {
        x1 = x.toWorld()
        if (blocks.testForBlock(checkTorch, x)) {
            blocks.place(newTorch, x)
            x2 = x1.add(relativePos)
            replacedblock = ebuilder.detect_block_at_pos(x2)
            ebuilder.acquire()
            if (ebuilder.mark_num() == 0) {
                detect_area(x2, replacedblock)
            }
            
            ebuilder.replace(replacedblock, setting.buildblock)
            ebuilder.release()
            break
        }
        
    }
}

blocks.onBlockPlaced(0x10032, function on_block_placed_west() {
    let checkpos = [pos(0, 1, 0), pos(-1, 1, 0), pos(-1, 0, 0), pos(-2, 1, 0), pos(-2, 0, 0), pos(-3, 1, 0), pos(-3, 0, 0)]
    //  0xA0032 represents for torch, 0xA004c represents for redstone torch
    //  A=0, EAST; A=1, WEST; A=2, SOUTH; A=4, NORTH
    do_replace(checkpos, 0x10032, 0x1004c, pos(-1, 0, 0))
})
// TORCH FACING EAST
blocks.onBlockPlaced(0x20032, function on_block_placed_east() {
    let checkpos = [pos(0, 1, 0), pos(1, 1, 0), pos(1, 0, 0), pos(2, 1, 0), pos(2, 0, 0), pos(3, 1, 0), pos(3, 0, 0)]
    do_replace(checkpos, 0x20032, 0x2004c, pos(1, 0, 0))
})
// TORCH FACING WEST
blocks.onBlockPlaced(0x30032, function on_block_placed_north() {
    let checkpos = [pos(0, 1, 0), pos(0, 1, -1), pos(0, 0, -1), pos(0, 1, -2), pos(0, 0, -2), pos(0, 1, -3), pos(0, 0, -3)]
    do_replace(checkpos, 0x30032, 0x3004c, pos(0, 0, -1))
})
// TORCH FACING SOUTH
blocks.onBlockPlaced(0x40032, function on_block_placed_south() {
    let checkpos = [pos(0, 1, 0), pos(0, 1, 1), pos(0, 0, 1), pos(0, 1, 2), pos(0, 0, 2), pos(0, 1, 3), pos(0, 0, 3)]
    do_replace(checkpos, 0x40032, 0x4004c, pos(0, 0, 1))
})
// TORCH FACING NORTH
//  on stat,here
player.execute("clear")
mobs.give(mobs.target(ALL_PLAYERS), GOLDEN_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS), IRON_BOOTS, 1)
mobs.give(mobs.target(ALL_PLAYERS), GOLDEN_SWORD, 1)
mobs.give(mobs.target(ALL_PLAYERS), GOLDEN_SHOVEL, 1)
mobs.give(mobs.target(ALL_PLAYERS), GOLDEN_CARROT, 1)
mobs.give(mobs.target(ALL_PLAYERS), TORCH, 1)
mobs.give(mobs.target(ALL_PLAYERS), GOLDEN_APPLE, 1)
mobs.give(mobs.target(ALL_PLAYERS), MELON, 1)
mobs.give(mobs.target(ALL_PLAYERS), GLISTERING_MELON, 1)
mobs.give(mobs.target(ALL_PLAYERS), DIAMOND_BOOTS, 1)
