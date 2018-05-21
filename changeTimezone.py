from sys import argv
import dateutil.parser
from datetime import timedelta

shift = int(argv[2])
output = open(argv[1].split(".")[0] + "-adjusted.gpx", "w")

with open(argv[1]) as f:
    for line in f:
        if "<time>" in line:
            s = line.split("T")
            time = s[1].split("Z")[0].split(":")
            date = s[0].replace('<time>', '').strip()
            indentation = s[0].split("<")[0]
            
            newHour = int(time[0]) + shift
            if newHour < 0:
                date  = (dateutil.parser.parse(date) - timedelta(1)).isoformat().split("T")[0]
                newHour = 24 + newHour
            elif newHour >= 24:
                date = (dateutil.parser.parse(date) + timedelta(1)).isoformat().split("T")[0]
                newHour = 0 + newHour - 24

            newHourStr = str(newHour)
            if newHour < 10:
                newHourStr = "0" + newHourStr

            output.write(indentation + "<time>" + date + "T" + newHourStr + ":" + time[1] + ":" + time[2] + "Z</time>\n")

        else:
            output.write(line)

output.close()





