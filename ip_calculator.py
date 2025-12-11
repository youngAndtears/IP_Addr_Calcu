import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import ipaddress
import math
import re
import socket
import struct
from tkinter import font


class IPCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("网络工程师IP计算器")
        self.root.geometry("1100x850")

        # 设置鲜艳的颜色主题
        self.colors = {
            'primary': '#3498db',  # 鲜艳蓝色
            'primary_dark': '#2980b9',  # 深蓝色
            'secondary': '#2ecc71',  # 鲜艳绿色
            'secondary_dark': '#27ae60',  # 深绿色
            'accent': '#e74c3c',  # 鲜艳红色
            'accent_dark': '#c0392b',  # 深红色
            'warning': '#f39c12',  # 鲜艳橙色
            'warning_dark': '#d35400',  # 深橙色
            'purple': '#9b59b6',  # 鲜艳紫色
            'purple_dark': '#8e44ad',  # 深紫色
            'teal': '#1abc9c',  # 鲜艳青色
            'teal_dark': '#16a085',  # 深青色
            'yellow': '#f1c40f',  # 鲜艳黄色
            'yellow_dark': '#f39c12',  # 深黄色
            'background': '#ecf0f1',  # 浅灰背景
            'card_bg': '#ffffff',  # 卡片背景
            'text_primary': '#2c3e50',  # 主要文字
            'text_secondary': '#7f8c8d',  # 次要文字
            'border': '#bdc3c7',  # 边框颜色
            'success': '#27ae60',  # 成功色
            'error': '#e74c3c',  # 错误色
            'info': '#3498db',  # 信息色
            'highlight': '#f1c40f'  # 高亮色
        }

        # 设置窗口背景
        self.root.configure(bg=self.colors['background'])

        # 设置图标和标题
        self.root.iconbitmap(default='./2.ico')  # 如果有图标文件可以添加

        # 设置样式
        self.setup_styles()

        # 创建主框架
        self.create_widgets()

    def setup_styles(self):
        """设置现代化UI样式"""
        style = ttk.Style()
        style.theme_use('clam')

        # 配置主框架样式
        style.configure('TFrame', background=self.colors['background'])
        style.configure('TLabel', background=self.colors['background'],
                        foreground=self.colors['text_primary'],
                        font=('Microsoft YaHei', 10))
        style.configure('Header.TLabel',
                        font=('Microsoft YaHei', 18, 'bold'),
                        foreground=self.colors['primary'])
        style.configure('Subheader.TLabel',
                        font=('Microsoft YaHei', 12, 'bold'),
                        foreground=self.colors['text_primary'])
        style.configure('Result.TLabel',
                        font=('Consolas', 10),
                        background=self.colors['card_bg'],
                        foreground=self.colors['text_primary'],
                        relief='solid', borderwidth=1)

        # 配置选项卡样式 - 使用鲜艳颜色
        style.configure('TNotebook',
                        background=self.colors['background'],
                        borderwidth=0)
        style.configure('TNotebook.Tab',
                        background=self.colors['primary'],
                        foreground='white',
                        padding=[15, 5],
                        font=('Microsoft YaHei', 10, 'bold'))
        style.map('TNotebook.Tab',
                  background=[('selected', self.colors['accent'])],
                  foreground=[('selected', 'white')],
                  expand=[('selected', [1, 1, 1, 0])])

        # 配置树形视图样式
        style.configure('Treeview',
                        background=self.colors['card_bg'],
                        foreground=self.colors['text_primary'],
                        fieldbackground=self.colors['card_bg'],
                        rowheight=30,
                        font=('Microsoft YaHei', 9),
                        borderwidth=1,
                        relief='solid')
        style.map('Treeview',
                  background=[('selected', self.colors['primary']),
                              ('focus', self.colors['primary_dark'])],
                  foreground=[('selected', 'white')])
        style.configure('Treeview.Heading',
                        background=self.colors['secondary'],
                        foreground='white',
                        font=('Microsoft YaHei', 10, 'bold'),
                        padding=6,
                        borderwidth=0,
                        relief='flat')
        style.map('Treeview.Heading',
                  background=[('active', self.colors['secondary_dark'])])

        # 配置滚动条样式
        style.configure('Vertical.TScrollbar',
                        background=self.colors['primary'],
                        troughcolor=self.colors['background'],
                        bordercolor=self.colors['border'],
                        arrowcolor='white',
                        gripcount=0)

        # 配置标签框架样式
        style.configure('TLabelframe',
                        background=self.colors['background'],
                        relief='solid',
                        borderwidth=1)
        style.configure('TLabelframe.Label',
                        background=self.colors['primary'],
                        foreground='white',
                        font=('Microsoft YaHei', 10, 'bold'),
                        padding=(10, 5))

        # 自定义圆角按钮样式
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """创建自定义圆角按钮样式"""
        style = ttk.Style()

        # 主要按钮样式 - 鲜艳蓝色
        style.configure('Rounded.TButton',
                        font=('Microsoft YaHei', 10, 'bold'),
                        padding=12,
                        background=self.colors['primary'],
                        foreground='white',
                        borderwidth=0,
                        focuscolor='none',
                        focusthickness=0,
                        relief='flat',
                        width=15)

        style.map('Rounded.TButton',
                  background=[('active', self.colors['primary_dark']),
                              ('pressed', self.colors['primary_dark'])],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        # 成功按钮样式 - 鲜艳绿色
        style.configure('Success.Rounded.TButton',
                        background=self.colors['secondary'],
                        foreground='white')

        style.map('Success.Rounded.TButton',
                  background=[('active', self.colors['secondary_dark']),
                              ('pressed', self.colors['secondary_dark'])],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        # 警告按钮样式 - 鲜艳橙色
        style.configure('Warning.Rounded.TButton',
                        background=self.colors['warning'],
                        foreground='white')

        style.map('Warning.Rounded.TButton',
                  background=[('active', self.colors['warning_dark']),
                              ('pressed', self.colors['warning_dark'])],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        # 危险按钮样式 - 鲜艳红色
        style.configure('Danger.Rounded.TButton',
                        background=self.colors['accent'],
                        foreground='white')

        style.map('Danger.Rounded.TButton',
                  background=[('active', self.colors['accent_dark']),
                              ('pressed', self.colors['accent_dark'])],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        # 次要按钮样式 - 青色
        style.configure('Secondary.Rounded.TButton',
                        background=self.colors['teal'],
                        foreground='white')

        style.map('Secondary.Rounded.TButton',
                  background=[('active', self.colors['teal_dark']),
                              ('pressed', self.colors['teal_dark'])],
                  foreground=[('active', 'white'), ('pressed', 'white')])

        # 紫色按钮样式
        style.configure('Purple.Rounded.TButton',
                        background=self.colors['purple'],
                        foreground='white')

        style.map('Purple.Rounded.TButton',
                  background=[('active', self.colors['purple_dark']),
                              ('pressed', self.colors['purple_dark'])],
                  foreground=[('active', 'white'), ('pressed', 'white')])

    def create_rounded_button(self, parent, text, command, style='Rounded.TButton', width=None):
        """创建圆角按钮"""
        btn = ttk.Button(parent, text=text, command=command, style=style)
        if width:
            btn.configure(width=width)
        return btn

    def create_gradient_frame(self, parent, width, height, color1, color2):
        """创建渐变背景框架"""
        frame = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        for i in range(width):
            # 计算渐变颜色
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)

            r = int(r1 + (r2 - r1) * i / width)
            g = int(g1 + (g2 - g1) * i / width)
            b = int(b1 + (b2 - b1) * i / width)

            color = f'#{r:02x}{g:02x}{b:02x}'
            frame.create_line(i, 0, i, height, fill=color)

        return frame

    def create_widgets(self):
        """创建界面组件"""
        # 创建渐变标题栏
        header_frame = tk.Frame(self.root, height=100, bg=self.colors['background'])
        header_frame.pack(fill='x', padx=0, pady=0)

        # 渐变背景装饰
        gradient_canvas = self.create_gradient_frame(header_frame, 1100, 4,
                                                     self.colors['primary'],
                                                     self.colors['secondary'])
        gradient_canvas.pack(fill='x', side='top')

        # 标题内容
        title_content = tk.Frame(header_frame, bg=self.colors['background'], height=96)
        title_content.pack(fill='both', expand=True, padx=20, pady=10)

        # 主标题 - 使用鲜艳颜色
        title_label = tk.Label(title_content,
                               text="🌐 网络工程师IP计算器",
                               font=('Microsoft YaHei', 24, 'bold'),
                               bg=self.colors['background'],
                               fg=self.colors['primary'])
        title_label.pack(side='left', anchor='w')

        # 副标题
        subtitle_label = tk.Label(title_content,
                                  text="IPv4地址计算、子网划分与网络工具集",
                                  font=('Microsoft YaHei', 12),
                                  bg=self.colors['background'],
                                  fg=self.colors['text_secondary'])
        subtitle_label.pack(side='left', padx=(20, 0), pady=(10, 0))

        # 装饰元素
        decor_frame = tk.Frame(title_content, bg=self.colors['background'])
        decor_frame.pack(side='right', padx=10)

        # 创建彩色装饰点
        colors = [self.colors['primary'], self.colors['secondary'],
                  self.colors['warning'], self.colors['accent'], self.colors['purple']]
        for i, color in enumerate(colors):
            dot = tk.Canvas(decor_frame, width=12, height=12, bg=self.colors['background'],
                            highlightthickness=0)
            dot.create_oval(1, 1, 11, 11, fill=color, outline=color)
            dot.grid(row=0, column=i, padx=2)

        # 主容器
        main_frame = tk.Frame(self.root, bg=self.colors['background'], padx=15, pady=10)
        main_frame.pack(fill='both', expand=True)

        # 创建选项卡
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True, pady=(0, 10))

        # 创建各个功能选项卡
        self.create_ip_info_tab()
        self.create_subnet_calculator_tab()
        self.create_subnet_division_tab()
        self.create_advanced_tools_tab()
        self.create_network_tools_tab()

        # 状态栏 - 使用鲜艳颜色
        status_frame = tk.Frame(self.root, height=40, bg=self.colors['primary'])
        status_frame.pack(fill='x', side='bottom', padx=0, pady=0)

        self.status_var = tk.StringVar(value="就绪 - 请输入IP地址或网络进行计算")
        status_label = tk.Label(status_frame,
                                textvariable=self.status_var,
                                font=('Microsoft YaHei', 10),
                                bg=self.colors['primary'],
                                fg='white',
                                padx=20)
        status_label.pack(side='left', anchor='w')

        # 添加装饰线
        decor_line = tk.Frame(status_frame, height=3, bg=self.colors['secondary'])
        decor_line.pack(side='bottom', fill='x')

    def create_styled_entry(self, parent, width=25, default_text=""):
        """创建样式化输入框"""
        entry = tk.Entry(parent,
                         width=width,
                         font=('Consolas', 10),
                         bg=self.colors['card_bg'],
                         fg=self.colors['text_primary'],
                         relief='solid',
                         borderwidth=2,
                         highlightbackground=self.colors['primary'],
                         highlightcolor=self.colors['secondary'],
                         highlightthickness=1,
                         insertbackground=self.colors['primary'])
        if default_text:
            entry.insert(0, default_text)
        return entry

    def create_styled_text(self, parent, width=45, height=15):
        """创建样式化文本框"""
        text = scrolledtext.ScrolledText(parent,
                                         width=width,
                                         height=height,
                                         bg=self.colors['card_bg'],
                                         fg=self.colors['text_primary'],
                                         font=('Consolas', 10),
                                         relief='solid',
                                         borderwidth=2,
                                         highlightbackground=self.colors['primary'],
                                         highlightthickness=1)
        return text

    def create_styled_label(self, parent, text, font_size=10, bold=False, color=None):
        """创建样式化标签"""
        font_config = ('Microsoft YaHei', font_size, 'bold' if bold else 'normal')
        fg_color = color if color else self.colors['text_primary']

        label = tk.Label(parent,
                         text=text,
                         font=font_config,
                         bg=self.colors['background'],
                         fg=fg_color)
        return label

    def create_ip_info_tab(self):
        """创建IP信息计算选项卡"""
        tab = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(tab, text="📊 IP信息计算")

        # 输入区域
        input_frame = tk.LabelFrame(tab,
                                    text="输入IP地址和掩码",
                                    font=('Microsoft YaHei', 11, 'bold'),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['primary'],
                                    relief='solid',
                                    borderwidth=2,
                                    padx=20,
                                    pady=15)
        input_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 15), padx=5)

        # 输入框和标签
        self.create_styled_label(input_frame, "IP地址/网络:", 10, True, self.colors['primary']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.ip_entry = self.create_styled_entry(input_frame, 30, "192.168.1.0/24")
        self.ip_entry.grid(row=0, column=1, padx=(0, 15))

        self.create_styled_label(input_frame, "或掩码位数:", 10, True, self.colors['primary']
                                 ).grid(row=0, column=2, sticky='w', padx=(0, 10))

        self.cidr_entry = self.create_styled_entry(input_frame, 8)
        self.cidr_entry.grid(row=0, column=3, padx=(0, 15))

        # 计算按钮 - 使用鲜艳绿色
        self.create_rounded_button(input_frame, "🚀 计算", self.calculate_ip_info,
                                   style='Success.Rounded.TButton').grid(row=0, column=4, padx=(10, 0))

        # 示例按钮区域
        example_frame = tk.Frame(input_frame, bg=self.colors['card_bg'])
        example_frame.grid(row=1, column=0, columnspan=5, pady=(15, 0))

        self.create_styled_label(example_frame, "示例:", 10, False, self.colors['text_secondary']
                                 ).grid(row=0, column=0, padx=(0, 10))

        examples = ["192.168.1.0/24", "10.0.0.0/8", "172.16.0.0/16", "65.13.111.169/27"]
        colors = [self.colors['primary'], self.colors['secondary'],
                  self.colors['warning'], self.colors['purple']]

        for i, (example, color) in enumerate(zip(examples, colors)):
            btn = self.create_rounded_button(example_frame, example, width=18,
                                             command=lambda e=example: self.load_example(e),
                                             style='Secondary.Rounded.TButton')
            btn.configure(style='Secondary.Rounded.TButton')
            btn.grid(row=0, column=i + 1, padx=5)

        # 结果区域 - 使用卡片式设计
        result_frame = tk.LabelFrame(tab,
                                     text="计算结果",
                                     font=('Microsoft YaHei', 11, 'bold'),
                                     bg=self.colors['card_bg'],
                                     fg=self.colors['secondary'],
                                     relief='solid',
                                     borderwidth=2,
                                     padx=20,
                                     pady=15)
        result_frame.grid(row=1, column=0, sticky='nsew', pady=(0, 10), padx=5)

        # 创建结果标签 - 使用鲜艳图标颜色
        results = [
            ("📌 网络地址:", "network", self.colors['primary']),
            ("📡 广播地址:", "broadcast", self.colors['secondary']),
            ("🔒 子网掩码:", "netmask", self.colors['warning']),
            ("🔄 反掩码:", "wildcard", self.colors['purple']),
            ("📈 可用地址范围:", "range", self.colors['teal']),
            ("👥 可用主机数:", "hosts", self.colors['accent']),
            ("🔤 IP类型:", "ip_type", self.colors['primary']),
            ("🏷️ 地址类别:", "class_type", self.colors['secondary']),
            ("🏠 是否为私有地址:", "is_private", self.colors['warning']),
        ]

        for i, (label, var_name, color) in enumerate(results):
            label_widget = self.create_styled_label(result_frame, label, 10, False, color)
            label_widget.grid(row=i, column=0, sticky='w', pady=4)

            setattr(self, f"{var_name}_var", tk.StringVar(value=""))

            result_label = tk.Label(result_frame,
                                    textvariable=getattr(self, f"{var_name}_var"),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['text_primary'],
                                    font=('Consolas', 10),
                                    relief='solid',
                                    borderwidth=1,
                                    anchor='w',
                                    padx=12,
                                    pady=6)
            result_label.grid(row=i, column=1, sticky='ew', pady=4, padx=(10, 0), ipadx=5, ipady=2)

        # 二进制表示区域
        binary_frame = tk.LabelFrame(tab,
                                     text="二进制和十六进制表示",
                                     font=('Microsoft YaHei', 11, 'bold'),
                                     bg=self.colors['card_bg'],
                                     fg=self.colors['teal'],
                                     relief='solid',
                                     borderwidth=2,
                                     padx=20,
                                     pady=15)
        binary_frame.grid(row=1, column=1, sticky='nsew', pady=(0, 10), padx=5)

        self.binary_text = self.create_styled_text(binary_frame, 45, 15)
        self.binary_text.grid(row=0, column=0, sticky='nsew')

        # 配置权重
        tab.columnconfigure(0, weight=1)
        tab.columnconfigure(1, weight=1)
        tab.rowconfigure(1, weight=1)
        result_frame.columnconfigure(1, weight=1)
        binary_frame.columnconfigure(0, weight=1)
        binary_frame.rowconfigure(0, weight=1)

    def create_subnet_calculator_tab(self):
        """创建子网计算器选项卡"""
        tab = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(tab, text="🔍 子网计算器")

        # 输入区域
        input_frame = tk.LabelFrame(tab,
                                    text="子网划分参数",
                                    font=('Microsoft YaHei', 11, 'bold'),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['primary'],
                                    relief='solid',
                                    borderwidth=2,
                                    padx=20,
                                    pady=15)
        input_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 15), padx=5)

        # 网络地址输入
        self.create_styled_label(input_frame, "网络地址:", 10, True, self.colors['primary']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.subnet_ip_entry = self.create_styled_entry(input_frame, 25, "192.168.1.0/24")
        self.subnet_ip_entry.grid(row=0, column=1, padx=(0, 15))

        # 子网数量输入
        self.create_styled_label(input_frame, "需要子网数:", 10, True, self.colors['primary']
                                 ).grid(row=0, column=2, sticky='w', padx=(0, 10))

        self.subnet_count_entry = self.create_styled_entry(input_frame, 12, "4")
        self.subnet_count_entry.grid(row=0, column=3, padx=(0, 15))

        # 主机数输入
        self.create_styled_label(input_frame, "或每子网主机数:", 10, True, self.colors['primary']
                                 ).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(15, 0))

        self.hosts_per_subnet_entry = self.create_styled_entry(input_frame, 12)
        self.hosts_per_subnet_entry.grid(row=1, column=1, padx=(0, 15), pady=(15, 0))

        # 按钮 - 使用不同鲜艳颜色
        self.create_rounded_button(input_frame, "按子网数划分", self.calculate_subnets_by_count,
                                   style='Purple.Rounded.TButton').grid(row=0, column=4, padx=(10, 0))

        self.create_rounded_button(input_frame, "按主机数划分", self.calculate_subnets_by_hosts,
                                   style='Success.Rounded.TButton').grid(row=1, column=4, padx=(10, 0), pady=(15, 0))

        # 双栏结果区域
        result_frame = tk.Frame(tab, bg=self.colors['background'])
        result_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(0, 10), padx=5)

        # 左栏：子网划分结果
        left_frame = tk.LabelFrame(result_frame,
                                   text="子网划分结果",
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   bg=self.colors['card_bg'],
                                   fg=self.colors['secondary'],
                                   relief='solid',
                                   borderwidth=2,
                                   padx=15,
                                   pady=15)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # 创建结果树形视图
        columns = ("子网", "网络地址", "广播地址", "可用地址范围", "子网掩码", "主机数", "利用率")
        self.subnet_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=10)

        column_widths = [60, 120, 120, 160, 120, 80, 80]
        for col, width in zip(columns, column_widths):
            self.subnet_tree.heading(col, text=col)
            self.subnet_tree.column(col, width=width, anchor='center')

        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=self.subnet_tree.yview)
        self.subnet_tree.configure(yscrollcommand=scrollbar.set)

        self.subnet_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # 汇总信息
        summary_frame = tk.Frame(left_frame, bg=self.colors['card_bg'])
        summary_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=(15, 0))

        summary_data = [
            ("所需掩码位数:", "new_cidr_var", self.colors['primary']),
            ("新子网掩码:", "new_mask_var", self.colors['secondary']),
            ("总主机数:", "total_hosts_var", self.colors['warning']),
            ("地址利用率:", "utilization_var", self.colors['teal'])
        ]

        for i, (label, var_name, color) in enumerate(summary_data):
            frame = tk.Frame(summary_frame, bg=self.colors['card_bg'])
            frame.grid(row=0, column=i, padx=(0, 15), sticky='w')

            self.create_styled_label(frame, label, 9, True, color).grid(row=0, column=0, sticky='w')

            setattr(self, var_name, tk.StringVar())

            value_label = tk.Label(frame,
                                   textvariable=getattr(self, var_name),
                                   bg=self.colors['card_bg'],
                                   fg=color,
                                   font=('Consolas', 9, 'bold'),
                                   relief='solid',
                                   borderwidth=1,
                                   anchor='w',
                                   padx=8,
                                   pady=4)
            value_label.grid(row=1, column=0, sticky='w', pady=(5, 0))

        # 右栏：计算过程
        right_frame = tk.LabelFrame(result_frame,
                                    text="计算过程",
                                    font=('Microsoft YaHei', 11, 'bold'),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['warning'],
                                    relief='solid',
                                    borderwidth=2,
                                    padx=15,
                                    pady=15)
        right_frame.grid(row=0, column=1, sticky='nsew')

        self.calculation_process_text = self.create_styled_text(right_frame, 45, 25)
        self.calculation_process_text.grid(row=0, column=0, sticky='nsew')

        # 配置权重
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        result_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

    def create_subnet_division_tab(self):
        """创建VLSM子网划分选项卡"""
        tab = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(tab, text="📐 VLSM子网划分")

        # 输入区域
        input_frame = tk.LabelFrame(tab,
                                    text="VLSM子网划分参数",
                                    font=('Microsoft YaHei', 11, 'bold'),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['purple'],
                                    relief='solid',
                                    borderwidth=2,
                                    padx=20,
                                    pady=15)
        input_frame.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 15), padx=5)

        # 网络地址输入
        self.create_styled_label(input_frame, "网络地址:", 10, True, self.colors['purple']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.vlsm_ip_entry = self.create_styled_entry(input_frame, 25, "192.168.1.0/24")
        self.vlsm_ip_entry.grid(row=0, column=1, padx=(0, 15))

        # 子网需求输入
        self.create_styled_label(input_frame, "子网需求(主机数，用逗号分隔):", 10, True, self.colors['purple']
                                 ).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(15, 0))

        self.vlsm_requirements_entry = self.create_styled_entry(input_frame, 45, "60, 30, 12, 5")
        self.vlsm_requirements_entry.grid(row=1, column=1, columnspan=2, sticky='w', padx=(0, 15), pady=(15, 0))

        # 按钮 - 使用鲜艳紫色
        self.create_rounded_button(input_frame, "执行VLSM划分", self.calculate_vlsm,
                                   style='Purple.Rounded.TButton').grid(row=2, column=0, columnspan=3, pady=(15, 0))

        # 双栏结果区域
        result_frame = tk.Frame(tab, bg=self.colors['background'])
        result_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', pady=(0, 10), padx=5)

        # 左栏：VLSM划分结果
        left_frame = tk.LabelFrame(result_frame,
                                   text="VLSM划分结果",
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   bg=self.colors['card_bg'],
                                   fg=self.colors['teal'],
                                   relief='solid',
                                   borderwidth=2,
                                   padx=15,
                                   pady=15)
        left_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 10))

        # 创建结果树形视图
        columns = ("需求", "子网", "网络地址", "广播地址", "可用地址范围", "子网掩码", "主机数", "利用率")
        self.vlsm_tree = ttk.Treeview(left_frame, columns=columns, show="headings", height=10)

        column_widths = [60, 60, 110, 110, 140, 110, 80, 60]
        for col, width in zip(columns, column_widths):
            self.vlsm_tree.heading(col, text=col)
            self.vlsm_tree.column(col, width=width, anchor='center')

        scrollbar = ttk.Scrollbar(left_frame, orient='vertical', command=self.vlsm_tree.yview)
        self.vlsm_tree.configure(yscrollcommand=scrollbar.set)

        self.vlsm_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')

        # 右栏：计算过程
        right_frame = tk.LabelFrame(result_frame,
                                    text="VLSM计算过程",
                                    font=('Microsoft YaHei', 11, 'bold'),
                                    bg=self.colors['card_bg'],
                                    fg=self.colors['accent'],
                                    relief='solid',
                                    borderwidth=2,
                                    padx=15,
                                    pady=15)
        right_frame.grid(row=0, column=1, sticky='nsew')

        self.vlsm_process_text = self.create_styled_text(right_frame, 45, 25)
        self.vlsm_process_text.grid(row=0, column=0, sticky='nsew')

        # 配置权重
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)
        result_frame.columnconfigure(0, weight=1)
        result_frame.columnconfigure(1, weight=1)
        result_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(0, weight=1)

    def create_advanced_tools_tab(self):
        """创建高级工具选项卡"""
        tab = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(tab, text="🛠️ 高级工具")

        # IP转换工具
        conversion_frame = tk.LabelFrame(tab,
                                         text="IP地址转换",
                                         font=('Microsoft YaHei', 11, 'bold'),
                                         bg=self.colors['card_bg'],
                                         fg=self.colors['primary'],
                                         relief='solid',
                                         borderwidth=2,
                                         padx=20,
                                         pady=15)
        conversion_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15), padx=5)

        self.create_styled_label(conversion_frame, "IP地址:", 10, True, self.colors['primary']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.convert_ip_entry = self.create_styled_entry(conversion_frame, 25, "192.168.1.1")
        self.convert_ip_entry.grid(row=0, column=1, padx=(0, 15))

        # 转换按钮 - 使用不同鲜艳颜色
        buttons = [
            ("十进制转二进制", self.convert_to_binary, "Rounded.TButton"),
            ("二进制转十进制", self.convert_from_binary, "Success.Rounded.TButton"),
            ("十进制转十六进制", self.convert_to_hex, "Warning.Rounded.TButton")
        ]

        for i, (text, command, style_name) in enumerate(buttons):
            btn = self.create_rounded_button(conversion_frame, text, command, style=style_name)
            btn.grid(row=0, column=i + 2, padx=(0, 5))

        # 转换结果
        self.conversion_result_var = tk.StringVar()
        result_label = tk.Label(conversion_frame,
                                textvariable=self.conversion_result_var,
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_primary'],
                                font=('Consolas', 10, 'bold'),
                                relief='solid',
                                borderwidth=1,
                                anchor='w',
                                padx=12,
                                pady=8)
        result_label.grid(row=1, column=0, columnspan=5, sticky='ew', pady=(15, 0))

        # 掩码转换工具
        mask_frame = tk.LabelFrame(tab,
                                   text="掩码转换",
                                   font=('Microsoft YaHei', 11, 'bold'),
                                   bg=self.colors['card_bg'],
                                   fg=self.colors['secondary'],
                                   relief='solid',
                                   borderwidth=2,
                                   padx=20,
                                   pady=15)
        mask_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15), padx=5)

        self.create_styled_label(mask_frame, "掩码位数:", 10, True, self.colors['secondary']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.mask_bits_entry = self.create_styled_entry(mask_frame, 8)
        self.mask_bits_entry.grid(row=0, column=1, padx=(0, 15))

        self.create_styled_label(mask_frame, "子网掩码:", 10, True, self.colors['secondary']
                                 ).grid(row=0, column=2, sticky='w', padx=(0, 10))

        self.mask_dotted_entry = self.create_styled_entry(mask_frame, 20)
        self.mask_dotted_entry.grid(row=0, column=3, padx=(0, 15))

        # 转换按钮
        self.create_rounded_button(mask_frame, "位数转掩码", self.bits_to_mask,
                                   style='Rounded.TButton').grid(row=0, column=4, padx=(0, 5))
        self.create_rounded_button(mask_frame, "掩码转位数", self.mask_to_bits,
                                   style='Success.Rounded.TButton').grid(row=0, column=5, padx=(0, 5))

        # 常用掩码快速按钮
        self.create_styled_label(mask_frame, "常用掩码:", 10, False, self.colors['text_secondary']
                                 ).grid(row=1, column=0, sticky='w', padx=(0, 10), pady=(15, 0))

        common_masks = ["/24", "/25", "/26", "/27", "/28", "/29", "/30"]
        for i, mask in enumerate(common_masks):
            btn = self.create_rounded_button(mask_frame, mask, width=5,
                                             command=lambda m=mask: self.load_mask(m),
                                             style='Secondary.Rounded.TButton')
            btn.grid(row=1, column=i + 1, padx=2, pady=(15, 0))

        # 网络验证工具
        validation_frame = tk.LabelFrame(tab,
                                         text="网络验证",
                                         font=('Microsoft YaHei', 11, 'bold'),
                                         bg=self.colors['card_bg'],
                                         fg=self.colors['warning'],
                                         relief='solid',
                                         borderwidth=2,
                                         padx=20,
                                         pady=15)
        validation_frame.grid(row=2, column=0, sticky='ew', pady=(0, 10), padx=5)

        self.create_styled_label(validation_frame, "IP地址:", 10, True, self.colors['warning']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.validate_ip_entry = self.create_styled_entry(validation_frame, 25, "192.168.1.10")
        self.validate_ip_entry.grid(row=0, column=1, padx=(0, 15))

        self.create_styled_label(validation_frame, "网络地址:", 10, True, self.colors['warning']
                                 ).grid(row=0, column=2, sticky='w', padx=(0, 10))

        self.validate_network_entry = self.create_styled_entry(validation_frame, 25, "192.168.1.0/24")
        self.validate_network_entry.grid(row=0, column=3, padx=(0, 15))

        self.create_rounded_button(validation_frame, "验证IP是否在网络内", self.validate_ip_in_network,
                                   style='Warning.Rounded.TButton').grid(row=1, column=0, columnspan=4, pady=(15, 0))

        self.validation_result_var = tk.StringVar()
        result_label = tk.Label(validation_frame,
                                textvariable=self.validation_result_var,
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_primary'],
                                font=('Consolas', 10, 'bold'),
                                relief='solid',
                                borderwidth=1,
                                anchor='w',
                                padx=12,
                                pady=8)
        result_label.grid(row=2, column=0, columnspan=4, sticky='ew', pady=(10, 0))

        # 配置权重
        tab.columnconfigure(0, weight=1)

    def create_network_tools_tab(self):
        """创建网络工具选项卡"""
        tab = tk.Frame(self.notebook, bg=self.colors['background'])
        self.notebook.add(tab, text="🌐 网络工具")

        # 网络汇总工具
        summarization_frame = tk.LabelFrame(tab,
                                            text="网络汇总计算",
                                            font=('Microsoft YaHei', 11, 'bold'),
                                            bg=self.colors['card_bg'],
                                            fg=self.colors['teal'],
                                            relief='solid',
                                            borderwidth=2,
                                            padx=20,
                                            pady=15)
        summarization_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15), padx=5)

        self.create_styled_label(summarization_frame, "输入网络地址(每行一个):", 10, True, self.colors['teal']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.summary_text = self.create_styled_text(summarization_frame, 60, 6)
        self.summary_text.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(10, 0))
        self.summary_text.insert(tk.END, "192.168.1.0/24\n192.168.2.0/24\n192.168.3.0/24\n192.168.4.0/24")

        self.create_rounded_button(summarization_frame, "计算汇总网络", self.calculate_summary,
                                   style='Teal.Rounded.TButton').grid(row=2, column=0, pady=(15, 0))

        self.summary_result_var = tk.StringVar()
        result_label = tk.Label(summarization_frame,
                                textvariable=self.summary_result_var,
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_primary'],
                                font=('Consolas', 10, 'bold'),
                                relief='solid',
                                borderwidth=1,
                                anchor='w',
                                padx=12,
                                pady=8)
        result_label.grid(row=3, column=0, columnspan=3, sticky='ew', pady=(10, 0))

        # 通配符掩码计算
        wildcard_frame = tk.LabelFrame(tab,
                                       text="通配符掩码计算",
                                       font=('Microsoft YaHei', 11, 'bold'),
                                       bg=self.colors['card_bg'],
                                       fg=self.colors['purple'],
                                       relief='solid',
                                       borderwidth=2,
                                       padx=20,
                                       pady=15)
        wildcard_frame.grid(row=1, column=0, sticky='ew', pady=(0, 15), padx=5)

        self.create_styled_label(wildcard_frame, "子网掩码:", 10, True, self.colors['purple']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.wildcard_mask_entry = self.create_styled_entry(wildcard_frame, 25, "255.255.255.0")
        self.wildcard_mask_entry.grid(row=0, column=1, padx=(0, 15))

        self.create_rounded_button(wildcard_frame, "计算通配符掩码", self.calculate_wildcard,
                                   style='Purple.Rounded.TButton').grid(row=0, column=2, padx=(0, 5))

        self.wildcard_result_var = tk.StringVar()
        result_label = tk.Label(wildcard_frame,
                                textvariable=self.wildcard_result_var,
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_primary'],
                                font=('Consolas', 10, 'bold'),
                                relief='solid',
                                borderwidth=1,
                                anchor='w',
                                padx=12,
                                pady=8)
        result_label.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(10, 0))

        # IP地址计算器
        ipcalc_frame = tk.LabelFrame(tab,
                                     text="IP地址加减计算",
                                     font=('Microsoft YaHei', 11, 'bold'),
                                     bg=self.colors['card_bg'],
                                     fg=self.colors['accent'],
                                     relief='solid',
                                     borderwidth=2,
                                     padx=20,
                                     pady=15)
        ipcalc_frame.grid(row=2, column=0, sticky='ew', pady=(0, 10), padx=5)

        self.create_styled_label(ipcalc_frame, "IP地址:", 10, True, self.colors['accent']
                                 ).grid(row=0, column=0, sticky='w', padx=(0, 10))

        self.ipcalc_ip_entry = self.create_styled_entry(ipcalc_frame, 25, "192.168.1.10")
        self.ipcalc_ip_entry.grid(row=0, column=1, padx=(0, 15))

        self.create_styled_label(ipcalc_frame, "加减数量:", 10, True, self.colors['accent']
                                 ).grid(row=0, column=2, sticky='w', padx=(0, 10))

        self.ipcalc_offset_entry = self.create_styled_entry(ipcalc_frame, 12, "5")
        self.ipcalc_offset_entry.grid(row=0, column=3, padx=(0, 15))

        self.create_rounded_button(ipcalc_frame, "增加", lambda: self.calculate_ip_offset(1),
                                   style='Success.Rounded.TButton').grid(row=0, column=4, padx=(0, 5))
        self.create_rounded_button(ipcalc_frame, "减少", lambda: self.calculate_ip_offset(-1),
                                   style='Danger.Rounded.TButton').grid(row=0, column=5, padx=(0, 5))

        self.ipcalc_result_var = tk.StringVar()
        result_label = tk.Label(ipcalc_frame,
                                textvariable=self.ipcalc_result_var,
                                bg=self.colors['card_bg'],
                                fg=self.colors['text_primary'],
                                font=('Consolas', 10, 'bold'),
                                relief='solid',
                                borderwidth=1,
                                anchor='w',
                                padx=12,
                                pady=8)
        result_label.grid(row=1, column=0, columnspan=6, sticky='ew', pady=(10, 0))

        # 配置权重
        tab.columnconfigure(0, weight=1)

    # 以下方法保持不变，只修改颜色相关的部分
    def load_example(self, example):
        """加载示例到输入框"""
        if '/' in example:
            self.ip_entry.delete(0, tk.END)
            self.ip_entry.insert(0, example)
        else:
            self.convert_ip_entry.delete(0, tk.END)
            self.convert_ip_entry.insert(0, example)

    def load_mask(self, mask):
        """加载常用掩码"""
        bits = mask.replace('/', '')
        self.mask_bits_entry.delete(0, tk.END)
        self.mask_bits_entry.insert(0, bits)
        self.bits_to_mask()

    def calculate_ip_info(self):
        """计算IP地址信息"""
        try:
            # 获取输入
            ip_input = self.ip_entry.get().strip()
            cidr_input = self.cidr_entry.get().strip()

            # 组合输入
            if cidr_input:
                if '/' in ip_input:
                    messagebox.showerror("输入错误", "请只在一个位置输入掩码信息")
                    return
                network_str = f"{ip_input}/{cidr_input}"
            else:
                network_str = ip_input

            # 解析网络
            network = ipaddress.ip_network(network_str, strict=False)

            # 更新结果
            self.network_var.set(str(network.network_address))
            self.broadcast_var.set(str(network.broadcast_address))
            self.netmask_var.set(str(network.netmask))
            self.wildcard_var.set(str(network.hostmask))

            # 可用地址范围
            hosts = list(network.hosts())
            if hosts:
                self.range_var.set(f"{hosts[0]} - {hosts[-1]}")
            else:
                self.range_var.set("无可用主机地址")

            # 可用主机数
            host_count = network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
            self.hosts_var.set(str(host_count))

            # IP类型
            if network.is_private:
                self.ip_type_var.set("私有地址")
            elif network.is_global:
                self.ip_type_var.set("公网地址")
            elif network.is_multicast:
                self.ip_type_var.set("组播地址")
            elif network.is_link_local:
                self.ip_type_var.set("链路本地地址")
            elif network.is_loopback:
                self.ip_type_var.set("回环地址")
            elif network.is_reserved:
                self.ip_type_var.set("保留地址")
            else:
                self.ip_type_var.set("其他")

            # 地址类别
            first_octet = int(str(network.network_address).split('.')[0])
            if first_octet <= 127:
                self.class_type_var.set("A类")
            elif first_octet <= 191:
                self.class_type_var.set("B类")
            elif first_octet <= 223:
                self.class_type_var.set("C类")
            elif first_octet <= 239:
                self.class_type_var.set("D类(组播)")
            else:
                self.class_type_var.set("E类(保留)")

            # 是否为私有地址
            self.is_private_var.set("是" if network.is_private else "否")

            # 二进制表示
            self.binary_text.delete(1.0, tk.END)

            network_bin = '.'.join([bin(int(x) + 256)[3:] for x in str(network.network_address).split('.')])
            mask_bin = '.'.join([bin(int(x) + 256)[3:] for x in str(network.netmask).split('.')])
            broadcast_bin = '.'.join([bin(int(x) + 256)[3:] for x in str(network.broadcast_address).split('.')])

            self.binary_text.insert(tk.END, "二进制表示:\n")
            self.binary_text.insert(tk.END, f"网络地址:  {network_bin}\n")
            self.binary_text.insert(tk.END, f"子网掩码:  {mask_bin}\n")
            self.binary_text.insert(tk.END, f"广播地址:  {broadcast_bin}\n")

            # 添加十六进制表示
            network_hex = '.'.join([hex(int(x))[2:].zfill(2) for x in str(network.network_address).split('.')])
            mask_hex = '.'.join([hex(int(x))[2:].zfill(2) for x in str(network.netmask).split('.')])
            self.binary_text.insert(tk.END, f"\n十六进制表示:\n")
            self.binary_text.insert(tk.END, f"网络地址:  {network_hex}\n")
            self.binary_text.insert(tk.END, f"子网掩码:  {mask_hex}\n")

            self.status_var.set(f"IP信息计算完成 - {network_str}")

        except Exception as e:
            messagebox.showerror("计算错误", f"输入格式错误: {str(e)}")
            self.status_var.set("计算错误")

    def calculate_subnets_by_count(self):
        """根据子网数量划分子网，显示计算过程"""
        try:
            # 清空树形视图和计算过程
            for item in self.subnet_tree.get_children():
                self.subnet_tree.delete(item)
            self.calculation_process_text.delete(1.0, tk.END)

            # 获取输入
            network_str = self.subnet_ip_entry.get().strip()
            subnet_count = int(self.subnet_count_entry.get().strip())

            # 验证输入
            if subnet_count <= 0:
                messagebox.showerror("输入错误", "子网数量必须大于0")
                return

            # 解析网络
            network = ipaddress.ip_network(network_str, strict=False)

            # 显示计算过程
            self.calculation_process_text.insert(tk.END, f"📋 子网划分计算过程\n")
            self.calculation_process_text.insert(tk.END, "=" * 50 + "\n\n")
            self.calculation_process_text.insert(tk.END, f"1. 原始网络: {network}\n")
            self.calculation_process_text.insert(tk.END, f"   网络地址: {network.network_address}\n")
            self.calculation_process_text.insert(tk.END, f"   子网掩码: {network.netmask}\n")
            self.calculation_process_text.insert(tk.END, f"   掩码位数: /{network.prefixlen}\n")
            self.calculation_process_text.insert(tk.END, f"   可用主机数: {network.num_addresses - 2}\n\n")

            self.calculation_process_text.insert(tk.END, f"2. 需求分析:\n")
            self.calculation_process_text.insert(tk.END, f"   需要划分的子网数: {subnet_count}\n")

            # 计算新的掩码位数
            needed_bits = math.ceil(math.log2(subnet_count))
            new_prefix_len = network.prefixlen + needed_bits

            self.calculation_process_text.insert(tk.END,
                                                 f"   所需额外位数: {needed_bits} (因为2^{needed_bits} = {2 ** needed_bits} >= {subnet_count})\n")
            self.calculation_process_text.insert(tk.END,
                                                 f"   新的掩码位数: /{new_prefix_len} (原{network.prefixlen} + {needed_bits})\n\n")

            # 验证新的前缀长度
            if new_prefix_len > 32:
                self.calculation_process_text.insert(tk.END, f"❌ 错误: 所需掩码位数{new_prefix_len}大于32，无法划分\n")
                messagebox.showerror("计算错误", f"无法划分{subnet_count}个子网，所需掩码位数{new_prefix_len}大于32")
                return

            # 计算新子网
            subnets = list(network.subnets(new_prefix=new_prefix_len))

            self.calculation_process_text.insert(tk.END, f"3. 子网划分结果:\n")
            self.calculation_process_text.insert(tk.END, f"   新子网掩码: {subnets[0].netmask}\n")
            self.calculation_process_text.insert(tk.END, f"   总共可创建子网数: {len(subnets)}\n")
            self.calculation_process_text.insert(tk.END, f"   实际使用子网数: {min(subnet_count, len(subnets))}\n\n")

            # 显示结果
            for i, subnet in enumerate(subnets[:subnet_count], 1):
                hosts = list(subnet.hosts())
                if hosts:
                    host_range = f"{hosts[0]} - {hosts[-1]}"
                else:
                    host_range = "无可用主机"

                # 计算地址利用率
                total_ips = subnet.num_addresses
                usable_ips = total_ips - 2 if total_ips > 2 else total_ips
                utilization = f"{(usable_ips / total_ips) * 100:.1f}%" if total_ips > 0 else "N/A"

                self.subnet_tree.insert("", "end", values=(
                    f"子网{i}",
                    str(subnet.network_address),
                    str(subnet.broadcast_address),
                    host_range,
                    str(subnet.netmask),
                    str(usable_ips),
                    utilization
                ))

                # 在计算过程中显示详细信息
                self.calculation_process_text.insert(tk.END, f"   子网{i}: {subnet}\n")
                self.calculation_process_text.insert(tk.END, f"     网络地址: {subnet.network_address}\n")
                self.calculation_process_text.insert(tk.END, f"     广播地址: {subnet.broadcast_address}\n")
                self.calculation_process_text.insert(tk.END, f"     可用地址: {host_range}\n")
                self.calculation_process_text.insert(tk.END, f"     可用主机数: {usable_ips}\n")
                self.calculation_process_text.insert(tk.END, f"     地址利用率: {utilization}\n\n")

            # 更新汇总信息
            self.new_cidr_var.set(str(new_prefix_len))
            self.new_mask_var.set(str(subnets[0].netmask))

            total_hosts = sum(subnet.num_addresses - 2 for subnet in subnets[:subnet_count] if subnet.num_addresses > 2)
            self.total_hosts_var.set(str(total_hosts))

            # 计算总体地址利用率
            original_usable = network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
            utilization_rate = f"{(total_hosts / original_usable) * 100:.1f}%" if original_usable > 0 else "N/A"
            self.utilization_var.set(utilization_rate)

            self.calculation_process_text.insert(tk.END, f"4. 汇总信息:\n")
            self.calculation_process_text.insert(tk.END, f"   新掩码位数: /{new_prefix_len}\n")
            self.calculation_process_text.insert(tk.END, f"   新子网掩码: {subnets[0].netmask}\n")
            self.calculation_process_text.insert(tk.END, f"   总可用主机数: {total_hosts}\n")
            self.calculation_process_text.insert(tk.END, f"   总体地址利用率: {utilization_rate}\n")

            self.status_var.set(f"成功划分{min(subnet_count, len(subnets))}个子网")

        except Exception as e:
            messagebox.showerror("计算错误", f"子网划分失败: {str(e)}")
            self.status_var.set("子网划分失败")

    def calculate_subnets_by_hosts(self):
        """根据每子网主机数划分子网，显示计算过程"""
        try:
            # 清空树形视图和计算过程
            for item in self.subnet_tree.get_children():
                self.subnet_tree.delete(item)
            self.calculation_process_text.delete(1.0, tk.END)

            # 获取输入
            network_str = self.subnet_ip_entry.get().strip()
            hosts_per_subnet = int(self.hosts_per_subnet_entry.get().strip())

            # 验证输入
            if hosts_per_subnet <= 0:
                messagebox.showerror("输入错误", "每子网主机数必须大于0")
                return

            # 解析网络
            network = ipaddress.ip_network(network_str, strict=False)

            # 显示计算过程
            self.calculation_process_text.insert(tk.END, f"📋 按主机数划分子网计算过程\n")
            self.calculation_process_text.insert(tk.END, "=" * 50 + "\n\n")
            self.calculation_process_text.insert(tk.END, f"1. 原始网络: {network}\n")
            self.calculation_process_text.insert(tk.END, f"   网络地址: {network.network_address}\n")
            self.calculation_process_text.insert(tk.END, f"   子网掩码: {network.netmask}\n")
            self.calculation_process_text.insert(tk.END, f"   掩码位数: /{network.prefixlen}\n")
            self.calculation_process_text.insert(tk.END, f"   可用主机数: {network.num_addresses - 2}\n\n")

            self.calculation_process_text.insert(tk.END, f"2. 需求分析:\n")
            self.calculation_process_text.insert(tk.END, f"   每个子网需要的主机数: {hosts_per_subnet}\n")

            # 计算所需主机位数
            needed_host_bits = math.ceil(math.log2(hosts_per_subnet + 2))

            self.calculation_process_text.insert(tk.END,
                                                 f"   所需主机位数: {needed_host_bits} (因为2^{needed_host_bits} >= {hosts_per_subnet + 2})\n")
            self.calculation_process_text.insert(tk.END, f"   每个子网实际可容纳主机数: {2 ** needed_host_bits - 2}\n")

            # 计算新的前缀长度
            new_prefix_len = 32 - needed_host_bits

            self.calculation_process_text.insert(tk.END,
                                                 f"   新的掩码位数: /{new_prefix_len} (32 - {needed_host_bits})\n\n")

            # 验证新的前缀长度
            if new_prefix_len <= network.prefixlen:
                self.calculation_process_text.insert(tk.END,
                                                     f"❌ 错误: 新掩码位数{new_prefix_len}不大于原掩码位数{network.prefixlen}\n")
                messagebox.showerror("计算错误", f"无法提供{hosts_per_subnet}个主机地址，所需主机位太多")
                return

            # 计算可划分的子网数
            subnet_bits = new_prefix_len - network.prefixlen
            max_subnets = 2 ** subnet_bits

            self.calculation_process_text.insert(tk.END, f"3. 子网划分能力:\n")
            self.calculation_process_text.insert(tk.END,
                                                 f"   子网位数: {subnet_bits} (新{new_prefix_len} - 原{network.prefixlen})\n")
            self.calculation_process_text.insert(tk.END, f"   最多可划分子网数: {max_subnets} (2^{subnet_bits})\n\n")

            # 计算子网
            subnets = list(network.subnets(new_prefix=new_prefix_len))

            self.calculation_process_text.insert(tk.END, f"4. 子网划分结果:\n")
            self.calculation_process_text.insert(tk.END, f"   新子网掩码: {subnets[0].netmask}\n")
            self.calculation_process_text.insert(tk.END, f"   每子网实际可用主机数: {2 ** needed_host_bits - 2}\n\n")

            # 显示结果
            for i, subnet in enumerate(subnets[:max_subnets], 1):
                hosts = list(subnet.hosts())
                if hosts:
                    host_range = f"{hosts[0]} - {hosts[-1]}"
                else:
                    host_range = "无可用主机"

                # 计算地址利用率
                total_ips = subnet.num_addresses
                usable_ips = total_ips - 2 if total_ips > 2 else total_ips
                utilization = f"{(usable_ips / total_ips) * 100:.1f}%" if total_ips > 0 else "N/A"

                self.subnet_tree.insert("", "end", values=(
                    f"子网{i}",
                    str(subnet.network_address),
                    str(subnet.broadcast_address),
                    host_range,
                    str(subnet.netmask),
                    str(usable_ips),
                    utilization
                ))

            # 更新汇总信息
            self.new_cidr_var.set(str(new_prefix_len))
            self.new_mask_var.set(str(subnets[0].netmask))

            total_hosts = sum(subnet.num_addresses - 2 for subnet in subnets[:max_subnets] if subnet.num_addresses > 2)
            self.total_hosts_var.set(str(total_hosts))

            # 计算总体地址利用率
            original_usable = network.num_addresses - 2 if network.num_addresses > 2 else network.num_addresses
            utilization_rate = f"{(total_hosts / original_usable) * 100:.1f}%" if original_usable > 0 else "N/A"
            self.utilization_var.set(utilization_rate)

            self.calculation_process_text.insert(tk.END, f"5. 汇总信息:\n")
            self.calculation_process_text.insert(tk.END, f"   新掩码位数: /{new_prefix_len}\n")
            self.calculation_process_text.insert(tk.END, f"   新子网掩码: {subnets[0].netmask}\n")
            self.calculation_process_text.insert(tk.END, f"   总可用主机数: {total_hosts}\n")
            self.calculation_process_text.insert(tk.END, f"   总体地址利用率: {utilization_rate}\n")
            self.calculation_process_text.insert(tk.END, f"   可划分子网数: {max_subnets}\n")

            self.status_var.set(f"可划分{max_subnets}个子网，每子网最多{2 ** needed_host_bits - 2}个主机地址")

        except Exception as e:
            messagebox.showerror("计算错误", f"子网划分失败: {str(e)}")
            self.status_var.set("子网划分失败")

    def calculate_vlsm(self):
        """执行VLSM子网划分，显示计算过程"""
        try:
            # 清空树形视图和计算过程
            for item in self.vlsm_tree.get_children():
                self.vlsm_tree.delete(item)
            self.vlsm_process_text.delete(1.0, tk.END)

            # 获取输入
            network_str = self.vlsm_ip_entry.get().strip()
            requirements_str = self.vlsm_requirements_entry.get().strip()

            # 解析需求
            requirements = [int(x.strip()) for x in requirements_str.split(',')]
            sorted_requirements = sorted(requirements, reverse=True)  # 从大到小排序

            # 解析网络
            network = ipaddress.ip_network(network_str, strict=False)

            # 显示计算过程
            self.vlsm_process_text.insert(tk.END, f"📋 VLSM子网划分计算过程\n")
            self.vlsm_process_text.insert(tk.END, "=" * 50 + "\n\n")
            self.vlsm_process_text.insert(tk.END, f"1. 原始网络: {network}\n")
            self.vlsm_process_text.insert(tk.END, f"   网络地址: {network.network_address}\n")
            self.vlsm_process_text.insert(tk.END, f"   子网掩码: {network.netmask}\n")
            self.vlsm_process_text.insert(tk.END, f"   掩码位数: /{network.prefixlen}\n")
            self.vlsm_process_text.insert(tk.END, f"   可用地址总数: {network.num_addresses}\n")
            self.vlsm_process_text.insert(tk.END, f"   可用主机数: {network.num_addresses - 2}\n\n")

            self.vlsm_process_text.insert(tk.END, f"2. 子网需求:\n")
            total_required = 0
            for i, req in enumerate(sorted_requirements, 1):
                self.vlsm_process_text.insert(tk.END, f"   子网{i}: {req}个主机\n")
                total_required += req

            self.vlsm_process_text.insert(tk.END, f"   总计需要主机数: {total_required}\n\n")

            # 执行VLSM划分
            current_network = network
            subnets = []

            self.vlsm_process_text.insert(tk.END, f"3. VLSM划分过程:\n")

            for i, hosts_needed in enumerate(sorted_requirements, 1):
                # 计算所需主机位数
                needed_host_bits = math.ceil(math.log2(hosts_needed + 2))
                new_prefix_len = 32 - needed_host_bits

                # 获取子网
                subnet_list = list(current_network.subnets(new_prefix=new_prefix_len))
                if not subnet_list:
                    self.vlsm_process_text.insert(tk.END, f"❌ 错误: 无法为需求{hosts_needed}划分子网，地址空间不足\n")
                    break

                subnet = subnet_list[0]
                subnets.append((subnet, hosts_needed))

                # 在计算过程中显示详细信息
                self.vlsm_process_text.insert(tk.END, f"   子网{i} (需求: {hosts_needed}主机):\n")
                self.vlsm_process_text.insert(tk.END,
                                              f"     所需主机位数: {needed_host_bits} (2^{needed_host_bits} >= {hosts_needed + 2})\n")
                self.vlsm_process_text.insert(tk.END, f"     新掩码位数: /{new_prefix_len}\n")
                self.vlsm_process_text.insert(tk.END, f"     子网掩码: {subnet.netmask}\n")
                self.vlsm_process_text.insert(tk.END, f"     网络地址: {subnet.network_address}\n")
                self.vlsm_process_text.insert(tk.END, f"     广播地址: {subnet.broadcast_address}\n")
                self.vlsm_process_text.insert(tk.END, f"     可用主机数: {subnet.num_addresses - 2}\n")
                self.vlsm_process_text.insert(tk.END,
                                              f"     地址利用率: {hosts_needed / (subnet.num_addresses - 2) * 100:.1f}%\n\n")

                # 更新当前网络为剩余部分
                if len(subnet_list) > 1:
                    current_network = ipaddress.ip_network(
                        f"{subnet_list[1].network_address}/{current_network.prefixlen}",
                        strict=False
                    )
                else:
                    self.vlsm_process_text.insert(tk.END, f"⚠️ 警告: 地址空间已用完\n")
                    break

            # 显示结果
            self.vlsm_process_text.insert(tk.END, f"4. VLSM划分结果:\n")
            for i, (subnet, hosts_needed) in enumerate(subnets, 1):
                hosts = list(subnet.hosts())
                if hosts:
                    host_range = f"{hosts[0]} - {hosts[-1]}"
                else:
                    host_range = "无可用主机"

                # 计算地址利用率
                total_ips = subnet.num_addresses
                usable_ips = total_ips - 2 if total_ips > 2 else total_ips
                actual_hosts = usable_ips
                utilization = f"{(hosts_needed / actual_hosts) * 100:.1f}%" if actual_hosts > 0 else "N/A"

                self.vlsm_tree.insert("", "end", values=(
                    hosts_needed,
                    f"子网{i}",
                    str(subnet.network_address),
                    str(subnet.broadcast_address),
                    host_range,
                    str(subnet.netmask),
                    str(usable_ips),
                    utilization
                ))

            # 计算总体地址利用率
            total_allocated = sum(subnet.num_addresses for subnet, _ in subnets)
            total_utilization = f"{(total_allocated / network.num_addresses) * 100:.1f}%" if network.num_addresses > 0 else "N/A"

            self.vlsm_process_text.insert(tk.END, f"   成功划分子网数: {len(subnets)}\n")
            self.vlsm_process_text.insert(tk.END, f"   已分配地址数: {total_allocated}\n")
            self.vlsm_process_text.insert(tk.END, f"   总体地址利用率: {total_utilization}\n")

            if len(subnets) < len(sorted_requirements):
                self.vlsm_process_text.insert(tk.END,
                                              f"⚠️ 注意: 只成功划分了{len(subnets)}个子网，需求{len(sorted_requirements)}个\n")

            self.status_var.set(f"VLSM划分完成，共{len(subnets)}个子网")

        except Exception as e:
            messagebox.showerror("计算错误", f"VLSM划分失败: {str(e)}")
            self.status_var.set("VLSM划分失败")

    def convert_to_binary(self):
        """将IP地址转换为二进制"""
        try:
            ip_str = self.convert_ip_entry.get().strip()
            ip = ipaddress.ip_address(ip_str)

            # 转换为二进制
            binary_parts = [bin(int(x) + 256)[3:] for x in str(ip).split('.')]
            binary_str = '.'.join(binary_parts)

            self.conversion_result_var.set(f"二进制: {binary_str}")
            self.status_var.set("IP地址转换完成")

        except Exception as e:
            messagebox.showerror("转换错误", f"IP地址转换失败: {str(e)}")
            self.status_var.set("转换失败")

    def convert_from_binary(self):
        """将二进制IP地址转换为十进制"""
        try:
            binary_str = self.convert_ip_entry.get().strip()

            # 验证二进制格式
            if not re.match(r'^[01]{8}\.[01]{8}\.[01]{8}\.[01]{8}$', binary_str):
                messagebox.showerror("格式错误",
                                     "请输入正确的二进制IP地址格式(如: 11000000.10101000.00000001.00000001)")
                return

            # 转换为十进制
            decimal_parts = [str(int(part, 2)) for part in binary_str.split('.')]
            decimal_str = '.'.join(decimal_parts)

            self.conversion_result_var.set(f"十进制: {decimal_str}")
            self.status_var.set("二进制转换完成")

        except Exception as e:
            messagebox.showerror("转换错误", f"二进制转换失败: {str(e)}")
            self.status_var.set("转换失败")

    def convert_to_hex(self):
        """将IP地址转换为十六进制"""
        try:
            ip_str = self.convert_ip_entry.get().strip()
            ip = ipaddress.ip_address(ip_str)

            # 转换为十六进制
            hex_parts = [hex(int(x))[2:].zfill(2) for x in str(ip).split('.')]
            hex_str = '.'.join(hex_parts)

            # 转换为连续的十六进制
            hex_continuous = '0x' + ''.join(hex_parts)

            self.conversion_result_var.set(f"十六进制: {hex_str} (连续: {hex_continuous})")
            self.status_var.set("IP地址十六进制转换完成")

        except Exception as e:
            messagebox.showerror("转换错误", f"IP地址转换失败: {str(e)}")
            self.status_var.set("转换失败")

    def bits_to_mask(self):
        """将掩码位数转换为点分十进制"""
        try:
            bits = int(self.mask_bits_entry.get().strip())

            if bits < 0 or bits > 32:
                messagebox.showerror("输入错误", "掩码位数必须在0-32之间")
                return

            # 计算掩码
            mask = (0xffffffff << (32 - bits)) & 0xffffffff
            mask_str = f"{(mask >> 24) & 0xff}.{(mask >> 16) & 0xff}.{(mask >> 8) & 0xff}.{mask & 0xff}"

            self.mask_dotted_entry.delete(0, tk.END)
            self.mask_dotted_entry.insert(0, mask_str)

            self.status_var.set(f"掩码位数{bits}转换为{mask_str}")

        except Exception as e:
            messagebox.showerror("转换错误", f"掩码转换失败: {str(e)}")
            self.status_var.set("转换失败")

    def mask_to_bits(self):
        """将点分十进制掩码转换为位数"""
        try:
            mask_str = self.mask_dotted_entry.get().strip()

            # 验证掩码格式
            parts = mask_str.split('.')
            if len(parts) != 4:
                messagebox.showerror("格式错误", "请输入正确的掩码格式(如: 255.255.255.0)")
                return

            # 计算位数
            mask = 0
            for part in parts:
                mask = (mask << 8) + int(part)

            # 计算连续1的个数
            bits = 0
            while mask & 0x80000000:
                bits += 1
                mask <<= 1

            self.mask_bits_entry.delete(0, tk.END)
            self.mask_bits_entry.insert(0, str(bits))

            self.status_var.set(f"掩码{mask_str}转换为{bits}位")

        except Exception as e:
            messagebox.showerror("转换错误", f"掩码转换失败: {str(e)}")
            self.status_var.set("转换失败")

    def validate_ip_in_network(self):
        """验证IP地址是否在指定网络内"""
        try:
            ip_str = self.validate_ip_entry.get().strip()
            network_str = self.validate_network_entry.get().strip()

            ip = ipaddress.ip_address(ip_str)
            network = ipaddress.ip_network(network_str, strict=False)

            if ip in network:
                self.validation_result_var.set(f"✅ IP地址 {ip_str} 在网络 {network_str} 内")
            else:
                self.validation_result_var.set(f"❌ IP地址 {ip_str} 不在网络 {network_str} 内")

            self.status_var.set("IP地址验证完成")

        except Exception as e:
            messagebox.showerror("验证错误", f"IP地址验证失败: {str(e)}")
            self.status_var.set("验证失败")

    def calculate_summary(self):
        """计算网络汇总"""
        try:
            # 获取输入的网络地址
            networks_text = self.summary_text.get(1.0, tk.END).strip()
            if not networks_text:
                messagebox.showerror("输入错误", "请输入至少一个网络地址")
                return

            # 解析网络地址
            network_strings = [line.strip() for line in networks_text.split('\n') if line.strip()]
            networks = [ipaddress.ip_network(net_str, strict=False) for net_str in network_strings]

            # 计算汇总网络
            if len(networks) == 1:
                summary = networks[0]
            else:
                # 找到最小和最大地址
                min_address = min(networks, key=lambda x: int(x.network_address)).network_address
                max_address = max(networks, key=lambda x: int(x.broadcast_address)).broadcast_address

                # 计算包含这些地址的最小网络
                address_range = int(max_address) - int(min_address) + 1
                prefix_len = 32 - math.ceil(math.log2(address_range))

                # 确保前缀长度不大于最小网络的前缀长度
                min_prefix = min(net.prefixlen for net in networks)
                prefix_len = min(prefix_len, min_prefix)

                summary = ipaddress.ip_network(f"{min_address}/{prefix_len}", strict=False)

            self.summary_result_var.set(f"汇总网络: {summary}")
            self.status_var.set("网络汇总计算完成")

        except Exception as e:
            messagebox.showerror("计算错误", f"网络汇总计算失败: {str(e)}")
            self.status_var.set("汇总计算失败")

    def calculate_wildcard(self):
        """计算通配符掩码"""
        try:
            mask_str = self.wildcard_mask_entry.get().strip()

            # 验证掩码格式
            parts = mask_str.split('.')
            if len(parts) != 4:
                messagebox.showerror("格式错误", "请输入正确的掩码格式(如: 255.255.255.0)")
                return

            # 计算通配符掩码
            wildcard_parts = [str(255 - int(part)) for part in parts]
            wildcard_str = '.'.join(wildcard_parts)

            self.wildcard_result_var.set(f"通配符掩码: {wildcard_str}")
            self.status_var.set("通配符掩码计算完成")

        except Exception as e:
            messagebox.showerror("计算错误", f"通配符掩码计算失败: {str(e)}")
            self.status_var.set("通配符掩码计算失败")

    def calculate_ip_offset(self, direction):
        """计算IP地址的偏移"""
        try:
            ip_str = self.ipcalc_ip_entry.get().strip()
            offset = int(self.ipcalc_offset_entry.get().strip())

            ip = ipaddress.ip_address(ip_str)

            # 计算新IP
            if direction == 1:
                new_ip = ip + offset
                operation = "增加"
            else:
                new_ip = ip - offset
                operation = "减少"

            self.ipcalc_result_var.set(f"{operation}{offset}后: {new_ip}")
            self.status_var.set("IP地址偏移计算完成")

        except Exception as e:
            messagebox.showerror("计算错误", f"IP地址偏移计算失败: {str(e)}")
            self.status_var.set("偏移计算失败")


def main():
    root = tk.Tk()
    app = IPCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
