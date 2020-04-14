from os import system
import pickle


class Instruction:
    def __init__(self, manager, main_arg=None, arguments={}):
        self.manager = manager
        self.main_arg = main_arg
        self.arguments = arguments
        self.mandatory_arguments = []

    def execute(self):
        pass


class Quit(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()

    def execute(self):
        confirmation = input('Do you want to save ? ')
        if confirmation in ['y', 'yes', 'Yes', '', ' ']:
            Save(self.manager)
        system('clear')
        self.manager.running = False


class CreateProject(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()

    def execute(self):
        self.manager.projects[self.main_arg] = Project(self.main_arg)


class AddTask(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

        self.execute()

    def execute(self):
        if self.main_arg is not None:
            task_content = self.main_arg
            if self.arguments is not None and 'to' in self.arguments:
                project_name = self.arguments['to']
            else:
                project_name = self.manager.project_in_focus
            self.manager.projects[project_name].create_task(task_content)


class ShiftFocus(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()

    def execute(self):
        if self.main_arg in self.manager.projects:
            self.manager.project_in_focus = self.main_arg


class CrossOut(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

        self.execute()

    def execute(self):
        if 'from' in self.arguments and self.arguments['from'] in self.manager.projects:
            project = self.manager.projects[self.arguments['from']]
        else:
            project = self.manager.projects[self.manager.project_in_focus]
        project.remove_task_nb(int(self.main_arg) - 1)


class Archive(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()

    def execute(self):
        if self.main_arg in self.manager.projects:
            del self.manager.projects[self.main_arg]


class Save(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)
        self.execute()

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
        self.execute()

    def execute(self):
        project = self.manager.projects[self.manager.project_in_focus]
        project.focus_on_task(self.main_arg)
