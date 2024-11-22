#!/usr/bin/env python
# %%
import os  
import shutil
import zipfile

# %%
def prompt_user_choice(item_path):
    if os.path.isdir(item_path):
        item_type = '文件夹'
        choices = {  
            'd': '文件夹 - 无法判断',  
            'n': '文件夹 - 不需要整理归类',  
            'y': '文件夹 - 需要整理（整体）',  
            'z': '文件夹 - 需要整理（整体-压缩）',  
        }
    else:
        item_type = '文件'
        choices = {  
            'n': '文件 - 不需要整理归类',  
            'y': '文件 - 需要整理（整体）',  
            'z': '文件 - 需要整理（整体-压缩）',  
        }  
    print(f"\n请为 {item_type} '{item_path}' 选择处理方式:")  
    for key, desc in choices.items():  
        print(f"{key}. {desc}")  
      
    while True:  
        choice = input(f"请输入选择（{'/'.join(choices.keys())}）: ").strip().lower()  
        if choice in choices:  
            return choice  
        else:  
            print("无效的选择，请重新输入。")  

# %%
def compress_item(item_path, zip_path):  
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:  
        if os.path.isfile(item_path):  
            zipf.write(item_path, os.path.basename(item_path))  
        elif os.path.isdir(item_path):  
            for root, dirs, files in os.walk(item_path):  
                for file in files:  
                    file_path = os.path.join(root, file)  
                    relative_path = os.path.relpath(file_path, item_path)  
                    zipf.write(file_path, relative_path)  

# %%
def get_tag_from_user(item_name):  
    tag = input(f"请输入对文件/文件夹 '{item_name}' 的标签: ")  
    return tag

# %%
def create_destination_path(tag):  
    while True:  
        destination_path = os.path.abspath(input(f"请你输入有关 - {tag} - 标签的目标路径"))
        # 检查路径是否存在  
        if os.path.exists(destination_path):  
            # 如果路径存在，检查它是否是一个目录  
            if os.path.isdir(destination_path):
                return destination_path  
            else:  
                print(f"错误：{destination_path} 已存在，但它不是一个目录。")  
                continue
        else:  
            # 如果路径不存在，尝试创建它  
            try:  
                os.makedirs(destination_path)  
                print(f"目标路径路径不存在 - {destination_path} - 已创建。")  
                return destination_path  
            except OSError as e:  
                print(f"创建目录时发生错误: {e}")  
                continue
     
# %%
def writeToFile(tag,cont):
    try:
        with open(recordFile,'a') as ff:
            x=f"{tag}@@@@@@@@@@{cont}\n"
            ff.write(x)
    except:
        print("路径记录到配置文件失败")
        pass
# %%
def process_directory(main_path):  
    if not os.path.isdir(main_path):  
        print(f"错误：'{main_path}' 不是一个有效的目录。")  
        return  
  
     # 用于存储标签和对应的目标路径  
  
    for item_name in os.listdir(main_path):  
        item_path = os.path.join(main_path, item_name)  
        choice = prompt_user_choice(item_path)  
        if choice == 'd':  
            process_directory(item_path)  
        elif choice == 'n':  
            print("已放弃")
            pass  
        elif choice == 'y' or choice == 'z':
            print("现存tag与路径：")
            print(tags_and_destinations)
            tag = get_tag_from_user(item_name)
            destination_path = tags_and_destinations.get(tag)  
            if not destination_path:  
                destination_path = create_destination_path(tag)  
                tags_and_destinations[tag] = destination_path
                writeToFile(tag, destination_path)
            if choice == 'z':
                zip_path = f"{item_path}.zip"
                compress_item(item_path, zip_path)
                print(f"{item_path}->X")
                if os.path.isfile(item_path):  
                    os.remove(item_path)  
                elif os.path.isdir(item_path):  
                    shutil.rmtree(item_path)  
                item_path=zip_path
            print(f"{item_path}->{destination_path}")
            try:
                shutil.move(item_path, destination_path)
            except:
                print(f"无法移动文件")
        else:  
            assert False, f"无效的选项: {choice}"  


# %%
# 主程序入口  
tags_and_destinations = {}
recordFile='./record.ini'
def main():  
    try:
        with open(recordFile,'r') as ff:
            for line in ff.readlines():
                cont=line.strip().split("@@@@@@@@@@")
                tags_and_destinations[cont[0]]=cont[1]
    except:
        print("无法读取配置文件，不存在或无权限")
        pass
    tags_and_destinations
    main_path = input("请输入需要整理的父目录 MainPath: ")  
    main_path = os.path.abspath(main_path)  
    process_directory(main_path)  
  
if __name__ == "__main__":  
    main()


