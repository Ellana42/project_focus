from os import system
from shutil import get_terminal_size
import pickle
from instructions import *
from project import Project, Task


class ProjectManager:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

    def __init__(self, save=0):
        self.projects = {}
        self.project_in_focus = 'Miscellaneous'
        self.width = get_terminal_size()[0]
        self.col_width = (self.width - 2) // 3

        self.running = True
        self.main_instructions = {'quit': Quit, 'create': CreateProject, 'add': AddTask,
                                  'shift focus to': ShiftFocus, 'mark as done': CrossOut,
                                  'archive': Archive, 'save': Save, 'done': CrossOut,
                                  'shift to': ShiftFocus, 'focus on': FocusTask}

        self.open_save()
        self.run()

    def open_save(self):
        open_save = open('save.pickle', 'rb')
        self.projects = pickle.load(open_save)
        open_save.close()

        focus_save = open('focus.pickle', 'rb')
        self.project_in_focus = pickle.load(focus_save)
        focus_save.close()

    def display_project(self):
        system('clear')
        print()
        focused_project = self.projects[self.project_in_focus]
        other_projects = [
            project for project in self.projects.values() if project.name != self.project_in_focus]
        print(' ' + '[' + focused_project.name + ']' + '\n \n')
        for task in focused_project.tasks:
            if task == focused_project.task_in_focus:
                print(self.BOLD + '     ' + '• ' +
                      task.content + '\n' + self.END)
            else:
                print('     ' + '• ' + task.content + '\n')

        print('\nOther projects: \n')
        for project in other_projects:
            print(' - ' + project.name)
        print('\n\n')

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
        if instruction in self.main_instructions:

            main_arg = None
            if nb_args > 1:
                main_arg = command[1]
            decomposed_arguments = {
                command[i].rstrip().lstrip(): command[i + 1] for i in range(2, nb_args // 2 + 1)}

            self.main_instructions[instruction](
                self, main_arg, decomposed_arguments)

    def center(self, string):
        return (self.width - len(string)) // 2 * ' '

    def reinitialize_projects(self):
        self.project_in_focus = 'Miscellaneous'
        new_project_file = {}
        for project in self.projects.values():
            tasks = project.tasks
            new_project = Project(project.name)
            new_project.tasks = tasks
            new_project_file[project.name] = new_project
        self.projects = new_project_file


ProjectManager()
