import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkcalendar import Calendar, DateEntry
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Define the path for JSON storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATA_FILE = os.path.join(DATA_DIR, "projects.json")

# Ensure the data directory exists
os.makedirs(DATA_DIR, exist_ok=True)

# Global variable to store the current project name
current_project = None

# Load projects from JSON
def load_projects():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Save projects to JSON
def save_projects(projects):
    with open(DATA_FILE, "w") as file:
        json.dump(projects, file, indent=4)

# Add a new project
def add_project():
    project_name = simpledialog.askstring("New Project", "Enter project name:")
    if project_name:
        projects = load_projects()
        if project_name in projects:
            messagebox.showwarning("Warning", "Project already exists!")
        else:
            projects[project_name] = []
            save_projects(projects)
            project_listbox.insert(tk.END, project_name)
            messagebox.showinfo("Success", f"Project '{project_name}' added!")

# Delete a project
def delete_project():
    global current_project
    selected = project_listbox.curselection()
    if not selected:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = project_listbox.get(selected[0])
    projects = load_projects()

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete the project '{project_name}'?")
    if confirm:
        del projects[project_name]
        save_projects(projects)
        project_listbox.delete(selected[0])
        if current_project == project_name:
            current_project = None
        messagebox.showinfo("Success", f"Project '{project_name}' deleted!")

# Add a task to a selected project
def add_task():
    global current_project
    if not current_project:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project
    task_name = simpledialog.askstring("New Task", "Enter task name:")

    def get_datetime_input(date_entry, time_entry):
        date_input = date_entry.get_date()  # tkcalendar DateEntry returns a date
        time_input = time_entry.get()         # Expected to be in HH:MM format
        return f"{date_input.strftime('%d.%m.%Y')} {time_input}"

    def submit_task():
        start_datetime = get_datetime_input(start_date_entry, start_time_entry)
        end_datetime = get_datetime_input(end_date_entry, end_time_entry)

        projects = load_projects()
        projects[project_name].append({
            "task": task_name, 
            "start": start_datetime, 
            "end": end_datetime
        })
        save_projects(projects)
        update_task_listbox(project_name)
        messagebox.showinfo("Success", f"Task '{task_name}' added to '{project_name}'!")

    dialog = tk.Toplevel(root)
    dialog.title("Enter Task Start and End Date/Time")

    tk.Label(dialog, text="Select Start Date and Time").pack(pady=5)
    start_date_entry = DateEntry(dialog, date_pattern='dd.mm.yyyy')
    start_date_entry.pack(pady=5)
    tk.Label(dialog, text="Enter Start Time (HH:MM)").pack(pady=5)
    start_time_entry = tk.Entry(dialog)
    start_time_entry.pack(pady=5)

    tk.Label(dialog, text="Select End Date and Time").pack(pady=5)
    end_date_entry = DateEntry(dialog, date_pattern='dd.mm.yyyy')
    end_date_entry.pack(pady=5)
    tk.Label(dialog, text="Enter End Time (HH:MM)").pack(pady=5)
    end_time_entry = tk.Entry(dialog)
    end_time_entry.pack(pady=5)

    btn_add_task = tk.Button(dialog, text="Submit Task", command=submit_task)
    btn_add_task.pack(pady=10)

# Delete a task using the current project
def delete_task():
    global current_project
    if not current_project:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project
    projects = load_projects()
    tasks = projects.get(project_name, [])

    selected_task = task_listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Warning", "Please select a task to delete!")
        return

    task_text = task_listbox.get(selected_task[0])
    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete:\n{task_text}?")
    if confirm:
        tasks.pop(selected_task[0])
        save_projects(projects)
        update_task_listbox(project_name)
        messagebox.showinfo("Success", f"Task '{task_text}' deleted!")

# Update the task listbox when a project is selected
def update_task_listbox(project_name):
    tasks = load_projects().get(project_name, [])

    # Sort tasks by start date
    tasks.sort(key=lambda task: datetime.strptime(task["start"], "%d.%m.%Y %H:%M"))

    task_listbox.delete(0, tk.END)
    for task in tasks:
        task_listbox.insert(tk.END, f"{task['task']} ({task['start']} - {task['end']})")

# Show Gantt chart for the selected project
def show_gantt_chart():
    global current_project
    if not current_project:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project
    projects = load_projects()
    tasks = projects.get(project_name, [])

    if not tasks:
        messagebox.showwarning("Warning", "No tasks in this project!")
        return

 # Sort tasks by start date
    tasks.sort(key=lambda task: datetime.strptime(task["start"], "%d.%m.%Y %H:%M"))
    
    fig, ax = plt.subplots(figsize=(10, 6))
    task_labels = []

    for i, task in enumerate(tasks):
        task_labels.append(task["task"])
        start_dt = datetime.strptime(task["start"], "%d.%m.%Y %H:%M")
        end_dt = datetime.strptime(task["end"], "%d.%m.%Y %H:%M")
        start_num = mdates.date2num(start_dt)
        end_num = mdates.date2num(end_dt)
        width = end_num - start_num
        ax.barh(i, width, left=start_num, color="skyblue", edgecolor="grey", height=0.8)

    ax.set_yticks(range(len(task_labels)))
    ax.set_yticklabels(task_labels)
    # Invert the y-axis so tasks are listed from top to bottom
    ax.invert_yaxis()
    
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y %H:%M"))
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Tasks")
    ax.set_title(f"Gantt Chart for {project_name}")
    fig.tight_layout()
    plt.show()

# Export Gantt chart as an image or PDF
def export_chart_as_image():
    global current_project
    if not current_project:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project
    projects = load_projects()
    tasks = projects.get(project_name, [])

    if not tasks:
        messagebox.showwarning("Warning", "No tasks in this project!")
        return

    fig, ax = plt.subplots(figsize=(10, 6))
    task_labels = []
    for i, task in enumerate(tasks):
        task_labels.append(task["task"])
        start_dt = datetime.strptime(task["start"], "%d.%m.%Y %H:%M")
        end_dt = datetime.strptime(task["end"], "%d.%m.%Y %H:%M")
        start_num = mdates.date2num(start_dt)
        end_num = mdates.date2num(end_dt)
        width = end_num - start_num
        ax.barh(i, width, left=start_num, color="skyblue", edgecolor="grey", height=0.8)
    
    ax.set_yticks(range(len(task_labels)))
    ax.set_yticklabels(task_labels)
    ax.invert_yaxis()  # Invert y-axis for top-to-bottom task order
    
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y %H:%M"))
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Tasks")
    ax.set_title(f"Gantt Chart for {project_name}")
    
    export_type = simpledialog.askstring("Export Type", "Enter 'image' or 'pdf' to export:")
    if export_type == "image":
        fig.savefig(os.path.join(DATA_DIR, f"{project_name}_gantt_chart.png"))
        messagebox.showinfo("Success", f"Gantt chart saved as {project_name}_gantt_chart.png!")
    elif export_type == "pdf":
        fig.savefig(os.path.join(DATA_DIR, f"{project_name}_gantt_chart.pdf"))
        messagebox.showinfo("Success", f"Gantt chart saved as {project_name}_gantt_chart.pdf!")
    else:
        messagebox.showerror("Error", "Invalid export type! Please enter 'image' or 'pdf'.")

# Create the main GUI window
root = tk.Tk()
root.title("Gantt Chart Manager")
root.geometry("600x600")

# Project Listbox
project_listbox = tk.Listbox(root)
project_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Task Listbox
task_listbox = tk.Listbox(root)
task_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Load projects into the project listbox
for project in load_projects().keys():
    project_listbox.insert(tk.END, project)

# Buttons Frame
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_add_project = tk.Button(btn_frame, text="Add Project", command=add_project)
btn_add_project.pack(side=tk.LEFT, padx=5)

btn_delete_project = tk.Button(btn_frame, text="Delete Project", command=delete_project)
btn_delete_project.pack(side=tk.LEFT, padx=5)

btn_add_task = tk.Button(btn_frame, text="Add Task", command=add_task)
btn_add_task.pack(side=tk.LEFT, padx=5)

btn_delete_task = tk.Button(btn_frame, text="Delete Task", command=delete_task)
btn_delete_task.pack(side=tk.LEFT, padx=5)

btn_show_chart = tk.Button(btn_frame, text="Show Gantt Chart", command=show_gantt_chart)
btn_show_chart.pack(side=tk.LEFT, padx=5)

btn_export_chart = tk.Button(btn_frame, text="Export Chart", command=export_chart_as_image)
btn_export_chart.pack(side=tk.LEFT, padx=5)

# Update the task listbox when a project is selected.
def on_project_select(event):
    global current_project
    selected = project_listbox.curselection()
    if selected:
        current_project = project_listbox.get(selected[0])
        update_task_listbox(current_project)

project_listbox.bind("<<ListboxSelect>>", on_project_select)

# Run the GUI loop
root.mainloop()
