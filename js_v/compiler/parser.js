import { CodeGenerator } from "./codegen.js";

export class Parser {
  constructor(tokens) {
    this.tokens = tokens;
    this.pos = 0;
    this.currentToken = this.tokens[this.pos] || null;
    this.codegen = new CodeGenerator();
  }

  next() {
    this.pos++;
    this.currentToken = this.tokens[this.pos] || null;
  }

  eat(type) {
    if (this.currentToken && this.currentToken[0] === type) {
      this.next();
    } else {
      throw new Error(`Expected ${type} but got ${this.currentToken}`);
    }
  }

  parse() {
    this.program();
    return this.codegen.getCode();
  }

  program() {
    this.stmtList();
  }

  stmtList() {
    while (this.currentToken && (this.currentToken[0] === "KEYWORD" || this.currentToken[0] === "ID")) {
      this.stmt();
    }
  }

  stmt() {
    const val = this.currentToken[1];
    if (val === "let") this.decl();
    else if (val === "print") this.printStmt();
    else if (val === "if") this.ifStmt();
    else if (val === "while") this.whileStmt();
    else if (this.currentToken[0] === "ID") this.assign();
    else throw new Error(`Unexpected statement: ${val}`);
  }

  decl() {
    this.eat("KEYWORD");
    const varName = this.currentToken[1];
    this.eat("ID");
    this.eat("ASSIGN");
    const val = this.expr();
    this.codegen.emit(`${varName} = ${val}`);
    this.eat("SEMI");
  }

  assign() {
    const varName = this.currentToken[1];
    this.eat("ID");
    this.eat("ASSIGN");
    const val = this.expr();
    this.codegen.emit(`${varName} = ${val}`);
    this.eat("SEMI");
  }

  printStmt() {
    this.eat("KEYWORD");
    this.eat("LPAREN");
    const val = this.expr();
    this.eat("RPAREN");
    this.eat("SEMI");
    this.codegen.emit(`print(${val})`);
  }

  ifStmt() {
    this.eat("KEYWORD");
    this.eat("LPAREN");
    const cond = this.cond();
    this.eat("RPAREN");

    const labelElse = this.codegen.newLabel();
    const labelEnd = this.codegen.newLabel();

    this.codegen.emit(`if_false ${cond} goto ${labelElse}`);

    this.eat("LBRACE");
    this.stmtList();
    this.eat("RBRACE");

    this.codegen.emit(`goto ${labelEnd}`);
    this.codegen.emit(`${labelElse}:`);

    if (this.currentToken && this.currentToken[1] === "else") {
      this.eat("KEYWORD");
      this.eat("LBRACE");
      this.stmtList();
      this.eat("RBRACE");
    }

    this.codegen.emit(`${labelEnd}:`);
  }

  whileStmt() {
    this.eat("KEYWORD");
    const labelStart = this.codegen.newLabel();
    const labelEnd = this.codegen.newLabel();

    this.codegen.emit(`${labelStart}:`);

    this.eat("LPAREN");
    const cond = this.cond();
    this.eat("RPAREN");

    this.codegen.emit(`if_false ${cond} goto ${labelEnd}`);
    this.eat("LBRACE");
    this.stmtList();
    this.eat("RBRACE");

    this.codegen.emit(`goto ${labelStart}`);
    this.codegen.emit(`${labelEnd}:`);
  }

  expr() {
    let left = this.term();
    return this.exprPrime(left);
  }

  exprPrime(inherited) {
    while (
      this.currentToken &&
      ["PLUS", "MINUS"].includes(this.currentToken[0])
    ) {
      const op = this.currentToken[1];
      this.eat(this.currentToken[0]);
      const right = this.term();
      const temp = this.codegen.newTemp();
      this.codegen.emit(`${temp} = ${inherited} ${op} ${right}`)
      // this.codegen.binaryOp(temp, op, inherited, right);
      inherited = temp;
    }
    return inherited;
  }

  term() {
    let left = this.factor();
    return this.termPrime(left);
  }

  termPrime(inherited) {
    while (
      this.currentToken &&
      ["MULT", "DIV"].includes(this.currentToken[0])
    ) {
      const op = this.currentToken[1];
      this.eat(this.currentToken[0]);
      const right = this.factor();
      const temp = this.codegen.newTemp();
      this.codegen.emit(`${temp} = ${inherited} ${op} ${right}`)
      // this.codegen.binaryOp(temp, op, inherited, right);
      inherited = temp;
    }
    return inherited;
  }

  factor() {
    if (this.currentToken[0] === "MINUS") {
      this.eat("MINUS")
      const val = this.factor()
      const temp = this.codegen.newTemp()
      this.codegen.emit(`${temp} = -${val}`)
      return temp;
    }

    if (this.currentToken[0] === "ID") {
      const val = this.currentToken[1];
      this.eat("ID");
      return val;
    } else if (this.currentToken[0] === "NUMBER") {
      const val = this.currentToken[1];
      this.eat("NUMBER");
      return val;
    } else if (this.currentToken[0] === "LPAREN") {
      this.eat("LPAREN");
      const val = this.expr();
      this.eat("RPAREN");
      return val;
    } else {
      throw new Error(`Unexpected factor: ${this.currentToken}`);
    }
  }

  cond() {
    return this.orExpr();
  }

  orExpr() {
    let left = this.andExpr();
    return this.orExprPrime(left);
  }

  orExprPrime(inherited) {
    while (this.currentToken && this.currentToken[1] === "or") {
      this.eat("KEYWORD");
      const right = this.andExpr();
      const temp = this.codegen.newTemp();
      this.codegen.emit(`${temp} = ${inherited} or ${right}`)
      // this.codegen.binaryOp(temp, "or", inherited, right);
      inherited = temp;
    }
    return inherited;
  }

  andExpr() {
    let left = this.notExpr();
    return this.andExprPrime(left);
  }

  andExprPrime(inherited) {
    while (this.currentToken && this.currentToken[1] === "and") {
      this.eat("KEYWORD");
      const right = this.notExpr();
      const temp = this.codegen.newTemp();
      this.codegen.emit(`${temp} = ${inherited} and ${right}`)
      // this.codegen.binaryOp(temp, "and", inherited, right);
      inherited = temp;
    }
    return inherited;
  }

  notExpr() {
    if (this.currentToken && this.currentToken[1] === "not") {
      this.eat("KEYWORD");
      const val = this.notExpr();
      const temp = this.codegen.newTemp();
      this.codegen.emit(`${temp} = not ${val}`)
      // this.codegen.binaryOp(temp, "not", val);
      return temp;
    } else {
      return this.relExpr();
    }
  }

  relExpr() {
    const left = this.boolPrimary();
    return this.relExprPrime(left);
  }

  relExprPrime(inherited) {
    if (this.currentToken && ["EQ", "NE", "LE", "GE", "LT", "GT"].includes(this.currentToken[0])) {
      const op = this.currentToken[1];
      this.eat(this.currentToken[0]);
      const right = this.boolPrimary();
      const temp = this.codegen.newTemp();
      this.codegen.emit(`${temp} = ${inherited} ${op} ${right}`)
      // this.codegen.binaryOp(temp, op, inherited, right);
      return temp;
    }
    return inherited;
  }

  boolPrimary() {
    if (this.currentToken[1] === "true" || this.currentToken[1] === "false") {
      const val = this.currentToken[1];
      this.eat("KEYWORD");
      return val;
    } else if (this.currentToken[0] === "LPAREN") {
      this.eat("LPAREN");
      const val = this.cond();
      this.eat("RPAREN");
      return val;
    } else {
      return this.expr();
    }
  }
}
