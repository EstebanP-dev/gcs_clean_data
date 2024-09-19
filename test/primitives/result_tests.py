import unittest
from src.primitives.result import *


class ResultTests(unittest.TestCase):
    def test_success_result(self):
        value = "success value"
        result = Result.success(value)

        self.assertTrue(result.is_success)
        self.assertFalse(result.is_failure)
        self.assertEqual(result.value, value)
        self.assertEqual(result.first_error, Result.NO_ERRORS)

    def test_failure_result_with_single_error(self):
        error = Error.custom(400, "Error message")
        result = Result.failure(error)

        self.assertFalse(result.is_success)
        self.assertTrue(result.is_failure)
        self.assertIsNone(result.value)
        self.assertEqual(result.first_error, error)

    def test_failure_result_with_multiple_errors(self):
        errors = [Error.custom(400, "Error 1"), Error.custom(500, "Error 2")]
        result = Result.failure(errors)

        self.assertFalse(result.is_success)
        self.assertTrue(result.is_failure)
        self.assertIsNone(result.value)
        self.assertEqual(result.first_error, errors[0])

    def test_result_equality(self):
        result1 = Result.success("value")
        result2 = Result.success("value")
        self.assertEqual(result1, result2)

        result3 = Result.failure([Error.custom(400, "Error")])
        result4 = Result.failure([Error.custom(400, "Error")])
        self.assertEqual(result3, result4)

        self.assertNotEqual(result1, result3)

    def test_result_errors_property(self):
        error1 = Error.custom(400, "Error 1")
        error2 = Error.custom(500, "Error 2")
        result = Result.failure([error1, error2])

        self.assertIn(error1, result.errors)
        self.assertIn(error2, result.errors)
        self.assertEqual(len(result.errors), 2)


if __name__ == '__main__':
    unittest.main()
