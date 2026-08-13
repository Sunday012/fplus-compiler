# F+ Lexer Design

## Identifier

Regular expression:

```regex
[A-Za-z][A-Za-z0-9]*
```

Simplified expression:

```regex
L(L|D)*
```

Where:

L represents a letter.
D represents a digit.

The first character must be a letter. After the first letter, the identifier
may contain zero or more letters or digits.

### DFA transition table

| Current state | Letter | Digit | Invalid character |
|---|---|---|---|
| `q0` | `q1` | `trap` | `trap` |
| `q1` | `q1` | `q1` | `trap` |
| `trap` | `trap` | `trap` | `trap` |

- Start state: `q0`
- Accepting state: `q1`
- Dead state: `trap`

### Accepted examples

```text
x
age
student2
Total10
```

### Rejected examples

```text
2ndStudent  
student_name

## Integer literal

Regular expression:

```regex
[0-9]+
```

Simplified expression:

```text
D+
```

Where `D` represents any digit from `0` to `9`.

The first digit moves the automaton from the starting state to the accepting
state. Every additional digit keeps it in the accepting state.

### DFA transition table

| Current state | Digit | Non-digit |
|---|---|---|
| `q0` | `q1` | `trap` |
| `q1` | `q1` | `trap` |
| `trap` | `trap` | `trap` |

- Start state: `q0`
- Accepting state: `q1`
- Dead state: `trap`

### Accepted examples

```text
0
7
19
250
```

### Rejected examples

```text
age
10.5
```

## Whitespace

Regular expression:

```regex
[ \t\r\n]+
```

Simplified expression:

```text
W+
```

Where `W` represents a space, tab, carriage return, or newline.

### DFA transition table

| Current state | Whitespace | Non-whitespace |
|---|---|---|
| `q0` | `q1` | `trap` |
| `q1` | `q1` | `trap` |
| `trap` | `trap` | `trap` |

- Start state: `q0`
- Accepting state: `q1`
- Dead state: `trap`

### Lexer action

Whitespace is recognised but does not produce a token. It is discarded after
the lexer updates its line and column position.

Newline characters increment the line number and reset the column position.