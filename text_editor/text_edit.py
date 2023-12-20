import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Text Editor")
        self.text_widget = tk.Text(root, wrap="word", undo=True)
        self.text_widget.pack(expand=True, fill="both")
        self.create_menu()
        self.text_widget.bind("<KeyRelease>", self.update_font_size)

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        file_menu.add_command(label="Save As", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_widget.edit_undo)
        edit_menu.add_command(label="Redo", command=self.text_widget.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text)
        edit_menu.add_command(label="Copy", command=self.copy_text)
        edit_menu.add_command(label="Paste", command=self.paste_text)

        format_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Format", menu=format_menu)
        self.configure_format_menu(format_menu)

        # Picture menu
        picture_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Picture", menu=picture_menu)
        picture_menu.add_command(label="Insert Image", command=self.insert_image)
        picture_menu.add_command(label="Delete Image", command=self.delete_image)

    def configure_format_menu(self, format_menu):
        format_menu.unbind("<Enter>")
        format_menu.unbind("<Leave>")
        format_menu.delete(0, tk.END)

        format_menu.add_command(label="Change Font Size", command=self.change_font_size)
        font_style_menu = tk.Menu(format_menu, tearoff=0)
        format_menu.add_cascade(label="Font Style", menu=font_style_menu)

        font_styles = ["TkDefaultFont", "Helvetica", "Times", "Courier", "Arial", "Verdana", "Calibri"]
        for style in font_styles:
            font_style_menu.add_command(label=style, command=lambda s=style: self.set_font_style(s))

        format_menu.add_command(label="Change Alignment", command=self.change_alignment)

        # Submenu for additional formatting options
        additional_format_menu = tk.Menu(format_menu, tearoff=0)
        format_menu.add_cascade(label="Formatting Options", menu=additional_format_menu)

        additional_format_menu.add_command(label="Change Line Spacing", command=self.change_line_spacing)
        additional_format_menu.add_command(label="Insert Header", command=self.insert_header)

    def new_file(self):
        self.text_widget.delete("1.0", tk.END)

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.delete("1.0", tk.END)
                self.text_widget.insert(tk.END, content)

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get("1.0", tk.END)
                file.write(content)

    def save_file_as(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                content = self.text_widget.get("1.0", tk.END)
                file.write(content)

    def cut_text(self):
        self.text_widget.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_widget.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_widget.event_generate("<<Paste>>")

    def change_font_size(self):
        size = simpledialog.askinteger("Font Size", "Enter Font Size:", initialvalue=12)
        if size:
            self.set_font_size(size)

    def set_font_size(self, size):
        self.text_widget.tag_configure("font", font=("TkDefaultFont", size))
        try:
            current_tags = self.text_widget.tag_names("sel.first")
            if "font" not in current_tags:
                self.text_widget.tag_add("font", self.text_widget.index(tk.SEL_FIRST), self.text_widget.index(tk.SEL_LAST))
                self.text_widget.tag_configure("font", font=("TkDefaultFont", size))
        except tk.TclError:
            pass

    def set_font_style(self, style):
        self.text_widget.tag_configure("font", font=(style, 12))
        try:
            current_tags = self.text_widget.tag_names("sel.first")
            if "font" not in current_tags:
                self.text_widget.tag_add("font", self.text_widget.index(tk.SEL_FIRST), self.text_widget.index(tk.SEL_LAST))
                self.text_widget.tag_configure("font", font=(style, 12))
        except tk.TclError:
            pass

    def update_font_size(self, event):
        current_font_size = self.text_widget.tag_cget("font", "size")
        if current_font_size:
            self.text_widget.tag_configure("font", font=("TkDefaultFont", current_font_size))
            try:
                current_tags = self.text_widget.tag_names("sel.first")
                if "font" not in current_tags:
                    self.text_widget.tag_add("font", self.text_widget.index(tk.SEL_FIRST), self.text_widget.index(tk.SEL_LAST))
                    self.text_widget.tag_configure("font", font=("TkDefaultFont", current_font_size))
            except tk.TclError:
                pass

    def change_alignment(self):
        alignment = filedialog.askstring("Alignment", "Enter Alignment (left, center, right):")
        if alignment:
            self.text_widget.tag_configure("align", justify=alignment)
            self.text_widget.tag_add("align", "1.0", tk.END)

    def change_line_spacing(self):
        spacing = simpledialog.askfloat("Line Spacing", "Enter Line Spacing (e.g., 1.0 for single spacing):", initialvalue=1.0)
        if spacing:
            self.text_widget.config(spacing1=spacing)

    def insert_header(self):
        header_text = filedialog.askstring("Insert Header", "Enter Header Text:")
        if header_text:
            self.text_widget.insert(tk.END, f"\n\n### {header_text} ###\n\n")

    def insert_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.gif;*.bmp")])
        if file_path:
            image = Image.open(file_path)
            resized_image = image.resize((400, 400), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(resized_image)

            # Create a Canvas widget and embed it into the Text widget
            canvas = tk.Canvas(self.text_widget, width=400, height=400)
            canvas.image = photo  # Keep a reference to the image to prevent garbage collection
            canvas.create_image(0, 0, anchor=tk.NW, image=photo, tags="img")
            self.text_widget.window_create(tk.END, window=canvas)
            self.text_widget.insert(tk.END, '\n')  # Add a newline after the image

    def delete_image(self):
        current_tags = self.text_widget.tag_names("sel.first")
        if "img" in current_tags:
            self.text_widget.delete(tk.SEL_FIRST, tk.SEL_LAST)

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
