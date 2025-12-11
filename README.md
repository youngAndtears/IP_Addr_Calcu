# IP_Addr_Calcu
IP地址计算器

源码可执行使用python运行，如果需要打包为win可执行文件，请执行 pyinstaller -F -w -i 你的图标名称.ico -n "网络工程师IP计算器" --clean --strip 你的python文件名.py

# 界面如图所示

<img width="1920" height="1030" alt="image" src="https://github.com/user-attachments/assets/034fd2fa-55b3-4de9-a5ea-556e4481ee25" />


# 如果编译打包后提示如下报错：

<img width="503" height="402" alt="image" src="https://github.com/user-attachments/assets/2bf9173d-0571-4466-b305-f824c03a4205" />

是因为打包后的exe所在的位置缺少ico图标文件，可自行在源码中删除图标文件的代码

或使用无图标启动，删除位置如下：

self.root.iconbitmap(default='./2.ico')  # 如果有图标文件可以添加
