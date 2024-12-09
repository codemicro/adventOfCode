import sys
from collections import namedtuple, defaultdict


Segment = namedtuple("Segment", ["id", "len"])


def parse(instr: str) -> list[Segment]:
    res = []
    next_id = 0
    
    for i, v in enumerate(instr):
        v = int(v)
        if i % 2 == 0:
            # this is a file
            res.append(Segment(next_id, v))
            next_id += 1
        else:
            # this is a gap
            res.append(Segment(None, v))
            
    if res[-1].id is None:
        # random gap at the end? no thanks
        res = res[:-1]
            
    return res


def calc_checksum(files: list[Segment]) -> int:
    acc = 0
    pos = 0
    for file in files:
        if file.id is not None:
            # sum of sequence of n consecutive integers is (n / 2)(first + last)
            acc += int((file.len / 2) * ((pos * 2) + file.len - 1) * file.id)
        pos += file.len
    return acc


def one(instr: str):
    files = parse(instr)
        
    i = 0
    while i < len(files) - 1:        
        f = files[i]
        last_file = files[-1]
        
        if last_file.id is None:
            files = files[:-1]
            continue
        
        if f.id is None:
            # _debug(i, files[i])
            last_file = files[-1]
            
            assert last_file.id is not None
            if last_file.len > f.len:
                files[-1] = Segment(last_file.id, last_file.len - f.len)
                files[i] = Segment(last_file.id, f.len)
            elif last_file.len == f.len:
                # we're gonna move all of this so just delete it
                files = files[:-1]
                files[i] = last_file
            else:
                # TODO: when we haven't got enough in this last file so we need to split f into two
                files = files[:-1]
                files[i] = last_file
                assert f.len - last_file.len != 0
                files.insert(i+1, Segment(None, f.len - last_file.len))            
        
        i += 1
    
    return calc_checksum(files)


def two(instr: str):
    files = parse(instr)
    
    gaps = defaultdict(list)
    
    for i, file in enumerate(files):
        if file.id is None and file.len != 0:
            gaps[file.len].append(i)
            
    moved = set()
    
    i = len(files) - 1
    while i > 0:
        f = files[i]
        
        if f.id is not None and f.id not in moved:
            gap_loc = None
            for j, v in enumerate(files):
                if j >= i:
                    break
                
                if v.id is None and v.len >= f.len:
                    gap_loc = j
                    break
                    
            if gap_loc is not None:
                v = files[gap_loc]
                if v.len == f.len:
                    files[i], files[gap_loc] = files[gap_loc], files[i]
                else:
                    files[i] = Segment(None, f.len)
                    files[gap_loc] = f
                    files.insert(gap_loc + 1, Segment(None, v.len - f.len))
                moved.add(f.id)
                
        i -= 1
        
    return calc_checksum(files)


def _debug(*args, **kwargs):
    kwargs["file"] = sys.stderr
    print(*args, **kwargs)


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["1", "2"]:
        print("Missing day argument", file=sys.stderr)
        sys.exit(1)
    inp = sys.stdin.read().strip()
    if sys.argv[1] == "1":
        print(one(inp))
    else:
        print(two(inp))