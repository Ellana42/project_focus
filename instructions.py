from os import system
from project import Project
import pickle


class Instruction:
    def __init__(self, manager, main_arg=None, arguments={}):
        self.manager = manager
        self.main_arg = main_arg
        self.arguments = arguments
        self.execute()


class Quit(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        EmptyDone(self.manager)
        system('clear')
        self.manager.running = False


class EmptyDone(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        for project in self.manager.projects.values():
            project.done_tasks = []


class CreateProject(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        self.manager.projects[self.main_arg] = Project(self.main_arg)


class AddTask(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        args = self.arguments
        if self.main_arg is not None:
            task_content = self.main_arg
            if args is not None and 'to' in args and args['to'] in self.manager.aliases:
                project_name = self.manager.aliases[args['to']]
            else:
                project_name = self.manager.project_in_focus
            self.manager.projects[project_name].create_task(task_content)


class ShiftFocus(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        if self.main_arg in self.manager.aliases:
            self.manager.project_in_focus = self.manager.aliases[self.main_arg]


class Delete(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        if 'from' in self.arguments and self.arguments['from'] in self.manager.aliases:
            project = self.manager.projects[self.manager.aliases[self.arguments['from']]]
        else:
            project = self.manager.projects[self.manager.project_in_focus]
        if self.main_arg is None:
            project.remove_task_nb(0)
        else:
            for i in reversed(sorted(list(self.main_arg))):
                project.remove_task_nb(int(i) - 1)


class CrossOut(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        if 'from' in self.arguments and self.arguments['from'] in self.manager.aliases:
            project = self.manager.projects[self.manager.aliases[self.arguments['from']]]
        else:
            project = self.manager.projects[self.manager.project_in_focus]
        if self.main_arg is None:
            project.mark_as_done(0)
        else:
            for i in reversed(sorted(list(self.main_arg))):
                project.mark_as_done(int(i) - 1)


class Archive(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        if self.main_arg in self.manager.aliases:
            del self.manager.projects[self.manager.aliases[self.main_arg]]


class Save(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        save = open('save.pickle', 'wb')
        pickle.dump(self.manager.projects, save)
        save.close()

        save_focus = open('focus.pickle', 'wb')
        pickle.dump(self.manager.project_in_focus, save_focus)
        save_focus.close()


class FocusTask(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        project = self.manager.projects[self.manager.project_in_focus]
        if self.main_arg is not None:
            project.focus_on_task(self.main_arg)
        else:
            project.focus_on_task('1')