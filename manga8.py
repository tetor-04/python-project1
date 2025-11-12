import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, Toplevel
from PIL import Image, ImageTk
import zipfile
import platform

class MangaManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manga Manager with Merge, Zip & Delete")
        self.root.geometry("1400x750")

        self.manga_folder = None
        self.output_folder = None
        self.zip_format = tk.StringVar(value=".zip")
        self.photo = None  # Keep reference for preview

        
        self.create_horizontal_ribbon()
        self.create_vertical_ribbon()
        self.create_content_area()

        self.vertical_ribbon_frame.pack_forget()
        self.panel_tabs.bind("<<NotebookTabChanged>>", self.on_horizontal_tab_changed)

    def create_horizontal_ribbon(self):
        self.panel_tabs = ttk.Notebook(self.root)
        self.panel_tabs.pack(fill='x')

        # Tabs
        self.home_tab = ttk.Frame(self.panel_tabs)
        self.insert_tab = ttk.Frame(self.panel_tabs)
        self.view_tab = ttk.Frame(self.panel_tabs)
        self.manga_tab = ttk.Frame(self.panel_tabs)
        self.web_tab = ttk.Frame(self.panel_tabs)

        for tab, text in [(self.home_tab, "Home"), (self.insert_tab, "Insert"),
                          (self.view_tab, "View"), (self.manga_tab, "Manga"),
                          (self.web_tab, "Browser")]:
            self.panel_tabs.add(tab, text=text)

        self.create_home_tab()
        self.create_insert_tab()
        self.create_view_tab()
        self.create_manga_tab()
        self.create_web_tab()

    def create_home_tab(self):
        clipboard_group = ttk.LabelFrame(self.home_tab, text='Clipboard', padding=10)
        clipboard_group.grid(row=0, column=0, padx=5, pady=5)
        for text, cmd in [('Paste', self.paste), ('Copy', self.copy), ('Cut', self.cut)]:
            ttk.Button(clipboard_group, text=text, command=cmd).pack(side='left', padx=5)

        edit_group = ttk.LabelFrame(self.home_tab, text='Editing', padding=10)
        edit_group.grid(row=0, column=1, padx=5, pady=5)
        for text, cmd in [('Undo', self.undo), ('Redo', self.redo)]:
            ttk.Button(edit_group, text=text, command=cmd).pack(side='left', padx=5)

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

        folder_group = ttk.LabelFrame(ribbon, text="Folder Setup", padding=10)
        folder_group.pack(side='left', padx=20)
        ttk.Button(folder_group, text='Source Folder', command=self.select_manga_folder).pack(side='left', padx=5)
        ttk.Button(folder_group, text='Output Folder', command=self.select_output_folder).pack(side='left', padx=5)

        merge_group = ttk.LabelFrame(ribbon, text="Merge Options", padding=10)
        merge_group.pack(side='left', padx=20)
        for text, cmd in [('Merge Manga', self.merge_all_manga),
                          ('Merge Selected Chapters', self.merge_selected_manga),
                          ('Merge Selected Chapter', self.merge_selected_chapter)]:
            ttk.Button(merge_group, text=text, command=cmd).pack(side='left', padx=5)

        compress_group = ttk.LabelFrame(ribbon, text="Compression Options", padding=10)
        compress_group.pack(side='left', padx=20)
        ttk.Label(compress_group, text="Format:").pack(side='left', padx=5)
        ttk.Combobox(compress_group, textvariable=self.zip_format,
                     values=[".zip", ".cbz"], width=5, state="readonly").pack(side='left', padx=5)
        ttk.Button(compress_group, text="Zip Selected Folder", command=self.zip_selected_folder).pack(side='left', padx=5)
        ttk.Button(compress_group, text="Zip Selected Images", command=self.zip_selected_images).pack(side='left', padx=5)

        # CRUD Group
        crud_group = ttk.LabelFrame(ribbon, text="CRUD", padding=10)
        crud_group.pack(side='left', padx=20)
        ttk.Button(crud_group, text="Delete Selected", command=self.delete_selected_items).pack(side='left', padx=5)
        # Future buttons like Copy can be added here

    def create_web_tab(self):
        ttk.Button(self.web_tab, text="Open WordPress Site", command=self.open_wordpress).pack(pady=20)

    def open_wordpress(self):
        import webview
        webview.create_window("Browser", "https://your-wordpress-site.com/wp-admin")
        webview.start()

    def create_vertical_ribbon(self):
        self.vertical_ribbon_frame = ttk.Frame(self.root, width=350, relief='raised', borderwidth=2)
        self.vertical_ribbon_frame.pack(side='left', fill='y')

        self.vertical_tabs = ttk.Notebook(self.vertical_ribbon_frame)
        self.vertical_tabs.pack(fill='both', expand=True)

        self.source_tab = ttk.Frame(self.vertical_tabs)
        self.output_tab = ttk.Frame(self.vertical_tabs)
        self.vertical_tabs.add(self.source_tab, text='Source')
        self.vertical_tabs.add(self.output_tab, text='Output')

        # Source pane
        self.source_tree = ttk.Treeview(self.source_tab, columns=('fullpath',), show='tree')
        self.source_tree.pack(side='left', fill='both', expand=True)
        self.source_tree.bind('<<TreeviewSelect>>', self.on_source_tree_select)

        source_scroll = ttk.Scrollbar(self.source_tab, orient='vertical', command=self.source_tree.yview)
        source_scroll.pack(side='right', fill='y')
        self.source_tree.configure(yscrollcommand=source_scroll.set)

        # Output pane
        self.output_tree = ttk.Treeview(self.output_tab, columns=('fullpath',), show='tree')
        self.output_tree.pack(side='left', fill='both', expand=True)
        self.output_tree.bind('<<TreeviewSelect>>', self.on_output_tree_select)

        output_scroll = ttk.Scrollbar(self.output_tab, orient='vertical', command=self.output_tree.yview)
        output_scroll.pack(side='right', fill='y')
        self.output_tree.configure(yscrollcommand=output_scroll.set)

    def create_content_area(self):
        content_frame = ttk.Frame(self.root)
        content_frame.pack(side='left', fill='both', expand=True, padx=5, pady=5)

        self.image_label = ttk.Label(content_frame, text='Select an image to preview',
                                     anchor='center', relief='sunken')
        self.image_label.pack(fill='both', expand=True)

        self.info_label = ttk.Label(content_frame, text='', anchor='w', justify='left', font=("Consolas", 10))
        self.info_label.pack(fill='x', pady=5)

        # Mouse wheel zoom for images
        self.image_label.bind("<MouseWheel>", self.mouse_zoom)
        self.image_label.bind("<Button-4>", self.mouse_zoom)
        self.image_label.bind("<Button-5>", self.mouse_zoom)

    def mouse_zoom(self, event):
        delta = (event.delta // 120) if platform.system() != 'Linux' else (1 if event.num == 4 else -1)
        if delta > 0:
            self.zoom_in()
        elif delta < 0:
            self.zoom_out()

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
                full = os.path.join(path, entry)
                node = tree.insert(parent, 'end', text=entry, values=(full,))
                if os.path.isdir(full):
                    insert_node(node, full)
        insert_node('', folder)

    def on_source_tree_select(self, event):
        self.preview_selected(self.source_tree)

    def on_output_tree_select(self, event):
        self.preview_selected(self.output_tree)

    def preview_selected(self, tree):
        sel = tree.selection()
        if not sel:
            self.image_label.config(image='', text='Select an image to preview')
            self.info_label.config(text='')
            return
        fullpath = tree.item(sel[0], 'values')[0]
        ext = os.path.splitext(fullpath)[1].lower()
        if os.path.isfile(fullpath) and ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.webp']:
            try:
                img = Image.open(fullpath)
                img.thumbnail((600, 600))
                self.photo = ImageTk.PhotoImage(img)
                self.image_label.config(image=self.photo, text='')
                size = os.path.getsize(fullpath) / (1024*1024)
                w, h = img.size
                info = f"File: {os.path.basename(fullpath)}\nSize: {size:.2f} MB\nDimensions: {w}x{h}"
                self.info_label.config(text=info)
            except Exception as e:
                self.image_label.config(image='', text='Error loading image')
                self.info_label.config(text=str(e))
        else:
            self.image_label.config(image='', text='No image preview available')
            self.info_label.config(text='')

    def zoom_in(self):
        # Placeholder zoom function
        print("Zoom In")

    def zoom_out(self):
        # Placeholder zoom function
        print("Zoom Out")

    def paste(self):
        print("Paste")

    def copy(self):
        print("Copy")

    def cut(self):
        print("Cut")

    def undo(self):
        print("Undo")

    def redo(self):
        print("Redo")

    def insert_picture(self):
        print("Insert Picture")

    def insert_table(self):
        print("Insert Table")

    def merge_all_manga(self):
        messagebox.showinfo("Merge Manga", "Merging all manga... (functionality not implemented)")

    def merge_selected_manga(self):
        messagebox.showinfo("Merge Selected Chapters", "Merging selected chapters... (functionality not implemented)")

    def merge_selected_chapter(self):
        messagebox.showinfo("Merge Selected Chapter", "Merging selected chapter... (functionality not implemented)")

    def zip_selected_folder(self):
        messagebox.showinfo("Zip Folder", "Zipping selected folder... (functionality not implemented)")

    def zip_selected_images(self):
        messagebox.showinfo("Zip Images", "Zipping selected images... (functionality not implemented)")

    def delete_selected_items(self):
        # Delete selected files from both source and output trees
        for tree in [self.source_tree, self.output_tree]:
            selected = tree.selection()
            if not selected:
                continue
            for item in selected:
                path = tree.item(item, 'values')[0]
                if messagebox.askyesno("Delete", f"Are you sure you want to delete:\n{path}?"):
                    try:
                        if os.path.isfile(path):
                            os.remove(path)
                        elif os.path.isdir(path):
                            shutil.rmtree(path)
                        tree.delete(item)
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to delete {path}\n{str(e)}")

    def on_horizontal_tab_changed(self, event):
        current_tab = event.widget.tab('current')['text']
        if current_tab == "Manga":
            self.vertical_ribbon_frame.pack(side='left', fill='y')
        else:
            self.vertical_ribbon_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = MangaManagerApp(root)
    root.mainloop()
