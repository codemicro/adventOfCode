import java.lang.System
import kotlin.system.*
import kotlin.sequences.generateSequence

fun parse(instr: String) {
    
}

fun one(instr: String): Int {
    return 0
}

fun two(instr: String): Int {
    return 0
}

fun main(args: Array<String>) {
    if (args.size < 1 || !(args[0] == "1" || args[0] == "2")) {
        debug("Missing or invalid day argument")
        exitProcess(1)
    }
    val inp = generateSequence(::readLine).joinToString("\n")
    if (args[0] == "1") {
        println("${one(inp)}")
    } else {
        println("${two(inp)}")
    }
}

fun debug(msg: String) {
    System.err.println(msg)
}