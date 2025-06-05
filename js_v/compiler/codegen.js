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
    return `t${++this.tempCount}`;
  }

  newLabel() {
    return `L${++this.labelCount}`;
  }

  getCode() {
    return this.code;
  }
}
