import argparse
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

try:
    from lib.models import Task, User
except ModuleNotFoundError:
    from models import Task, User

users = {}


def add_task(args):
    user_name = args.user.strip()
    title = args.title.strip()

    if not user_name or not title:
        print("❌ User name and task title cannot be empty.")
        return

    user = users.get(user_name)
    if user is None:
        user = User(user_name)
        users[user_name] = user

    task = Task(title)
    user.add_task(task)


def complete_task(args):
    user_name = args.user.strip()
    title = args.title.strip()

    if not user_name or not title:
        print("❌ User name and task title cannot be empty.")
        return

    user = users.get(user_name)
    if user is None:
        print("❌ User not found.")
        return

    task = user.get_task_by_title(title)
    if task is None:
        print("❌ Task not found.")
        return

    task.complete()


def main():
    parser = argparse.ArgumentParser(description="Task Manager CLI")
    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add-task", help="Add a task for a user")
    add_parser.add_argument("user")
    add_parser.add_argument("title")
    add_parser.set_defaults(func=add_task)

    complete_parser = subparsers.add_parser("complete-task", help="Complete a user's task")
    complete_parser.add_argument("user")
    complete_parser.add_argument("title")
    complete_parser.set_defaults(func=complete_task)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
