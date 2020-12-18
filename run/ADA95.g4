grammar ADA95;

@parser::members {
@property
def ada_ctx(self):
    return self._ada_ctx

@ada_ctx.setter
def ada_ctx(self, value):
    self._ada_ctx = value

}

/*Reversed words*/

Abort: 'abort';

Abs: 'abs';

Abstract: 'abstract';

Accept: 'accept';

Access: 'access';

Aliased: 'aliased';

All: 'all';

And: 'and';

Array: 'array';

At: 'at';

Begin: 'begin';

Body: 'body';

Case: 'case';

Constant: 'constant';

Declare: 'declare';

Delay: 'delay';

Delta: 'delta';

Digits: 'digits';

Do: 'do';

Else: 'else';

Elsif: 'elsif';

End: 'end';

Entry: 'entry';
 
Exception: 'exception';
 
Exit: 'exit';
 
For: 'for';
 
Function: 'function';
 
Generic: 'generic';
 
Goto: 'goto';
 
If: 'if';
 
In: 'in';
 
Is: 'is';
 
Limited: 'limited';
 
Loop: 'loop';
 
Mod: 'mod';

New: 'new';

Not: 'not';

Null: 'null';

Of: 'of';

Or: 'or';

Others: 'others';

Out: 'out';

Package: 'package';

Pragma: 'pragma';

Private: 'private';

Procedure: 'procedure';

Protected: 'protected';

Raise: 'raise';

Range: 'range';

Record: 'record';

Rem: 'rem';

Renames: 'renames';

Requeue: 'requeue';

Return: 'return';

Reverse: 'reverse';

Select: 'select';

Separate: 'separate';

Subtype: 'subtype';

Tagged: 'tagged';

Task: 'task';

Terminate: 'terminate';

Then: 'then';

Type: 'type';

Until: 'until';

Use: 'use';

When: 'when';

While: 'while';

With: 'with';

Xor: 'xor';

Positive: 'positive';

PreRange: 'R' [aA][nN][gG][eE];



Numeric_literal:  Decimal_literal | Based_literal;

fragment Decimal_literal:  Numeral ('.' Numeral)? Exponent?;

fragment Based_literal:  
   Base '#' Based_numeral ('.' Based_numeral)? '#' Exponent?;
   
fragment Exponent:  Exp [+-]? Numeral;

fragment Base:  Numeral;

fragment Numeral:  Digit ('_'? Digit)*;

fragment Based_numeral:  
   Extended_digit ('_'? Extended_digit)*;

String_literal:  '"' StringCharacters? '"';

/*Pragma*/

pragma_clause:  
   Pragma Identifier ('(' pragma_argument_association (',' pragma_argument_association)* ')')? ';';
   
pragma_argument_association:  
     (Identifier '=>' )? name
   | (Identifier '=>' )? expression;


/*declaration*/
/*3.1*/
basic_declaration:  
     type_declaration  | subtype_declaration
   | object_declaration | number_declaration
   | subprogram_declaration | abstract_subprogram_declaration
   | package_declaration | renaming_declaration
   | exception_declaration | generic_declaration
   | generic_instantiation;
   
defining_identifier:  Identifier;

type_declaration:   full_type_declaration
   | incomplete_type_declaration
   | private_type_declaration
   | private_extension_declaration;
   
full_type_declaration:  
     Type defining_identifier known_discriminant_part? Is type_definition ';' # type_definition_clause
   | task_type_declaration                                                    # task_definition_clause
   | protected_type_declaration                                               # pro_type_definition_clause
   ;
   
type_definition:  
     enumeration_type_definition | integer_type_definition
   | real_type_definition | array_type_definition
   | record_type_definition | access_type_definition
   | derived_type_definition;
   
subtype_declaration:  
   Subtype defining_identifier Is subtype_indication ';';
   
subtype_indication:   subtype_mark constraint?;

subtype_mark:  subtype_name;

subtype_name: name;

constraint:  scalar_constraint | composite_constraint;

scalar_constraint:  
     range_constraint | digits_constraint | delta_constraint;
     
composite_constraint:  
     index_constraint | discriminant_constraint;
     
object_declaration:  
    defining_identifier_list ':' Aliased? Constant? subtype_indication (':=' expression)? ';'
  | defining_identifier_list ':' Aliased? Constant? array_type_definition (':=' expression)? ';'
  | single_task_declaration
  | single_protected_declaration;
  
defining_identifier_list:  
  defining_identifier (',' defining_identifier)*;
  
number_declaration:  
     defining_identifier_list ':' Constant ':=' expression ';';
     
derived_type_definition:  Abstract? New subtype_indication record_extension_part?;

range_constraint:   Range range_state;

/*3.5*/
range_state:   range_attribute_reference
   | simple_expression '..' simple_expression;
   
enumeration_type_definition:  
   '(' enumeration_literal_specification (',' enumeration_literal_specification)* ')';
   
enumeration_literal_specification:   
  defining_identifier 
  | defining_character_literal;
  
defining_character_literal:  Character_literal;

integer_type_definition:  signed_integer_type_definition | modular_type_definition;

signed_integer_type_definition:  Range simple_expression '..' simple_expression;

modular_type_definition:  Mod expression;

real_type_definition:  
   floating_point_definition | fixed_point_definition;
   
floating_point_definition:  
  Digits expression real_range_specification?;
  
real_range_specification:  
  Range simple_expression '..' simple_expression;
  
fixed_point_definition:  ordinary_fixed_point_definition | decimal_fixed_point_definition;

ordinary_fixed_point_definition:  
   Delta expression  real_range_specification;
   
decimal_fixed_point_definition:  
   Delta expression Digits expression real_range_specification?;
   
digits_constraint:  
   Digits expression range_constraint?;
   
array_type_definition:  
   unconstrained_array_definition | constrained_array_definition;
   
unconstrained_array_definition:  
   Array '(' index_subtype_definition (',' index_subtype_definition)* ')' Of component_definition;
   
index_subtype_definition:  subtype_mark Range '<>';

constrained_array_definition:  
   Array '(' discrete_subtype_definition (',' discrete_subtype_definition)* ')' Of component_definition;
   
discrete_subtype_definition:  discrete_subtype_indication | range_state;

component_definition:  Aliased? subtype_indication;

index_constraint:   '(' discrete_range (',' discrete_range)* ')';

discrete_range:  discrete_subtype_indication | range_state;

discrete_subtype_indication: name;

/*3.7*/
discriminant_part:  unknown_discriminant_part | known_discriminant_part;

unknown_discriminant_part:  '(' '<>' ')';

known_discriminant_part:  
   '(' discriminant_specification (';' discriminant_specification)* ')';
   
discriminant_specification:  
   defining_identifier_list ':' subtype_mark (':=' default_expression)?
 | defining_identifier_list ':' access_definition (':=' default_expression)?;
 
default_expression:  expression;

discriminant_constraint:  
   '(' discriminant_association (',' discriminant_association)* ')';
   
discriminant_association:  
   (discriminant_selector_name ('|' discriminant_selector_name)* '=>' )? expression;
   
discriminant_selector_name: name;

record_type_definition:  (Abstract? Tagged)? Limited? record_definition;

record_definition:  
    Record component_list End Record
  | Null Record;
  
component_list:  
      component_item+
   | component_item* variant_part
   |  Null ';' ;
   
component_item:  component_declaration | aspect_clause;

component_declaration:  
   defining_identifier_list ':' component_definition (':=' default_expression)? ';';
   
variant_part:  
   Case discriminant_direct_name Is variant variant*  End Case ';';
   
discriminant_direct_name: name;

variant:  
   When discrete_choice_list '=>'   component_list;
   
discrete_choice_list:  discrete_choice ('|' discrete_choice)*;

discrete_choice:  expression | discrete_range | Others;

record_extension_part:  With record_definition;




/*3.10*/
access_type_definition:  
    access_to_object_definition
  | access_to_subprogram_definition;
  
access_to_object_definition:  
    Access general_access_modifier? subtype_indication;
    
general_access_modifier:  All | Constant;

access_to_subprogram_definition:  
    Access Protected? Procedure formal_part?
  | Access Protected? Function  parameter_and_result_profile;
  
access_definition:  Access subtype_mark;

incomplete_type_declaration:  Type defining_identifier discriminant_part? ';';

declarative_part:  declarative_item*;

declarative_item:  
    basic_declarative_item | body_block;
    
basic_declarative_item:  
    basic_declaration | aspect_clause | use_clause;
    
body_block:  proper_body | body_stub;

proper_body:  
    subprogram_body | package_body | task_body | protected_body;
    
name:  
  direct_name | name '.' All
//     direct_name | explicit_dereference
   | name '(' expression (',' expression)* ')' | name '(' discrete_range ')'
   | name '.' selector_name | name '\'' attribute_designator
   | name '(' expression ')'
   | name '(' name ')' | name actual_parameter_part
   | Character_literal;
   
direct_name:  Identifier | operator_symbol;

//explicit_dereference:  name '.' All;

//implicit_dereference:  name;

//indexed_component:  name '(' expression (',' expression)* ')';

//slice:  name '(' discrete_range ')';

//selected_component:  name '.' selector_name;

selector_name:  Identifier | Character_literal | operator_symbol;

//attribute_reference:  name '\'' attribute_designator;


/*4.1.4*/
attribute_designator:  
    Identifier ('(' expression ')')?
  | Access | Delta | Digits;
  
range_attribute_reference:  name '\'' range_attribute_designator;

range_attribute_designator:  PreRange ('(' expression ')')?;

aggregate:  record_aggregate | extension_aggregate | array_aggregate;

record_aggregate:  '(' record_component_association_list ')';

record_component_association_list:  
    record_component_association (',' record_component_association)*
  | Null Record;
  
record_component_association:  
    (component_choice_list '=>')* expression;
    
component_choice_list:  
     component_selector_name ('|' component_selector_name)*
   | Others;
   
component_selector_name: name;

extension_aggregate:  
    '(' ancestor_part With record_component_association_list ')';
    
ancestor_part:  expression | subtype_mark;

array_aggregate:  
  positional_array_aggregate | named_array_aggregate;
  
positional_array_aggregate:  
    '(' expression (',' expression)+ ')'
  | '(' expression (',' expression)* ',' Others '=>' expression ')';
  
named_array_aggregate:  
    '(' array_component_association (',' array_component_association)* ')';
    
array_component_association:  
    discrete_choice_list '=>' expression;
    
expression:  
     relation (And relation)* | relation (And Then relation)*
   | relation (Or relation)* | relation (Or Else relation)*
   | relation (Xor relation)*;
   
relation:  
     simple_expression (Relational_operator simple_expression)?
   | simple_expression Not? In range_state
   | simple_expression Not? In subtype_mark;
   
   
simple_expression:  (ADD | SUB)? term ((ADD | SUB | CONCAT) term)*;

term:  factor (Multiplying_operator factor)*;

 
/*4.4*/
factor:  primary ('**' primary)? | Abs primary | Not primary;

primary:  
   Numeric_literal | Null | String_literal | aggregate
 | name | qualified_expression | allocator | '(' expression ')';
 

Highest_precedence_operator:   '**'  | Abs | Not;

//Binary_adding_operator:   '+'   | '–'  | '&';

Multiplying_operator:   '*'   | '/'   | Mod | Rem;

//Unary_adding_operator:   '+'   | '–';

Relational_operator:   '='   | '/='  | '<'   | '<=' | '>' | '>=';

//Logical_operator: And | Or | Xor

/*type_conversion:  
    subtype_mark '(' expression ')'
  | subtype_mark '(' name ')';*/
  
qualified_expression:  
   subtype_mark '\'' '(' expression ')'  | subtype_mark '\'' aggregate;
   
allocator:  
   New subtype_indication | New qualified_expression;
   
sequence_of_statements:  statement statement*;

statement:  
   label* simple_statement | label* compound_statement;
   
simple_statement:  null_statement
   | assignment_statement | exit_statement
   | goto_statement | procedure_call_statement
   | return_statement | entry_call_statement
   | requeue_statement | delay_statement
   | abort_statement | raise_statement
   | code_statement;
   
compound_statement:  
     if_statement | case_statement
   | loop_statement | block_statement
   | accept_statement | select_statement;
   
null_statement:  Null ';';

label:  '<<' label_statement_identifier '>>';

label_statement_identifier: defining_identifier;

statement_identifier:  direct_name;

assignment_statement:  
   variable_name ':=' expression ';';
   
variable_name: name;

/*5.3*/
if_statement:  
    If condition Then sequence_of_statements (
    Elsif condition Then sequence_of_statements)* (
    Else sequence_of_statements)?    End If ';';
    
condition:  boolean_expression;

boolean_expression: expression;

case_statement:  
   Case expression Is case_statement_alternative+  End Case ';';
   
case_statement_alternative:  
   When discrete_choice_list '=>' sequence_of_statements;
   
loop_statement:  
   (Identifier ':')? iteration_scheme? Loop sequence_of_statements  End Loop Identifier? ';';
   
iteration_scheme:  While condition
   | For loop_parameter_specification;
   
loop_parameter_specification:  
   defining_identifier In Reverse? discrete_subtype_definition;
   
block_statement:  
   (Identifier ':')? (
       Declare
            declarative_part)?  Begin handled_sequence_of_statements  End Identifier? ';' ;
            
exit_statement:  
   Exit loop_name? (When condition)? ';';
   
loop_name: name;

goto_statement:  Goto label_name ';';

label_name: name;

subprogram_declaration:  subprogram_specification ';';

abstract_subprogram_declaration:  subprogram_specification Is Abstract ';';

subprogram_specification:  
     Procedure defining_program_unit_name  formal_part?
   | Function defining_designator  parameter_and_result_profile;
   
designator:  (parent_unit_name '.' )? Identifier | operator_symbol;

defining_designator:  defining_program_unit_name | defining_operator_symbol;


/*6.1*/
defining_program_unit_name:  (parent_unit_name '.' )? defining_identifier;

operator_symbol:  String_literal;

defining_operator_symbol:  operator_symbol;

parameter_and_result_profile:  formal_part? Return subtype_mark;

formal_part:  
   '(' parameter_specification (';' parameter_specification)* ')';
   
parameter_specification:  
    defining_identifier_list ':' io_mode?  subtype_mark (':=' default_expression)?
  | defining_identifier_list ':' access_definition (':=' default_expression)?;
  
io_mode:  In | In Out | Out;

subprogram_body:  
    subprogram_specification Is declarative_part Begin handled_sequence_of_statements End designator? ';';
    
procedure_call_statement:  
  procedure_name actual_parameter_part? ';';
  
procedure_name: name;

/*function_call:  
    function_name actual_parameter_part?;*/
  
function_name: name;

actual_parameter_part:  
    '(' parameter_association (',' parameter_association)* ')';
    
parameter_association:  
   (formal_parameter_selector_name '=>')? explicit_actual_parameter;
   
formal_parameter_selector_name: name;

explicit_actual_parameter:  expression | variable_name;

return_statement:  Return expression? ';';

package_declaration:  package_specification ';';

package_specification:  
    Package defining_program_unit_name Is basic_declarative_item* (
    Private
      basic_declarative_item*
      )?    End ((parent_unit_name '.')? Identifier)?;



/*7.2*/
package_body:  
    Package Body defining_program_unit_name Is declarative_part (
    Begin
        handled_sequence_of_statements
    )? End ((parent_unit_name '.')? Identifier)? ';';
    
private_type_declaration:  
   Type defining_identifier discriminant_part? Is (Abstract? Tagged)? Limited? Private ';' ;
   
private_extension_declaration:  
   Type defining_identifier discriminant_part? Is Abstract? New defining_identifier With Private ';';
   
use_clause:  use_package_clause | use_type_clause;

use_package_clause:  Use package_name (',' package_name)* ';';

package_name: name;

use_type_clause:  Use Type subtype_mark (',' subtype_mark)* ';';

renaming_declaration:  
      object_renaming_declaration
    | exception_renaming_declaration
    | package_renaming_declaration
    | subprogram_renaming_declaration
    | generic_renaming_declaration;
    
object_renaming_declaration:  defining_identifier ':' subtype_mark Renames object_name ';';

object_name: name;

exception_renaming_declaration:  defining_identifier ':' Exception Renames exception_name ';';

exception_name: name;

package_renaming_declaration:  Package defining_program_unit_name Renames package_name ';';

subprogram_renaming_declaration:  subprogram_specification Renames callable_entity_name ';';

callable_entity_name: name;

generic_renaming_declaration:  
    Generic Package defining_program_unit_name Renames generic_package_name ';' 
  | Generic Procedure defining_program_unit_name Renames generic_procedure_name ';'
  | Generic Function defining_program_unit_name Renames generic_function_name ';';
  
generic_package_name: name;

generic_procedure_name: name;

generic_function_name: name;

task_type_declaration:  
   Task Type defining_identifier known_discriminant_part? (Is task_definition)? ';';
   
single_task_declaration:  
   Task defining_identifier (Is task_definition)? ';';
   
task_definition:  
     task_item* (
    Private
     task_item*
  )? End defining_identifier?;
  
task_item:  entry_declaration | aspect_clause;


/*9.1*/
task_body:  
   Task Body defining_identifier Is declarative_part Begin handled_sequence_of_statements  End defining_identifier? ';';
   
protected_type_declaration:  
  Protected Type defining_identifier known_discriminant_part? Is protected_definition ';';
  
single_protected_declaration:  
  Protected defining_identifier Is protected_definition ';';
  
protected_definition:  
     protected_operation_declaration* (
  Private
     protected_element_declaration* 
  )? End defining_identifier?;
  
protected_operation_declaration:  subprogram_declaration
     | entry_declaration
     | aspect_clause;
     
protected_element_declaration:  protected_operation_declaration
     | component_declaration;
     
protected_body:  
  Protected Body defining_identifier Is protected_operation_item*  End defining_identifier? ';';
  
protected_operation_item:  subprogram_declaration
     | subprogram_body
     | entry_body
     | aspect_clause;
     
entry_declaration:  
   Entry defining_identifier ('(' discrete_subtype_definition ')' )? formal_part? ';';
   
accept_statement:  
   Accept entry_direct_name ('(' entry_index ')')? formal_part? (Do
     handled_sequence_of_statements
   End defining_identifier?)? ';';
   
entry_direct_name: direct_name;

entry_index:  expression;

entry_body:  
  Entry defining_identifier  entry_body_formal_part  entry_barrier Is   declarative_part  Begin  handled_sequence_of_statements End defining_identifier? ';';
  
entry_body_formal_part:  ('(' entry_index_specification ')' )? formal_part?;

entry_barrier:  When condition;



/*9.5.2*/
entry_index_specification:  For defining_identifier In discrete_subtype_definition;

entry_call_statement:  entry_name actual_parameter_part? ';';

requeue_statement:  Requeue entry_name (With Abort)? ';';

entry_name: name;

delay_statement:  delay_until_statement | delay_relative_statement;

delay_until_statement:  Delay Until simple_expression ';' ;

delay_relative_statement:  Delay simple_expression ';';

select_statement:  
   selective_accept
  | timed_entry_call
  | conditional_entry_call
  | asynchronous_select;
  
selective_accept:  
  Select guard? select_alternative (
  Or
   guard?
     select_alternative )* (
  Else
   sequence_of_statements )?  End Select ';';
   
guard:  When condition '=>';

select_alternative:  
   accept_alternative
  | delay_alternative
  | terminate_alternative;
  
accept_alternative:  
  accept_statement sequence_of_statements?;
  
delay_alternative:  
  delay_statement sequence_of_statements?;
  
terminate_alternative:  Terminate ';';

timed_entry_call:  
  Select entry_call_alternative Or delay_alternative End Select ';';
  
entry_call_alternative:  
  entry_call_statement sequence_of_statements?;



/*9.7.3*/
conditional_entry_call:  
  Select entry_call_alternative Else sequence_of_statements End Select ';';
  
asynchronous_select:  
  Select triggering_alternative Then Abort abortable_part End Select ';';
  
triggering_alternative:  triggering_statement sequence_of_statements?;

triggering_statement:  entry_call_statement | delay_statement;

abortable_part:  sequence_of_statements;

abort_statement:  Abort task_name (',' task_name)* ';';

task_name: name;

compilation:  compilation_unit*;

compilation_unit:  
    context_item* library_item # compilation_unit_lib
  | context_item* subunit      # compilation_unit_sep
  ;    
  
library_item:  Private? library_unit_declaration
  | library_unit_body
  | Private? library_unit_renaming_declaration;
  
library_unit_declaration:  
     subprogram_declaration | package_declaration
   | generic_declaration | generic_instantiation;
   
library_unit_renaming_declaration:  
   package_renaming_declaration
 | generic_renaming_declaration
 | subprogram_renaming_declaration;
 
library_unit_body:  subprogram_body | package_body;

parent_unit_name:  name;

context_item:  with_clause | use_clause;

with_clause:  With library_unit_name (',' library_unit_name)* ';';

library_unit_name: direct_name | direct_name '.' library_unit_name;

body_stub:  subprogram_body_stub | package_body_stub | task_body_stub | protected_body_stub;

subprogram_body_stub:  subprogram_specification Is Separate ';';



/*10.1.3*/
package_body_stub:  Package Body defining_identifier Is Separate ';';

task_body_stub:  Task Body defining_identifier Is Separate ';';

protected_body_stub:  Protected Body defining_identifier Is Separate ';';

subunit:  Separate '(' parent_unit_name ')' proper_body;

exception_declaration:  defining_identifier_list ':' Exception ';';

handled_sequence_of_statements:  
     sequence_of_statements (
  Exception
     exception_handler+ )?;
 
exception_handler:  When (choice_parameter_specification ':')? exception_choice ('|' exception_choice)* '=>' sequence_of_statements;
 
choice_parameter_specification:  defining_identifier;

exception_choice:  exception_name | Others;

raise_statement:  Raise exception_name? ';';

generic_declaration:  generic_subprogram_declaration | generic_package_declaration;

generic_subprogram_declaration:  
     generic_formal_part  subprogram_specification ';';
     
generic_package_declaration:  
     generic_formal_part  package_specification ';';
     
generic_formal_part:  Generic (generic_formal_parameter_declaration | use_clause)*;

generic_formal_parameter_declaration:  
      formal_object_declaration
    | formal_type_declaration
    | formal_subprogram_declaration
    | formal_package_declaration;
    
generic_instantiation:  
     Package defining_program_unit_name Is New generic_package_name generic_actual_part? ';'
   | Procedure defining_program_unit_name Is New generic_procedure_name generic_actual_part? ';'
   | Function defining_designator Is New generic_function_name generic_actual_part? ';' ;
   
generic_actual_part:  
   '(' generic_association (',' generic_association)* ')';
   
generic_association:  
   (generic_formal_parameter_selector_name '=>')? explicit_generic_actual_parameter;

generic_formal_parameter_selector_name: name;

/*12.3*/
explicit_generic_actual_parameter:  expression | variable_name
   | subtype_mark;
   
formal_object_declaration:  
    defining_identifier_list ':' io_mode? subtype_mark (':=' default_expression) ';';
    
formal_type_declaration:  
    Type defining_identifier discriminant_part? Is formal_type_definition ';';
    
formal_type_definition:  
      formal_private_type_definition
    | formal_derived_type_definition
    | formal_discrete_type_definition
    | formal_signed_integer_type_definition
    | formal_modular_type_definition
    | formal_floating_point_definition
    | formal_ordinary_fixed_point_definition
    | formal_decimal_fixed_point_definition
    | formal_array_type_definition
    | formal_access_type_definition;
    
formal_private_type_definition:  (Abstract? Tagged)? Limited? Private;

formal_derived_type_definition:  Abstract? New subtype_mark (With Private)?;

formal_discrete_type_definition:  '(' '<>' ')';

formal_signed_integer_type_definition:  Range '<>';

formal_modular_type_definition:  Mod '<>';

formal_floating_point_definition:  Digits '<>';

formal_ordinary_fixed_point_definition:  Delta '<>';

formal_decimal_fixed_point_definition:  Delta '<>' Digits '<>';

formal_array_type_definition:  array_type_definition;

formal_access_type_definition:  access_type_definition;

formal_subprogram_declaration:  With subprogram_specification (Is subprogram_default)? ';';

subprogram_default:  default_name | '<>';

default_name:  name;

formal_package_declaration:  
    With Package defining_identifier Is New generic_package_name  formal_package_actual_part ';';
    
formal_package_actual_part:  
    '(' '<>' ')' | generic_actual_part?;



/*13.1*/
aspect_clause:  attribute_definition_clause
      | enumeration_representation_clause
      | record_representation_clause
      | at_clause;
      
local_name:  direct_name
      | direct_name '\'' attribute_designator
      | library_unit_name;
      
attribute_definition_clause:  
      For local_name '\'' attribute_designator Use expression ';'
    | For local_name '\'' attribute_designator Use name ';';
    
enumeration_representation_clause:  
    For first_subtype_local_name Use enumeration_aggregate ';';
    
enumeration_aggregate:  array_aggregate;

record_representation_clause:  
    For first_subtype_local_name Use  Record mod_clause?  component_clause*  End Record ';';
    
first_subtype_local_name: local_name;

component_clause:  
    component_local_name At position Range first_bit '..' last_bit ';';
    
component_local_name: local_name;

position:  expression;

first_bit:  simple_expression;

last_bit:  simple_expression;

code_statement:  qualified_expression ';';

restriction:  defining_identifier
    | defining_identifier '=>' expression;
    

delta_constraint:  Delta expression range_constraint?;


at_clause:  For direct_name Use At expression ';' ;

mod_clause:  At Mod expression ';';

/*fragment*/

fragment Identifier_letter: [a-zA-Z];

fragment Digit: [0-9];
    
fragment Exp: [eE];

fragment Extended_digit:  Digit | [aA] | [bB] | [cC] | [dD] | [eE] | [fF];

/*char, Digit, str*/
Character_literal
    :   '\'' SingleCharacter '\''
    |   '\'' EscapeSequence '\''
    ;

fragment
SingleCharacter
    :   ~['\\]
    ;

fragment
StringCharacters
    :   StringCharacter+
    ;

fragment
StringCharacter
    :   ~["\\]
    |   EscapeSequence
    ;

fragment
EscapeSequence
    :   '\\' [btnfr"'\\];
    
fragment Letter_or_digit:  Identifier_letter | Digit;

//LPAREN          : '(';
//RPAREN          : ')';
//LBRACE          : '{';
//RBRACE          : '}';
//SEMI            : ';';
//COMMA           : ',';
//DOT             : '.';
//
//// §3.12 Operators
//
//ASSIGN          : ':=';
//GT              : '>';
//LT              : '<';
//QUESTION        : '?';
//COLON           : ':';
//EQUAL           : '=';
//LE              : '<=';
//GE              : '>=';
//NOTEQUAL        : '/=';
CONCAT          : '&';
//CHOOSE          : '|';
ADD             : '+';
SUB             : '-';
//MUL             : '*';
//DIV             : '/';
//CARET           : '^';
//
//CHOICE : '=>';


Identifier:  
   Identifier_letter ('_'? Letter_or_digit)*;


Whitespace: [ \t]+ -> skip;
Newline: ('\r' '\n'? | '\n') -> skip;
LineComment: '--' ~ [\r\n]* -> skip;