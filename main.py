import customtkinter as ctk
import os
import json
from PIL import Image

from FilesOrganizer import FilesOrganizerFrame
from FilesRenamer import FilesRenamerFrame 
from FileDeleter import FileDeleterFrame
from DuplicateFinder import DuplicateFinderFrame
from StorageAnalyzer import StorageAnalyzerFrame
from Settings import SettingsFrame

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Project Suite")
        self.width = 1300
        self.height = 900
        self.center_window()
        
        self.active_button_color = "#1f538d" 
        ctk.set_appearance_mode("Dark")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- SIDEBAR ---
        self.sidebar_frame = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_propagate(False)
        
        self.app_title = ctk.CTkLabel(self.sidebar_frame, text="MENU", 
                                      font=("Arial Black", 22), text_color=self.active_button_color)
        self.app_title.pack(pady=(50, 40))

        self.nav_btns = {}
        self.nav_btns["home"] = self.create_nav_button("Dashboard", self.show_home)
        self.nav_btns["org"] = self.create_nav_button("Organizer", self.show_organizer)
        self.nav_btns["ren"] = self.create_nav_button("Renamer", self.show_renamer)
        self.nav_btns["del"] = self.create_nav_button("Deleter", self.show_deleter)
        self.nav_btns["dup"] = self.create_nav_button("Duplicates", self.show_duplicate_finder)
        self.nav_btns["sto"] = self.create_nav_button("Analyzer", self.show_storage_analyzer)

        self.btn_settings_nav = self.create_nav_button("⚙️ Settings", self.show_settings)
        self.btn_settings_nav.pack(side="bottom", pady=30)

        # --- MAIN CONTAINER ---
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.grid(row=0, column=1, sticky="nsew")

        self.header_label = ctk.CTkLabel(self.main_container, text="DASHBOARD", 
                                         font=("Arial", 36, "bold"))
        self.header_label.pack(pady=(40, 20))

        # --- PAGES ---
        self.home_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.setup_home_page()
        
        self.organizer_frame = FilesOrganizerFrame(self.main_container, fg_color="transparent")
        self.renamer_frame = FilesRenamerFrame(self.main_container, fg_color="transparent")
        self.deleter_frame = FileDeleterFrame(self.main_container, fg_color="transparent")
        self.duplicate_frame = DuplicateFinderFrame(self.main_container, fg_color="transparent")
        self.storage_analyzer_frame = StorageAnalyzerFrame(self.main_container, fg_color="transparent")
        self.settings_frame = SettingsFrame(self.main_container, 
                                            on_color_change_callback=self.update_app_accent_color, 
                                            fg_color="transparent")

        self.current_nav_key = "home"
        self.show_home()

    def create_nav_button(self, text, command):
        btn = ctk.CTkButton(self.sidebar_frame, text=text, fg_color="transparent", 
                            text_color="gray90", hover_color=("#D1D5DB", "#333333"), 
                            anchor="center", font=("Arial", 16), height=50, corner_radius=10, 
                            command=command)
        btn.pack(pady=5, padx=20, fill="x")
        return btn

    def setup_home_page(self):
        self.dash_grid = ctk.CTkFrame(self.home_frame, fg_color="transparent")
        self.dash_grid.place(relx=0.5, rely=0.5, anchor="center")

        tile_args = {"width": 240, "height": 240, "font": ("Arial", 18, "bold"), 
                     "corner_radius": 25, "border_width": 1, "border_color": "gray30",
                     "fg_color": "#2b2b2b", "hover_color": self.active_button_color}

        buttons = [
            ("FILE\nORGANIZER", self.show_organizer, 0, 0),
            ("FILE\nRENAMER", self.show_renamer, 0, 1),
            ("FILE\nDELETER", self.show_deleter, 0, 2),
            ("DUPLICATE\nFINDER", self.show_duplicate_finder, 1, 0),
            ("STORAGE\nANALYZER", self.show_storage_analyzer, 1, 1),
            ("SETTINGS", self.show_settings, 1, 2)
        ]

        self.tiles = []
        for text, cmd, r, c in buttons:
            btn = ctk.CTkButton(self.dash_grid, text=text, command=cmd, **tile_args)
            btn.grid(row=r, column=c, padx=15, pady=15)
            self.tiles.append(btn)

    def show_page(self, frame, title, nav_key):
        self.current_nav_key = nav_key
        
        for f in [self.home_frame, self.organizer_frame, self.renamer_frame, 
                  self.deleter_frame, self.duplicate_frame, 
                  self.storage_analyzer_frame, self.settings_frame]:
            f.pack_forget()
        
        self.update_sidebar_highlight()
        frame.pack(expand=True, fill="both", padx=40, pady=40)
        self.header_label.configure(text=title)

    def update_sidebar_highlight(self):
        for k, b in self.nav_btns.items():
            b.configure(fg_color=self.active_button_color if self.current_nav_key == k else "transparent")
        self.btn_settings_nav.configure(fg_color=self.active_button_color if self.current_nav_key == "settings" else "transparent")

    def show_home(self): self.show_page(self.home_frame, "DASHBOARD", "home")
    def show_organizer(self): self.show_page(self.organizer_frame, "FILE ORGANIZER", "org")
    def show_renamer(self): self.show_page(self.renamer_frame, "FILE RENAMER", "ren")
    def show_deleter(self): self.show_page(self.deleter_frame, "FILE DELETER", "del")
    def show_duplicate_finder(self): self.show_page(self.duplicate_frame, "DUPLICATE FINDER", "dup")
    def show_storage_analyzer(self): self.show_page(self.storage_analyzer_frame, "STORAGE ANALYZER", "sto")
    def show_settings(self): self.show_page(self.settings_frame, "SETTINGS", "settings")

    def update_app_accent_color(self, new_color):
        self.active_button_color = new_color
        self.app_title.configure(text_color=new_color)
        
        for tile in self.tiles:
            tile.configure(hover_color=new_color)
        
        self.update_sidebar_highlight()

        for attr in ["organizer_frame", "renamer_frame", "deleter_frame", "duplicate_frame", "storage_analyzer_frame"]:
            frame = getattr(self, attr)
            if hasattr(frame, "update_colors"):
                frame.update_colors(new_color)

    def center_window(self):
        x = (self.winfo_screenwidth() // 2) - (self.width // 2)
        y = (self.winfo_screenheight() // 2) - (self.height // 2)
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

if __name__ == "__main__":
    app = App()
    app.mainloop()