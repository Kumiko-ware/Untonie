#import pdb; pdb.set_trace()

string="24.mp3"

def filename(path) :
    end_ptr=0
    for i in range(len(path)-1,0,-1) :
        if end_ptr == 0 and path[i]=="." :
            end_ptr = i
        if path[i]=="/" :
            break
    return path[i+1:end_ptr]

def break_16(msg):
    last_break = 0
    last_space = 0
    lines = []
    for i in range (0, len(msg)):
        if msg[i] == " " :
            last_space = i
        if i % 16 == 0 and i != 0:
            if last_space == last_break :
                print("No break")
                lines.append(msg[last_break:i])
                last_break = i
            else :
                print("Do it")
                lines.append(msg[last_break:last_space])
                last_break = last_space + 1
            last_space = last_break
    if (last_break<len(msg)):
        lines.append(msg[last_break:])
    if len(lines) == 0 :
        lines.append(msg)
    return lines

name=filename(string)
print(name)
lines=break_16(name)
print(len(lines))
for i in range(0,len(lines)):
    print(str(i))
    print(lines[i])
