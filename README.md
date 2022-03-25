# ics-to-text-converter-python
CLI App written in Python, that takes dates as an input and prints out events within those dates. The format for the CLI argument is referred to in the TESTS.md file. A call to tester4.py will use arguments like: `./tester4.py --start=2021/2/14 --end=2021/2/14 --file=one.ics | diff test01.txt -`. This would print the events between those dates. My app accounts for events that would repeat as well, formatting them and printing it out in a chronological order.
The program was written including user-defined classes and regular expressions.

In essence the program will:
• read text input from a file, line by line;
• implement required methods for the solution;
• extract substrings from lines produced when reading a file;
• return lists of strings corresponding to the format of the human-readable version of the calendar.
