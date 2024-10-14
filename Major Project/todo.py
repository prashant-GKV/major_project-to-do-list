import json
import tkinter as tk
from tkinter import messagebox

# Task class to represent a task
class Task:
    def __init__(self, title, description, category):
        self.title = title
        self.description = description
        self.category = category
        self.completed = False

    def mark_completed(self):
        self.completed = True

# Function to save tasks to a JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f, indent=4)

# Function to load tasks from a JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            return [Task(**data) for data in json.load(f)]
    except FileNotFoundError:
        return []

# GUI Application
class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List")

        # Task list loaded from file
        self.tasks = load_tasks()

        # Task List Display
        self.task_listbox = tk.Listbox(root, height=10, width=50)
        self.task_listbox.grid(row=0, column=0, columnspan=4)

        self.update_task_listbox()

        # Buttons
        tk.Button(root, text="Add Task", command=self.add_task_popup).grid(row=1, column=0)
        tk.Button(root, text="Mark Completed", command=self.mark_task_completed).grid(row=1, column=1)
        tk.Button(root, text="Delete Task", command=self.delete_task).grid(row=1, column=2)
        tk.Button(root, text="Save & Exit", command=self.save_and_exit).grid(row=1, column=3)

    def update_task_listbox(self):
        """Updates the task listbox with the current tasks."""
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.tasks, start=1):
            status = "✓" if task.completed else "✗"
            task_info = f"{idx}. {task.title} [{task.category}] - {status}"
            self.task_listbox.insert(tk.END, task_info)

    def add_task_popup(self):
        """Popup window to add a new task."""
        popup = tk.Toplevel(self.root)
        popup.title("Add Task")

        tk.Label(popup, text="Title:").grid(row=0, column=0)
        title_entry = tk.Entry(popup)
        title_entry.grid(row=0, column=1)

        tk.Label(popup, text="Description:").grid(row=1, column=0)
        description_entry = tk.Entry(popup)
        description_entry.grid(row=1, column=1)

        tk.Label(popup, text="Category:").grid(row=2, column=0)
        category_entry = tk.Entry(popup)
        category_entry.grid(row=2, column=1)

        def save_task():
            title = title_entry.get()
            description = description_entry.get()
            category = category_entry.get()
            if title and description and category:
                new_task = Task(title, description, category)
                self.tasks.append(new_task)
                self.update_task_listbox()
                popup.destroy()
            else:
                messagebox.showwarning("Input Error", "All fields must be filled out")

        tk.Button(popup, text="Save", command=save_task).grid(row=3, column=1)

    def mark_task_completed(self):
        """Marks the selected task as completed."""
        selected = self.task_listbox.curselection()
        if selected:
            task_index = selected[0]
            self.tasks[task_index].mark_completed()
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected")

    def delete_task(self):
        """Deletes the selected task."""
        selected = self.task_listbox.curselection()
        if selected:
            task_index = selected[0]
            del self.tasks[task_index]
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "No task selected")

    def save_and_exit(self):
        """Saves tasks to the file and exits the application."""
        save_tasks(self.tasks)
        self.root.quit()

# Running the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
