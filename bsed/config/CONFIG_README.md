# bsed configuration

## Summary

There are two primary types of documents: parse tree JSON files, and translation JSON files.

### Translation files
Translation files are mappings to a sequence of words and a corresponding code snippet or executable statement.

Keys of the translation file are strings containing the lowercase sequence of words representing a user command. 

#### Variable types

There are two types of variables, represented in two ways:

- $CAPITAL_WORD format for simple input variables
- ${lower_case_in_braces} format for translations of sub-expressions

Simple variables are values substituted into placeholder locations before execution. Examples include line numbers, 
search patterns, or text to be inserted.

Sub-expressions are evaluated independently, translated, and their translations are substituted into the command 
before execution.

The values of the translation file entries hold code with placeholders for inputs and the results of sub-expression 
translations.

### Parse tree files

Parse tree files hold the mappings of words to acceptable next words in the path. 

The file is loaded in by a TokenTree object which accepts a stream of tokens. Valid commands are parsed by traversing 
the tree to a completed state using the input. 

#### Variable types

Parse tree files have three special value types, with three formats: 

- $CAPITAL_WORD for simple variables, usually placeholders for user inputs 
    - These are values like regex patterns, line numbers to operate on, or text to be inserted somewhere.
- $EVAL__lower-case-name for reusable sub-trees
    - These are simply for notational convenience, referencing sub-trees found elsewhere in the file. Equivalent to 
    copy-and-pasting the subtree in. The TokenTree expands these when it builds the tree.
- $EXPR__lower-case-name for sub-expressions
    - These represent sub-trees which are independently interpreted and translated. The translation is stored to a 
    variable to be input to the parent expression.
    - At the root of the expression tree is a key $var which maps to the variable that the expression's translation 
    is stored to.

 
 NOTE: When further parse tokens follow an $EVAL or $EXPR token, it means that all leaves of the subtree to be 
 substituted in can be succeeded by the parse tokens which follow."
 
 #### Metadata types

There are two other tokens which may appear which are not normal command words:

- $var_name: The variable an input var or sub-expression is stored as.
- $translations_file_name: At the root of any expression tree is the name of the file which translates its parsed 
phrases.
 
Each of variable types will include a $var_name. This is the variable name that the translation expects. For 
example, if
 an input marked with the token $USER_TEXT_INPUT has $var_name: 
"search_pattern", then the translation contains `{search_pattern}` (or the equivalent in its language) so that the 
value can be substituted in.
 