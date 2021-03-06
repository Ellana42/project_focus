class Project:
    def __init__(self, name):
        self.name = name
        self.tasks = []
        self.due_date = ''
        self.task_in_focus = None
        self.done_tasks = []

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

    def mark_as_done(self, nb_task):
        if nb_task < len(self.tasks):
            task = self.tasks.pop(nb_task)
            self.done_tasks.append(task)
            if task == self.task_in_focus:
                self.task_in_focus = None

    def get_due_date(self):
        return self.due_date

    def stop_focusing(self):
        self.task_in_focus = None


class Task:
    def __init__(self, content, due_date):
        self.content = content
        self.due_date = due_date
