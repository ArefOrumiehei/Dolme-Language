import { CodeGenerator } from "./codegen.js";

export class Parser {
  constructor(tokens) {
    this.tokens = tokens;
    this.pos = 0;
    this.current = this.tokens[this.pos] || null;
    this.tempCount = 0;
    this.labelCount = 0;
    this.codegen = new CodeGenerator();
  }

  next() {
    this.pos++;
    this.current = this.tokens[this.pos] || null;
  }

  eat(type) {
    if (this.current && this.current[0] === type) {
      this.next();
    } else {
      throw new Error(`Expected ${type} but got ${this.current}`);
    }
  }

  newTemp() {
    return `_t${++this.tempCount}`;
  }

  newLabel() {
    return `_L${++this.labelCount}`;
  }

  parse() {
    this.program();
    return this.codegen.getCode();
  }

  program() {
    this.stmtList();
  }

  stmtList() {
    while (
      this.current &&
      (this.current[0] === "KEYWORD" || this.current[0] === "ID")
    ) {
      this.stmt();
    }
  }

  stmt() {
    const val = this.current[1];
    if (val === "let") this.decl();
    else if (val === "print") this.printStmt();
    else if (val === "if") this.ifStmt();
    else if (val === "while") this.whileStmt();
    else if (this.current[0] === "ID") this.assign();
    else throw new Error(`Unexpected statement: ${val}`);
  }

  decl() {
    this.eat("KEYWORD"); // let
    const varName = this.current[1];
    this.eat("ID");
    this.eat("ASSIGN");
    const val = this.expr();
    this.codegen.assign(varName, val);
    this.eat("SEMI");
  }

  assign() {
    const varName = this.current[1];
    this.eat("ID");
    this.eat("ASSIGN");
    const val = this.expr();
    this.codegen.assign(varName, val);
    this.eat("SEMI");
  }

  printStmt() {
    this.eat("KEYWORD"); // print
    this.eat("LPAREN");
    const val = this.expr();
    this.eat("RPAREN");
    this.eat("SEMI");
    this.codegen.print(val);
  }

  ifStmt() {
    this.eat("KEYWORD"); // if
    this.eat("LPAREN");
    const cond = this.cond();
    this.eat("RPAREN");

    const labelElse = this.newLabel();
    const labelEnd = this.newLabel();

    this.codegen.ifFalse(cond, labelElse);

    this.eat("LBRACE");
    this.stmtList();
    this.eat("RBRACE");

    this.codegen.goto(labelEnd);
    this.codegen.label(labelElse);

    if (this.current && this.current[1] === "else") {
      this.eat("KEYWORD");
      this.eat("LBRACE");
      this.stmtList();
      this.eat("RBRACE");
    }

    this.codegen.label(labelEnd);
  }

  whileStmt() {
    this.eat("KEYWORD"); // while
    const labelStart = this.newLabel();
    const labelEnd = this.newLabel();

    this.codegen.label(labelStart);

    this.eat("LPAREN");
    const cond = this.cond();
    this.eat("RPAREN");

    this.codegen.ifFalse(cond, labelEnd);
    this.eat("LBRACE");
    this.stmtList();
    this.eat("RBRACE");

    this.codegen.goto(labelStart);
    this.codegen.label(labelEnd);
  }

  expr() {
    let left = this.term();
    while (this.current && ["PLUS", "MINUS"].includes(this.current[0])) {
      const op = this.current[1];
      this.eat(this.current[0]);
      const right = this.term();
      const temp = this.newTemp();
      this.codegen.binaryOp(temp, op, left, right);
      left = temp;
    }
    return left;
  }

  term() {
    let left = this.factor();
    while (this.current && ["MULT", "DIV"].includes(this.current[0])) {
      const op = this.current[1];
      this.eat(this.current[0]);
      const right = this.factor();
      const temp = this.newTemp();
      this.codegen.binaryOp(temp, op, left, right);
      left = temp;
    }
    return left;
  }

  factor() {
    if (this.current[0] === "ID") {
      const val = this.current[1];
      this.eat("ID");
      return val;
    } else if (this.current[0] === "NUMBER") {
      const val = this.current[1];
      this.eat("NUMBER");
      return val;
    } else if (this.current[0] === "LPAREN") {
      this.eat("LPAREN");
      const val = this.expr();
      this.eat("RPAREN");
      return val;
    } else {
      throw new Error(`Unexpected factor: ${this.current}`);
    }
  }

  cond() {
    return this.orExpr();
  }

  orExpr() {
    let left = this.andExpr();
    while (this.current && this.current[1] === "or") {
      this.eat("KEYWORD");
      const right = this.andExpr();
      const temp = this.newTemp();
      this.codegen.binaryOp(temp, "or", left, right);
      left = temp;
    }
    return left;
  }

  andExpr() {
    let left = this.notExpr();
    while (this.current && this.current[1] === "and") {
      this.eat("KEYWORD");
      const right = this.notExpr();
      const temp = this.newTemp();
      this.codegen.binaryOp(temp, "and", left, right);
      left = temp;
    }
    return left;
  }

  notExpr() {
    if (this.current && this.current[1] === "not") {
      this.eat("KEYWORD");
      const val = this.notExpr();
      const temp = this.newTemp();
      this.codegen.unaryOp(temp, "not", val);
      return temp;
    } else {
      return this.relExpr();
    }
  }

  relExpr() {
    const left = this.expr();
    if (
      this.current &&
      ["EQ", "NE", "LE", "GE", "LT", "GT"].includes(this.current[0])
    ) {
      const op = this.current[1];
      this.eat(this.current[0]);
      const right = this.expr();
      const temp = this.newTemp();
      this.codegen.binaryOp(temp, op, left, right);
      return temp;
    }
    return left;
  }
}
