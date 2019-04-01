# bsed
Simple, english syntax on top of Perl text processing. Designed to replace simple uses of sed/grep/awk/perl.


Bsed is a stream editor. In contrast to interactive text editors, stream editors process text in one go and 
apply a command to an entire input stream or open file. 


# Quick Start

1. Install bsed
    - pip3 install --upgrade bsed
2. Install argcomplete
    - pip3 install argcomplete
3. Register bsed for autocompletion
    - echo eval "$(register-python-argcomplete bsed)" >> ~/.bash_profile

Open a new shell (or run `source ~/.bash_profile`), and run `bsed commands` for some common usages and `bsed help` for 
info on flag options.


# Motivation
Many common text transformations are fit for tools such as grep, sed, and awk. These utilities allow for fast 
modification of text in one operation (as opposed to interactive text editors). Being command line tools, they also 
allow for piping of outputs into subsequent commands. Finally, they are common default software on many systems, 
making them easy to rely on and good subjects for to find support/help.
 
 Some usage examples include:
  - Getting lines from a file containing a word
  - Find-and-replace
  - Deleting, replacing, or clearing lines containing a regex pattern match
  - Placing text at beginning or end of certain lines
  - Getting a range of line numbers

## Problems with grep/sed/awk

1. People don't know which tool to use
2. Varying levels of regex support
3. Varying levels of efficiency

## Enter Perl

Perl solves these issues–in theory–by providing a one-stop shop for all of these uses. 
Perl one-liners provide the set of functionality containing grep, sed, and awk use cases, and have syntax designed to
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

Awk: `awk '{gsub(/Jack/,"Jill")}' file.txt`

Sed: `sed -i 's/Jack/Jill/g' file.txt`

Perl: `perl -nl -e "s/{Jack}/{Jill}/g; print;" file.txt` 

None of these is particularly intuitive, and the details of the syntax are complex even for the simplest of commands.

As a point of contrast, consider the structure of SQL:

`SELECT email FROM User WHERE country='Argentina';`

You don't need to know SQL to be able to understand the purpose of the command. Likewise, a day's usage of SQL is 
sufficient to recall the basics for years.

## For the average user

The most common use case is a one-off command they need to clean up a single file. Because of this, the learning 
curve of understanding Perl (or sed for that matter) is often not worth the upfront investment.

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
 
 `bsed customer_info.txt replace "Jim Johnson" with "John Johnson" | replace "jimjohnson@gmail.com" with 
 "johnjohnson@gmail.com"`
 
 - Fix a mistaken first name
 
 ## Use the -t flag to learn or debug
 
 Any command can be executed and the command translation will be printed. This is good for debugging regex, build up 
 more complex queries, or just for learning. Without having to remember Perl from scratch, you can get a quick 
 command structure and then modify it or build on it. 
 
 For users wishing to dive into Perl, learning with examples can be done easily with the -t flag.
