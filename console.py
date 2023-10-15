#!/bin/usr/python3
"""Module that contains the H Airbnb console."""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import re
from shlex import split


def parse(input_str):
    curly = re.search(r"\{(.*?)\}", input_str)
    square = re.search(r"\[(.*?)\]", input_str)

    if curly is None:
        if square is None:
            return [word.strip(",") for word in input_str.split()]
        else:
            words = input_str.split()[:square.span()[0]]
            result = [word.strip(",") for word in words]
            result.append(square.group())
            return result
    else:
        words = input_str.split()[:curly.span()[0]]
        result = [word.strip(",") for word in words]
        result.append(curly.group())
        return result


class HBNBCommand(cmd.Cmd):
    """Cls that contains the entry point of the command interpreter.

    Attributes:
        prompt (str): the interpreter prompt.
    """
    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing when receiving empty line"""
        pass

    def do_quit(self, arg):
        """Quit command line to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Creates from basemodel class and print cls ID.
        Usage: create <class>
        """
        parsed = parse(arg)
        if len(parsed) == 0:
            print("** class name missing **")
        elif parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(parsed[0])().id)
            storage.save()

    def do_show(self, arg):
        """Print the string representation of a class instance of a given id.
    Usage: show <class> <id> or <class>.show(<id>).
        """
        parsed = parse(arg)
        objects_dict = storage.all()
        if len(parsed) == 0:
            print("** class name missing **")
        elif parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parsed) == 1:
            print("** instance id missing **")
        elif f"{parsed[0]}.{parsed[1]}" not in objects_dict:
            print("** no instance found **")
        else:
            print(objects_dict[f"{parsed[0]}.{parsed[1]}"])

    def do_destroy(self, arg):
        """Delete a class instance of a given id.
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        """
        parsed = parse(arg)
        objdict = storage.all()
        if len(parsed) == 0:
            print("** class name missing **")
        elif parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(parsed) == 1:
            print("** instance id missing **")
        elif f"{parsed[0]}.{parsed[1]}" not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict[f"{parsed[0]}.{parsed[1]}"]
            storage.save()

    def do_all(self, arg):
        """Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects.
        Usage: all or all <class> or <class>.all()
        """
        parsed = parse(arg)
        if len(parsed) > 0 and parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_list = []
            for obj in storage.all().values():
                if len(parsed) > 0 and parsed[0] == obj.__class__.__name__:
                    obj_list.append(obj.__str__())
                elif len(parsed) == 0:
                    obj_list.append(obj.__str__())
            print(obj_list)

    def do_update(self, arg):
        """Updates a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary.
        Usage: update <class> <id> <attribute_name> <attribute_value> or
                <class>.update(<id>, <attribute_name>, <attribute_value>)
                or <class>.update(<id>, <dictionary>)
        """
        parsed = parse(arg)
        objdict = storage.all()

        if len(parsed) == 0:
            print("** class name missing **")
            return False
        if parsed[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(parsed) == 1:
            print("** instance id missing **")
            return False
        if f"{parsed[0]}.{parsed[1]}" not in objdict.keys():
            print("** no instance found **")
            return False
        if len(parsed) == 2:
            print("** attribute name missing **")
            return False
        if len(parsed) == 3:
            try:
                type(eval(parsed[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(parsed) == 4:
            obj = objdict[f"{parsed[0]}.{parsed[1]}"]
            if parsed[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[parsed[2]])
                obj.__dict__[parsed[2]] = valtype(parsed[3])
            else:
                obj.__dict__[parsed[2]] = parsed[3]
        elif type(eval(parsed[2])) == dict:
            obj = objdict[f"{parsed[0]}.{parsed[1]}"]
            for key, val in eval(parsed[2]).items():
                if (key in obj.__class__.__dict__.keys() and
                        type(
                        obj.__class__.__dict__[key]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[key])
                    obj.__dict__[key] = valtype(val)
                else:
                    obj.__dict__[key] = val
        storage.save()

    def do_count(self, arg):
        """Retrieves the number of instances of a given class.
        Usage: count <class> or <class>.count()
        """
        parsed = parse(arg)
        count = 0
        for obj in storage.all().values():
            if parsed[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r".", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"((.?))", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = f"{argl[0]} {command[1]}"
                    return argdict[command[0]](call)
        print(f"** Unknown syntax: {arg}")
        return False


if __name__ == "__main__":
    HBNBCommand().cmdloop()
