Wordlebrain Changelog
=====================

1.1.1
-----
* Fixed bug in handling `n` hints (letter not in word) that sometimes allowed eliminated words to be included
  in recommendations. 
* Added starting recommendation of `CARES` (see readme).
* Updated README.md with new thoughts on guessing strategy.

1.1.0
-----
* Changed scoring method to score better relative to the current set of constraints.  The old scoring method scored the words relative to the global word list.
* Fixed a bug in the `show` command in the CLI.
* Improved CLI error handling.

1.0
---
First release. Basic functionality.