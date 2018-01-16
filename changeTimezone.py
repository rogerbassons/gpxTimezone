from sys import argv

shift = int(argv[2])
output = open(argv[1].split(".")[0] + "-adjusted.gpx", "w")

with open(argv[1]) as f:
    for line in f:
        if "<time>" in line:
            s = line.split("T")
            time = s[1].split(":")
            
            new = int(time[0]) + shift

            newStr = str(new)
            if new < 10:
                newStr = "0" + newStr

            output.write(s[0] + "T" + newStr + ":" + time[1] + ":" + time[2].split("Z")[0] + "Z</time>\n")

        else:
            output.write(line)

output.close()





