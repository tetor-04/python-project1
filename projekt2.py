import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# --- App Setup ---
class RibbonApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Word-Like Ribbon UI with Manga Support")
        self.root.geometry("1000x600")

        self.manga_folder = None

        self.create_ribbon()
        self.create_content_area()

    def create_ribbon(self):
        """Create the ribbon menu using ttk.Notebook"""
        self.ribbon = ttk.Notebook(self.root)
        self.ribbon.pack(fill='x')

        # Define ribbon tabs
        self.home_tab = ttk.Frame(self.ribbon)
        self.insert_tab = ttk.Frame(self.ribbon)
        self.view_tab = ttk.Frame(self.ribbon)
        self.manga_tab = ttk.Frame(self.ribbon)  # New Manga tab

        self.ribbon.add(self.home_tab, text='Home')
        self.ribbon.add(self.insert_tab, text='Insert')
        self.ribbon.add(self.view_tab, text='View')
        self.ribbon.add(self.manga_tab, text='Manga')  # Add Manga tab

        # Fill tabs with content
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
        # Group for buttons
        manga_group = ttk.LabelFrame(self.manga_tab, text='Manga Tools', padding=10)
        manga_group.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        ttk.Button(manga_group, text='Select Manga Folder', command=self.select_manga_folder).grid(row=0, column=0, padx=5)
        ttk.Button(manga_group, text='Import Manga', command=self.import_manga).grid(row=0, column=1, padx=5)
        ttk.Button(manga_group, text='View Chapter', command=self.view_chapter).grid(row=0, column=2, padx=5)
        ttk.Button(manga_group, text='Bookmark Page', command=self.bookmark_page).grid(row=0, column=3, padx=5)

        # Folder path label
        self.manga_path_label = ttk.Label(self.manga_tab, text="No folder selected", foreground="gray")
        self.manga_path_label.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Listbox to display manga series (folder names)
        listbox_frame = ttk.LabelFrame(self.manga_tab, text="Manga Series", padding=10)
        listbox_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.manga_listbox = tk.Listbox(listbox_frame, height=10, width=50)
        self.manga_listbox.pack(side='left', fill='y')

        scrollbar = ttk.Scrollbar(listbox_frame, orient='vertical', command=self.manga_listbox.yview)
        scrollbar.pack(side='right', fill='y')

        self.manga_listbox.config(yscrollcommand=scrollbar.set)

    def create_content_area(self):
        """Main text editor area"""
        self.text_area = tk.Text(self.root, wrap='word', undo=True)
        self.text_area.pack(fill='both', expand=True)

    # --- Clipboard Commands ---
    def copy(self):
        try:
            self.root.clipboard_clear()
            selected = self.text_area.selection_get()
            self.root.clipboard_append(selected)
        except tk.TclError:
            messagebox.showinfo("Copy", "No text selected.")

    def cut(self):
        try:
            self.copy()
            self.text_area.delete("sel.first", "sel.last")
        except tk.TclError:
            messagebox.showinfo("Cut", "No text selected.")

    def paste(self):
        try:
            content = self.root.clipboard_get()
            self.text_area.insert(tk.INSERT, content)
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

    # --- Insert Commands ---
    def insert_picture(self):
        messagebox.showinfo("Insert Picture", "This would insert a picture (not implemented).")

    def insert_table(self):
        messagebox.showinfo("Insert Table", "This would insert a table (not implemented).")

    # --- Zoom Commands ---
    def zoom_in(self):
        current_size = self.get_text_font_size()
        self.set_text_font_size(current_size + 2)

    def zoom_out(self):
        current_size = self.get_text_font_size()
        if current_size > 8:
            self.set_text_font_size(current_size - 2)

    def get_text_font_size(self):
        font = self.text_area.cget("font")
        try:
            size = int(font.split(" ")[-1])
        except:
            size = 12
        return size

    def set_text_font_size(self, size):
        self.text_area.configure(font=("TkDefaultFont", size))

    # --- Manga Tab Functions ---
    def select_manga_folder(self):
        folder = filedialog.askdirectory(title="Select Manga Folder")
        if folder:
            self.manga_folder = folder
            self.manga_path_label.config(text=f"Selected: {folder}", foreground="black")
            self.update_manga_list(folder)
        else:
            self.manga_path_label.config(text="No folder selected", foreground="gray")

    def update_manga_list(self, folder):
        self.manga_listbox.delete(0, tk.END)
        try:
            subfolders = [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]
            for name in sorted(subfolders):
                self.manga_listbox.insert(tk.END, name)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to list manga folders:\n{e}")

    def import_manga(self):
        messagebox.showinfo("Import Manga", "This would allow you to import manga files (not implemented).")

    def view_chapter(self):
        selected = self.manga_listbox.get(tk.ACTIVE)
        if selected:
            messagebox.showinfo("View Chapter", f"Viewing chapters for: {selected} (not implemented).")
        else:
            messagebox.showinfo("View Chapter", "Please select a manga series from the list.")

    def bookmark_page(self):
        messagebox.showinfo("Bookmark Page", "This would bookmark the current page (not implemented).")

# --- Run the App ---
if __name__ == "__main__":
    root = tk.Tk()
    app = RibbonApp(root)
    root.mainloop()
