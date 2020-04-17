from os import system
from project import Project
import pickle


class Instruction:
    def __init__(self, manager, main_arg=None, arguments={}):
        self.manager = manager
        self.main_arg = main_arg
        self.arguments = arguments
        self.execute()

    def is_int(self):
        try:
            int(self.main_arg)
            return True
        except ValueError:
            return False


class Quit(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        EmptyDone(self.manager)
        Save(self.manager)
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
        if type(self.main_arg) is str:
            self.manager.projects[self.main_arg] = Project(self.main_arg)
            self.manager.last_opened.insert(0, self.main_arg)
            self.manager.generate_aliases()


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
            project = self.manager.aliases[self.main_arg]
            self.manager.project_in_focus = project
            self.manager.last_opened.remove(project)
            self.manager.last_opened.insert(0, project)


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
            self.manager.last_opened.remove(
                self.manager.aliases[self.main_arg])
            self.manager.generate_aliases()


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

        shortcut_save = open('shortcuts.pickle', 'wb')
        pickle.dump(self.manager.instructions, shortcut_save)
        shortcut_save.close()

        settings = open('settings.pickle', 'wb')
        pickle.dump(self.manager.settings, settings)
        settings.close()

        last_opened_save = open('last_opened.pickle', 'wb')
        pickle.dump(self.manager.last_opened, last_opened_save)
        last_opened_save.close()


class FocusTask(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        project = self.manager.projects[self.manager.project_in_focus]
        if self.main_arg in ['none', 'None', 'nothing']:
            project.stop_focusing()
        elif self.main_arg is not None:
            project.focus_on_task(self.main_arg)
        else:
            project.focus_on_task('1')


class UnfocusTasks(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        project = self.manager.projects[self.manager.project_in_focus]
        project.stop_focusing()


class AddShortcut(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        instructions = self.manager.instructions
        old_command = self.main_arg
        alias = self.arguments.get('as')
        if old_command in instructions and type(alias) is str:
            command = instructions[old_command]
            self.manager.instructions[alias] = command


class DeleteShortcut(Instruction):
    def __init__(self, manager, main_arg, arguments):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        alias_to_delete = self.main_arg
        confirmation = input(
            'Are you sure you want to delete {} ? \n- '.format(alias_to_delete))
        if confirmation in ['yes', 'y', ' ']:
            self.manager.instructions.pop(alias_to_delete)


class DisplayShortcuts(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        instruction_list = self.manager.instructions
        for alias, command in instruction_list.items():
            description = command
            print('{}: {}'.format(alias, description))
        input('Press enter when done reading ')


class Due(Instruction):
    def __init__(self, manager, main_arg, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        project = self.manager.projects[self.manager.project_in_focus]
        date = self.main_arg
        project.due_date = date


class ToggleDue(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        self.manager.settings.toggle_due = not self.manager.settings.toggle_due


class RenameProject(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        if self.main_arg is None:
            project_name = self.manager.project_in_focus
        else:
            project_name = self.manager.aliases[self.main_arg]

        project = self.manager.projects.pop(project_name)
        new_name = input(
            'What to you want to change {}\'s name to ? \n- '.format(project_name))
        if new_name in ['', ' ']:
            self.manager.projects[project_name] = project
            project.name = project_name
        else:
            self.manager.projects[new_name] = project
            project.name = new_name
            self.manager.last_opened[self.manager.last_opened.index(
                project_name)] = new_name
            self.manager.generate_aliases()


class DisplayProjects(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        for project in self.manager.projects.items():
            print(project)
        input('Press enter when done reading ')


class NbDisplayed(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        if self.main_arg == 'all':
            self.manager.settings.other_lenght = 1000
        else:
            previous_lenght = self.manager.settings.other_lenght
            self.manager.settings.other_lenght = int(
                self.main_arg) if self.is_int() else previous_lenght


class DefaultSettings(Instruction):
    def __init__(self, manager, main_arg=None, arguments={}):
        super().__init__(manager, main_arg, arguments)

    def execute(self):
        confirmation = input(
            'Are you sure ? This will reset all your settings \n- ')
        if confirmation in ['yes', 'y', ' ']:
            self.manager.settings.default_settings()
