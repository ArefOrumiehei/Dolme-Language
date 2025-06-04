export class CodeGenerator {
  constructor() {
    this.code = [];
    this.tempCount = 0;
    this.labelCount = 0;
  }

  emit(instruction) {
    this.code.push(instruction);
  }

  newTemp() {
    return `_t${++this.tempCount}`;
  }

  newLabel() {
    return `_L${++this.labelCount}`;
  }

  assign(varName, value) {
    this.emit(`${varName} = ${value}`);
  }

  binaryOp(instruction) {
    this.emit(instruction);
  }

  print(value) {
    this.emit(`print ${value}`);
  }

  ifFalse(condition, label) {
    this.emit(`ifFalse ${condition} goto ${label}`);
  }

  goto(label) {
    this.emit(`goto ${label}`);
  }

  label(label) {
    this.emit(`${label}:`);
  }

  getCode() {
    return this.code;
  }
}
