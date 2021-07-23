import os
basepath = "D://carla-master//carla-master//LibCarla//source//carla//client//"
target = "factory"
results=[]
lines=[]
i =-1
for filename in os.listdir(basepath):
    if basepath+filename == "D://carla-master//carla-master//LibCarla//source//carla//client//detail":
        continue
    with open(basepath + filename) as openfile:
        for line in openfile:
            line = line.strip().lower()
            lines.append(line)
            if target in line:
                results.append((target, line,filename))
print(results)
