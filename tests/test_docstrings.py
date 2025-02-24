import pytest
from pytest_examples import find_examples, CodeExample, EvalExample


# --------------------------------------------------------------------------- #
# API                                                                         #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./planck"), ids=str)
def test_docstrings_api(example: CodeExample, eval_example: EvalExample):
    if eval_example.update_examples:
        eval_example.format(example)
        eval_example.run_print_update(example)
    else:
        eval_example.lint(example)
        eval_example.run_print_check(
            example,
        )


# --------------------------------------------------------------------------- #
# Markdowns                                                                   #
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize("example", find_examples("./docs/"), ids=str)
def test_docstrings_markdown(example: CodeExample, eval_example: EvalExample):
    """
    Examples in markdown documentation.
    """
    if eval_example.update_examples:
        eval_example.format(example)
        eval_example.run_print_update(example)

    else:
        eval_example.lint(example)
        eval_example.run_print_check(example)
