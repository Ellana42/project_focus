from os import system
from shutil import get_terminal_size


class Project:
    def __init__(self, name, due_date=None):
        self.name = name
        self.tasks = []
        self.due_date = due_date

    def create_task(self, content, due_date=None):
        self.tasks.append(Task(content, due_date))

    def remove_task_nb(self, nb_task):
        if nb_task < len(self.tasks):
            self.tasks.pop(nb_task)


class Task:
    def __init__(self, content, due_date):
        self.content = content
        self.due_date = due_date


class ProjectManager:
    def __init__(self, save=0):
        self.projects = {'Miscellaneous': Project('Miscellaneous')}
        self.project_in_focus = 'Miscellaneous'
        self.width = get_terminal_size()[0]

        self.running = True
        self.main_instructions = {'quit': Quit, 'create': CreateProject, 'add': AddTask,
                                  'shift focus to': ShiftFocus, 'mark as done': CrossOut, 'archive': Archive}

        self.save = save
        self.open_save()

        self.run()

    def open_save(self):
        pass

    def display_project(self):
        self.width = get_terminal_size()[0]
        system('clear')
        title = '[Project Focus]'
        print(self.center(title) + title)
        print(self.width * '_')
        print('[Projects]:' + ' \n')
        for project in self.projects.values():
            if project == self.project_in_focus:
                print('*[{}]'.format(project.name))
            else:
                print('[{}]'.format(project.name))
            for task in project.tasks:
                print('    ' + '• ' + task.content)

    def run(self):
        while self.running:
            self.display_project()
            self.interpret_command(input('- '))

    def interpret_command(self, command):
        command = command.split('\'')
        if len(command) > 1:
            command.pop()
        nb_args = len(command)
        instruction = command[0].rstrip().lstrip()
        main_arg = None
        if nb_args > 1:
            main_arg = command[1]
        decomposed_arguments = {
            command[i].rstrip().lstrip(): command[i + 1] for i in range(2, nb_args // 2 + 1)}
        self.main_instructions[instruction](
            self, main_arg, decomposed_arguments)

    def get_instructions(self):
        pass

    def make_save(self):
        pass

    def center(self, string):
        return (self.width - len(string)) // 2 * ' '

    def get_project_names(self):
        return {project.name: project for project in self.projects}


class Instruction:
    def __init__(self, manager, main_arg, arguments):
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
        task_content = self.main_arg
        if self.arguments is not None and 'to' in self.arguments:
            project_name = self.arguments['to']
        else:
            project_name = 'Miscellaneous'
        self.manager.projects[project_name].create_task(task_content)


class ShiftFocus(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()

    def execute(self):
        self.manager.project_in_focus = self.manager.projects[self.main_arg]


class CrossOut(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

        self.execute()

    def execute(self):
        if 'from' in self.arguments and self.arguments['from'] in self.manager.projects:
            project = self.manager.projects[self.arguments['from']]
        else:
            project = self.manager.projects['Miscellaneous']
        project.remove_task_nb(int(self.main_arg) - 1)


class Archive(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()

    def execute(self):
        if self.main_arg in self.manager.projects:
            del self.manager.projects[self.main_arg]


class Save(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)
        self.execute()


ProjectManager()
