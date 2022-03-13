import os


i= 0
with open("data16.csv", "w") as f: #用于从文件中读取图片名字并添加标签 至data3.csv
    for dir in os.listdir("C:/Users/86159/Desktop/data16"):
        for sub_dir in os.listdir(os.path.join("C:/Users/86159/Desktop/data16", dir)):
            name = dir + "/" + sub_dir
            for file in os.listdir(os.path.join("C:/Users/86159/Desktop/data16", dir, sub_dir)):
                line = name + "/" + file + "\t" + str(i) + "\n"
                f.write(line)
            i += 1

