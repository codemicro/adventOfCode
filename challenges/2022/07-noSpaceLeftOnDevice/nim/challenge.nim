import std/strutils
import std/tables

type
    Path = ref object
        parts: seq[string]

proc newPath(): Path =
    new result
    result.parts = newSeq[string]()

proc cd(self: Path, arg: string) =
    if arg == "..":
        self.parts = self.parts[0..<self.parts.len-1]
    elif arg != ".":
        self.parts.add(arg)
    
proc cwd(self: Path): string =
    let x = self.parts.join("/")
    if x.len == 0:
        return "/"
    return x

proc absInCWD(self: Path, path: string): string =
    let cwd = self.cwd()
    if cwd == "/":
        return "/" & path
    return cwd & "/" & path

type
    Directories = ref object
        directoryNames: seq[string]
        files: TableRef[string, int]

proc newDirectories(): Directories =
    new result
    result.directoryNames = newSeq[string]()
    result.files = newTable[string, int]()

proc addDir(self: Directories, path: string) =
    if not self.directoryNames.contains(path):
        self.directoryNames.add(path)

proc addFile(self: Directories, path: string, size: int) = 
    self.files[path] = size

proc parse(instr: string): Directories =
    let dirs = newDirectories()
    let fp = newPath()

    var i = 0
    let lines = instr.strip().splitlines()
    while i < lines.len:
        var line = lines[i]
        if line.startsWith("$ cd"):
            line.removePrefix("$ cd ")
            fp.cd(line)
            dirs.addDir(fp.cwd())

        elif line.startsWith("$ ls"):
            while i < lines.len - 1 and not lines[i + 1].startsWith("$"):
                i += 1
                line = lines[i]

                let sp = line.split(" ")
                if sp[0] == "dir":
                    dirs.addDir(fp.absInCWD(sp[1]))
                else:
                    dirs.addFile(fp.absInCWD(sp[1]), parseInt(sp[0]))
        
        i += 1
    
    return dirs

proc calculateDirectorySize(dirs: Directories, targetDirName: string): int =
    for fname, size in dirs.files.pairs():
        if fname.startsWith(targetDirName & "/"):
            result += size

proc partOne*(instr: string): int = 
    let dirs = parse(instr)

    for dirName in dirs.directoryNames:
        let size = calculateDirectorySize(dirs, dirName)
        if size <= 100000:
            result += size

proc partTwo*(instr: string): int = 
    let
        dirs = parse(instr)
        
        used = 70000000 - calculateDirectorySize(dirs, "")
        amountToDelete = 30000000 - used

    var opts: seq[int]
    for dirName in dirs.directoryNames:
        let size = calculateDirectorySize(dirs, dirName)
        if size >= amountToDelete:
            opts.add(size)

    return min(opts)