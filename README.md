# cfgantt
A Gantt chart builder based on frappe.

## Basic usage

You write a plain text file and the app converts it to an HTML.

You define a task like this:

```
task: Write dissertation
date: 2023-6-1 2050-09-31
```

You can specify the task in any language.

Dates must be either YYYY-MM or YYYY-MM-DD (leading zeros are omittable).

If the day of the month is not given, the app assumes that the task is supposed to start on the first day of the month and end on the last. So instead of `date: 2023-06-01 2050-09-30`, you can save a few key strokes by writing `date: 2023-6 2050-9`.

You may also omit the second date, in which case the app assumes the task will take just one day (if you specify the day of the month) or an entire month (if you don't).

The `task: ...` line is how the app recognizes that a new task is being defined. So make sure it comes before the dates and other optional attributes discussed below.

## Progress and dependencies

You can indicate how much of a task has been completed using the `progress` attribute, which should be an integer between 0 and 100:

```
task: ...
progress: 80
```

You can also indicate that the completion of one task depends on the completion of others:

```
task: foundational task 1
date: ...
id: foundation 1

task: foundational task 2
date: ...
id: foundation 2

task: dependant task
date: ...
dependencies: foundation 1, foundation 2
```

You need to assign a unique id to every task on which other tasks depend (an id can be anything in any language that doesn't contain commas). Then for a task that's dependent on other tasks, you specify its dependencies as a comma-separated list of ids.

## Task Classification

You may group tasks into classes and assign them different colors. To define a class, begin a line with `define class:` followed by the name of the class and one or two colors, like this:

```
define class: research pink #ff0000
define class: writing yellowgreen
```

The first color is for the unfinished portion of tasks, while the second (if provided) is used for the finished portion. One color is enough if you don't need the distinction.

Class names can be in any language but they must not have space in them. `easy_peasy` is okay; `easy peasy` is not.

Colors can be named (see [HTML color names](https://www.w3schools.com/tags/ref_colornames.asp)) or specified using hex codes (`#ff0000` and the like).

Although not necessary, it makes sense to put class definitions at the beginning of your file. Once they are in place, you can start classifying your tasks:

```
task: Write dissertation
...
class: writing
```

If you defined your own classes, a legend will display at the top left of the chart showing the names of the classes and their associated colors.

## Title, Logo, etc.

These fields, if defined, will be shown at the top of the chart.

```
title: 
state label: 
state: 
goals label: 
goals: 
```

Play with them and see what they do.

If you put a file named `logo.svg` in the same directory as the app, the generated chart will automatically include the SVG logo at the top left corner.

