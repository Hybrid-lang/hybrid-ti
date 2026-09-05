# -*-encoding=utf-8-*-
import io

def clean_spaceline(code):
    result = ""
    for line in io.StringIO(code):
        if line.strip():
            result += line
    return result

def clean_notation(code):
    result = ""
    flag = False
    # code = clean_spaceline(code)
    for line in io.StringIO(code):
        i = 0
        #for i in range(len(line)):
        while i < len(line):
            #print(i)
            #if flag:
                #if i+1 < len(line) and line[i] == "#" and
            #else:
            #if flag:
            #    pass
            #else:
            #    if line[i] == "#":
            #        result += "\n"
            #        break
            #    else:
            #        result += line[i]
            if i+1 < len(line) and line[i] == "#" and line[i+1] == "#":
                flag = not flag
                #print("+2")
                i += 2
            if flag:
                if line[i] == "\n":
                    result += "\n"
                else:
                    pass
            else:
                if line[i] == "#":
                    result += "\n"
                    break
                else:
                    result += line[i]
            i += 1
    # result = clean_spaceline(result)
    return result

if __name__ == "__main__":
    code = """# 1
1/0
"""

    print(repr(clean_notation(code)))
