#!/usr/bin/python3
"""This module contain a class HBNBCommand(cmd.Cmd) whose instances are
command line interpreter.
"""
import cmd
from models import storage
import re


class HBNBCommand(cmd.Cmd):
    """Command interpreter class."""
    prompt = '(hbnb) '

    def do_quit(self, cmd_line):
        """Exit the console."""
        return True

    def help_quit(self):
        """Prints help documentation for quit."""
        print("Quit command to exit the program\n")

    def do_EOF(self, cmd_line):
        """Exit the console."""
        return True

    def emptyline(self):
        """This is called when no command is given- does nothing."""
        pass

    def do_create(self, cmd_line):
        """Create new instances of valid classes."""
        if not cmd_line:
            print("** class name missing **")
        elif cmd_line not in storage.cls_ref():
            print("** class doesn't exist **")
        else:
            new_obj = storage.cls_ref()[cmd_line]()
            new_obj.save()
            print(new_obj.id)

    def do_show(self, cmd_line):
        """Prints the string representation of an instance from its class name
        and id.
        """
        if not cmd_line:
            print("** class name missing **")
        else:
            cmd_line = cmd_line.split(' ')
            if cmd_line[0] not in storage.cls_ref():
                print("** class doesn't exist **")
            elif len(cmd_line) < 2:
                print("** instance id missing **")
            else:
                key = f"{cmd_line[0]}.{cmd_line[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    print(storage.all()[key])

    def do_destroy(self, cmd_line):
        """Deletes an instance based on its class name and id."""
        if not cmd_line:
            print("** class name missing **")
        else:
            cmd_line = cmd_line.split()
            if cmd_line[0] not in storage.cls_ref():
                print("** class doesn't exist **")
            elif len(cmd_line) < 2:
                print("** instance id missing **")
            else:
                key = f"{cmd_line[0]}.{cmd_line[1]}"
                if key not in storage.all():
                    print("** no instance found **")
                else:
                    del storage.all()[key]
                    storage.save()

    def do_all(self, cmd_line):
        """Print all string representation of all instances."""
        if not cmd_line:
            print([str(obj) for key, obj in storage.all().items()])
        elif cmd_line not in storage.cls_ref():
            print("** class doesn't exist **")
        else:
            print([str(obj) for key, obj in storage.all().items()
                   if type(obj).__name__ == cmd_line])

    def do_update(self, cmd_line):
        """Update an instance by add an attribute or updating its value."""

        regex = r'^(\S+)(?:\s(\S+)(?:\s(\S+)(?:\s((?:"[^"]*")|(?:(\S)+)))?)?)?'
        match_obj = re.search(regex, cmd_line)
        if not match_obj:
            print("** class name missing **")
            return
        cls_name = match_obj.group(1)
        uuid = match_obj.group(2)
        attr_name = match_obj.group(3)
        attr_val = match_obj.group(4)
        if cls_name not in storage.cls_ref():
            print("** class doesn't exist **")
        elif not uuid:
            print("** instance id missing **")
        else:
            key = f'{cls_name}.{uuid}'
            if key not in storage.all():
                print("** no instance found **")
            elif not attr_name:
                print("** attribute name missing **")
            elif not attr_val:
                print("** value missing **")
            else:
                attr_val = attr_val.replace('"', '')
                if attr_val.isdigit():
                    attr_val = int(attr_val)
                else:
                    try:
                        attr_val = float(attr_val)
                    except ValueError:
                        pass
                setattr(storage.all()[key], attr_name, attr_val)
                storage.save()

    def do_count(self, cmd_line):
        """Retrieve the number of instances of a class."""
        if not cmd_line:
            return self.default(cmd_line)
        count = 0
        objs_dict = storage.all()
        for k, v in objs_dict.items():
            cls_name, uuid = k.split('.')
            if cmd_line == cls_name:
                count += 1
        print(count)

    def precmd(self, input_line):
        """Capture and formart input line of the format
        <class name>.<method name>().
        """
        cls_ = r'([A-Z][A-Za-z]+)'
        do = r'([a-z]+)'
        uid = (r'(?:\"([0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}'
               r'-[89ab][0-9a-f]{3}-[0-9a-f]{12})\")')
        dic = r'(?:\{([^\{\}\)]+)\})'
        attr = r'("[a-z_]+")'
        vals = r'((?:[\d.]+)|(?:"[^"\)]+")|(?:\[[^\[\]\)]+\]))'
        regex = fr'^\s*{cls_}\.{do}\({uid}?,?\s?{dic}?{attr}?,?\s?{vals}?\)'
        match_obj = re.search(regex, input_line)
        if not match_obj:
            return input_line
        cls_name = match_obj.group(1)
        do_method = match_obj.group(2)
        obj_id = match_obj.group(3)
        dico = match_obj.group(4)
        key = match_obj.group(5)
        val = match_obj.group(6)
        cmd_line = f'{do_method} {cls_name}'
        if obj_id:
            cmd_line += f' {obj_id}'
        if key or val:
            if key:
                key = key.strip('"')
                key = key.strip("'")
                cmd_line += f' {key}'
            if val:
                cmd_line += f' {val}'
        elif dico:
            cmd_one = self.onecmd
            key_val_ls = dico.split(',')
            for key_val in key_val_ls:
                key, val = key_val.split(':')
                key = key.strip()
                key = key.strip('"')
                key = key.strip("'")
                val = val.strip()
                dup_cmd_line = cmd_line
                dup_cmd_line += f' {key} {val}'
                cmd_one(dup_cmd_line)
            return ""
        return cmd_line


if __name__ == '__main__':
    HBNBCommand().cmdloop()
