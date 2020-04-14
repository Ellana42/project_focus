class Project:
    def __init__(self, name, due_date=None):
        self.name = name
        self.tasks = []
        self.due_date = due_date
        self.task_in_focus = None

    def create_task(self, content, due_date=None):
        self.tasks.append(Task(content, due_date))

    def remove_task_nb(self, nb_task):
        if nb_task < len(self.tasks):
            if self.tasks.pop(nb_task) == self.task_in_focus:
                self.task_in_focus = None

    def focus_on_task(self, nb_task):
        if int(nb_task) - 1 < len(self.tasks):
            self.task_in_focus = self.tasks[int(nb_task) - 1]

    def focus_on_no_task(self):
        self.task_in_focus = None


class Task:
    def __init__(self, content, due_date):
        self.content = content
        self.due_date = due_date
