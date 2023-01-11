import tkinter
import requests
from tkinter import ttk, font, messagebox
from bs4 import BeautifulSoup
from markdown import markdown


class App(tkinter.Tk):
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Minimal App")
        self.resizable(width=False, height=False)
        self.maxsize(
            width=self.winfo_screenwidth() - 10,
            height=self.winfo_screenheight() - 10
        )
        self.configure(padx=10, pady=15)

        # Insert a title
        self.title_label = ttk.Label(
            self, text='TabNews Contents', font=font.Font(size=18)
        )
        self.title_label.grid(row=0, columnspan=2, pady=(0, 5))

        # insert a list_box
        self.raw_contents_list = self.get_contents()
        self.contents_var = tkinter.StringVar(value=[])
        self.list_box = tkinter.Listbox(
            self, listvariable=self.contents_var, width=60
        )
        self.list_box.bind('<Double-1>', lambda r: self.open_content())
        self.list_box.grid(row=1, columnspan=2)

        # insert a Button
        self.refresh_btn = ttk.Button(
            self, text='Refresh', padding=(10, 5),
            command=self.refresh_label
        )
        self.refresh_btn.grid(row=2, column=0, pady=(10, 0))

        # insert a Button
        self.finish_btn = ttk.Button(
            self, text='Finish', padding=(10, 5),
            command=lambda: self.quit()
        )
        self.finish_btn.grid(row=2, column=1, pady=(10, 0))

    def get_contents(self):
        url = 'https://www.tabnews.com.br/api/v1/contents?strategy=new'
        return requests.get(url).json()

    def refresh_label(self):
        self.raw_contents_list = self.get_contents()
        temp_list = []
        for index, content in enumerate(self.raw_contents_list):
            if index < 10:
                index = f'0{index}'
            temp_list.append(f"[ {index} ] - {content['title']}")
        self.contents_var.set(temp_list)

    def open_content(self):
        selected: str = self.list_box.selection_get()
        selected_index = int(selected.split(' -')[0][2:4])
        selected_content = self.raw_contents_list[selected_index]
        selected_owner_username = selected_content['owner_username']
        selected_slug = selected_content['slug']
        url = f'https://www.tabnews.com.br/api/v1/contents/{selected_owner_username}/{selected_slug}'
        result = requests.get(url).json()
        selected_body = self.parse_markdown(result['body'])
        messagebox.showinfo(result['title'], selected_body)

    def parse_markdown(self, text: str) -> str:
        html = markdown(text)
        soup = BeautifulSoup(html, features='html.parser')
        return soup.get_text()


if __name__ == "__main__":
    app = App()
    app.mainloop()
