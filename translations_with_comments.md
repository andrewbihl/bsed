# SimpleSed command translations

This document explains and tracks the translations used in SimpleSed. The goal of the translations is to be efficient; simplicity is not preferred because the main purpose of the product is to present a simpler interface for technologies like sed and grep. Underneath the hood, whatever is performant and portable should be used. Changes and rationales for choosing implementations should be documented in this document.

### Example
This is a general outline of the stages of conversion. Details are excluded.
```
file_name = 'input.txt'
input_str = 'prepend hello with world'
normalized_command = 'prepend $USER_TEXT_INPUT with $USER_TEXT_INPUT'
command_template = """sed 's/{1}/{2}{1}{2}/' {0}"""
text_inputs = ['input.txt', 'hello', 'world']
command = command_template.format(*text_inputs)
print("Translated command:", command)
```
> Translated command: sed 's/hello/worldhelloworld/ input.txt' 

### Notes

- The translations are written to work with Python's `.format()` function on strings.

- Some command statements may have multiple translations. Unless a clear preference is marked, testing is needed to determine which is optimal.

- Where there is a particular implementation found to be best, that number should be marked with a * and an explanation should be written below.

- Arguments are referenced by index of the order they appear in the command statement. The file argument is always index 0.


***
# The translations

### Basic word functions

- delete $USER_TEXT_INPUT
  1. `sed 's/{1}//g' {0}`

- replace $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed 's/%{1}/%{2}/' {0}`

- append $USER_TEXT_INPUT with $USER_TEXT_INPUT: sed 's/{1}/{1}{2}/' {0}
  1. `sed 's/{1}/{1}{2}/' {0}`

- prepend $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed 's/{1}/{2}{1}/' {0}`

- wrap $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed 's/{1}/{2}{1}{2}/' {0}`

### Line functions

##### Delete

- delete lines containing $USER_TEXT_INPUT
  1. `sed '/{1}/d' {0}`

- delete lines starting with $USER_TEXT_INPUT
  1. `sed '/^{1}/d' {0}`

- delete lines ending with $USER_TEXT_INPUT
  1. `sed '/{1}$/d' {0}`

##### Clear
This leaves blank lines behind

- clear lines containing $USER_TEXT_INPUT
  1. `sed 's/.*{1}.*//g' {0}`

- clear lines starting with $USER_TEXT_INPUT
  1. `sed 's/^{1}.*//g' {0}`

- clear lines ending with $USER_TEXT_INPUT
  1. `sed 's/.*{1}$//g' {0}`


##### Replace

- replace lines containing $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed 's/.*{1}.*/{2}/g' {0}`


- replace lines starting with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed 's/^{1}.*/{2}/g' {0}`

- replace lines ending with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed 's/.*{1}$/{2}/g' {0}`


##### Append

- append lines containing $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed -e '/{1}/s/$/{2}/' {0}`

- append lines starting with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed -e '/^{1}/s/$/{2}/' {0}`

- append lines ending with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed -e '/{1}$/s/$/{2}/' {0}`


##### Prepend

- prepend lines containing $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed -e '/{1}/s/$/{2}/' {0}`

- prepend lines starting with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed -e '/^{1}/s/^/{2}/' {0}`

- prepend lines ending with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed -e '/{1}$/s/^/{2}/' {0}`


##### Wrap

- wrap lines containing $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed '/{0}/ s/.*{2}&{2}/' {0}`

- wrap lines starting with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed '/^{0}/ s/.*{2}&{2}/' {0}`

- wrap lines ending with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `sed '/{0}$/ s/.*{2}&{2}/' {0}`


##### Select

- select lines containing $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `grep {1} {0}`

- select lines starting with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `grep ^{1} {0}`

- select lines ending with $USER_TEXT_INPUT with $USER_TEXT_INPUT
  1. `grep {1}$ {0}`
