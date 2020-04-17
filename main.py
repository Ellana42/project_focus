from project import Project, Task
from os import system
from shutil import get_terminal_size
import pickle
from instructions import *
from settings import Settings


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
        self.settings = Settings()
        self.instructions = {'quit': Quit, 'create': CreateProject, 'add': AddTask,
                             'shift focus to': ShiftFocus, 'mark as done': CrossOut,
                             'archive': Archive, 'focus on': FocusTask, 'delete': Delete,
                             'empty done': EmptyDone, 'alias': AddShortcut,
                             'delete alias': DeleteShortcut, 'show alias': DisplayShortcuts,
                             'due': Due, 'toggle due dates': ToggleDue, 'focus on nothing': UnfocusTasks,
                             'rename': RenameProject, 'display projects': DisplayProjects,
                             'projects displayed': NbDisplayed, 'reset settings': DefaultSettings}

        self.display_modes = {'display_project': self.display_project}

        self.last_opened = []
        self.open_save()
        self.reinitialize_queue()
        self.run()

    def run(self):
        while self.running:
            Save(self)
            display_mode = self.display_modes[self.settings.display_mode]
            display_mode()
            self.interpret_command(input('- '))

    def open_save(self):
        open_save = open('save.pickle', 'rb')
        self.projects = pickle.load(open_save)
        open_save.close()

        focus_save = open('focus.pickle', 'rb')
        self.project_in_focus = pickle.load(focus_save)
        focus_save.close()

        shortcut_save = open('shortcuts.pickle', 'rb')
        self.instructions.update(pickle.load(shortcut_save))
        shortcut_save.close()

        settings = open('settings.pickle', 'rb')
        self.settings = pickle.load(settings)
        settings.close()

        last_opened_save = open('last_opened.pickle', 'rb')
        self.last_opened = pickle.load(last_opened_save)
        last_opened_save.close()

        self.generate_aliases()

    def display_project(self):
        system('clear')
        print()
        focused_project = self.projects[self.project_in_focus]

        self.detailed_project(focused_project)

        print('\nOther projects: \n')
        projects_displayed = self.settings.other_lenght
        other_projects = [self.projects[project_name]
                          for project_name in self.last_opened[1:projects_displayed + 1]]
        self.project_list(other_projects)

    def interpret_command(self, command):
        command = command.split('\'')
        command = [argument.rstrip().lstrip()
                   for argument in command if argument not in ['', ' ']]

        nb_args = len(command)
        instruction = command[0] if nb_args > 0 else None
        main_arg = command[1] if nb_args > 1 else None

        if instruction in self.instructions:
            sub_args = {command[i]: command[i + 1]
                        for i in range(2, nb_args // 2 + 1)}

            self.instructions[instruction](
                self, main_arg, sub_args)

    def center(self, string):
        return (self.width - len(string)) // 2 * ' '

    def reinitialize_projects(self):
        self.project_in_focus = 'Miscellaneous'
        new_project_file = {}
        for project in self.projects.values():
            tasks = project.tasks
            new_project = Project(project.name)
            new_project.tasks = tasks
            new_project.due_date = project.due_date
            new_project_file[project.name] = new_project
        self.projects = new_project_file

    def reinitialize_queue(self):
        old_queue = self.last_opened
        new_queue = [
            project for project in old_queue if project in self.projects]
        missing_projects = [
            project for project in self.projects if project not in new_queue]
        new_queue.extend(missing_projects)
        self.last_opened = new_queue

    def generate_aliases(self):
        projects = self.projects
        alias_dict = {}

        for project in projects.values():
            project_alias = {
                alias: project.name for alias in self.create_aliases(project.name)}
            alias_dict.update(project_alias)

        self.aliases = alias_dict

    @classmethod
    def create_aliases(cls, project_name):
        short = project_name.lower()[0: 4]
        lowercase = project_name.lower()
        words = project_name.lower().split()
        first_word = words[0]
        initials = ''.join(word[0] for word in words)
        return [project_name, short, lowercase, first_word, initials]

    @classmethod
    def generate_pickle(cls, file_name, initial_content):
        new_file = open(file_name + '.pickle', 'wb')
        pickle.dump(initial_content, new_file)
        new_file.close()

    #------------- Displaying ----------------------

    def detailed_project(self, project):
        display_dates = self.settings.toggle_due
        if display_dates and project.due_date != '':
            print(' ' + '[' + project.name + ']' +
                  '  -  ' + project.get_due_date())
        else:
            print(' ' + '[' + project.name + ']')
        print('\n')
        for task in project.tasks:
            if task == project.task_in_focus:
                print(self.BOLD + '     ' + '• ' +
                      task.content + '\n' + self.END)
            else:
                print('     ' + '• ' + task.content + '\n')
        for task in project.done_tasks:
            print(self.CYAN + '     ' + '• ' +
                  task.content + '\n' + self.END)

    def project_list(self, project_list):
        display_dates = self.settings.toggle_due
        for project in project_list:
            if display_dates and project.due_date != '':
                print(' - ' + project.name +
                      ' ({})'.format(project.get_due_date()))
            else:
                print(' - ' + project.name)
        print('\n\n')


ProjectManager()
