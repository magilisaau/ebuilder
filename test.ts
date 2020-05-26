/**
 * Use this file to define custom functions and blocks.
 * Read more at https://minecraft.makecode.com/blocks/custom
 */

enum MyEnum {
    //% block="one"
    One,
    //% block="two"
    Two
}

player.onItemInteracted(GOLDEN_SHOVEL, function () {
    player.say("hello")
})

player.say(":)")
/**
 * Custom blocks
 */
//% weight=100 color=#0fba11 icon=""
namespace custom {
    let weather=128
    /**
     * TODO: describe your function here
     * @param n describe parameter here, eg: 5
     * @param s describe parameter here, eg: "Hello"
     * @param e describe parameter here
     */
    //% block
    export function foo(n: number, s: string, e: MyEnum): number {
        // Add code here
        blocks.place(TOP_SNOW, pos(0,0,0))
        return weather;
    }

    /**
     * TODO: describe your function here
     * @param value describe value here, eg: 5
     */
    //% block
    export function fib(value: number): number {
        return value <= 1 ? value : fib(value -1) + fib(value - 2);
    }
}
// tests go here; this will not be compiled when this package is used as an extension.
