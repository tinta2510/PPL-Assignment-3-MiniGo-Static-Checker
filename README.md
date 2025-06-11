# PPL-Assignment-3-MiniGo-Static-Checker
## Overview

This project is the third assignment in the **Principles of Programming Languages (CO3005)** course at HCMC University of Technology (VNU-HCM). In this phase, we implement a **static checker** for the MiniGo language.

The static checker validates the **semantic correctness** of MiniGo programs by traversing the **Abstract Syntax Tree (AST)** (generated in Assignment 2). It ensures that MiniGo programs adhere to rules regarding **type safety, scope, and declaration correctness**.

## Related Assignments
Project's related parts:
- [Assignment 1 – Lexer & Recognizer](https://github.com/tinta2510/PPL-Assignment-1-MiniGo-Lexer-and-Recognizer)
- [Assignment 2 – AST Generation](https://github.com/tinta2510/PPL-Assignment-2-MiniGo-AST-Generation)

Upcoming:
- [Assignment 4 – Code Generator](https://github.com/tinta2510/PPL-Assignment-4-Code-Generator)

## Environment Setup
Refer to the Assignment 1 repository for environment setup instructions: [Assignment 1](https://github.com/tinta2510/PPL-Assignment-1-MiniGo-Lexer-and-Recognizer)

## Usage
From the `src` directory, run:

```bash
python run.py test CheckSuite
```

## Project Files
- StaticCheck.py: Implements the StaticChecker class and all logic to validate MiniGo semantics.
- CheckSuite.py: Contains 100 test cases, each testing a specific semantic rule.
- StaticError.py: defines exceptions like Redeclared, Undeclared, TypeMismatch, etc. Do not modify.

## Semantic Checks
This checker handles various static constraints defined in the MiniGo specification:
1. **Redeclarations**  
   Detect and raise `Redeclared(<kind>, <name>)` when:
   - A name is declared more than once in the same scope.
   - Applies to Variables, Constants, Parameters, Types, Functions, Methods, Prototypes, Fields.
  
2. **Undeclared Usage**
   Raise `Undeclared(<kind>, <name>)` for:
   - Unrecognized variable/constant/parameter names.
   - Calls to undefined functions or methods.
   - Accessing fields or methods that do not exist.

3. **Type Mismatches**
   Raise `TypeMismatch(<context>)` in cases like:
   - Assigning incompatible types (e.g., `float := string`).
   - Returning incorrect types in functions.
   - Using a non-boolean in an if condition.
   - Misusing subscripting on non-arrays or field access on non-structs.
   - Passing wrong types or argument count in function/method calls.

More detailed follow the documents in the `docs` directory.