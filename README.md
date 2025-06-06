# Dolme Language Compiler   
![Dolme](./assets/images/dolme.jpg)


### Project Overview 📚
This project implements a simple programming language called **Dolme**. It covers lexical analysis (Lexer), LL(1) parsing, and three-address intermediate code generation. The main goal is to learn compiler fundamentals and build a basic compiler.

### Language Features ✨
- Variable declaration with `let`  
- Assignments  
- Conditional statements `if-else`  
- Loops `while`  
- Boolean expressions `and`, `or`, `not`  
- Arithmetic expressions with `+`, `-`, `*`, `/`  
- Print statement with `print`
- Write comments with `/*...*/` for multi line comment and `//...` for single line comments  

### Implementation Details 🔧
- **Lexer:** Tokenizes input source code  
- **Parser:** LL(1) parser handling statements and expressions  
- **Code Generator:** Produces three-address intermediate code with labels and temporary variables  
- **Input/Output:**  
  - Reads from `input.txt`  
  - Outputs intermediate code to `output.txt`  
- **Interpreter**: Execute the three-address code and display the output

### How to Run 🚀
1. Write your Dolme code in `input.txt`  
2. Run `main.py`  
3. Check generated intermediate code in `output.txt`  

### Notes
- Limited support to defined grammar and tokens  
- Errors are mostly syntax errors reported clearly  

---

### معرفی پروژه 📚
در این پروژه یک زبان برنامه نویسی ساده به نام **دلمه** رو پیاده سازی میکنیم. شامل سه مرحله تحلیل لغوی(lexer) ، تحلیل نحوی (LL1) و تولید کد سه آدرسه است. هدف اصلی از این پروژه یادگیری مفاهیم پایه کامپایلر و ساخت یک کامپایلر ساده است.

### ویژگی‌های زبان ✨
- تعریف متغیر با `let`
- اختصاص مقدار به متغیرها
- ساختار شرطی `if-else`
- حلقه `while`
- عبارات منطقی `and`, `or`, `not`
- عبارات حسابی با `+`, `-`, `*`, `/`
- دستور چاپ مقدار با `print`
- کامنت گذاری با `/*...*/` برای کامنت های چند خطی و `//...` برای کامنت های تک خطی

### جزئیات پیاده‌سازی 🔧
- **تحلیلگر لغوی (Lexer):** تجزیه کد ورودی به توکن‌های معنی‌دار  
- **تحلیلگر نحوی (Parser):** پیاده‌سازی LL(1) با بررسی دستورها و عبارات  
- **تولید کد (Code Generator):** تولید کد میانی سه آدرسه همراه با برچسب‌ها و متغیرهای موقت  
- **ورودی و خروجی:**  
  - ورودی از فایل `input.txt`  
  - خروجی کد میانی در `output.txt`  
- **مفسر(Interpreter)**: اجرای کد سه آدرسه و نمایش خروجیش 

### نحوه اجرا 🚀
1. کد زبان Dolme را در `input.txt` بنویسید  
2. اسکریپت `main.py` را اجرا کنید  
3. کد میانی تولید شده را در `output.txt` مشاهده کنید  

### نکته
- پشتیبانی محدود به گرامر و توکن‌های تعریف شده  
- خطاها عمدتاً نحوی هستند و با پیام خطا گزارش می‌شوند  

---

### Grammar of Dolme language

Program       → StmtList

StmtList      → Stmt StmtList | ε

Stmt          → Decl 
              | Assign 
              | IfStmt 
              | WhileStmt 
              | PrintStmt

Decl          → let id = Expr ;

Assign        → id = Expr ;

IfStmt        → if ( Cond ) { StmtList } ElsePart

ElsePart      → else { StmtList } | ε

WhileStmt     → while ( Cond ) { StmtList }

PrintStmt     → print ( id ) ;

Expr          → Term Expr'

Expr'         → + Term Expr' 
              | - Term Expr' 
              | ε

Term          → Factor Term'

Term'         → * Factor Term' 
              | / Factor Term' 
              | ε

Factor        → id 
              | num 
              | ( Expr )

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

---

در کنار نسخه Python، یک نسخه وبی از کامپایلر Dolme نیز توسعه داده شده است تا کاربران بتوانند مستقیماً در مرورگر خود کد بنویسند و کد میانی تولید شده را مشاهده کنند.

#### ویژگی‌های نسخه وب:

* رابط کاربری ساده و قابل‌استفاده در مرورگر
* نوشتن کد Dolme در یک ویرایشگر
* دکمه "Compile" برای مشاهده کد میانی سه‌آدرسه
* بدون نیاز به نصب یا اجرای فایل‌های محلی

#### تکنولوژی‌ها:

* JavaScript (پیاده‌سازی Lexer، Parser و Code Generator به صورت کامل در JS)
* HTML/CSS برای ساخت رابط کاربری
* بدون نیاز به سرور یا backend

#### نحوه استفاده:

1. به صفحه نسخه وب بروید (در صورت انتشار روی GitHub Pages یا هاست دیگر)
2. کد خود را در پنجره ویرایشگر وارد کنید
3. روی دکمه "Compile" کلیک کنید
4. خروجی در پنجره پایین نمایش داده می‌شود

---
![Dolme](./assets/images/dolme2.png)
