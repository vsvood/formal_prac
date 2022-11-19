# CYK algorithm implementation
## Usage
```shell
$ python main.py <grammar> <word>
```
### Example
```shell
$ python main.py tests/CBS "(()()(()())"
True
```
```shell
$ python main.py tests/CBS "(()()()())"
False
```
## Tests
warning: testing may take a while (up to 5 minutes on local machine)
```shell
$ coverage run --source=. -m pytest -v . && coverage report -m
```
## Grammar format
### Optional header
#### $VARIABLES:
list of space-separated non-terminals

if not specified, all tokens mentioned in left part of rules will be considered as variables

#### $TERMINALS:
list of space-separated terminals

if not specified, all tokens which are not in variable set will be considered as terminals

### $START:
start variable

if not specified, first variable will be considered as start variable

### Rules
#### variable->rule_set

rule set is a list of |-separated rules

rule is a space-separated list of variables and terminals

#### Example
##### Full grammar
```text
$VARIABLES: S A B C
$TERMINALS: ( )
$START: S
S->A B
A->( A )|( )
B->( B )|( )
```
##### Grammar without header
```text
S->A B
A->( A )|( )
B->( B )|( )
```
##### Rule can be empty:
```text
S->A B C
A->( A )|( )
B->( B )|( )
C->
```