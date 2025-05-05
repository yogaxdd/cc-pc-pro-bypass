# Script Dibuat Oleh @yogakokxd, @mohfer
# Recode Boleh Jangan Lupa Credit:v

import os
import time
import glob
import shutil
import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from threading import Thread

class CapCutBypasserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CapCut Pro Bypasser")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        
        # Default draft folder path
        self.default_draft_path = os.path.join(
            os.path.expanduser('~'),
            'AppData', 'Local', 'CapCut', 'User Data',
            'Projects', 'com.lveditor.draft'
        )
        
        # Default output folder
        self.default_output_path = os.path.join(
            os.path.expanduser('~'), 'Videos'
        )
        
        self.draft_path = tk.StringVar(value=self.default_draft_path)
        self.output_path = tk.StringVar(value=self.default_output_path)
        self.selected_project = tk.StringVar()
        self.status_text = tk.StringVar(value="Status: Ready")
        self.project_list = []
        
        self.create_widgets()
        self.load_projects()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create header/banner
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="CapCut Pro Bypasser", font=("Arial", 16, "bold"))
        title_label.pack(side=tk.LEFT)
        
        credit_label = ttk.Label(header_frame, text="By @yogakokxd, @mohfer", font=("Arial", 10))
        credit_label.pack(side=tk.RIGHT)
        
        # Create draft folder selection section
        draft_frame = ttk.LabelFrame(main_frame, text="Draft Folder", padding="10")
        draft_frame.pack(fill=tk.X, pady=(0, 10))
        
        draft_entry = ttk.Entry(draft_frame, textvariable=self.draft_path, width=50)
        draft_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        draft_button = ttk.Button(draft_frame, text="Browse", command=self.browse_draft_folder)
        draft_button.pack(side=tk.LEFT)
        
        refresh_button = ttk.Button(draft_frame, text="Refresh Projects", command=self.load_projects)
        refresh_button.pack(side=tk.LEFT, padx=(5, 0))
        
        # Create project selection section
        project_frame = ttk.LabelFrame(main_frame, text="Select Project", padding="10")
        project_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Create scrollable frame for projects
        project_canvas = tk.Canvas(project_frame)
        scrollbar = ttk.Scrollbar(project_frame, orient="vertical", command=project_canvas.yview)
        self.scrollable_frame = ttk.Frame(project_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: project_canvas.configure(scrollregion=project_canvas.bbox("all"))
        )
        
        project_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        project_canvas.configure(yscrollcommand=scrollbar.set)
        
        project_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create output folder selection section
        output_frame = ttk.LabelFrame(main_frame, text="Output Folder", padding="10")
        output_frame.pack(fill=tk.X, pady=(0, 10))
        
        output_entry = ttk.Entry(output_frame, textvariable=self.output_path, width=50)
        output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        output_button = ttk.Button(output_frame, text="Browse", command=self.browse_output_folder)
        output_button.pack(side=tk.LEFT)
        
        # Create export button and status label
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        export_button = ttk.Button(action_frame, text="Export Project", command=self.export_project)
        export_button.pack(side=tk.LEFT, padx=(0, 10))
        
        status_label = ttk.Label(action_frame, textvariable=self.status_text)
        status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, orient="horizontal", 
                                           length=100, mode="determinate", 
                                           variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X)
        
    def browse_draft_folder(self):
        folder_path = filedialog.askdirectory(initialdir=self.draft_path.get())
        if folder_path:
            self.draft_path.set(folder_path)
            self.load_projects()
    
    def browse_output_folder(self):
        folder_path = filedialog.askdirectory(initialdir=self.output_path.get())
        if folder_path:
            self.output_path.set(folder_path)
    
    def load_projects(self):
        # Clear existing radio buttons
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            
        draft_path = self.draft_path.get()
        if not os.path.isdir(draft_path):
            self.status_text.set("Status: Draft folder not found!")
            return
            
        # Get all directories in the draft folder
        try:
            self.project_list = [d for d in os.listdir(draft_path) if os.path.isdir(os.path.join(draft_path, d))]
            
            if not self.project_list:
                ttk.Label(self.scrollable_frame, text="No projects found").pack(anchor="w", pady=5)
                self.status_text.set("Status: No projects found in folder!")
                return
                
            # Create radio buttons for each project
            for i, project in enumerate(self.project_list):
                project_frame = ttk.Frame(self.scrollable_frame)
                project_frame.pack(fill=tk.X, pady=2)
                
                radio = ttk.Radiobutton(project_frame, text=project, value=project, variable=self.selected_project)
                radio.pack(side=tk.LEFT)
                
                # Get project created date if possible
                project_path = os.path.join(draft_path, project)
                try:
                    mtime = os.path.getmtime(project_path)
                    dt = datetime.datetime.fromtimestamp(mtime)
                    date_label = ttk.Label(project_frame, text=f"Modified: {dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    date_label.pack(side=tk.RIGHT)
                except:
                    pass
                    
            if self.project_list:
                self.selected_project.set(self.project_list[0])
                self.status_text.set(f"Status: Loaded {len(self.project_list)} projects")
                
        except Exception as e:
            self.status_text.set(f"Status: Error loading projects - {str(e)}")
            messagebox.showerror("Error", f"Failed to load projects: {str(e)}")
    
    def export_project(self):
        project = self.selected_project.get()
        if not project:
            messagebox.showwarning("Warning", "Please select a project first!")
            return
            
        draft_path = self.draft_path.get()
        output_path = self.output_path.get()
        
        # Check if paths exist
        if not os.path.isdir(draft_path):
            messagebox.showerror("Error", "Draft folder does not exist!")
            return
            
        if not os.path.isdir(output_path):
            try:
                os.makedirs(output_path, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create output folder: {str(e)}")
                return
        
        # Start export in a separate thread
        Thread(target=self.export_thread, args=(project, draft_path, output_path)).start()
    
    def export_thread(self, project, draft_path, output_path):
        try:
            self.status_text.set(f"Status: Exporting {project}...")
            self.progress_var.set(0)
            self.root.update_idletasks()
            
            proj_dir = os.path.join(draft_path, project)
            if not os.path.isdir(proj_dir):
                self.status_text.set(f"Status: Project '{project}' not found!")
                messagebox.showerror("Error", f"Project '{project}' not found!")
                return
                
            comb_dir = os.path.join(proj_dir, 'Resources', 'combination')
            
            # Check if combination directory exists
            if not os.path.isdir(comb_dir):
                self.status_text.set(f"Status: No export files found for '{project}'!")
                messagebox.showerror("Error", f"No export files found for '{project}'!")
                return
                
            pct = 0
            found = False
            
            # Look for mp4 files
            for i in range(20):  # Try for 20 seconds max
                # Get only mp4 files without "alpha" in filename
                files = [f for f in glob.glob(os.path.join(comb_dir, '*.mp4')) 
                         if 'alpha' not in os.path.basename(f).lower()]
                         
                if files:
                    found = True
                    break
                    
                pct = min(pct + 5, 95)
                self.progress_var.set(pct)
                self.status_text.set(f"Status: Processing export... ({pct}%)")
                self.root.update_idletasks()
                time.sleep(1)
                
            if not found:
                self.status_text.set("Status: No video files found!")
                messagebox.showerror("Error", "No video files found for this project!")
                return
                
            # Find the latest mp4 file
            mp4_files = [f for f in glob.glob(os.path.join(comb_dir, '*.mp4')) 
                        if 'alpha' not in os.path.basename(f).lower()]
                        
            latest = max(mp4_files, key=os.path.getmtime)
            mtime = os.path.getmtime(latest)
            dt = datetime.datetime.fromtimestamp(mtime)
            
            self.progress_var.set(100)
            self.status_text.set(f"Status: Found video file from {dt.strftime('%Y-%m-%d %H:%M:%S')}")
            self.root.update_idletasks()
            
            # Create unique filename
            dest_path = os.path.join(output_path, f"{project}.mp4")
            counter = 1
            while os.path.exists(dest_path):
                dest_path = os.path.join(output_path, f"{project}({counter}).mp4")
                counter += 1
                
            # Copy the file
            shutil.copy2(latest, dest_path)
            
            self.status_text.set(f"Status: Exported to {dest_path}")
            messagebox.showinfo("Success", f"Video has been saved to:\n{dest_path}")
            
        except Exception as e:
            self.status_text.set(f"Status: Error - {str(e)}")
            messagebox.showerror("Error", f"Export failed: {str(e)}")

def main():
    root = tk.Tk()
    app = CapCutBypasserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()