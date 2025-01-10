import tkinter as tk
import  os
from PIL import Image , ImageTk
from tkinter import filedialog
import torch
from torchvision import transforms

# 创建主窗口
root = tk.Tk()
root.title("wsz GUI")  # 设置窗口标题
root.config(bg='white')
root.geometry("1220x700")  # 设置窗口大小
folder='./diatom/'

classes = {0: 'Achnanthes', 1: 'Achnanthidium', 2: 'Aulacoseira', 3: 'Cocconeis',
           4: 'Cymbella', 5: 'Cymbopleura', 6: 'Diploneis', 7: 'Encyonema', 8: 'Encyonopsis',
           9: 'Epithemia', 10: 'Eunotia', 11: 'Frustulia', 12: 'Gomphoneis', 13: 'Gomphonema',
           14: 'Halamphora', 15: 'Lindavia', 16: 'Navicula', 17: 'Nitzschia', 18: 'Nupela',
           19: 'Pinnularia', 20: 'Planothidium', 21: 'Platessa', 22: 'Psammothidium',
           23: 'Sellaphora', 24: 'Stauroneis', 25: 'Stephanodiscus', 26: 'Surirella', 27: 'dummy'}

classeslist = ['Achnanthes', 'Achnanthidium', 'Aulacoseira', 'Cocconeis',
               'Cymbella', 'Cymbopleura', 'Diploneis\n', 'Encyonema', 'Encyonopsis',
               'Epithemia', 'Eunotia', 'Frustulia\n', 'Gomphoneis', 'Gomphonema',
               'Halamphora', 'Lindavia', 'Navicula', 'Nitzschia', 'Nupela',
               'Pinnularia', 'Planothidium\n', 'Platessa', 'Psammothidium',
               'Sellaphora', 'Stauroneis', 'Stephanodiscus', 'Surirella']

classes_str = ', '.join(classeslist)


# 使用 join() 方法将列表元素连接成逗号分隔的字符串
classes_str = ', '.join(classeslist)
print(classes_str)
def model_output(image_path):  # input img path @ output img class
    # 加载模型
    model = torch.load('./model.pth', map_location=torch.device('cpu'))
    # image_path = '/home/wesjos/one/one/diatom/diatom/aug/diatom genera dataset/diatom genera dataset/35/all-o/fillblack/6000/test/Cymbopleura/Cymbopleura apiculata -25.1(10μm).jpg'
    image = Image.open(image_path).convert('RGB')  # 将图片转换为RGB格式


    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor()
    ])

    # 4. 对图片进行预处理
    input_tensor = transform(image)
    input_batch = input_tensor.unsqueeze(0)

    with torch.no_grad():
        output = model(input_batch)
        topk_values, topk_indices = torch.topk(output, k=3, dim=1)
        print(topk_values, topk_indices)
        a, b = torch.max(output, 1)
        x1=topk_indices[0][0].item()
        x2=topk_indices[0][1].item()
        x3=topk_indices[0][2].item()

        print(classes[x1],classes[x2],classes[x3])
        print(classes[b.numpy()[0]])


    return classes[x1],classes[x2],classes[x3]
def select_image(): # 打开文件对话框，选择图片文件
    # 初始化Tkinter的根窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    # 打开文件对话框，选择图片文件
    file_path = filedialog.askopenfilename(
        title="选择图片",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.tif")]
    )
    # 打印并返回文件路径
    if file_path:
        print(f"选择的图片路径: {file_path}")
    else:
        print("未选择图片")
    return file_path

def show_image(img_path): # 显示图片slot1
    # 创建标签
    img = Image.open(img_path).resize((360, 360))
    image=ImageTk.PhotoImage(img)
    label = tk.Label(root, image=image)
    label.photo=image
    label.place(x=35, y=55)

def right_image(img_path): # 显示图片slot2
    # 创建标签
    img = Image.open(img_path).resize((360, 360))
    image=ImageTk.PhotoImage(img)
    label = tk.Label(root, image=image)
    label.photo=image
    label.place(x=585, y=55)

def right_detail(list): #
    for k,i in enumerate(list):
        label = tk.Label(root, text=f' {i}',font=("Arial", 12), bg="white")
        label.place(x=20, y=480+k*40)
def load_image_from_folder(folder_path):  # input folder path @ output img
    files = os.listdir(folder_path)
    # 筛选出图片文件（可以根据需要扩展支持的格式）
    image_files = [f for f in files if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'))]

    # 如果文件夹中有图片文件，则加载第一张图片
    if image_files:
        image_path = os.path.join(folder_path, image_files[0])  # 读取第一张图片
        return image_path
def get_class_from_txt_files(folder_path):  # input folder path @ output class detail list
    class_values = {}  # 用于存储每个文件的 Class 值
    class_values=[]
    keywords = ['Category', 'Class', 'Order', 'Family', 'Description']
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    txt_files = [f for f in files if f.lower().endswith('.txt')]

    # 遍历每个 .txt 文件
    for txt_file in txt_files:
        file_path = os.path.join(folder_path, txt_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()  # 读取文件中的所有行
                for keyword in keywords:
                    for line in lines:
                        if keyword in line:
                            # class_values[keyword] = line
                            class_values.append(line)
        except Exception as e:
            print(f"无法读取文件 {txt_file}: {e}")

    return class_values

def clear_all_labels():
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

def back_ground():
    slot1path='./img/bg1.png'
    slot2path='./img/bg2.png'
    slot3path='./img/bg3.png'

    label=tk.Label(root, text=f'Your selected image',font=("Arial", 15), bg="white")
    label.place(x=130, y=10)
    label = tk.Label(root, text=f'predicted label',font=("Arial", 15), bg="white")
    label.place(x=700, y=10)

    img1 = Image.open(slot1path).resize((370, 370))
    image=ImageTk.PhotoImage(img1)
    label = tk.Label(root, image=image)
    label.photo=image
    label.place(x=30, y=50)

    img2 = Image.open(slot2path).resize((370, 370))
    image=ImageTk.PhotoImage(img2)
    label = tk.Label(root, image=image)
    label.photo=image
    label.place(x=580, y=50)

    img3 = Image.open(slot3path).resize((100, 100))
    image=ImageTk.PhotoImage(img3)
    label = tk.Label(root, image=image)
    label.photo=image
    label.place(x=440, y=180)
def display_image():#总开关
    global img_path
    global x1,x2,x3
    img_path = select_image()
    clear_all_labels()
    back_ground()
    show_image(img_path)
    x1,x2,x3=model_output(img_path)


def best_choice():#总开关
    clear_all_labels()
    back_ground()
    show_image(img_path)
    nextpath=os.path.join(folder,x1)
    next_img=load_image_from_folder(nextpath)
    nextdetail=get_class_from_txt_files(nextpath)

    right_image(next_img)
    right_detail(nextdetail)

    label=tk.Label(root, text=f'BEST POSSIBILITY:  {x1}',font=("Arial", 20), bg="white",fg='red')
    label.place(x=580, y=430)

def second_choice():
    clear_all_labels()
    back_ground()
    show_image(img_path)
    nextpath=os.path.join(folder,x2)
    next_img=load_image_from_folder(nextpath)
    nextdetail=get_class_from_txt_files(nextpath)

    right_image(next_img)
    right_detail(nextdetail)

    label=tk.Label(root, text=f'SECOND POSSIBILITY:  {x2}',font=("Arial", 20), bg="white",fg='orange')
    label.place(x=580, y=430)

def third_choice():
    clear_all_labels()
    back_ground()
    show_image(img_path)
    nextpath=os.path.join(folder,x3)
    next_img=load_image_from_folder(nextpath)
    nextdetail=get_class_from_txt_files(nextpath)
    right_image(next_img)
    right_detail(nextdetail)

    label=tk.Label(root, text=f'THIRD POSSIBILITY:  {x3}',font=("Arial", 20), bg="white",fg='grey' )
    label.place(x=580, y=430)

def show_popup():
    # 创建一个新窗口
    popup = tk.Toplevel()
    length=len(classeslist)
    # 设置新窗口的标题
    popup.title(f"Identified diatom genera {length}")
    # 设置新窗口的大小
    popup.geometry("800x300")

    # 在新窗口中显示文本
    label = tk.Label(popup, text=classes_str, font=("Arial", 12),fg='black',bg='white')
    label.pack(padx=10, pady=30)
    # label.place(x=0, y=0)
    # 添加一个关闭按钮
    close_button = tk.Button(popup, text="关闭", command=popup.destroy)
    close_button.pack()
    # close_button.place(x=230, y=250)


back_ground()
button = tk.Button(root, text="SELECT  IMAGE", command=display_image,padx=12,pady=12,font=("Arial", 15),fg='white',bg='purple')
button0=tk.Button(root, text="Best     Possibility", command=best_choice,padx=12,pady=12,font=("Arial", 15),fg='white',bg='red')
button1 =tk.Button(root, text="Second Possibility", command=second_choice,padx=12,pady=12,font=("Arial", 15),fg='white',bg='orange')
button2 =tk.Button(root, text="Thied    Possibility", command=third_choice,padx=12,pady=12,font=("Arial", 15),fg='white',bg='grey')
button3 =tk.Button(root, text="HELP", command=show_popup,padx=12,pady=12,font=("Arial", 15),fg='white',bg='green')
button4 =tk.Button(root, text="EXIT", command=root.quit,padx=12,pady=12,font=("Arial", 15),fg='white',bg='black')

button.pack(pady=10)  # 使用 pack 布局，pady设置上下间距
button0.pack(pady=10)  # 使用 pack 布局，pady设置上下间距
button1.pack(pady=10)  # 使用 pack 布局，pady设置上下间距
button2.pack(pady=10)  # 使用 pack 布局，pady设置上下间距
button3.pack(pady=10)  # 使用 pack 布局，pady设置上下间距
button4.pack(pady=10)  # 使用 pack 布局，pady设置上下间距

button.place(x=1000,y=50)
button0.place(x=1000,y=130)
button1.place(x=1000,y=210)
button2.place(x=1000,y=290)
button3.place(x=1000,y=370)
button4.place(x=1120,y=370)
# 启动GUI主循环
root.mainloop()
