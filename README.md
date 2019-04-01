# bsed
Simple SQL-like syntax on top of Perl text processing. Designed to replace simple uses of sed/grep/AWK/Perl.


Bsed is a stream editor. In contrast to interactive text editors, stream editors process text in one go,
applying a command to an entire input stream or open file. 

Some example commands:

- `bsed contacts.csv delete lines containing 'myemail@website.com'`
- `bsed giant_malformatted.json replace '\'' with '\"' | bsed replace 'True' with 'true' | bsed replace 'False' with 
'false'` 
- `bsed file.txt append 'Yahoo' with '!'`
- `bsed file.py on lines 25 to 75 replace 'San Francisco' with 'San Diego'`
- `bsed file.py append lines containing 'deprecated_package' with '  # TODO: Update module'`

# Quick Start

1. Install bsed
    - `pip3 install --upgrade bsed`
2. Register bsed for autocompletion
    - `echo eval "$(register-python-argcomplete bsed)" >> ~/.bash_profile`

Open a new shell (or run `source ~/.bash_profile`). 
Run `bsed commands` for some common usages, and run `bsed help` for 
info on flag options.


# Motivation

**TLDR**: Most batch text processing tools are too complex for the very occasional user. bsed has simple, english 
syntax with bash autocomplete so that you don't have to go searching Stackoverflow each time you need sed/AWK/Perl.

Many common text transformations are fit for tools such as grep, sed, and AWK. These utilities allow for fast 
modification of text in one operation (as opposed to interactive text editors). Being command line tools, they also 
allow for piping of outputs into subsequent commands. Finally, they are common default software on many systems, 
making them easy to rely on and good subjects for to find support/help.
 
 Some usage examples include:
  - Getting lines from a file containing a word
  - Find-and-replace
  - Deleting, replacing, or clearing lines containing a regex pattern match
  - Placing text at beginning or end of certain lines
  - Getting a range of line numbers

## Problems with grep/sed/AWK

1. People don't know which tool to use
2. Varying levels of regex support
3. Varying levels of efficiency

## Enter Perl

Perl solves these issues–in theory–by providing a one-stop shop for all of these uses. 
Perl one-liners provide the set of functionality containing grep, sed, and AWK use cases, and have syntax designed to
 mimic that of sed. Furthermore, Perl includes advanced regex support and is for many cases more efficient than any of 
 its counterparts. 

Perl one-lines can be executed at the command line like the other text utilities. Finally, Perl also is commonly 
installed by default on popular operating systems. In conclusion, Perl is functionally the best general choice for 
stream editing.

## Why not use Perl?

In practice, few people know sed well enough to fire off commands from memory. For the casual or infrequent user, 
usually the path to success is to search stackoverflow.com for a quick sed command they can parse and tweak for their purposes. 

Even fewer people know Perl, as the syntax proves to be even more daunting and difficult to remember than sed. 

For example, a user may wish to perform a find-and-replace, replace "Jack" with "Jill".

AWK: `awk '{gsub(/Jack/,"Jill")}' file.txt`

Sed: `sed -i 's/Jack/Jill/g' file.txt`

Perl: `perl -p -i -e 's/Jack/Jill/g' file.txt` 

None of these is particularly intuitive, and the details of the syntax are complex even for the simplest of commands. To the beginning user, none of the following is obvious:

- What is the difference between {} and () in the AWK command?
- What is `-i` in sed? What are the `s` or the `g` for? 
- Why single quotes as opposed to double quotes? Are these interchangeable?
- What are those flags in Perl?

As a point of contrast, consider the structure of SQL:

`SELECT email FROM User WHERE country='Argentina';`

You don't need to know SQL to be able to understand the purpose of the command. Because of its intuitive syntax, a day's usage of SQL is sufficient to recall the basics for years.

## For the average user

The most common use case is a one-off command they need to transform a single file. Because of this, the learning 
curve of understanding Perl (or sed for that matter) is often not worth the upfront time investment.

## Use bsed for basic tasks

To solve this, bsed implements many common command types in an understandable English syntax designed to be as usable
 as SQL. Some examples of uses:
 
 `bsed file.txt select lines 0 to 50`
 
 - Print first 50 lines, indexed from zero.
 
 `bsed file.py clear lines starting with '\s*#'`
 
 - Replace comments in a python file with blank lines
 
 `bsed file.csv delete lines containing 'Andrew Johnson'` 
 
 - Remove any records with this person's name in the CSV
 
 `bsed performance_review.txt wrap 'Employee of the Month' with '\"'`
 
 - Puts the phrase "Employee of the Month" in quotes
 
 `bsed data.csv on lines 0 to 2000 select lines containing 'San Diego'`
 
 - Finds records on the first 2000 lines referencing the city. Good for quick exploration of very large files.
 
 `bsed customer_info.txt replace 'Jim Johnson' with 'John Johnson' | bsed replace 'jimjohnson@gmail.com' with 
 'johnjohnson@gmail.com'`
 
 - Fix a mistaken first name. Notice commands are chained together with `|`.
 
 ## Use the -t flag to learn or debug
 
 Any command can be executed with the -t flag and the command translation will be printed. 
 
 This is nice to debug 
 regex, build up  more complex queries, or just learn some Perl through examples. Without having to remember Perl from 
 scratch, you can get a quick command structure and then modify it or build on it. 
 
