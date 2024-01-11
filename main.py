import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Task:
    def __init__(self, description, priority, due_date=None):
        self.description = description
        self.priority = priority
        self.completed = False
        self.created_at = datetime.now()
        self.due_date = due_date

    def mark_as_done(self):
        self.completed = True

class ToDoListApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")

        self.tasks = []
        self.load_tasks()  # Load tasks from file
        self.create_widgets()

    def create_widgets(self):
        # Task entry, priority entry, due date entry, and add button
        self.task_entry = tk.Entry(self.master, width=25)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.priority_label = tk.Label(self.master, text="Priority (High/Medium/Low):")
        self.priority_label.grid(row=0, column=1, padx=10, pady=10)

        self.priority_entry = tk.Entry(self.master, width=10)
        self.priority_entry.grid(row=0, column=2, padx=10, pady=10)

        self.due_date_label = tk.Label(self.master, text="Due Date (DD/MM/YYYY):")
        self.due_date_label.grid(row=0, column=3, padx=10, pady=10)

        self.due_date_entry = tk.Entry(self.master, width=12)
        self.due_date_entry.grid(row=0, column=4, padx=10, pady=10)

        self.add_button = tk.Button(self.master, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=5, padx=10, pady=10)

        # Task listbox
        self.task_listbox = tk.Listbox(self.master, width=50, height=10, selectmode=tk.SINGLE)
        self.task_listbox.grid(row=1, column=0, columnspan=6, padx=10, pady=10)

        # Buttons for marking as done and removing tasks
        self.done_button = tk.Button(self.master, text="Mark as Done", command=self.mark_as_done)
        self.done_button.grid(row=2, column=0, padx=10, pady=10)

        self.remove_button = tk.Button(self.master, text="Remove Task", command=self.remove_task)
        self.remove_button.grid(row=2, column=1, padx=10, pady=10)

        # Save button
        self.save_button = tk.Button(self.master, text="Save Tasks", command=self.save_tasks)
        self.save_button.grid(row=2, column=2, padx=10, pady=10)

    def add_task(self):
        task_description = self.task_entry.get()
        task_priority = self.priority_entry.get()
        task_due_date_str = self.due_date_entry.get()

        try:
            task_due_date = datetime.strptime(task_due_date_str, "%d/%m/%Y")
            
            if task_description and task_priority.lower() in ['high', 'medium', 'low'] and task_due_date > datetime.now():
                new_task = Task(task_description, task_priority.capitalize(), task_due_date)
                self.tasks.append(new_task)
                self.update_task_listbox()
                self.task_entry.delete(0, tk.END)
                self.priority_entry.delete(0, tk.END)
                self.due_date_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Warning", "Task description cannot be empty, priority must be High, Medium, or Low, and due date must be in the future.")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid date format. Please use DD/MM/YYYY.")

    def mark_as_done(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            self.tasks[task_index].mark_as_done()
            self.update_task_listbox()
        else:
            messagebox.showwarning("Warning", "Select a task to mark as done!")

    def remove_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task_index = selected_index[0]
            removed_task = self.tasks.pop(task_index)
            self.update_task_listbox()
            messagebox.showinfo("Task Removed", f'Task "{removed_task.description}" removed from the to-do list.')
        else:
            messagebox.showwarning("Warning", "Select a task to remove!")

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in sorted(self.tasks, key=lambda x: x.priority, reverse=True):
            status = "[Done]" if task.completed else "[Pending]"
            due_date_str = f"Due Date: {task.due_date.strftime('%d/%m/%Y')}" if task.due_date else ""
            self.task_listbox.insert(tk.END, f"{status} Priority: {task.priority} - {task.description} {due_date_str}")

    def save_tasks(self):
        try:
            timestamp = datetime.now().strftime("%d%m%Y_%H%M")
            filename = f"Todo_{timestamp}.txt"

            with open(filename, "w") as file:
                for task in self.tasks:
                    file.write(f"Task: {task.description}\n")
                    file.write(f"Completion: {task.completed}\n")
                    file.write(f"Due date: {task.due_date.strftime('%d/%m/%Y')}\n")
                    file.write(f"Priority: {task.priority}\n")
                    file.write(f"Created at: {task.created_at}\n")
                    file.write("\n")  # Separate tasks with a blank line

            messagebox.showinfo("Tasks Saved", f"Tasks saved to '{filename}'")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving tasks: {str(e)}")

    def load_tasks(self):
        try:
            self.tasks = []  # Clear existing tasks
            timestamp = datetime.now().strftime("%d%m%Y_%H%M")
            filename = f"Todo_{timestamp}.txt"

            with open(filename, "r") as file:
                task_lines = file.read().split('\n\n')  # Separate tasks with two newlines
                for task_str in task_lines:
                    lines = task_str.strip().split('\n')
                    if len(lines) >= 4:
                        description = lines[0].replace("Task: ", "")
                        completion = lines[1].replace("Completion: ", "").lower() == 'true'
                        due_date = lines[2].replace("Due date: ", "")
                        priority = lines[3].replace("Priority: ", "")
                        created_at = lines[4].replace("Created at: ", "")

                        new_task = Task(description, priority, due_date)
                        new_task.completed = completion
                        new_task.created_at = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S.%f")

                        self.tasks.append(new_task)
        except FileNotFoundError:
            pass  # Ignore

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoListApp(root)
    root.mainloop()
