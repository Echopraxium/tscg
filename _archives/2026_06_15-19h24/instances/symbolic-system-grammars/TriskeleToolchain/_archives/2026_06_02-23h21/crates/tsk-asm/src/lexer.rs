// tsk-asm/src/lexer.rs
// Author: Echopraxium with the collaboration of Claude AI
// Version: 0.2.0
//
// Tokenizer for .tasm assembly source files.
// One pass — produces a flat token stream consumed by the parser.

#[derive(Debug, Clone, PartialEq)]
pub enum Token {
    // Identifiers and keywords
    Ident(String),          // opcode, label ref, directive name
    Label(String),          // "foo:" — the label definition itself
    Register(u8),           // R0..R31, FP, SP, LR, PC

    // Literals
    Integer(i64),           // decimal, hex (0x...), Base16 Triskele (#...)
    StringLit(String),      // "hello\n"
    CharLit(u8),            // 'A'

    // Punctuation
    Comma,
    Colon,
    LParen,
    RParen,

    // Directives (leading dot)
    Directive(String),      // .module .type .entry .section .define etc.

    // Preprocessor (leading #)
    Define,                 // #define
    Undef,                  // #undef
    Include,                // #include
    Ifdef,                  // #ifdef
    Ifndef,                 // #ifndef
    Endif,                  // #endif
    ErrorDir,               // #error

    // End of line / end of file (significant for one-stmt-per-line rule)
    Newline,
    Eof,
}

#[derive(Debug, Clone)]
pub struct Span {
    pub line: usize,
    #[allow(dead_code)]
    pub col:  usize,
}

#[derive(Debug, Clone)]
pub struct Spanned {
    pub token: Token,
    pub span:  Span,
}

pub struct Lexer<'a> {
    src:  &'a str,
    pos:  usize,
    line: usize,
    col:  usize,
}

impl<'a> Lexer<'a> {
    pub fn new(src: &'a str) -> Self {
        Self { src, pos: 0, line: 1, col: 1 }
    }

    pub fn tokenize(mut self) -> anyhow::Result<Vec<Spanned>> {
        let mut tokens = Vec::new();
        loop {
            self.skip_spaces();
            if self.pos >= self.src.len() {
                tokens.push(Spanned { token: Token::Eof, span: self.span() });
                break;
            }
            let ch = self.peek();

            // Comment: ; to end of line
            if ch == ';' {
                self.skip_line();
                tokens.push(Spanned { token: Token::Newline, span: self.span() });
                continue;
            }

            // Newline
            if ch == '\n' || ch == '\r' {
                self.skip_newline();
                tokens.push(Spanned { token: Token::Newline, span: self.span() });
                continue;
            }

            // Line continuation backslash
            if ch == '\\' && self.peek_at(1) == '\n' {
                self.advance(); self.advance();
                continue;
            }

            let span = self.span();

            // Directive: .something
            if ch == '.' {
                self.advance();
                let name = self.read_ident();
                tokens.push(Spanned { token: Token::Directive(name), span });
                continue;
            }

            // Preprocessor: #something
            if ch == '#' {
                self.advance();
                // Base16 Triskele literal: #A_St_F etc.
                if self.peek().is_alphabetic() || self.peek() == '_' {
                    let word = self.read_ident();
                    // Check if it's a preprocessor keyword
                    let tok = match word.as_str() {
                        "define"  => Token::Define,
                        "undef"   => Token::Undef,
                        "include" => Token::Include,
                        "ifdef"   => Token::Ifdef,
                        "ifndef"  => Token::Ifndef,
                        "endif"   => Token::Endif,
                        "error"   => Token::ErrorDir,
                        _ => {
                            // Base16 Triskele literal: word contains e.g. "F_A"
                            let val = parse_base16_triskele(&word)?;
                            Token::Integer(val)
                        }
                    };
                    tokens.push(Spanned { token: tok, span });
                    continue;
                }
                return Err(anyhow::anyhow!("{}:{}: unexpected '#'", self.line, self.col));
            }

            // String literal
            if ch == '"' {
                self.advance();
                let s = self.read_string()?;
                tokens.push(Spanned { token: Token::StringLit(s), span });
                continue;
            }

            // Char literal
            if ch == '\'' {
                self.advance();
                let c = self.read_char()?;
                tokens.push(Spanned { token: Token::CharLit(c), span });
                continue;
            }

            // Numeric literal
            if ch.is_ascii_digit() || (ch == '-' && self.peek_at(1).is_ascii_digit()) {
                let n = self.read_number()?;
                tokens.push(Spanned { token: Token::Integer(n), span });
                continue;
            }

            // Punctuation
            match ch {
                ',' => { self.advance(); tokens.push(Spanned { token: Token::Comma, span }); continue; }
                ':' => { self.advance(); tokens.push(Spanned { token: Token::Colon, span }); continue; }
                '(' => { self.advance(); tokens.push(Spanned { token: Token::LParen, span }); continue; }
                ')' => { self.advance(); tokens.push(Spanned { token: Token::RParen, span }); continue; }
                _ => {}
            }

            // Identifier, register, opcode, or label
            if ch.is_alphabetic() || ch == '_' {
                let ident = self.read_ident();

                // Check for label definition (next non-space char is ':')
                self.skip_spaces();
                if self.peek() == ':' {
                    self.advance(); // consume ':'
                    tokens.push(Spanned { token: Token::Label(ident), span });
                    continue;
                }

                // Register?
                if let Some(reg) = parse_register(&ident) {
                    tokens.push(Spanned { token: Token::Register(reg), span });
                    continue;
                }

                tokens.push(Spanned { token: Token::Ident(ident), span });
                continue;
            }

            return Err(anyhow::anyhow!(
                "{}:{}: unexpected character '{}'", self.line, self.col, ch
            ));
        }
        Ok(tokens)
    }

    // ── Helpers ───────────────────────────────────────────────────────────────

    fn peek(&self) -> char { self.src[self.pos..].chars().next().unwrap_or('\0') }
    fn peek_at(&self, offset: usize) -> char {
        self.src[self.pos..].chars().nth(offset).unwrap_or('\0')
    }

    fn advance(&mut self) -> char {
        let ch = self.peek();
        self.pos += ch.len_utf8();
        if ch == '\n' { self.line += 1; self.col = 1; } else { self.col += 1; }
        ch
    }

    fn span(&self) -> Span { Span { line: self.line, col: self.col } }

    fn skip_spaces(&mut self) {
        while self.pos < self.src.len() {
            let ch = self.peek();
            if ch == ' ' || ch == '\t' { self.advance(); } else { break; }
        }
    }

    fn skip_line(&mut self) {
        while self.pos < self.src.len() && self.peek() != '\n' { self.advance(); }
    }

    fn skip_newline(&mut self) {
        if self.peek() == '\r' { self.advance(); }
        if self.peek() == '\n' { self.advance(); }
    }

    fn read_ident(&mut self) -> String {
        let mut s = String::new();
        while self.pos < self.src.len() {
            let ch = self.peek();
            if ch.is_alphanumeric() || ch == '_' { s.push(self.advance()); } else { break; }
        }
        s
    }

    fn read_number(&mut self) -> anyhow::Result<i64> {
        let neg = if self.peek() == '-' { self.advance(); true } else { false };
        // Hex: 0x...
        if self.peek() == '0' && (self.peek_at(1) == 'x' || self.peek_at(1) == 'X') {
            self.advance(); self.advance();
            let mut s = String::new();
            while self.pos < self.src.len() {
                let ch = self.peek();
                if ch.is_ascii_hexdigit() || ch == '_' {
                    if ch != '_' { s.push(ch); }
                    self.advance();
                } else { break; }
            }
            let v = i64::from_str_radix(&s, 16)
                .map_err(|_| anyhow::anyhow!("invalid hex literal: 0x{}", s))?;
            return Ok(if neg { -v } else { v });
        }
        // Decimal
        let mut s = String::new();
        while self.pos < self.src.len() {
            let ch = self.peek();
            if ch.is_ascii_digit() || ch == '_' {
                if ch != '_' { s.push(ch); }
                self.advance();
            } else { break; }
        }
        let v = s.parse::<i64>()
            .map_err(|_| anyhow::anyhow!("invalid integer: {}", s))?;
        Ok(if neg { -v } else { v })
    }

    fn read_string(&mut self) -> anyhow::Result<String> {
        let mut s = String::new();
        loop {
            if self.pos >= self.src.len() {
                return Err(anyhow::anyhow!("unterminated string literal"));
            }
            let ch = self.advance();
            if ch == '"' { break; }
            if ch == '\\' {
                match self.advance() {
                    'n'  => s.push('\n'),
                    't'  => s.push('\t'),
                    'r'  => s.push('\r'),
                    '0'  => s.push('\0'),
                    '\\' => s.push('\\'),
                    '"'  => s.push('"'),
                    c    => s.push(c),
                }
            } else {
                s.push(ch);
            }
        }
        Ok(s)
    }

    fn read_char(&mut self) -> anyhow::Result<u8> {
        let ch = if self.peek() == '\\' {
            self.advance();
            match self.advance() {
                'n'  => b'\n',
                't'  => b'\t',
                'r'  => b'\r',
                '0'  => b'\0',
                '\\' => b'\\',
                '\'' => b'\'',
                c    => c as u8,
            }
        } else {
            self.advance() as u8
        };
        if self.peek() != '\'' {
            return Err(anyhow::anyhow!("unterminated char literal"));
        }
        self.advance();
        Ok(ch)
    }
}

// ─────────────────────────────────────────────────────────────────────────────
// Register parsing
// ─────────────────────────────────────────────────────────────────────────────

pub fn parse_register(s: &str) -> Option<u8> {
    let upper = s.to_uppercase();
    match upper.as_str() {
        "FP" => return Some(28),
        "SP" => return Some(29),
        "LR" => return Some(30),
        "PC" => return Some(31),
        _ => {}
    }
    // R0..R31 (case-insensitive)
    if upper.starts_with('R') {
        if let Ok(n) = upper[1..].parse::<u8>() {
            if n < 32 { return Some(n); }
        }
    }
    None
}

// ─────────────────────────────────────────────────────────────────────────────
// Base16 Triskele literal parser: #A_St_F → 0x012
// ─────────────────────────────────────────────────────────────────────────────

pub fn parse_base16_triskele(s: &str) -> anyhow::Result<i64> {
    // s is the part after '#', e.g. "F_A" or "St_Im_A_A"
    // Each token maps to a 4-bit nibble
    let parts: Vec<&str> = s.split('_').collect();
    let mut result: i64 = 0;
    for part in &parts {
        let nibble = match *part {
            "A"   => 0x0,
            "S" | "St" => 0x1,
            "F"   => 0x2,
            "It"  => 0x3,
            "D"   => 0x4,
            "R"   => 0x5,
            "E"   => 0x6,
            "V"   => 0x7,
            "O"   => 0x8,
            "Im"  => 0x9,
            "T"   => 0xA,
            "POS" | "Pos" => 0xB,
            "NEG" | "Neg" => 0xC,
            "K"   => 0xD,
            "Ss"  => 0xE,
            "L"   => 0xF,
            other => return Err(anyhow::anyhow!("unknown Base16 primitive: '{}'", other)),
        };
        result = (result << 4) | nibble;
    }
    Ok(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_lex_simple() {
        let src = "D_MOV_I R0, 72\nF_HALT\n";
        let tokens: Vec<_> = Lexer::new(src).tokenize().unwrap()
            .into_iter().map(|s| s.token).collect();
        assert!(matches!(&tokens[0], Token::Ident(s) if s == "D_MOV_I"));
        assert!(matches!(&tokens[1], Token::Register(0)));
        assert!(matches!(&tokens[2], Token::Comma));
        assert!(matches!(&tokens[3], Token::Integer(72)));
        assert!(matches!(&tokens[4], Token::Newline));
    }

    #[test]
    fn test_lex_label() {
        let src = "main:\n  F_HALT\n";
        let tokens: Vec<_> = Lexer::new(src).tokenize().unwrap()
            .into_iter().map(|s| s.token).collect();
        assert!(matches!(&tokens[0], Token::Label(s) if s == "main"));
    }

    #[test]
    fn test_lex_hex() {
        let src = "D_MOV_I R0, 0xFF\n";
        let tokens: Vec<_> = Lexer::new(src).tokenize().unwrap()
            .into_iter().map(|s| s.token).collect();
        assert!(matches!(&tokens[3], Token::Integer(0xFF)));
    }

    #[test]
    fn test_base16_triskele() {
        assert_eq!(parse_base16_triskele("F_A").unwrap(), 0x20);
        assert_eq!(parse_base16_triskele("St_Im_A_A").unwrap(), 0x1900);
        assert_eq!(parse_base16_triskele("L").unwrap(), 0xF);
    }

    #[test]
    fn test_lex_comment() {
        let src = "F_HALT ; this is a comment\n";
        let tokens: Vec<_> = Lexer::new(src).tokenize().unwrap()
            .into_iter().map(|s| s.token).collect();
        assert!(matches!(&tokens[0], Token::Ident(s) if s == "F_HALT"));
        assert!(matches!(&tokens[1], Token::Newline));
    }

    #[test]
    fn test_lex_char_literal() {
        let src = "D_MOV_I R0, 'H'\n";
        let tokens: Vec<_> = Lexer::new(src).tokenize().unwrap()
            .into_iter().map(|s| s.token).collect();
        // 'H' = 72 — lexed as CharLit(72), which assembler converts to Integer(72)
        assert!(matches!(&tokens[3], Token::CharLit(72)), "expected CharLit(72), got {:?}", &tokens[3]);
    }
}
