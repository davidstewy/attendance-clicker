# Attendance Auto Clicker

One of the most annoying parts of taking attendance in classe is that you have to click a small square multiple times to cycle through attendance statuses. 

The purpose of this project is to create a python automation script that will allow you to press some key, or combination of keys while hovering the mouse over a neutral attendance status, the program will then preform the correct number of clicks to get you to the status symbol you are looking for. 

# Compatibility

This program has currently only been tested on MacOS Catalina, some modification of the code may be required if you are using a different operating system. I plan on making this work cross platform but I wanted to get this working as soon as possible to make taking attendance less of a burden.

When running this program on mac you must run it as sudo or mac wont allow the program to capture key presses. You will also be prompted to allow your terminal/vs code (depedning on where you run this program from) to be marked as an accessibility app, you must allow this in order for the program to work. 

# Getting started

I used [poetry](https://python-poetry.org/docs/) to create the virtual environment and install local dependencies. Once you have poetry installed and configured 

just run: `poetry install` 

then: `poetry shell` 

then: `python attendanceclicker.py`

This will start the script listening for specific hotkey presses, which will then click the mouse some number of times. At any time just press esc and the script will stop and will then need to be restarted.

# Configuration

## Creating hotkeys

In order to customize your preferred keyboard shortcuts you just need to edit the keyconfig.ini file, under the key combos section.

for example in the keyconfig.ini file as it stands in currently in the repo I have the keyboard shortcut for marking a student as Absent Excused set to:

```shift+alt+a=AE```

so you would hover over a neutral status symbol then hit (on mac alt is actually the option key) shift + option + a and the program would click until the status symbol says AE for you. the non-alphanumeric keys have specific words associated with them, these will be listed at the bottom of the readme.

The way to write these is basically 

```key_one+key_two+alphanumeric=status_symbol```

the status_symbol can be anything as long as it matches an entry in the status clicks section of the .ini file.

you dont necessarily need alphanumeric just putting something like:

```shift+alt=AE```

will work as well. You can also just use an alphanumeric key:

```a=AE```

this will allow you to just press the letter 'a' on the keyboard to cause the mouse to click the correct number of times. Be cautious using this, as if you are using search to look for a students name and they have a letter in it that you have assigned as a hotkey there could be some unintended consequences as this will still cause clicks.

## Configuring status symbol clicks

Inside the keyconfig.ini file there is also a section that is called status clicks.  Because each class may be configured differently and have different amounts and order of status symbols you can configure the number of times the mouse clicks for each status.

the format for this section is:
```status_symbol=number_of_clicks```

where status_symbol is whatever status you want to set a student, for example to mark a student as present you would click until the status symbol is `p`. For me the number of clicks from `n` you would click 5 times.

So for me I have in my keyconfig.ini:

```P=5```

this means that any of my key combos that have an `=P` at the end of it will cause my mouse to click 5 times.

# Non-AlphaNumeric Key Map

alt = any alt or option key (mac)

alt_r = right alt or option key (mac) exclusively

cmd = alt or command key (mac)

cmd_r = right alt or command key (mac) exclusively

ctrl = any control key

ctrl_r = right control key exclusively

shift = any shift key

shift_r = right shift key exclusively