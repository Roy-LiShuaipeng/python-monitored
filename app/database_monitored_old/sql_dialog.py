import tkinter as tk


class SqlDialog(tk.Toplevel):
    def __init__(self, sql):
        super().__init__()
        self.title('查看SQL语句')
        self.geometry('585x550')

        # 接收显示信息
        self.sql = sql

        # 弹窗界面
        self._init_window()

    def _init_window(self):
        self.__sql_text = tk.Text(self, height=40)

        # 字符串处理
        self.sql = self.sql.replace('SELECT ', 'SELECT\n\n      ')
        self.sql = self.sql.replace('WHERE ', '\n\nWHERE\n\n      ')
        self.sql = self.sql.replace('FROM ', '\n\nFROM\n\n      ')
        self.sql = self.sql.replace('ORDER BY ', '\n\nORDER BY\n\n      ')
        self.sql = self.sql.replace('GROUP BY ', '\n\nGROUP BY\n\n      ')

        self.sql = self.sql.replace(' INNER JOIN ', ' INNER JOIN\n\n      ')
        self.sql = self.sql.replace(' LEFT JOIN ', ' LEFT JOIN\n\n      ')
        self.sql = self.sql.replace(' RIGHT JOIN ', ' RIGHT JOIN\n\n      ')
        self.sql = self.sql.replace('AND ', 'AND\n      ')
        self.sql = self.sql.replace('OR ', 'OR\n      ')
        self.sql = self.sql.replace(', ', ',\n      ')

        self.__sql_text.insert(tk.END, self.sql)
        # self.__sql_text.config(state=tk.DISABLED)
        self.__sql_text.grid(row=0, column=0, sticky=tk.W + tk.E + tk.N + tk.S, padx=10, pady=10)


