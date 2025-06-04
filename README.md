# کامپایلر زبان Dolme 🛠️

---

### معرفی پروژه 📚
این پروژه یک زبان برنامه‌نویسی ساده به نام **Dolme** را پیاده‌سازی می‌کند. شامل مراحل تحلیل لغوی (Lexer)، تحلیل نحوی LL(1) و تولید کد سه آدرسه (Intermediate Code) است. هدف اصلی، آموزش مفاهیم پایه کامپایلر و ساخت یک کامپایلر ابتدایی می‌باشد.

### ویژگی‌های زبان ✨
- تعریف متغیر با `let`
- اختصاص مقدار به متغیرها
- ساختار شرطی `if-else`
- حلقه `while`
- عبارات منطقی `and`, `or`, `not`
- عبارات حسابی با `+`, `-`, `*`, `/`
- دستور چاپ مقدار با `print`

### جزئیات پیاده‌سازی 🔧
- **تحلیلگر لغوی (Lexer):** تجزیه کد ورودی به توکن‌های معنی‌دار  
- **تحلیلگر نحوی (Parser):** پیاده‌سازی LL(1) با بررسی دستورها و عبارات  
- **تولید کد (Code Generator):** تولید کد میانی سه آدرسه همراه با برچسب‌ها و متغیرهای موقت  
- **ورودی و خروجی:**  
  - ورودی از فایل `input.txt`  
  - خروجی کد میانی در `output.txt`  

### نحوه اجرا 🚀
1. کد زبان Dolme را در `input.txt` بنویسید  
2. اسکریپت `main.py` را اجرا کنید  
3. کد میانی تولید شده را در `output.txt` مشاهده کنید  

### نکات مهم ⚠️
- پشتیبانی محدود به گرامر و توکن‌های تعریف شده  
- خطاها عمدتاً نحوی هستند و با پیام خطا گزارش می‌شوند  

---

# Dolme Language Compiler 🛠️

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

### Implementation Details 🔧
- **Lexer:** Tokenizes input source code  
- **Parser:** LL(1) parser handling statements and expressions  
- **Code Generator:** Produces three-address intermediate code with labels and temporary variables  
- **Input/Output:**  
  - Reads from `input.txt`  
  - Outputs intermediate code to `output.txt`  

### How to Run 🚀
1. Write your Dolme code in `input.txt`  
2. Run `main.py`  
3. Check generated intermediate code in `output.txt`  

### Notes ⚠️
- Limited support to defined grammar and tokens  
- Errors are mostly syntax errors reported clearly  

---

