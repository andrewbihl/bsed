# bsed
Simple, english syntax on top of Perl text processing. Designed to replace simple uses of sed/grep/awk/perl.


Bsed is a stream editor. In contrast to interactive text editors, stream editors process text in one go and 
apply a command to an entire input stream or open file. 


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

# Problems with grep/sed/awk

1. People don't know which tool to use
2. Varying levels of regex support
3. Varying levels of efficiency

# Enter Perl

Perl solves these issues–in theory–by providing a one-stop shop for all of these uses. 
Perl one-liners provide the set of functionality containing grep, sed, and awk use cases, and have syntax designed to
 mimic that of sed. Furthermore, Perl includes advanced regex support and is for many cases more efficient than any of 
 its counterparts. 

Perl one-lines can be executed at the command line like the other text utilities. Finally, Perl also is commonly 
installed by default on popular operating systems. In conclusion, Perl is functionally the best general choice for 
stream editing.

# Why not use Perl?

In practice, few people know sed well enough to fire off commands from memory. For the casual or infrequent user, 
usually the path to success is to search stackoverflow.com for a quick sed command they can parse and tweak for their purposes. 

Even fewer people know Perl, as the syntax proves to be even more daunting and difficult to remember than sed. 

For example, a user may wish to perform a find-and-replace, replace "Jack" with "Jill". 