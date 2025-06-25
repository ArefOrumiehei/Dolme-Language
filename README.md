# Dolme Language Compiler   
![Dolme](./assets/images/dolme.jpg)


### Project Overview 📚
This project implements a simple programming language called **Dolme**. It covers lexical analysis (Lexer), LL(1) parsing, and three-address intermediate code generation. The main goal is to learn compiler fundamentals and build a basic compiler.

### What is Dolme? 
Dolma is a traditional dish popular in many Middle Eastern, Mediterranean and Balkan cuisines. The name "dolma" means "stuffed" in Turkish and refers to vegetables such as grape leaves, peppers, zucchini or cabbage leaves (the photo shows grape leaf dolma, which is the best) stuffed with a savory mixture of rice, meat, vegetables and spices. The dish is loved by many people for its rich taste, comforting texture and cultural heritage that dates back centuries.


### Language Features ✨
- Variable declaration with `let`  
- Assignments  
- Conditional statements `if-else`  
- Loops `while` 
- Can assign and print `string` 
- Boolean expressions `and`, `or`, `not`  
- Arithmetic expressions with `+`, `-`, `*`, `/`, `%`
- Print statement with `print`
- Write comments with `/*...*/` for multi line comment and `//...` for single line comments  

### Implementation Details 🔧
- **Lexer:** Tokenizes input source code  
- **Parser:** LL(1) parser handling statements and expressions  
- **Code Generator:** Produces three-address intermediate code with temporary variables start from 600 and main variables start from 400
- **Input/Output:**  
  - Reads from `input.txt`  
  - Outputs intermediate code to `output.txt`  
- **Interpreter**: Execute the three-address code and display the output

### How to Run 🚀
1. Write your Dolme code in `input.txt`  
2. Run `main.py`  
3. Check generated intermediate code in `output.txt`
4. Results display in terminal

### Notes
- Limited support to defined grammar and tokens  
- Errors are mostly syntax errors reported clearly  

### Last Features ♿
- Now can write `break` and `continue` in while loop
---

### Grammer of Dolme language

Program       → StmtList

StmtList      → Stmt StmtList | ε

Stmt          → Decl 
              | Assign 
              | IfStmt 
              | WhileStmt 
              | PrintStmt
              | BreakStmt
              | ContinueStmt

Decl          → let id = Expr ;

Assign        → id = Expr ;

IfStmt        → if ( Cond ) { StmtList } ElsePart

ElsePart      → else { StmtList } | ε

WhileStmt     → while ( Cond ) { StmtList }

PrintStmt     → print ( expr ) ;

BreakStmt     → break ;

ContinueStmt     → Continue ;

Expr          → Term Expr'

Expr'         → + Term Expr' 
              | - Term Expr' 
              | ε

Term          → Factor Term'

Term'         → * Factor Term' 
              | / Factor Term' 
              | % Factor Term'
              | ε

Factor        → id 
              | num 
              | string
              | ( Expr )
              | - Factor

Cond          → OrExpr

OrExpr        → AndExpr OrExpr'

OrExpr'       → or AndExpr OrExpr' 
              | ε

AndExpr       → NotExpr AndExpr'

AndExpr'      → and NotExpr AndExpr' 
              | ε

NotExpr       → not NotExpr 
              | RelExpr

RelExpr       → BoolPrimary RelExpr'

RelExpr'      → RelOp BoolPrimary 
              | ε

BoolPrimary   → true 
              | false 
              | ( Cond ) 
              | Expr

RelOp         → < | > | <= | >= | == | !=

---

### 🌐 Web Version (JavaScript)

Alongside the Python version, a **web-based version** of the **Dolme** compiler is also available, allowing users to write and compile Dolme code directly in their browser.

#### Web Features:

* Simple and user-friendly interface
* Code editor to write Dolme code
* "Compile" button to generate and view three-address intermediate code
* No installation or setup required – runs entirely in the browser

#### Technologies Used:

* JavaScript (full implementation of Lexer, Parser, and Code Generator)
* HTML/CSS for UI design
* Fully client-side (no backend/server required)

#### How to Use:

1. Visit the web version (e.g., via GitHub Pages or any web host)
2. Write your Dolme code in the editor window
3. Click the **"Compile"** button
4. The generated intermediate code will be displayed below the editor

### License 📝
This project is licensed under the [MIT License](./LICENSE).

---
<div align="center">
  <img src="./assets/images/dolme2.png" alt="Dolme" />
</div>
