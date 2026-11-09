# Changes to Question 1

This note is for whoever wrote `Question1_Group109.ipynb`. It lists every edit
made to the notebook.

**No code was changed.** Every code cell and every saved output is exactly as
you wrote and ran it, including the recorded game in the last cell. Only
text (markdown) cells were edited, so the notebook doesn't need to be re-run.

If you keep working on your own copy, take this version first, or copy the
text cells across. The code is the same in both.

## Why it was edited (2026-11-09)

A strict review against the assignment found that the code meets every
requirement and has no bugs. The gaps were in the write-up:

1. The Contributors line was empty.
2. The question has parts (a), (b) and (c), but the notebook didn't label
   them, so a grader would have to hunt for each answer.
3. Part (a) asks you to justify the evaluation weights. The justification
   was only a few sentences long.
4. Part (a) also asks you to explain the evaluation with a sample game
   state. The sample state's score was computed by code but not explained
   in words.

## What changed, cell by cell

Cells are listed in notebook order, by their heading in your original.

| # | Cell (original heading) | What changed |
|--:|:--|:--|
| 1 | Title cell | Filled in Contributors with a table of names, BITS IDs and contribution. Added "(Group 109)" to the Assignment line. Added a table at the end showing where parts (a), (b) and (c) are answered. |
| 2 | Board representation and game design | Heading only, now "Part (c): Board representation and game design". |
| 3 | Static evaluation and choice of weights | Heading is now "Part (a): Static evaluation design and choice of weights". The opening paragraphs and the weights table are unchanged. The text after the table was replaced by a new "Why these weights" section (old text quoted below). |
| 4 | Fixed-depth search | Heading only, now "Part (c): Fixed-depth Minimax search". |
| 5 | Human input and alternating game loop | Was a level-3 heading on its own. Now a level-2 heading, "Part (b): Human input and alternating game loop", with four lines describing `read_human_column` and `play_game`. |
| 6 | Worked game state and tactical decision | Heading only, now "Part (a): Worked sample game state". |
| 7 | Cell after the worked example (starts "The chosen move blocks column 4") | The first two sentences were replaced by a new "Reading the static score by hand" table and explanation. The rest of the cell, from "The same search also takes an immediate computer win" through the Verification section, is unchanged. |
| 8 | Complete sample game | Heading only, now "Part (b): Complete sample game". |
| 9 | Limits and conclusion | Only the last heading changed: "Play against the computer" is now "Part (b): Play against the computer". |

## Original text that was replaced

Your wording is kept here so nothing is lost.

**Cell 1, Contributors line (was empty):**

> \*\*Contributors:\*\*

**Cell 3, the text after the weights table:**

> Each computer disc in the centre column adds 6; each human disc there subtracts 6.
> The centre belongs to more potential winning lines. Three-disc threats receive
> much more weight than pairs. Slightly larger human penalties favour defence in
> otherwise similar positions. A forced win still takes priority because terminal
> scores dominate every heuristic score.
>
> The maximum absolute window contribution is 150, so a conservative nonterminal
> bound is 69 * 150 + 6 * 6 = 10,386. This is far below 1,000,000. Mixed windows
> cannot become a four for either player and contribute zero. The heuristic does
> not treat an unsupported empty cell as an immediate winning move; it is only a
> positional estimate. Legal move simulation and terminal checks determine actual
> tactical wins.

The new section keeps every point from this text. The first sentence and the
10,386 bound are kept word for word.

**Cell 7, the first two sentences:**

> The chosen move blocks column 4. Every other move lets the human win on the next
> turn and receives a terminal loss score.

The new explanation says the same thing, with the actual scores (+118 for
column 4, -1,000,001 for every other column).

## What the new text says

**"Why these weights" (cell 3)** gives one reason for each design choice:

- Only windows holding one player's discs score, because a mixed window can
  never become a four.
- Scores rise steeply (2, 12, 120) because a three is one move from a win.
  One open three is worth as much as ten open pairs.
- Human pairs and threes weigh 25% more (15 and 150 against 12 and 120). A
  depth-3 search always ends with the human to move, so a human three at
  the end of the search can be completed on the very next move.
- The centre column gets a bonus of 6 per disc. Its cells lie in 7 to 13 of
  the 69 possible lines, while edge cells lie in only 3 to 5.
- Wins and losses always outrank the heuristic, which can't exceed 10,386.
- Known limit: the heuristic doesn't check whether a three's empty cell can
  be played right away.

**"Reading the static score by hand" (cell 7)** breaks the sample board's
score into the 15 lines that score on it:

| Lines | Score |
|:--|--:|
| Human three on the bottom row | -150 |
| Human pair on the bottom row | -15 |
| 7 lines with one human disc | -14 |
| Computer pair in column 7 | +12 |
| 5 lines with one computer disc | +10 |
| Centre column (empty) | 0 |
| **Total** | **-157** |

Each line was checked by hand against the code's output.

## Testing after the edits

- All 52 of the notebook's own checks still pass, including the 8 comparisons
  with plain (unpruned) depth-3 Minimax.
- Extra tests, run outside the notebook and not added to it:
  - 300 games against a human playing random moves. The computer won all
    300, never missed an immediate win and never failed to block a single
    threat. The slowest move took about 27 ms.
  - A full game played to a draw. The game loop announces the draw correctly.

## Left as it was

- The search uses alpha-beta pruning, not plain Minimax. That's fine,
  because the notebook already shows it picks the same moves.
- The human always moves first.
- The notebook's own checks don't play a game through to a draw. The extra
  draw test above covers it.

## Not in this repository yet

- Question 2: one individual PDF per member, named by BITS ID.
