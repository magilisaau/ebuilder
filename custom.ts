 /*
	Author: Magi
	Contact: magilisaau@gmail.com
	CreateTime: 2020/04/20
	ModifyTime: 2020/5/10
	Description: the project is to help kids build house more efficiently and easily in the game minecraft
	
	Author: Magi
	Contact: magilisaau@gmail.com
	ModifyTime: 2020/5/17
	Description: bug fix, clear marks after clear/cube/hollowcube

	Author: Magi
	Contact: magilisaau@gmail.com
	ModifyTime: 2020/6/27
	Description: detatch ruler

	Author: Magi
	Contact: magilisaau@gmail.com
	ModifyTime: 2020/6/28
	Description: rewrite ruler
*/
/*  ############################### section ONE: lib #################################################
	section ONE are fundermental lib for process marks
	detect_block_at_pos(pos)            :get the id of the block at pos
	get_enclosure_from_marks(marks)     :get the cube area enclosed by the marks which previous added
	push_mark(marks,pos)                :add a new mark
	pop_mark(marks)                     :remove the last added mark
	clear_marks(marks)                  :clear all marks previous added
	show_marks(marks)                   :show the marks previous added
	build_wall_from_marks(marks,block)  :build walls according to the previously marks,using block as materials
	increase_wall_from_marks(marks,block): increase one floor on the wall
	decrease_wall_from_marks(marks)     :  decrease one floor of the wall
	clone_from_marks(marks,into,align)  :clone the cube space enclosed by the marks [into] a new place, if align is True, it will align automaticlly with the origin area
	replace_from_marks(marks,newblk, oldblk):replace the old block to new block in the cube space enclosed by the marks 
	clear_from_marks(marks)             :clear the cube space enclosed by the marks 
	build_cube_from_marks(marks)        :build a solid cube according to the previously marks
	build_hollow_cube_from_marks(marks) :like build_cube_from_marks() do, but a hollow cube
	plant_trees_from_marks(marks,tree,interval):plant [trees] in the projective region of the marks on the ground, every [interval] distance
*/

//% weight=100 color=#0fbc20 icon=""
namespace ebuilder{
    function print(msg:string){
        player.say(msg)
    }
    /**
     * get id of the block at the position
     * @param position the position to detect
     */
    //% weight=120
    //% block="detect_block_at_pos %position=minecraftCreatePosition"
	export function detect_block_at_pos(position: Position) {
	    let detail: number;
	    agent.teleport(position.add(pos(0, 1, 0)), WEST)
	    let what = agent.inspect(AgentInspection.Block, DOWN)
	    for (let i = 1; i < 16; i++) {
	        detail = 65536 * i + what
	        if (blocks.testForBlock(detail, position.add(pos(0, -1, 0)))) {
	            return detail
	        }
	        
	    }
	    return what
	}

	//  caculate the cube space the marks occupy
	function get_enclosure_from_marks(marks: Position[]) {
	    let mark = marks[0]
	    let x1 = mark.getValue(Axis.X)
	    let y1 = mark.getValue(Axis.Y)
	    let z1 = mark.getValue(Axis.Z)
	    let x2 = x1
	    let y2 = y1
	    let z2 = z1
	    for (let x of marks) {
	        mark = x
	        if (mark.getValue(Axis.X) < x1) {
	            x1 = mark.getValue(Axis.X)
	        }
	        
	        if (mark.getValue(Axis.X) > x2) {
	            x2 = mark.getValue(Axis.X)
	        }
	        
	        if (mark.getValue(Axis.Y) < y1) {
	            y1 = mark.getValue(Axis.Y)
	        }
	        
	        if (mark.getValue(Axis.Y) > y2) {
	            y2 = mark.getValue(Axis.Y)
	        }
	        
	        if (mark.getValue(Axis.Z) < z1) {
	            z1 = mark.getValue(Axis.Z)
	        }
	        
	        if (mark.getValue(Axis.Z) > z2) {
	            z2 = mark.getValue(Axis.Z)
	        }
	        
	    }
	    return [world(x1, y1, z1), world(x2, y2, z2)]
	}
	
	// place a flag on the top of the cubic space enclosed by the marks, which is useful when clone to a new place
	function place_on_enclosure_top(marks: Position[]) {
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
	    let x1 = start.getValue(Axis.X)
	    let y1 = start.getValue(Axis.Y)
	    let y2 = end.getValue(Axis.Y)
	    let z1 = start.getValue(Axis.Z)
	    let newstart = world(x1, y1, z1).add(pos(0, y2 - y1 + 1, 0))
	    let nesstart_ground = positions.groundPosition(newstart)
	    if (blocks.testForBlock(AIR, nesstart_ground) || blocks.testForBlock(WATER, nesstart_ground)) {
	        blocks.place(REDSTONE_TORCH, nesstart_ground)
	    }
	    
	}
	
	//  add mark
	function push_mark(marks: Position[], curpos: Position, showmark: Boolean = true) {
	    marks.push(curpos.toWorld())
	    if (showmark) {
    	    blocks.place(TOP_SNOW, curpos.toWorld())
	    }	    
	}
	
	//  remove last mark
	function pop_mark(marks: Position[]) {
	    let size = marks.length
	    if (size == 0) {
	        return
	    }
	    let curpos = marks[size - 1]
	    if (blocks.testForBlock(TOP_SNOW, curpos)) {
	        blocks.place(AIR, curpos)
	    }
		_py.py_array_pop(marks)
	}
    //hide marks
    function hide_marks(marks :Position[]){
        let size =marks.length
        if (size > 0){
        for (let p of marks) {
                if (blocks.testForBlock(TOP_SNOW, p)){
                    blocks.place(AIR, p)
                }
	        }
        }
    }
	//  build line from a serial of adjacent marks
	function build_line_from_marks(marks: Position[], block: number = GRASS) {
	    let end: Position;
	    let size = marks.length
	    if (size < 2) {
            //print("error,must mark first")
	        return false
	    }
	    let start = marks[0]
	    for (let i = 1; i < size; i++) {
	        end = marks[i]
	        //blocks.fill(block, start, end)
            shapes.line(GRASS, start, end)
	        start = marks[i]
	    }
	    return true
	}

	//  build wall from a serial of adjacent marks
	function build_wall_from_marks(marks: Position[], block: number = GRASS) {
	    let end: Position;
	    let size = marks.length
	    if (size < 2) {
            //print("error,must mark first")
	        return false
	    }
	    let start = marks[0]
	    for (let i = 1; i < size; i++) {
	        end = marks[i]
	        blocks.fill(block, start, end)
	        start = marks[i]
	    }
	    return true
	}
	
	function increase_wall_from_marks(marks: Position[], block: number = GRASS) {
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return
	    }
	    let closure = get_enclosure_from_marks(marks)
	    let floor = closure[0]
	    let ceil = closure[1]
	    let dy = ceil.getValue(Axis.Y) - floor.getValue(Axis.Y) + 1
	    let newmarks = []
	    for (let x of marks) {
	        newmarks.push(x.add(pos(0, dy, 0)))
	    }
	    copy_marks(marks, newmarks)
	    build_wall_from_marks(marks, block)
	}
	
	function decrease_wall_from_marks(marks: Position[]) {
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return
	    }
	    let closure = get_enclosure_from_marks(marks)
	    let floor = closure[0]
	    let ceil = closure[1]
	    let dy = ceil.getValue(Axis.Y) - floor.getValue(Axis.Y) + 1
	    let newmarks = []
	    for (let x of marks) {
	        newmarks.push(x.add(pos(0, -dy, 0)))
	    }
	    build_wall_from_marks(marks, AIR)
	    copy_marks(marks, newmarks)
	}
/*
	function build_ruler_from_marks(marks: Position[]) {
        let size =marks.length
	    if (size < 2) {
            //print("error,must mark first")
	        return
	    }
        let start =marks[size-2]
        let end =marks[size-1]
        if (size >2){
            let closure = get_enclosure_from_marks(marks)
            start =closure[0]
            end =closure[1]
        }
	    let x1 = start.getValue(Axis.X)
	    let x2 = end.getValue(Axis.X)
	    let y1 = start.getValue(Axis.Y)
	    let z1 = start.getValue(Axis.Z)
	    let z2 = end.getValue(Axis.Z)
        if(z2 > z1){
            for(let z=z1; z<=z2; z+=5){
                blocks.fill(REDSTONE_TORCH, world(x1,y1,z), world(x2,y1,z))
            }
        }
        else{
            for(let z=z1; z>=z2; z-=5){
                blocks.fill(REDSTONE_TORCH, world(x1,y1,z), world(x2,y1,z))
            }            
        }
        if(x2 > x1){
            for(let x=x1; x<=x2; x+=5){
                blocks.fill(REDSTONE_TORCH, world(x,y1,z1), world(x,y1,z2))
            }  
        }
        else{
            for(let x=x1; x>=x2; x-=5){
                blocks.fill(REDSTONE_TORCH, world(x,y1,z1), world(x,y1,z2))
            }              
        }
	}
*/
	function hide_ruler_from_marks(marks: Position[]) {
	    if (marks.length < 2) {
	        return
	    }
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
        blocks.replace(AIR, REDSTONE_TORCH,start,end)
	}

	//  clear all marks
	function clear_marks(marks: Position[]) {
	    while (marks.length) {
	        _py.py_array_pop(marks)
	    }
	}
	
	function copy_marks(dst: Position[], src: Position[]) {
	    clear_marks(dst)
	    for (let x of src) {
	        dst.push(x)
	    }
	}

	function marks_info(marks: Position[]) {
	    let strr = ""
	    for (let x of marks) {
	        strr += "(" + ("" + x) + ")"
	    }
	    return strr
	}
	
	// get mark num
	function marks_num(marks: Position[]) {
	    return marks.length
	}
	
	//  clone from the cube space enclosed by all marks
	function clone_from_marks(marks: Position[], into: Position = player.position(), align: boolean = true) {
	    let xin: boolean;
	    let zin: boolean;
	    let dz: number;
	    let _into_z: number;
	    let dx: number;
	    let _into_x: number;
	    if (marks.length < 2) {
	        return undefined
	    }
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]; let end = closure[1]
	    let x1 = start.getValue(Axis.X); let x2 = end.getValue(Axis.X); let x = into.getValue(Axis.X);
	    let y1 = start.getValue(Axis.Y); let y2 = end.getValue(Axis.Y); let y = into.getValue(Axis.Y);
	    let z1 = start.getValue(Axis.Z); let z2 = end.getValue(Axis.Z); let z = into.getValue(Axis.Z)
	    if (align) {
	        xin = false
	        zin = false
	        if (x >= x1 && x <= x2) {
	            xin = true
	        }
	        if (z >= z1 && z <= z2) {
	            zin = true
	        }
	        if (xin && zin) {
	            x = x1
	            z = z1
	        }
	        if (xin && !zin) {
	            dz = z2 - z1        
	            _into_z = z + dz
	            if (_into_z >= z1 && _into_z <= z2) {
	                z -= dz
	            }
	            x = x1
	        }
	        if (!xin && zin) {
	            dx = x2 - x1
	            _into_x = x + dx
	            if (_into_x >= x1 && _into_x <= x2) {
	                x -= dx
	            }
	            z = z1
	        }
	    }
	    let _into = world(x, y, z)
	    blocks.clone(start, end, _into, CloneMask.Replace, CloneMode.Normal)
	    copy_marks(marks, [_into, world(x + x2 - x1, y + y2 - y1, z + z2 - z1)])
	    return _into.add(pos(0, y2 - y1 + 1, 0))
	}
	
	function replace_from_marks(marks: Position[], newblk: number = GRASS, oldblk: number = GRASS) {
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return false
	    }
	    
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
	    blocks.replace(newblk, oldblk, start, end)
	    return true
	}
	
	function clear_from_marks(marks: Position[] = []) {
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return false
	    }
	    
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
	    blocks.fill(AIR, start, end)
	    return true
	}
	
	// 
	function build_cube_from_marks(marks: Position[], block: number) {
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return false
	    }
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
	    blocks.fill(block, start, end)
	    return true
	}
	
	// 
	function build_hollow_cube_from_marks(marks: Position[], block: number) {
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return false
	    }
	    
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
	    blocks.fill(block, start, end, FillOperation.Hollow)
	    return true
	}
	
	function plant_trees_from_marks(marks: Position[], tree: number = ACACIA_SAPLING, interval: number = 2) {
	    let where: Position;
	    if (marks.length < 2) {
            //print("error,must mark first")
	        return false
	    }
	    
	    let closure = get_enclosure_from_marks(marks)
	    let start = closure[0]
	    let end = closure[1]
	    let x1 = start.getValue(Axis.X)
	    let x2 = end.getValue(Axis.X)
	    let y1 = start.getValue(Axis.Y)
	    let y2 = end.getValue(Axis.Y)
	    let z1 = start.getValue(Axis.Z)
	    let z2 = end.getValue(Axis.Z)
	    for (let x = x1; x < x2 + 1; x += interval) {
	        for (let z = z1; z < z2 + 1; z += interval) {
	            where = positions.groundPosition(world(x, y2, z))
	            blocks.place(tree, where)
	        }
	    }
	    return true
	}
	
/*  ############################### section two ############################################## 
	mark(pos,show)          :mark at the position, show the mark if show=True,else hide it
	unmark()                :del the last mark
	show_marks()            :show all the marks on screen
	show_ruler(pos)         :show rulers in the position
	hide_ruler()            :hide all rulers 
    build_wall(block)       :build walls according to all marks, one wall each two adjacent marks
	build_line(block)       :build lines according to all marks, one line each two adjacent marks
    build_cube(block)       :build a solid cube according to all marks 
	build_hollow_cube(block):build a hollow cube according to all marks 
	reset_marks()           :clear all marks
	increase_wall(block,n)  :add n more floors on the current wall
	decrease_wall(n)        :del n floors of wall
	clone(pos,align)        :clone the cubic space enclosed by all marks to a new position
	clear()                 :clear the cubic space enclosed by all marks
	replace(oldblk,newblk)  :replace the old blocks in the cubic space to the new blocks
	plant(tree,interval)    :plant trees on the ground enclosed by all marks
*/
	// private data 
	let buildmarks:Position[] = []
	let clonemarks:Position[] = []
    let increasemarks:Position[]=[]
    let rulers:Position[]=[]
	/**
     * place a new mark
     * @param position the position to mark
     */
    //% weight=111
    //% show.defl=true
    //% block="place a mark at %position=minecraftCreatePosition and show %show"
    export function mark(position: Position =pos(0,0,0),show: boolean = true) {
	    push_mark(buildmarks, position, show) 
	}  
	/**
     * remove the last mark
     */
    //% weight=110
    //% block="remove the last mark"
    //% hidden
	export function unmark() {
	    pop_mark(buildmarks)
	}

	/**
     * show information of marks
     */
    //% weight=100
    //% block
    //% hidden
	export function show_marks() {
	    player.say(marks_info(buildmarks))
	}

	/**
     * build walls between every two adjacent marks
     * @param block building block id
     */
    //% block="build wall with %block=minecraftBlock"
    //% weight=91
    //% hidden
    //% color="#AA278D"
	export function build_wall(block: number =GRASS) {
	    let result = build_wall_from_marks(buildmarks, block)
	    if (result) {
	        place_on_enclosure_top(buildmarks)
            copy_marks(increasemarks,buildmarks)
            reset_marks()
	    }
	}

	/**
     * build lines between each two adjacent marks
     * @param block building block id
     */
    //% block="build line with %block=minecraftBlock"
    //% weight=90
    //% hidden
    //% color="#AA278D"
	export function build_line(block: number =GRASS) {
        if (marks_num(buildmarks)>=2){
	        build_line_from_marks(buildmarks, block)
            reset_marks()
        }
	}

    let ruler_length =2;
    let ruler_unit =5;
	function hide_one_ruler(curpos: Position) {
        blocks.replace(AIR, REDSTONE_TORCH, curpos.add(pos(-ruler_length*ruler_unit, 0, 0)), curpos.add(pos(ruler_length*ruler_unit, 0, 0)))
	    blocks.replace(AIR, REDSTONE_TORCH, curpos.add(pos(0, 0, -ruler_length*ruler_unit)), curpos.add(pos(0, 0, ruler_length*ruler_unit)))
	}
	/**
     * show ruler
     */
    //% block="show ruler at %curpos=minecraftCreatePosition"
    //% weight=93
    //% hidden
	export function show_ruler(curpos: Position=pos(0,0,0)) {
        let wpos =curpos.toWorld();
        rulers.push(wpos)
        for(let p=0; p< ruler_length; p++){
            blocks.replace(REDSTONE_TORCH, AIR, wpos.add(pos(p*ruler_unit+1,0,0)), wpos.add(pos((p+1)*ruler_unit-1,0,0)))
            blocks.replace(REDSTONE_TORCH, AIR, wpos.add(pos(-p*ruler_unit-1,0,0)),wpos.add(pos(-(p+1)*ruler_unit+1,0,0)))
            blocks.replace(REDSTONE_TORCH, AIR, wpos.add(pos(0,0,p*ruler_unit+1)), wpos.add(pos(0,0,(p+1)*ruler_unit-1)))
            blocks.replace(REDSTONE_TORCH, AIR, wpos.add(pos(0,0,-p*ruler_unit-1)),wpos.add(pos(0,0,-(p+1)*ruler_unit+1)))
        }
	}


   	/**
     * hide ruler from marks
     */
    //% block="hide ruler"
    //% weight=92
    //% hidden
	export function hide_ruler() {
        if(buildmarks.length >= 2){
            hide_ruler_from_marks(buildmarks)
            reset_marks()
            return
        }
        for (let p of rulers) {
            hide_one_ruler(p)
        }
        clear_marks(rulers)
	}

	/**
     * build a solid cube from marks
     * @param block building block id
     */
    //% block="build cube with %block=minecraftBlock"
    //% weight=80
    //% hidden
    //% color="#AA278D"
	export function build_cube(block: number =GRASS) {
	    if(build_cube_from_marks(buildmarks, block)){
            reset_marks()
        }
	}

	/**
     * build a hollow cube from marks
     * @param block building block id
     */
    //% block="build hollow cube with %block=minecraftBlock"
    //% weight=80
    //% hidden
    //% color="#AA278D"
    
	export function build_hollow_cube(block: number =GRASS) {
	    if(build_hollow_cube_from_marks(buildmarks, block)){
            reset_marks()
        }
	}

	/**
     * commit changes and clear all marks
     */
    //% block
    //% weight=100
    //% hidden
	export function reset_marks() {
        let size =buildmarks.length
        if (size > 0){
            hide_marks(buildmarks)
	        clear_marks(buildmarks)
        }
	}
	
	/**
     * get the number of build marks
     */
    //% block
    //% weight=100
    //% hidden
	export function mark_num() {

	    return buildmarks.length
	}


	/**
     * increase the height of the current wall
     * @param cnt wall height
     * @param block building block id
     */
    //% block="increase wall with %block=minecraftBlock by %cnt"
    //% cnt.defl=1
    //% weight=70
    //% hidden
    //% color="#AA278D"
	export function increase_wall(block: number =GRASS,cnt: number=1) {
	    for (let i = 0; i < cnt; i++) {
	        increase_wall_from_marks(increasemarks,block)
	    }
	}
	/**
     * decrease the height of the current wall
     * @param cnt wall height
     */
    //% block="decrease wall by %cnt"
    //% cnt.defl=1
    //% weight=70
    //% hidden
    //% color="#AA278D"
	export function decrease_wall(cnt: number=1) {
	    for (let i = 0; i < cnt; i++) {
	        decrease_wall_from_marks(increasemarks)
	    }
	}
	
	/**
     * clone the cubic space enclosed by all marks into a new position
     * @param to the place to clone into
     * @param align if True,align automaticlly with the cloned space
     */
    //% block="clone %to=minecraftCreatePosition align  %align"
    //% align.defl=true
    //% weight=60
    //% hidden
    //% color="#AA278D"
	export function clone(to: Position, align: boolean = true) {
	    let newpos: Position;
	    if (marks_num(buildmarks) >= 2) {
	        copy_marks(clonemarks, buildmarks)
            reset_marks()
	    }
	    
	    if (marks_num(clonemarks) >= 2) {
	        newpos = clone_from_marks(clonemarks, to, align)
	    }
	}
	/**
     * clear the cubic space enclosed by all marks
     */
    //% block="clear the space enclosed by marks"
    //% weight=60
    //% hidden
    //% color="#AA278D"
	export function clear() {
	    if(clear_from_marks(buildmarks)){
            reset_marks()
        }
	}

	/**
     * replace the old block to new block in the cube space enclosed by the marks 
     * @param oldblk old block
     * @param newblk new block
     */
    //% block="replace %oldblk=minecraftBlock with %newblk=minecraftBlock"
    //% weight=60
    //% hidden 
    //% color="#AA278D"
	export function replace(oldblk: number,newblk: number ) {
	    if(replace_from_marks(buildmarks, newblk, oldblk)){
            reset_marks()
        }
	}
	/**
     * plant trees on the ground enclosed by marks
     * @param tree tree id
     * @param interval tree interval
     */
    //% block="plant %tree=minecraftBlock interval %interval"
    //% interval.defl=1
    //% weight=50
    //% hidden
    //% color="#AA278D"
	export function plant(tree: number, interval: number) {
	    if(plant_trees_from_marks(buildmarks, tree, interval)){
            reset_marks()
        }
	}
	
	class TestBit {
	    static lock = 0
	}
	
    /**
     * acquire a lock
     */
    //% block
    //% weight=10
    //% hidden
	export function acquire() {
	    while (TestBit.lock) {
	        loops.pause(50)
	    }
	    TestBit.lock = 1
	}
	/**
     * release a lock
     */
    //% block
    //% weight=10
    //% hidden
	export function release() {
	    TestBit.lock = 0
	}
}


         