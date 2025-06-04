export function tokenize(input) {
  const keywords = new Set(['let', 'if', 'else', 'while', 'print', 'true', 'false', 'not', 'and', 'or']);
  const tokenSpecs = [
    ['NUMBER',    /\d+(\.\d+)?([eE][+-]?\d+)?/y],
    ['ID',        /[a-zA-Z_][a-zA-Z0-9_]*/y],
    ['EQ',        /==/y],
    ['NE',        /!=/y],
    ['LE',        /<=/y],
    ['GE',        />=/y],
    ['ASSIGN',    /=/y],
    ['LT',        /</y],
    ['GT',        />/y],
    ['PLUS',      /\+/y],
    ['MINUS',     /-/y],
    ['MULT',      /\*/y],
    ['DIV',       /\//y],
    ['LPAREN',    /\(/y],
    ['RPAREN',    /\)/y],
    ['LBRACE',    /\{/y],
    ['RBRACE',    /\}/y],
    ['SEMI',      /;/y],
    ['SKIP',      /[ \t\r\n]+/y],
    ['MISMATCH',  /./y]
  ];

  const tokens = [];
  let pos = 0;

  while (pos < input.length) {
    let match = false;
    for (const [type, regex] of tokenSpecs) {
      regex.lastIndex = pos;
      const result = regex.exec(input);
      if (result) {
        const value = result[0];
        match = true;

        if (type === 'SKIP') {
          pos += value.length;
          break;
        }

        if (type === 'ID' && keywords.has(value)) {
          tokens.push(['KEYWORD', value]);
        } else if (type === 'MISMATCH') {
          throw new SyntaxError(`Illegal token at position ${pos}: ${value}`);
        } else {
          tokens.push([type, value]);
        }

        pos += value.length;
        break;
      }
    }

    if (!match) {
      throw new SyntaxError(`Unexpected character at position ${pos}: '${input[pos]}'`);
    }
  }

  return tokens;
}
