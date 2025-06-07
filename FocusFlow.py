import random
import json
import os

# ----------- Constants -----------
MENU_OPTIONS = {
    'MAIN': [
        "🗂 Manage To-Do List",
        "📅 Weekly Planner", 
        "💬 Motivational Quote",
        "❌ Exit"
    ],
    'TODO': [
        "➕ Add Task",
        "✅ Mark Task as Complete", 
        "📄 View Tasks",
        "🗑️ Delete Task",
        "🔙 Back to Main Menu"
    ]
}

QUOTES = [
    "The journey of a thousand miles begins with one step.",
    "Push yourself, because no one else is going to do it for you.",
    "Don't worry, it's not as big and scary as it seems.",
    "You are not behind, you are right on time.",
    "We're where we meant to be and it's perfect",
    "Learn to rest, not to quit.",
    "The journey of growth is not linear.",
    "Every day may not be good, but there is something good in every day.",
    "Don't expect perfection at first, just start.",
    "Success is the sum of small efforts repeated daily.",
    "Remember that there is no need to be stressed. You are doing your best.",
    "When you arise in the morning think of what a privilege it is to be alive, to think, to enjoy, to love..."
]

# ----------- Data Storage -----------
todo_list = []
weekly_plan = {
    "Monday": [],
    "Tuesday": [],
    "Wednesday": [],
    "Thursday": [],
    "Friday": [],
    "Saturday": [],
    "Sunday": []
}

# ----------- Helper Functions -----------

def show_main_menu(name):
    # Show main menu
    print(f"\n📋 What would you like to do, {name}?")
    for i, option in enumerate(MENU_OPTIONS['MAIN'], 1):
        print(f"{i}. {option}")

def show_todo_menu():
    # Show To-Do menu
    print("\n\033[92m--- To-Do List Menu ---\033[0m")
    for i, option in enumerate(MENU_OPTIONS['TODO'], 1):
        print(f"{i}. {option}")

def get_valid_input(prompt, valid_range):
    # Get valid input from user
    while True:
        try:
            choice = int(input(prompt))
            if choice in valid_range:
                return choice
            else:
                print(f"❗ Please enter a number between {min(valid_range)} and {max(valid_range)}.")
        except ValueError:
            print("❗ Please enter a valid number.")

def manage_todo():
    # To-Do list management
    while True:
        show_todo_menu()
        choice = get_valid_input("👉 Enter your choice (1-5): ", range(1, 6))

        if choice == 1:  # Add Task
            task = input("📝 Enter a new task: ").strip()
            if task:
                todo_list.append({
                    "task": task, 
                    "completed": False
                })
                print("✅ Task added successfully!")
            else:
                print("❗ Task cannot be empty.")
                
        elif choice == 2:  # Mark Complete
            if not todo_list:
                print("\033[91m⚠️ No tasks to mark as complete.\033[0m")
                continue

            view_tasks()
            task_num = get_valid_input("Enter the task number to mark as complete: ", 
                                     range(1, len(todo_list) + 1))
            todo_list[task_num - 1]["completed"] = True
            print("✅ Task marked as complete!")
            
        elif choice == 3:  # View Tasks
            view_tasks()
            
        elif choice == 4:  # Delete Task
            if not todo_list:
                print("\033[91m⚠️ No tasks to delete.\033[0m")
                continue
                
            view_tasks()
            task_num = get_valid_input("Enter the task number to delete: ", 
                                     range(1, len(todo_list) + 1))
            deleted_task = todo_list.pop(task_num - 1)
            print(f"🗑️ Deleted task: {deleted_task['task']}")
            
        elif choice == 5:  # Back
            break

def view_tasks():
    # Display tasks
    print("\n📄 Your Tasks:")
    if not todo_list:
        print("⚠️ No tasks yet.")
        return
        
    # Show incomplete tasks first
    sorted_tasks = sorted(enumerate(todo_list), key=lambda x: x[1]["completed"])
    
    for original_index, task in sorted_tasks:
        status = "✅" if task["completed"] else "❌"
        print(f"{original_index + 1}. {status} {task['task']}")

def weekly_planner():
    # Weekly planner
    days = list(weekly_plan.keys())
    while True:
        print("\n📅 WEEKLY PLANNER:")
        for i, day in enumerate(days, 1):
            task_count = len(weekly_plan[day])
            print(f"{i}. {day} ({task_count} tasks)")
        
        print("8. Clear a Day's Tasks")
        print("9. Clear Entire Week's Tasks")
        print("10. View All Week")
        print("11. Back to Main Menu")
        
        choice = get_valid_input("Choose an option (1-11): ", range(1, 12))

        if 1 <= choice <= 7:  # Specific day
            day = days[choice - 1]
            manage_day_tasks(day)
            
        elif choice == 8:  # Clear day
            clear_day_tasks(days)
            
        elif choice == 9:  # Clear week
            clear_week_tasks(days)
            
        elif choice == 10:  # View all week
            view_all_week()
            
        elif choice == 11:  # Back
            break

def manage_day_tasks(day):
    # Daily task management
    while True:
        print(f"\n📝 {day}'s Plan:")
        if not weekly_plan[day]:
            print("No tasks yet.")
        else:
            for idx, task in enumerate(weekly_plan[day], 1):
                print(f"{idx}. {task}")
                
        print("\nOptions:")
        print("1. Add a task")
        print("2. Remove a task")
        print("3. Back to Weekly Planner Menu")
        
        sub_choice = get_valid_input("Choose an option (1-3): ", range(1, 4))

        if sub_choice == 1:  # Add task
            task = input("Enter your task: ").strip()
            if task:
                weekly_plan[day].append(task)
                print("✅ Task added!")
            else:
                print("❗ Task cannot be empty.")
                
        elif sub_choice == 2:  # Remove task
            if not weekly_plan[day]:
                print("⚠️ No tasks to remove.")
                continue
                
            task_num = get_valid_input("Enter task number to remove: ", 
                                     range(1, len(weekly_plan[day]) + 1))
            removed = weekly_plan[day].pop(task_num - 1)
            print(f"🗑️ Removed task: {removed}")
            
        elif sub_choice == 3:  # Back
            break

def clear_day_tasks(days):
    # Clear daily tasks
    print("Available days:", ", ".join(days))
    day_to_clear = input("Enter the day name to clear: ").strip().lower().capitalize()
    
    if day_to_clear in weekly_plan:
        if weekly_plan[day_to_clear]:
            confirm = input(f"Are you sure you want to clear all tasks for {day_to_clear}? (y/n): ")
            if confirm.lower() == "y":
                weekly_plan[day_to_clear] = []
                print(f"✅ All tasks cleared for {day_to_clear}.")
            else:
                print("❌ Clear operation canceled.")
        else:
            print(f"⚠️ {day_to_clear} already has no tasks.")
    else:
        print("❗ Invalid day name.")

def clear_week_tasks(days):
    # Clear weekly tasks
    confirm = input("Are you sure you want to clear all tasks for the entire week? (y/n): ")
    if confirm.lower() == "y":
        for day in days:
            weekly_plan[day] = []
        print("✅ All weekly tasks cleared!")
    else:
        print("❌ Clear all week canceled.")

def view_all_week():
    # Display entire week
    print("\n📅 FULL WEEK OVERVIEW:")
    print("=" * 50)
    for day, tasks in weekly_plan.items():
        print(f"\n📌 {day}:")
        if not tasks:
            print("  No tasks scheduled")
        else:
            for i, task in enumerate(tasks, 1):
                print(f"  {i}. {task}")
    print("=" * 50)

def show_motivation():
    # Show motivational quote
    print("\n💬 MOTIVATION:")
    print(f"✨ {random.choice(QUOTES)} ✨")

# ----------- Main Program -----------
def main():
    name = input("👋 Hi! I hope you are doing well 💞 What's your name? ").strip().capitalize()
    if not name:
        name = "Friend"
    
    print(f"\n🌟 Welcome to Your Productivity App, {name}! 🌟")

    while True:
        show_main_menu(name)
        choice = get_valid_input("👉 Enter your choice (1-4): ", range(1, 5))

        if choice == 1:  # To-Do List
            manage_todo()
            
        elif choice == 2:  # Weekly Planner
            weekly_planner()
            
        elif choice == 3:  # Motivation
            show_motivation()
            
        elif choice == 4:  # Exit
            print(f"👋 Goodbye, {name}! Take care 💌")
            break

# ----------- Run -----------
if __name__ == "__main__":
    main()