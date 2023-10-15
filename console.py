#!/usr/bin/python3
import cmd
import re
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


class HBNBCommand(cmd.Cmd):
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program (EOF)."""
        return True

    def emptyline(self):
        """an empty line + ENTER shouldn’t execute anything"""
        pass

    def do_create(self, arg):
        if not arg:
            print("** class name missing **")
        if arg in globals():
            cls = globals()[arg]
            new_instance = cls()
            new_instance.save()
        else:
            print("** class doesn't exist **")

    def do_show(self, args):
        args = args.split()
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in globals():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            for key, value in storage.all().items():
                if value.to_dict()['id'] == args[1]:
                    print(value)
                    return
            print("** no instance found **")

    def do_destroy(self, args):
        args = args.split()
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in globals():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        else:
            for key, value in storage.all().items():
                if value.to_dict()['id'] == args[1]:
                    storage.all().pop(key)
                    storage.save()
                    return
            print("** no instance found **")

    def do_all(self, class_name):
        if class_name == "":
            print([str(value) for key, value in storage.all().items()])
        elif class_name not in globals():
            print("** class doesn't exist **")

        else:
            list = []
            for key, value in storage.all().items():
                if key.split(".")[0] == class_name:
                    list.append(str(value))
            print(list)

    def do_update(self, args):
        args = args.split()
        if len(args) < 1:
            print("** class name missing **")
        elif args[0] not in globals():
            print("** class doesn't exist **")
        elif len(args) < 2:
            print("** instance id missing **")
        elif len(args) < 3:
            print("** attribute name missing *")
        elif len(args) < 4:
            print("** value missing **")
        else:
            instance = "{}.{}".format(args[0], args[1])
            if instance in storage.all().keys():
                setattr(storage.all()[instance], args[2], args[3])
                storage.save()
            else:
                print("** no instance found **")

    def do_count(self, class_name):
        count = 0
        for key, value in storage.all().items():
            if key.split(".")[0] == class_name:
                count += 1
        print(count)

    def get_arg(self, arg):
        match = re.search(r'\("([^"]+)"\)', arg)
        if match:
            return match.group(1)
        else:
            return None

    def default(self, command):
        parts = command.split(".")
        class_name = parts[0]
        pattern = r'^(\w+)\.(\w+)\("([\w\s,-]*)"?\)$'
        match = re.match(pattern, command)
        id, method = None, None
        if match:
            id = match.group(3)
            method = match.group(2)
            str = "{} {}".format(class_name, id)
            arguments = re.split(r',\s*|\s*,', match.group(3))
            update_arguments = f'{class_name} {" ".join(arguments)}'
        if len(parts) == 2:
            if parts[1] == "all()":
                self.do_all(class_name)
            elif parts[1] == "count()":
                self.do_count(class_name)
            elif method == "show":
                self.do_show(str)
            elif method == "destroy":
                self.do_destroy(str)
            elif method == "update":
                self.do_update(update_arguments)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
