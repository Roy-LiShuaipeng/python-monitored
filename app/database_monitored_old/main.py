import math
import threading

from tkinter import ttk
import tkinter as tk

from app.database_monitored_old import ConfigDialog, DBHelper
from app.database_monitored_old.sql_dialog import SqlDialog


class Main(tk.Tk):

    def __init__(self):
        super().__init__()

        # 设置窗体显示及规格
        self.title('数据库连接监听')
        self.wm_maxsize(width=1000, height=730)
        self.wm_minsize(width=1000, height=730)
        self.geometry('1000x730')
        self.resizable(False, False)

        # 布局
        self._layout()
        # 绘制界面
        self._creat_top()
        self._create_tree_view()
        self._draw_widget()

        # 加载数据库访问对象
        self.db_helper = DBHelper()

        # 显示窗体
        self.mainloop()

    def _layout(self):
        # 头部
        self.top_frame = tk.Frame(self)
        self.top_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.top_left_frame = tk.Frame(self.top_frame)
        self.top_left_frame.grid(row=0, column=0, sticky=tk.W)
        self.top_right_frame = tk.Frame(self.top_frame)
        self.top_right_frame.grid(row=0, column=1, sticky=tk.W)

        # 业务区域
        self.main_frame = tk.Frame(self)
        self.main_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W)
        self.tree_frame = tk.Frame(self.main_frame)
        self.tree_frame.grid(row=0, column=0, columnspan=2, sticky=tk.W)
        self.page_frame = tk.Frame(self.main_frame)
        self.page_frame.grid(row=1, column=1, sticky=tk.E)

        self.page_before_frame = tk.Frame(self.page_frame)
        self.page_before_frame.grid(row=0, column=1, sticky=tk.E)
        self.page_index_frame = tk.Frame(self.page_frame)
        self.page_index_frame.grid(row=0, column=2, sticky=tk.E)
        self.page_next_frame = tk.Frame(self.page_frame)
        self.page_next_frame.grid(row=0, column=3, sticky=tk.E)

        # 底部
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky=tk.W)

    def _draw_widget(self):
        self.config_btn.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)
        self.monitor_btn.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)
        self.lbl_time_step.grid(row=0, column=2, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)
        self.entry_time_step.grid(row=0, column=3, sticky=tk.W + tk.E + tk.N + tk.S, padx=1, pady=10)

        self.lbl_frame.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)
        self.refresh_btn.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)
        self.show_sql_btn.grid(row=0, column=2, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)

        self.tree_view.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10)

        self.btn_page_before.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)
        self.btn_page_next.grid(row=0, column=0, sticky=tk.W, padx=10, pady=10)

    def _creat_top(self):
        # 配置监听数据库按钮
        self.config_btn_text = tk.StringVar()
        self.config_btn_text.set("配置监听数据库")
        self.config_btn = tk.Button(
            self.top_left_frame, textvariable=self.config_btn_text, command=self._on_config_btn_click
        )

        # 开始监听按钮
        self.monitor_btn_text = tk.StringVar()
        self.monitor_btn_text.set("开始监听")
        self.monitor_btn = tk.Button(
            self.top_left_frame, textvariable=self.monitor_btn_text, command=self._on_monitor_btn_click
        )
        self.monitor_btn.configure(state=tk.DISABLED)

        # 扫描配置label和entry
        self.entry_time_step_text = tk.StringVar()
        self.entry_time_step_text.set(60)
        self.lbl_time_step = tk.Label(self.top_left_frame, text='扫描间隔（秒）：', width=16)
        self.entry_time_step = tk.Entry(self.top_left_frame, textvariable=self.entry_time_step_text, width=8)

        # 分割右边内容label
        self.lbl_frame = tk.Label(self.top_right_frame, width=53)

        # 手动刷新按钮
        self.refresh_btn_text = tk.StringVar()
        self.refresh_btn_text.set("手动刷新")
        self.refresh_btn = tk.Button(
            self.top_right_frame, textvariable=self.refresh_btn_text, command=self._on_refresh_btn_click
        )
        self.refresh_btn.configure(state=tk.DISABLED)

        # 查看完整SQL语句按钮
        self.sql_btn_text = tk.StringVar()
        self.sql_btn_text.set("查看完整SQL语句")
        self.show_sql_btn = tk.Button(
            self.top_right_frame, textvariable=self.sql_btn_text, command=self._on_show_sql_btn_click
        )
        self.show_sql_btn.configure(state=tk.DISABLED)

    def _create_tree_view(self):
        # 定义分页显示数据条数
        self.page_data_count = 31

        # 定义列名，并创建控件
        columns = ("backend_start", "state_change", "datid", "datname", "pid", "state", "client_addr", "query")

        self.tree_view = ttk.Treeview(
            self.tree_frame, show="headings", columns=columns, height=self.page_data_count-1
        )

        # 设置列头
        self.tree_view.column("backend_start", width=150, anchor='center')
        self.tree_view.column("state_change", width=150, anchor='center')
        self.tree_view.column("datid", width=80, anchor='center')
        self.tree_view.column("datname", width=80, anchor='center')
        self.tree_view.column("pid", width=80, anchor='center')
        self.tree_view.column("state", width=140, anchor='center')
        self.tree_view.column("client_addr", width=120, anchor='center')
        self.tree_view.column("query", width=177)

        # 绑定列显示数据
        self.tree_view.heading("backend_start", text="backend_start")
        self.tree_view.heading("state_change", text="state_change")
        self.tree_view.heading("datid", text="datid")
        self.tree_view.heading("datname", text="datname")
        self.tree_view.heading("pid", text="pid")
        self.tree_view.heading("state", text="state")
        self.tree_view.heading("client_addr", text="client_addr")
        self.tree_view.heading("query", text="query")

        # 绑定控件点击事件
        self.tree_view.bind('<<TreeviewSelect>>', self._tree_view_click)

        # 创建分页按钮及展示
        self.btn_page_index_list = []
        self.btn_page_before = tk.Button(self.page_before_frame, text="上一页", command=self._on_page_before_btn_click)
        self.btn_page_next = tk.Button(self.page_next_frame, text="下一页", command=self._on_page_next_btn_click)
        self.btn_page_before.configure(state=tk.DISABLED)
        self.btn_page_next.configure(state=tk.DISABLED)

    def _on_config_btn_click(self):
        sql_dialog = ConfigDialog()
        self.wait_window(sql_dialog)
        self.connection_config = sql_dialog.connection_info

        success_count = 0
        for config_item in self.connection_config:
            if len(config_item.strip()) > 0:
                success_count += 1

        if success_count == 5:
            self.monitor_btn.configure(state=tk.NORMAL)
            self.refresh_btn.configure(state=tk.NORMAL)
            self.db_helper.create_connection(self.connection_config)
        else:
            self.monitor_btn.configure(state=tk.DISABLED)
            self.refresh_btn.configure(state=tk.DISABLED)

    def _on_monitor_btn_click(self):
        if self.monitor_btn_text.get() == "开始监听":
            self.monitor_btn_text.set("停止监听")
            # self.timer = threading.Timer(1, self.refresh_data)
            # self.timer.start()
            self.run_after = True
            self.after(1000, self.refresh_data)
        else:
            self.monitor_btn_text.set("开始监听")
            # self.timer.cancel()
            self.run_after = False

    def _on_refresh_btn_click(self):
        # 1、清除数据
        self._clear_data()

        # 3、获取数据
        self._get_data()

        # 4、绘制数据
        self._draw_data(1)

    def _on_show_sql_btn_click(self):
        # 创建显示SQL窗口，等待关闭后继续
        sql_dialog = SqlDialog(self.tree_select_data)
        self.wait_window(sql_dialog)
        return

    def _tree_view_click(self, event):
        # 获取选择对象
        for item in self.tree_view.selection():
            self.tree_select_data = self.tree_view.item(item, "values")[7]
            self.show_sql_btn.configure(state=tk.NORMAL)

    def _on_page_before_btn_click(self):
        # 计算分页
        self.select_index = self.select_index - 1
        if self.select_index < 1:
            self.select_index = 1
            return

        # 清除数据
        self._clear_data()

        # 重新加载数据
        self._draw_data(self.select_index)

    def _on_page_next_btn_click(self):
        # 计算分页
        self.select_index = self.select_index + 1
        if self.select_index > self.page_count:
            self.select_index = self.page_count
            return

        # 清除数据
        self._clear_data()

        # 重新加载数据
        self._draw_data(self.select_index)

    def _on_page_index_btn_click(self, event):
        # 清除数据
        self._clear_data()

        # 获取按钮对象名称
        self.select_index = int(event.widget.config('text')[-1])

        # 重新加载数据
        self._draw_data(self.select_index)

    def refresh_data(self):
        # 1、清除数据
        self._clear_data()

        # 2、绘制表格, 这里提取到初始化中做节省性能
        # self._draw_tree_view()

        # 3、获取数据
        self._get_data()

        # 4、绘制数据
        self._draw_data(1)

        # 5、重新自调用继续循环    -还是用自带的after递归好用，线程操作会有明显卡顿
        # self.timer = threading.Timer(10, self.refresh_data)
        # self.timer.start()
        if self.run_after is True:
            if len(self.entry_time_step_text.get().strip()) > 0:
                after_step = int(self.entry_time_step_text.get().strip())
                if after_step > 60:
                    after_step = 60
                    self.entry_time_step_text.set("60")

                self.after(after_step * 1000, self.refresh_data)

    def _clear_data(self):
        rows = self.tree_view.get_children()
        for row in rows:
            self.tree_view.delete(row)

    def _get_data(self):
        # 获取数据集
        self.bind_data = self.db_helper.get_data()

    def _draw_data(self, select_index):
        # 获取分页，初始化传1
        self.select_index = select_index

        # 配置显示分页控件
        self._page_init(select_index)

        # 页码计算
        start_index = 0 + (self.select_index - 1) * 30
        end_index = 0 + (self.select_index - 1) * 30 + 30
        if end_index > len(self.bind_data) - 1:
            end_index = len(self.bind_data)

        # 显示数据
        while start_index < end_index:
            values = (
                str(self.bind_data[start_index][0])[1:19],
                str(self.bind_data[start_index][1])[1:19],
                str(self.bind_data[start_index][2]),
                str(self.bind_data[start_index][3]),
                str(self.bind_data[start_index][4]),
                str(self.bind_data[start_index][5]),
                str(self.bind_data[start_index][6]),
                str(self.bind_data[start_index][7])
            )
            self.tree_view.insert("", "end", values=values)

            start_index = start_index + 1

        self.title('数据库连接监听' + '      共' + str(len(self.bind_data)) + '条数据')
        if len(self.bind_data) > 0:
            self.btn_page_before.configure(state=tk.NORMAL)
            self.btn_page_next.configure(state=tk.NORMAL)
            self.show_sql_btn.configure(state=tk.DISABLED)

    def _page_init(self, select_index):
        # 清空分页
        for page_btn in self.btn_page_index_list:
            page_btn.destroy()
        self.btn_page_index_list = []

        # 获取分页
        self.page_count = math.ceil(len(self.bind_data) / 30)

        # 初始化页码控件组
        index = 0
        while index < self.page_count:
            # 不用属性绑定可以多个event对象，点击事件中获取按钮对象，不然动态生成对象不知道是哪个
            page_btn = tk.Button(self.page_index_frame, text=str(index+1))
            page_btn.bind('<Button-1>', self._on_page_index_btn_click)
            page_btn.grid(row=0, column=index, sticky=tk.W, padx=2, pady=10)
            self.btn_page_index_list.append(page_btn)
            index = index + 1

        # 设置当前页按钮颜色
        self.btn_page_index_list[select_index - 1].configure(bg="blue")







