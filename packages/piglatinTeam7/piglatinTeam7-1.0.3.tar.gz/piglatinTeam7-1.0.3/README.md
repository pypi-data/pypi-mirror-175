![example workflow](https://github.com/software-students-fall2022/python-package-exercise-project-3-team-7/actions/workflows/build.yaml/badge.svg)

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9126635&assignment_repo_type=AssignmentRepo)
# Python Package Exercise

A little exercise to create a Python package, build it, test it, distribute it, and use it. See [instructions](./instructions.md) for details.

## Group members
- [Maaz Ahmed](https://github.com/maazahmedd)
- [Hillary Davis](https://github.com/hillarydavis1)
- [Wuji Cao](https://github.com/cwj2099)
- [Ankit Jain](https://github.com/ankit181818)

# Functions in our package

> ## Our Pig Latin Translation Rules:
    Our rules for pig latin are as follows: take away the first letter of a word, then add a new word that uses the first letter of the word with "ay" added to it e.g., hello becomes ello-hay. For words that start with a vowel, you add "ay" to the end of the word e.g., enter becomes enter-ay, for words that start with a consonant, all letters are removed until a vowel is reached and then all removed consonants are used to create a second word, with "ay" added to the end of it e.g., happy becomes appy-hay

### toEnglish(string s):
This function **takes pig Latin words as input**. These words must be hyphenated at the end with their pig latin translation/addition in order for our system to be able to process them properly. As a result it returns **the english translation** to the user.

### toPl(string s, boolean intermediate_output_flag = True):
This function takes **an english word** as input and returns this word in **our pig latin translation** of it. In the case of an intermediate flag set to True (as is default) it will return the word in its hyphenated format. Otherwise it will return the word without hyphenation.

### process_input(string s, boolean translation_flag):
Function that takes in a **an input string and a flag corresponding to the type of translation** and returns a **parsed usable list**, depending on the type of translation needed. Also prints useful output for debugging / running.

When we call this function, we can make sure that it returns a non-empty list by checking the len().

### speech_bubble(string message):
**arguments:** one argument, message
**returns:** a string that is essentially ASCII art, with the message enclosed in a speech bubble

### arrow_to_bubble():
**no arguments**
**returns:** a string that represents ASCII art, pointing to the speech bubble

### print_pig():
**no_arguments**
**returns:** a string that represents ASCII art of a pig

### print_everything(message):
**arguments:** one argument, message
**returns:** a string that represents ASCII art, with a speech bubble enclosing the message, a pig and an arrow pointing from the pig to the speech bubble
<hr>

We believe that the functions most useful to potential users are (with their use shown in the [example file](example.py))
 - toEnglish
 - toPL
 - speech_bubble
 - print_pig
 - print_everything

[PYPI](https://test.pypi.org/project/piglatin/1.0.3/)
# How to install and use our package

- Create a pipenv-managed virtual environment and install the latest version of your package installed：https://test.pypi.org/project/piglatin/1.0.3/ (Note that if you've previously created a pipenv virtual environment in the same directory, you may have to delete the old one first. Find out where it is located with the pipenv --venv command.)
- Activate the virtual environment: pipenv shell.
- Create a Python program file that imports your package and uses it, e.g. from piglatin import pig and then print(pig.toPL("Hello World")).
- Run the program: python3 my_program_filename.py.
- Exit the virtual environment: exit.


# How to contribute in this package

- Clone the repo
- Install pipenv, build, and twine if not already installed.
- Add settings in pyproject.toml suitable for a setuptools-based build and add metadata fields to this file (our package do not requires any additional package apart from pytest for testing)
- Include your code in src/piglatin/pig.py
- Build the project by running python -m build from the same directory where the pyproject.toml file is located.
- Verify that the built .tar archive has the files you expect your package to have (including any important non-code files) by running the command: tar --list -f dist/piglatin-1.0.1.tar.gz, where piglatin-1.0.1 is replaced the new version.
- Create an account on TestPyPI where one can upload to a test repository instead of the production PyPI repo.
- Create a new API token on TestPyPI with the "Scope" set to “Entire account”. Save a copy of the token somewhere safe.
- Upload your package to the TestPyPI repository using twine, e.g. twine upload -r testpypi dist/*
- twine will output the URL of your package on the PyPI website - load that URL in your web browser to see your packaged published 

Every time you change the code in your package, you will need to rebuild and reupload it to PyPI. You will need to build from a clean slate and update the version number to achieve this:

- delete the autogenerated dist directory
- delete the autogenerated src/*.egg-info directory
- update the version number in pyproject.toml and anywhere else it is mentioned (do a find/replace)
- build the package again with python -m build
- upload the package again with twine upload -r testpypi dist/*

Repeat as many times as necessary until the package works as expected. Once complete, upload to the real PyPI instead of the TestPyPI repository.