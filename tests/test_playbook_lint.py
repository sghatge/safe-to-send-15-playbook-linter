import unittest

from playbook_lint import lint, score


class PlaybookLintTest(unittest.TestCase):
    def test_before_fails(self):
        with open("examples/presend_check_before.md", encoding="utf-8") as fh:
            f = lint(fh.read())
        self.assertEqual({d for k, d in f if k == "missing"}, {"trigger", "guardrails", "steps", "output"})
        self.assertLess(score(f), 50)

    def test_after_is_clean(self):
        with open("examples/presend_check_after.md", encoding="utf-8") as fh:
            self.assertEqual(lint(fh.read()), [])

    def test_vague_word_found_with_line(self):
        f = lint("## When to use\nx\n## Never\nx\n1. Fix it as needed\n## Output\nx")
        self.assertEqual(f, [("vague", "line 5: 'as needed' -> 1. Fix it as needed")])


if __name__ == "__main__":
    unittest.main()
