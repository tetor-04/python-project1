import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import re

class RibbonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word-Like Ribbon UI with Manga Support")
        self.root.geometry("1200x700")

        self.manga_folder = None
        self.output_folder = None

        self.create_horizontal_ribbon()
        self.create_vertical_ribbon()
        self.create_content_area()

        self.vertical_ribbon_frame.pack_forget()
        self.panel_tabs.bind("<<NotebookTabChanged>>", self.on_horizontal_tab_changed)

    def create_horizontal_ribbon(self):
        self.panel_tabs = ttk.Notebook(self.root)
        self.panel_tabs.pack(fill='x')

        self.home_tab = ttk.Frame(self.panel_tabs)
        self.insert_tab = ttk.Frame(self.panel_tabs)
        self.view_tab = ttk.Frame(self.panel_tabs)
        self.manga_tab = ttk.Frame(self.panel_tabs)

        self.panel_tabs.add(self.home_tab, text='Home')
        self.panel_tabs.add(self.insert_tab, text='Insert')
        self.panel_tabs.add(self.view_tab, text='View')
        self.panel_tabs.add(self.manga_tab, text='Manga')

        self.create_home_tab()
        self.create_insert_tab()
        self.create_view_tab()
        self.create_manga_tab()

    def create_home_tab(self):
        clipboard_group = ttk.LabelFrame(self.home_tab, text='Clipboard', padding=10)
        clipboard_group.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(clipboard_group, text='Paste', command=self.paste).grid(row=0, column=0, padx=5)
        ttk.Button(clipboard_group, text='Copy', command=self.copy).grid(row=0, column=1, padx=5)
        ttk.Button(clipboard_group, text='Cut', command=self.cut).grid(row=0, column=2, padx=5)

        edit_group = ttk.LabelFrame(self.home_tab, text='Editing', padding=10)
        edit_group.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(edit_group, text='Undo', command=self.undo).grid(row=0, column=0, padx=5)
        ttk.Button(edit_group, text='Redo', command=self.redo).grid(row=0, column=1, padx=5)

    def create_insert_tab(self):
        insert_group = ttk.LabelFrame(self.insert_tab, text='Insert Items', padding=10)
        insert_group.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(insert_group, text='Picture', command=self.insert_picture).grid(row=0, column=0, padx=5)
        ttk.Button(insert_group, text='Table', command=self.insert_table).grid(row=0, column=1, padx=5)

    def create_view_tab(self):
        view_group = ttk.LabelFrame(self.view_tab, text='Display', padding=10)
        view_group.grid(row=0, column=0, padx=5, pady=5)

        ttk.Button(view_group, text='Zoom In', command=self.zoom_in).grid(row=0, column=0, padx=5)
        ttk.Button(view_group, text='Zoom Out', command=self.zoom_out).grid(row=0, column=1, padx=5)

    def create_manga_tab(self):
        ribbon = ttk.Frame(self.manga_tab, padding=10)
        ribbon.pack(fill='x')

        # Folder Setup Group
        folder_group = ttk.LabelFrame(ribbon, text="Folder Setup", padding=10)
        folder_group.pack(side='left', padx=10)

        ttk.Button(folder_group, text='Source Folder', command=self.select_manga_folder).pack(pady=2)
        ttk.Button(folder_group, text='Output Folder', command=self.select_output_folder).pack(pady=2)

        # Merge Options Group
        merge_group = ttk.LabelFrame(ribbon, text="Merge Options", padding=10)
        merge_group.pack(side='left', padx=10)

        ttk.Button(merge_group, text='Merge All', command=self.merge_all_manga).pack(pady=2)
        ttk.Button(merge_group, text='Merge Manga', command=self.merge_selected_manga).pack(pady=2)
        ttk.Button(merge_group, text='Merge Chapter', command=self.merge_selected_chapter).pack(pady=2)
        ttk.Button(merge_group, text='Merge Selected Images', command=self.merge_selected_images).pack(pady=2)

    def create_vertical_ribbon(self):
        self.vertical_ribbon_frame = ttk.Frame(self.root, width=350, relief='raised', borderwidth=2)
        self.vertical_ribbon_frame.pack(side='left', fill='y')

        self.vertical_tabs = ttk.Notebook(self.vertical_ribbon_frame)
        self.vertical_tabs.pack(fill='both', expand=True)

        self.source_tab = ttk.Frame(self.vertical_tabs)
        self.vertical_tabs.add(self.source_tab, text='Source')

        self.source_tree = ttk.Treeview(self.source_tab, columns=('fullpath',), show='tree')
        self.source_tree.pack(side='left', fill='both', expand=True)
        self.source_tree.bind('<<TreeviewSelect>>', self.on_source_tree_select)

        source_scroll = ttk.Scrollbar(self.source_tab, orient='vertical', command=self.source_tree.yview)
        source_scroll.pack(side='right', fill='y')
        self.source_tree.configure(yscrollcommand=source_scroll.set)

        self.output_tab = ttk.Frame(self.vertical_tabs)
        self.vertical_tabs.add(self.output_tab, text='Output')

        self.output_tree = ttk.Treeview(self.output_tab, columns=('fullpath',), show='tree')
        self.output_tree.pack(side='left', fill='both', expand=True)
        self.output_tree.bind('<<TreeviewSelect>>', self.on_output_tree_select)

        output_scroll = ttk.Scrollbar(self.output_tab, orient='vertical', command=self.output_tree.yview)
        output_scroll.pack(side='right', fill='y')
        self.output_tree.configure(yscrollcommand=output_scroll.set)

    def create_content_area(self):
        content_frame = ttk.Frame(self.root)
        content_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.image_label = ttk.Label(content_frame, text='Select an image to preview', anchor='center', relief='sunken')
        self.image_label.pack(fill='both', expand=True)

        self.info_text = tk.Text(content_frame, height=6)
        self.info_text.pack(fill='x')

        self.text_area = tk.Text(content_frame, height=8)
        self.text_area.pack(fill='both', expand=True)

    def select_manga_folder(self):
        folder = filedialog.askdirectory(title="Select Manga Source Folder")
        if folder:
            self.manga_folder = folder
            self.populate_tree(self.source_tree, folder)

    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder = folder
            self.populate_tree(self.output_tree, folder)

    def populate_tree(self, tree, folder):
        tree.delete(*tree.get_children())

        def insert_node(parent, path):
            for entry in sorted(os.listdir(path)):
                full_path = os.path.join(path, entry)
                node = tree.insert(parent, 'end', text=entry, values=(full_path,))
                if os.path.isdir(full_path):
                    insert_node(node, full_path)
        insert_node('', folder)

    def on_source_tree_select(self, event):
        self.preview_selected(self.source_tree)

    def on_output_tree_select(self, event):
        self.preview_selected(self.output_tree)

    def preview_selected(self, tree):
        selected = tree.selection()
        if not selected:
            return
        node = selected[0]
        fullpath = tree.item(node, 'values')[0]

        if os.path.isfile(fullpath) and fullpath.lower().endswith(('.jpg', '.png', '.jpeg')):
            try:
                image = Image.open(fullpath)
                image.thumbnail((400, 400))
                photo = ImageTk.PhotoImage(image)
                self.image_label.config(image=photo, text='')
                self.image_label.image = photo

                info = f"Filename: {os.path.basename(fullpath)}\n"
                info += f"Size: {os.path.getsize(fullpath)} bytes\n"
                info += f"Dimensions: {image.width} x {image.height}"
                self.info_text.delete('1.0', tk.END)
                self.info_text.insert(tk.END, info)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            self.image_label.config(image='', text="Not an image")
            self.info_text.delete('1.0', tk.END)

    def merge_selected_manga(self):
        if not self.manga_folder or not self.output_folder:
            messagebox.showwarning("Missing Folder", "Please select both source and output folders.")
            return

        for manga_name in os.listdir(self.manga_folder):
            manga_path = os.path.join(self.manga_folder, manga_name)
            if os.path.isdir(manga_path):
                self.merge_manga_structure(manga_path, os.path.join(self.output_folder, manga_name))

        self.populate_tree(self.output_tree, self.output_folder)
        messagebox.showinfo("Done", "Merge completed.")

    def merge_manga_structure(self, src, dest):
        for root, dirs, files in os.walk(src):
            if any(f.lower().endswith(('.jpg', '.png', '.jpeg')) for f in files):
                rel_path = os.path.relpath(root, src)
                target_path = os.path.join(dest, rel_path)
                self.merge_or_copy_images(root, target_path)

    def merge_or_copy_images(self, src_folder, dest_folder):
        images = sorted(
            [f for f in os.listdir(src_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))],
            key=lambda s: [int(t) if t.isdigit() else t.lower() for t in re.split(r'(\d+)', s)]
        )

        num_images = len(images)
        os.makedirs(dest_folder, exist_ok=True)

        if num_images <= 25:
            for img in images:
                src = os.path.join(src_folder, img)
                dst = os.path.join(dest_folder, img)
                with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
                    fdst.write(fsrc.read())
            return

        group_size = self.choose_group_size(num_images)
        index = 1

        for i in range(0, num_images, group_size):
            group = images[i:i + group_size]
            imgs = [Image.open(os.path.join(src_folder, name)).convert("RGBA") for name in group]
            widths, heights = zip(*(img.size for img in imgs))

            merged = Image.new("RGBA", (max(widths), sum(heights)))
            y = 0
            for img in imgs:
                merged.paste(img, (0, y))
                y += img.height

            merged.convert("RGB").save(os.path.join(dest_folder, f"{index:03}.png"))
            index += 1

    def choose_group_size(self, count):
        for size in range(20, 26):
            if count % size == 0 or count // size <= size:
                return size
        return 25

    # New merge function stubs
    def merge_all_manga(self):
        messagebox.showinfo("TODO", "Merge All Manga - Not Implemented Yet")

    def merge_selected_chapter(self):
        messagebox.showinfo("TODO", "Merge Selected Chapter - Not Implemented Yet")

    def merge_selected_images(self):
        messagebox.showinfo("TODO", "Merge Selected Images - Not Implemented Yet")

    def copy(self):
        try:
            self.root.clipboard_clear()
            text = self.text_area.selection_get()
            self.root.clipboard_append(text)
        except tk.TclError:
            pass

    def cut(self):
        try:
            self.copy()
            self.text_area.delete("sel.first", "sel.last")
        except tk.TclError:
            pass

    def paste(self):
        try:
            self.text_area.insert(tk.INSERT, self.root.clipboard_get())
        except tk.TclError:
            pass

    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass

    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass

    def insert_picture(self):
        messagebox.showinfo("Insert Picture", "Insert Picture - Not Implemented")

    def insert_table(self):
        messagebox.showinfo("Insert Table", "Insert Table - Not Implemented")

    def zoom_in(self):
        current = self.get_text_font_size()
        self.set_text_font_size(current + 2)

    def zoom_out(self):
        current = self.get_text_font_size()
        if current > 8:
            self.set_text_font_size(current - 2)

    def get_text_font_size(self):
        try:
            return int(self.text_area.cget("font").split(" ")[-1])
        except:
            return 12

    def set_text_font_size(self, size):
        self.text_area.configure(font=("TkDefaultFont", size))

    def on_horizontal_tab_changed(self, event):
        tab = self.panel_tabs.tab(self.panel_tabs.select(), "text")
        if tab == "Manga":
            self.vertical_ribbon_frame.pack(side='left', fill='y')
        else:
            self.vertical_ribbon_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = RibbonApp(root)
    root.mainloop()
