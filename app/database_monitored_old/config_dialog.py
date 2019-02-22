import tkinter as tk


class ConfigDialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('配置目标源')
        self.geometry('500x260')

        # 初始化默认信息
        self.host = "172.22.24.142"
        self.port = "5433"
        self.database = "ag_simple"
        self.user = "postgres"
        self.password = "postgres"

        # 弹窗界面
        self._init_window()

    def _init_window(self):
        self.entry_host_text = tk.StringVar()
        self.entry_host_text.set(self.host)
        self.entry_port_text = tk.StringVar()
        self.entry_port_text.set(self.port)
        self.entry_database_text = tk.StringVar()
        self.entry_database_text.set(self.database)
        self.entry_user_text = tk.StringVar()
        self.entry_user_text.set(self.user)
        self.entry_password_text = tk.StringVar()
        self.entry_password_text.set(self.password)

        self.lbl_host = tk.Label(self, text='数据库IP地址：', width=20)
        self.entry_host = tk.Entry(self, textvariable=self.entry_host_text, width=44)
        self.lbl_port = tk.Label(self, text='数据库端口：', width=20)
        self.entry_port = tk.Entry(self, textvariable=self.entry_port_text, width=44)
        self.lbl_database = tk.Label(self, text='数据库名称：', width=20)
        self.entry_database = tk.Entry(self, textvariable=self.entry_database_text, width=44)
        self.lbl_user = tk.Label(self, text='用户名：', width=20)
        self.entry_user = tk.Entry(self, textvariable=self.entry_user_text, width=44)
        self.lbl_password = tk.Label(self, text='密码：', width=20)
        self.entry_password = tk.Entry(self, textvariable=self.entry_password_text, width=44)
        self.frame_operation = tk.Frame(self)
        self.btn_ok = tk.Button(self.frame_operation, text="保存", command=self._on_ok_btn_click, width=20)
        self.btn_cancel = tk.Button(self.frame_operation, text="取消", command=self._on_cancel_btn_click, width=20)

        self.lbl_host.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.entry_host.grid(row=0, column=1, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.lbl_port.grid(row=1, column=0, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.entry_port.grid(row=1, column=1, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.lbl_database.grid(row=2, column=0, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.entry_database.grid(row=2, column=1, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.lbl_user.grid(row=3, column=0, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.entry_user.grid(row=3, column=1, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.lbl_password.grid(row=4, column=0, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.entry_password.grid(row=4, column=1, sticky=tk.W + tk.E + tk.N + tk.S, pady=10)
        self.frame_operation.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=10)
        self.btn_ok.grid(row=0, column=0, sticky=tk.E, padx=32)
        self.btn_cancel.grid(row=0, column=1, sticky=tk.E, padx=32)

    def _on_ok_btn_click(self):
        self.connection_info = [
            self.entry_host_text.get(),
            self.entry_port_text.get(),
            self.entry_database_text.get(),
            self.entry_user_text.get(),
            self.entry_password_text.get()
        ]
        self.destroy()

    def _on_cancel_btn_click(self):
        self.destroy()
