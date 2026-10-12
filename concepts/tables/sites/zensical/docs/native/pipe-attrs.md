---
title: Pipe table class and id
---

Case 1: a class and an id, comment on the line directly above.

<!-- table: .table-compact #probe-one -->
| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 2: two classes, a blank line between the comment and the table.

<!-- table: .table-compact .table-striped #probe-two -->

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 3: an unrelated comment above the table changes nothing.

<!-- an ordinary comment -->
| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 4: a table in a list item.

1. A step with a table:

    <!-- table: .table-compact #probe-four -->
    | Key | Value | Notes |
    | --- | --- | --- |
    | `a` | 1 | first |
    | `b` | 2 | second |

Case 5: no comment, as before.

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 6: the syntax shown in a code block stays as written.

```markdown
<!-- table: .table-compact #probe-six -->
| Key | Value |
| --- | --- |
```

Case 7: the comment above a title, a blank line between them.

<!-- table: .table-compact #probe-seven -->

**Title seven**

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 8: the comment directly above a title.

<!-- table: .table-compact #probe-eight -->
**Title eight**

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 9: a normal paragraph between the comment and the table.

<!-- table: .table-compact #probe-nine -->

A normal paragraph, not a title.

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 10: a title without a comment.

**Title ten**

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 11: two titles between the comment and the table.

<!-- table: .table-compact #probe-eleven -->

**Title eleven**

**Title eleven again**

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 12: a title above the comment, the comment directly above the table.

**Title twelve**

<!-- table: .table-compact #probe-twelve -->
| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 13: a title with more than bold text.

<!-- table: .table-compact #probe-thirteen -->

**Title thirteen** and more text

| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |

Case 14: the standard class named as well.

<!-- table: .table .table-compact #probe-fourteen -->
| Key | Value | Notes |
| --- | --- | --- |
| `a` | 1 | first |
| `b` | 2 | second |
