import os  # Provides a way of using operating system dependent functionality (e.g., file paths)
import json  # Used for encoding and decoding JSON data (to save and load projects)
import tkinter as tk  # Imports the Tkinter GUI library and gives it the alias 'tk'
from tkinter import messagebox, simpledialog  # Imports specific Tkinter modules for popup messages and dialogs
from tkcalendar import Calendar, DateEntry  # Imports calendar widgets to allow date selection in the GUI
from datetime import datetime  # Provides classes for manipulating dates and times
import matplotlib.pyplot as plt  # Imports Matplotlib's pyplot module for plotting graphs
import matplotlib.dates as mdates  # Provides functions to handle dates on Matplotlib plots

# Define the path for JSON storage.
# BASE_DIR is set to the parent directory of the directory containing this file.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# DATA_DIR is a subdirectory named "data" within BASE_DIR.
DATA_DIR = os.path.join(BASE_DIR, "data")
# DATA_FILE is the full path to the JSON file that will store project data.
DATA_FILE = os.path.join(DATA_DIR, "projects.json")

# Ensure that the data directory exists; if it doesn't, create it.
os.makedirs(DATA_DIR, exist_ok=True)

# Global variable to store the currently selected project name.
current_project = None

# Function to load projects from the JSON file.
def load_projects():
    try:
        # Open the JSON file in read mode.
        with open(DATA_FILE, "r") as file:
            # Parse and return the JSON data as a Python dictionary.
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        # If the file doesn't exist or contains invalid JSON, return an empty dictionary.
        return {}

# Function to save the projects dictionary to the JSON file.
def save_projects(projects):
    # Open the JSON file in write mode.
    with open(DATA_FILE, "w") as file:
        # Write the projects dictionary to the file in JSON format with indentation for readability.
        json.dump(projects, file, indent=4)

# Function to add a new project.
def add_project():
    # Prompt the user to enter a project name.
    project_name = simpledialog.askstring("New Project", "Enter project name:")
    if project_name:
        # Load existing projects.
        projects = load_projects()
        if project_name in projects:
            # Warn the user if the project already exists.
            messagebox.showwarning("Warning", "Project already exists!")
        else:
            # Create a new project entry with an empty task list.
            projects[project_name] = []
            # Save the updated projects dictionary.
            save_projects(projects)
            # Add the new project to the project listbox in the GUI.
            project_listbox.insert(tk.END, project_name)
            # Inform the user that the project was added successfully.
            messagebox.showinfo("Success", f"Project '{project_name}' added!")

# Function to delete a selected project.
def delete_project():
    global current_project  # Declare that we will modify the global current_project variable.
    # Get the currently selected project index from the project listbox.
    selected = project_listbox.curselection()
    if not selected:
        # Warn the user if no project is selected.
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    # Retrieve the project name from the selected listbox item.
    project_name = project_listbox.get(selected[0])
    # Load the current projects.
    projects = load_projects()

    # Ask the user to confirm deletion of the project.
    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete the project '{project_name}'?")
    if confirm:
        # Remove the project from the dictionary.
        del projects[project_name]
        # Save the updated projects data.
        save_projects(projects)
        # Remove the project from the listbox.
        project_listbox.delete(selected[0])
        # If the deleted project was the current one, reset current_project.
        if current_project == project_name:
            current_project = None
        # Inform the user that the project was deleted.
        messagebox.showinfo("Success", f"Project '{project_name}' deleted!")

# Function to add a task to the selected project.
def add_task():
    global current_project  # Use the global current_project variable.
    if not current_project:
        # Warn the user if no project is selected.
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project  # Get the name of the current project.
    # Ask the user to enter a task name.
    task_name = simpledialog.askstring("New Task", "Enter task name:")

    # Helper function to retrieve and format the datetime from date and time inputs.
    def get_datetime_input(date_entry, time_entry):
        # Get the date from the DateEntry widget.
        date_input = date_entry.get_date()
        # Get the time from the Entry widget (expected in HH:MM format).
        time_input = time_entry.get()
        # Return the formatted date and time as a string.
        return f"{date_input.strftime('%d.%m.%Y')} {time_input}"

    # Function to handle the submission of a new task.
    def submit_task():
        # Retrieve and format the start and end datetime strings.
        start_datetime = get_datetime_input(start_date_entry, start_time_entry)
        end_datetime = get_datetime_input(end_date_entry, end_time_entry)

        # Load the current projects data.
        projects = load_projects()
        # Append the new task (with its name, start, and end times) to the current project.
        projects[project_name].append({
            "task": task_name, 
            "start": start_datetime, 
            "end": end_datetime
        })
        # Save the updated projects data.
        save_projects(projects)
        # Refresh the task listbox to include the new task.
        update_task_listbox(project_name)
        # Inform the user that the task was added successfully.
        messagebox.showinfo("Success", f"Task '{task_name}' added to '{project_name}'!")

    # Create a new window (dialog) for entering task details.
    dialog = tk.Toplevel(root)
    dialog.title("Enter Task Start and End Date/Time")

    # --- Start Date and Time Widgets ---
    tk.Label(dialog, text="Select Start Date and Time").pack(pady=5)
    start_date_entry = DateEntry(dialog, date_pattern='dd.mm.yyyy')  # Date selector for start date.
    start_date_entry.pack(pady=5)
    tk.Label(dialog, text="Enter Start Time (HH:MM)").pack(pady=5)
    start_time_entry = tk.Entry(dialog)  # Entry widget for start time.
    start_time_entry.pack(pady=5)

    # --- End Date and Time Widgets ---
    tk.Label(dialog, text="Select End Date and Time").pack(pady=5)
    end_date_entry = DateEntry(dialog, date_pattern='dd.mm.yyyy')  # Date selector for end date.
    end_date_entry.pack(pady=5)
    tk.Label(dialog, text="Enter End Time (HH:MM)").pack(pady=5)
    end_time_entry = tk.Entry(dialog)  # Entry widget for end time.
    end_time_entry.pack(pady=5)

    # Button to submit the task details; it calls the submit_task function when clicked.
    btn_add_task = tk.Button(dialog, text="Submit Task", command=submit_task)
    btn_add_task.pack(pady=10)


def get_sorted_tasks(project_name):
    tasks = load_projects().get(project_name, [])
    return sorted(tasks, key=lambda task: datetime.strptime(task["start"], "%d.%m.%Y %H:%M"))



# Function to delete a selected task from the current project.
def delete_task():
    global current_project
    if not current_project:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project
    projects = load_projects()
    tasks = projects.get(project_name, [])
    sorted_tasks = sorted(tasks, key=lambda task: datetime.strptime(task["start"], "%d.%m.%Y %H:%M"))

    selected_task = task_listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Warning", "Please select a task to delete!")
        return

    selected_index = selected_task[0]
    task_data = sorted_tasks[selected_index]
    original_index = tasks.index(task_data)

    confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete:\n{task_data['task']}?")
    if confirm:
        tasks.pop(original_index)
        save_projects(projects)
        update_task_listbox(project_name)
        messagebox.showinfo("Success", f"Task '{task_data['task']}' deleted!")


# Function to edit an existing task in the current project.
def edit_task():
    global current_project
    if not current_project:
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project
    projects = load_projects()
    # Get the original unsorted tasks list.
    tasks = projects.get(project_name, [])
    # Create a sorted copy for display.
    sorted_tasks = sorted(tasks, key=lambda task: datetime.strptime(task["start"], "%d.%m.%Y %H:%M"))

    selected_task = task_listbox.curselection()
    if not selected_task:
        messagebox.showwarning("Warning", "Please select a task to edit!")
        return

    selected_index = selected_task[0]
    # Get the task data from the sorted list.
    task_data = sorted_tasks[selected_index]
    # Find its index in the original tasks list.
    original_index = tasks.index(task_data)

    # Convert the stored start and end datetime strings into datetime objects.
    start_dt = datetime.strptime(task_data["start"], "%d.%m.%Y %H:%M")
    end_dt = datetime.strptime(task_data["end"], "%d.%m.%Y %H:%M")

    dialog = tk.Toplevel(root)
    dialog.title("Edit Task")

    tk.Label(dialog, text="Task Name:").pack(pady=5)
    name_entry = tk.Entry(dialog)
    name_entry.insert(0, task_data["task"])
    name_entry.pack(pady=5)

    tk.Label(dialog, text="Select Start Date:").pack(pady=5)
    start_date_entry = DateEntry(dialog, date_pattern='dd.mm.yyyy')
    start_date_entry.set_date(start_dt)
    start_date_entry.pack(pady=5)

    tk.Label(dialog, text="Enter Start Time (HH:MM):").pack(pady=5)
    start_time_entry = tk.Entry(dialog)
    start_time_entry.insert(0, start_dt.strftime("%H:%M"))
    start_time_entry.pack(pady=5)

    tk.Label(dialog, text="Select End Date:").pack(pady=5)
    end_date_entry = DateEntry(dialog, date_pattern='dd.mm.yyyy')
    end_date_entry.set_date(end_dt)
    end_date_entry.pack(pady=5)

    tk.Label(dialog, text="Enter End Time (HH:MM):").pack(pady=5)
    end_time_entry = tk.Entry(dialog)
    end_time_entry.insert(0, end_dt.strftime("%H:%M"))
    end_time_entry.pack(pady=5)

    def submit_edit():
        new_name = name_entry.get()
        new_start_date = start_date_entry.get_date()
        new_start_time = start_time_entry.get()
        new_end_date = end_date_entry.get_date()
        new_end_time = end_time_entry.get()

        new_start_datetime = f"{new_start_date.strftime('%d.%m.%Y')} {new_start_time}"
        new_end_datetime = f"{new_end_date.strftime('%d.%m.%Y')} {new_end_time}"

        # Update the task in the original tasks list.
        tasks[original_index] = {
            "task": new_name,
            "start": new_start_datetime,
            "end": new_end_datetime
        }
        save_projects(projects)
        update_task_listbox(project_name)
        messagebox.showinfo("Success", f"Task '{new_name}' updated successfully!")
        dialog.destroy()

    tk.Button(dialog, text="Submit", command=submit_edit).pack(pady=10)


# Function to update the task listbox to show all tasks for a given project.
def update_task_listbox(project_name):
    sorted_tasks = get_sorted_tasks(project_name)
    task_listbox.delete(0, tk.END)
    for task in sorted_tasks:
        task_listbox.insert(tk.END, f"{task['task']} ({task['start']} - {task['end']})")


# Function to display a Gantt chart for the selected project using Matplotlib.
def show_gantt_chart():
    global current_project  # Use the global current_project variable.
    if not current_project:
        # Warn the user if no project is selected.
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project  # Get the current project name.
    projects = load_projects()  # Load the projects data.
    tasks = projects.get(project_name, [])  # Retrieve the tasks for the project.

    if not tasks:
        # Warn the user if the project has no tasks.
        messagebox.showwarning("Warning", "No tasks in this project!")
        return

    # Sort tasks by start datetime for plotting.
    tasks.sort(key=lambda task: datetime.strptime(task["start"], "%d.%m.%Y %H:%M"))
    
    # Create a new Matplotlib figure and axis for the Gantt chart.
    fig, ax = plt.subplots(figsize=(10, 6))
    task_labels = []  # List to store task names for labeling the y-axis.

    # Loop through the tasks and add a horizontal bar for each.
    for i, task in enumerate(tasks):
        task_labels.append(task["task"])
        # Convert the task's start and end strings into datetime objects.
        start_dt = datetime.strptime(task["start"], "%d.%m.%Y %H:%M")
        end_dt = datetime.strptime(task["end"], "%d.%m.%Y %H:%M")
        # Convert datetime objects to Matplotlib's numeric format.
        start_num = mdates.date2num(start_dt)
        end_num = mdates.date2num(end_dt)
        width = end_num - start_num  # Determine the duration of the task.
        # Plot a horizontal bar representing the task.
        ax.barh(i, width, left=start_num, color="skyblue", edgecolor="grey", height=0.8)

    # Set the y-axis ticks and labels based on the number of tasks.
    ax.set_yticks(range(len(task_labels)))
    ax.set_yticklabels(task_labels)
    # Invert the y-axis so that tasks are listed from top to bottom.
    ax.invert_yaxis()
    
    # Configure the x-axis to display dates and times.
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y %H:%M"))
    plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for clarity.
    plt.grid(axis="x", linestyle="--", alpha=0.7)  # Add gridlines to the x-axis.
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Tasks")
    ax.set_title(f"Gantt Chart for {project_name}")
    fig.tight_layout()  # Adjust layout to ensure everything fits without overlap.
    plt.show()  # Display the Gantt chart window.

# Function to export the Gantt chart as an image (PNG) or PDF file.
def export_chart_as_image():
    global current_project  # Use the global current_project variable.
    if not current_project:
        # Warn the user if no project is selected.
        messagebox.showwarning("Warning", "Please select a project first!")
        return

    project_name = current_project  # Get the current project name.
    projects = load_projects()  # Load the projects data.
    tasks = projects.get(project_name, [])  # Retrieve the tasks for the project.

    if not tasks:
        # Warn the user if there are no tasks to display.
        messagebox.showwarning("Warning", "No tasks in this project!")
        return

    # Create a new Matplotlib figure and axis for the chart.
    fig, ax = plt.subplots(figsize=(10, 6))
    task_labels = []  # List for task names.
    for i, task in enumerate(tasks):
        task_labels.append(task["task"])
        # Convert start and end times from strings to datetime objects.
        start_dt = datetime.strptime(task["start"], "%d.%m.%Y %H:%M")
        end_dt = datetime.strptime(task["end"], "%d.%m.%Y %H:%M")
        start_num = mdates.date2num(start_dt)
        end_num = mdates.date2num(end_dt)
        width = end_num - start_num  # Calculate task duration.
        # Plot a horizontal bar for the task.
        ax.barh(i, width, left=start_num, color="skyblue", edgecolor="grey", height=0.8)
    
    # Configure y-axis ticks and labels.
    ax.set_yticks(range(len(task_labels)))
    ax.set_yticklabels(task_labels)
    ax.invert_yaxis()  # Invert the y-axis for proper task order.
    
    # Configure x-axis to display dates.
    ax.xaxis_date()
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%Y %H:%M"))
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="x", linestyle="--", alpha=0.7)
    ax.set_xlabel("Date/Time")
    ax.set_ylabel("Tasks")
    ax.set_title(f"Gantt Chart for {project_name}")
    
    # Ask the user whether they want to export as an image or PDF.
    export_type = simpledialog.askstring("Export Type", "Enter 'image' or 'pdf' to export:")
    if export_type == "image":
        # Save the figure as a PNG image in the data directory.
        fig.savefig(os.path.join(DATA_DIR, f"{project_name}_gantt_chart.png"))
        messagebox.showinfo("Success", f"Gantt chart saved as {project_name}_gantt_chart.png!")
    elif export_type == "pdf":
        # Save the figure as a PDF file in the data directory.
        fig.savefig(os.path.join(DATA_DIR, f"{project_name}_gantt_chart.pdf"))
        messagebox.showinfo("Success", f"Gantt chart saved as {project_name}_gantt_chart.pdf!")
    else:
        # Inform the user if an invalid export type was entered.
        messagebox.showerror("Error", "Invalid export type! Please enter 'image' or 'pdf'.")

# ---------------------------
# Main GUI Setup and Widgets
# ---------------------------

# Create the main GUI window.
root = tk.Tk()
root.title("Gantt Chart Manager")  # Set the title of the window.
root.geometry("600x600")  # Set the window size to 600x600 pixels.

# Create a Listbox widget to display the list of projects.
project_listbox = tk.Listbox(root)
# Pack the project listbox into the window with padding and allow it to expand.
project_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Create a Listbox widget to display the tasks for the selected project.
task_listbox = tk.Listbox(root)
# Pack the task listbox into the window with padding and allow it to expand.
task_listbox.pack(pady=10, fill=tk.BOTH, expand=True)

# Load existing projects from the JSON file and add them to the project listbox.
for project in load_projects().keys():
    project_listbox.insert(tk.END, project)

# Create a Frame widget to hold all the buttons.
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

# Create and pack the "Add Project" button.
btn_add_project = tk.Button(btn_frame, text="Add Project", command=add_project)
btn_add_project.pack(side=tk.LEFT, padx=5)

# Create and pack the "Delete Project" button.
btn_delete_project = tk.Button(btn_frame, text="Delete Project", command=delete_project)
btn_delete_project.pack(side=tk.LEFT, padx=5)

# Create and pack the "Add Task" button.
btn_add_task = tk.Button(btn_frame, text="Add Task", command=add_task)
btn_add_task.pack(side=tk.LEFT, padx=5)

# Create and pack the "Delete Task" button.
btn_delete_task = tk.Button(btn_frame, text="Delete Task", command=delete_task)
btn_delete_task.pack(side=tk.LEFT, padx=5)

# Create and pack the "Edit Task" button.
btn_edit_task = tk.Button(btn_frame, text="Edit Task", command=edit_task)
btn_edit_task.pack(side=tk.LEFT, padx=5)

# Create and pack the "Show Gantt Chart" button.
btn_show_chart = tk.Button(btn_frame, text="Show Gantt Chart", command=show_gantt_chart)
btn_show_chart.pack(side=tk.LEFT, padx=5)

# Create and pack the "Export Chart" button.
btn_export_chart = tk.Button(btn_frame, text="Export Chart", command=export_chart_as_image)
btn_export_chart.pack(side=tk.LEFT, padx=5)

# Function to update tasks when a project is selected.
def on_project_select(event):
    global current_project  # Use the global current_project variable.
    # Get the selected project index.
    selected = project_listbox.curselection()
    if selected:
        # Update current_project with the selected project name.
        current_project = project_listbox.get(selected[0])
        # Refresh the task listbox to display tasks for the selected project.
        update_task_listbox(current_project)

# Bind the listbox selection event to the on_project_select function.
project_listbox.bind("<<ListboxSelect>>", on_project_select)

# Start the Tkinter event loop to run the GUI.
root.mainloop()
