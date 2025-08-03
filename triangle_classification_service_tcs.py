"""
FOCUSED TEST SUITE - Triangle Classification Service
QA Focus: Existing test cases + Failure scenarios + Input manipulation

TEST CATEGORIES:
1. Valid Triangle Classification (From original test cases)
2. Invalid Triangle Detection (Failure scenarios)
3. Console Input Manipulation & Edge Cases
4. Error Handling Verification

Testing Framework: pytest with focused coverage
"""

import pytest
import math
from unittest.mock import patch
from typing import List, Tuple, Optional
from dataclasses import dataclass

from triangle_classification_service import (
    TriangleType, 
    TriangleClassificationService, 
    TriangleValidationService,
    TriangleRequest,
    TriangleConsoleController,
    TriangleApplicationService,
    InMemoryTriangleRepository,
    ServiceContainer
)


@dataclass
class TestCase:
    """Test Case Structure"""
    id: str
    description: str
    sides: Tuple[float, float, float]
    expected_type: Optional[TriangleType]
    should_fail: bool = False
    expected_error: Optional[str] = None
    category: str = ""
    notes: str = ""


@dataclass
class InputTestCase:
    """Input Test Case Structure"""
    id: str
    description: str
    inputs: List[str]
    should_succeed: bool = True
    expected_error: Optional[str] = None


class TestDataGenerator:
    """Enhanced test data generator with failure cases"""
    
    @staticmethod
    def generate_equilateral_cases() -> List[TestCase]:
        """Original equilateral cases"""
        return [
            TestCase("EQ001", "Standard equilateral", (5, 5, 5), TriangleType.EQUILATERAL, category="basic"),
            TestCase("EQ002", "Minimum valid equilateral", (1, 1, 1), TriangleType.EQUILATERAL, category="basic"),
            TestCase("EQ003", "Large equilateral", (1000, 1000, 1000), TriangleType.EQUILATERAL, category="basic"),
            TestCase("EQ004", "Decimal equilateral", (3.14159, 3.14159, 3.14159), TriangleType.EQUILATERAL, category="precision"),
            TestCase("EQ005", "Small decimal equilateral", (0.001, 0.001, 0.001), TriangleType.EQUILATERAL, category="precision"),
            TestCase("EQ006", "Float precision limit", (0.1 + 0.2, 0.1 + 0.2, 0.1 + 0.2), TriangleType.EQUILATERAL, category="floating_point"),
        ]
    
    @staticmethod
    def generate_isosceles_cases() -> List[TestCase]:
        """Original isosceles cases"""
        return [
            TestCase("IS001", "Standard isosceles (A=B)", (5, 5, 3), TriangleType.ISOSCELES, category="basic_ab"),
            TestCase("IS002", "Standard isosceles (A=C)", (5, 3, 5), TriangleType.ISOSCELES, category="basic_ac"),
            TestCase("IS003", "Standard isosceles (B=C)", (3, 5, 5), TriangleType.ISOSCELES, category="basic_bc"),
            TestCase("IS004", "Right isosceles (A=B)", (5, 5, math.sqrt(50)), TriangleType.ISOSCELES, category="right_angled"),
            TestCase("IS005", "Almost equilateral (A=B)", (5, 5, 4.9999999999), TriangleType.ISOSCELES, category="precision"),
            TestCase("IS006", "Float precision (A=B)", (0.1 + 0.2, 0.1 + 0.2, 0.2), TriangleType.ISOSCELES, category="floating_point"),
        ]
    
    @staticmethod
    def generate_scalene_cases() -> List[TestCase]:
        """Original scalene cases"""
        return [
            TestCase("SC001", "Pythagorean 3-4-5", (3, 4, 5), TriangleType.SCALENE, category="pythagorean"),
            TestCase("SC002", "Pythagorean 5-12-13", (5, 12, 13), TriangleType.SCALENE, category="pythagorean"),
            TestCase("SC003", "Scaled 3-4-5 (×2)", (6, 8, 10), TriangleType.SCALENE, category="scaled_pythagorean"),
            TestCase("SC004", "Random scalene", (6, 8, 11), TriangleType.SCALENE, category="random"),
            TestCase("SC005", "Decimal scalene", (2.5, 3.7, 4.8), TriangleType.SCALENE, category="decimal"),
            TestCase("SC006", "Almost isosceles", (5, 5.0000001, 3), TriangleType.SCALENE, category="almost_isosceles"),
        ]
    
    @staticmethod
    def generate_failure_cases() -> List[TestCase]:
        """NEW: Cases that should fail"""
        return [
            # Triangle inequality violations
            TestCase("F001", "Sum equals third side", (5, 5, 10), None, True, "triangle inequality", "invalid"),
            TestCase("F002", "Sum less than third side", (2, 3, 10), None, True, "triangle inequality", "invalid"),
            TestCase("F003", "One side too large", (1, 1, 5), None, True, "triangle inequality", "invalid"),
            TestCase("F004", "Extreme inequality", (1, 2, 100), None, True, "triangle inequality", "invalid"),
            
            # Invalid values during request creation
            TestCase("F005", "Negative side", (-3, 4, 5), None, True, "positive numbers", "negative"),
            TestCase("F006", "Zero side", (0, 5, 5), None, True, "positive numbers", "zero"),
            TestCase("F007", "All zero", (0, 0, 0), None, True, "positive numbers", "zero"),
            TestCase("F008", "Mixed negative", (-3, -4, 5), None, True, "positive numbers", "negative"),
            
            # Special numeric values
            TestCase("F009", "Infinity side", (float('inf'), 5, 5), None, True, "positive numbers", "special"),
            TestCase("F010", "NaN side", (float('nan'), 5, 5), None, True, "positive numbers", "special"),
            TestCase("F011", "All infinity", (float('inf'), float('inf'), float('inf')), None, True, "positive numbers", "special"),
        ]
    
    @staticmethod
    def generate_input_test_cases() -> List[InputTestCase]:
        """Console input test cases"""
        return [
            # Valid inputs
            InputTestCase("I001", "Valid numeric input", ["5", "5", "3"], True),
            InputTestCase("I002", "Valid decimal input", ["3.14", "2.71", "4.47"], True),
            InputTestCase("I003", "Valid with spaces", [" 5 ", " 5 ", " 3 "], True),
            InputTestCase("I004", "Scientific notation", ["1e2", "2e2", "1.5e2"], True),
            
            # Invalid inputs that should fail
            InputTestCase("I005", "Non-numeric input", ["abc", "5", "3"], False, "ValueError"),
            InputTestCase("I006", "Empty input", ["", "5", "3"], False, "ValueError"),
            InputTestCase("I007", "Special characters", ["5!", "5", "3"], False, "ValueError"),
            InputTestCase("I008", "Mixed valid/invalid", ["5", "xyz", "3"], False, "ValueError"),
            InputTestCase("I009", "Negative input", ["-5", "5", "3"], False, "ValueError"),
            InputTestCase("I010", "Zero input", ["0", "5", "3"], False, "ValueError"),
            InputTestCase("I011", "Infinity input", ["inf", "5", "3"], False, "ValueError"),
            InputTestCase("I012", "NaN input", ["nan", "5", "3"], False, "ValueError"),
            InputTestCase("I013", "Whitespace only", ["   ", "5", "3"], False, "ValueError"),
        ]


class TestTriangleClassificationSuccess:
    """Test successful triangle classification (original test cases)"""
    
    @classmethod
    def setup_class(cls):
        cls.validation_service = TriangleValidationService()
        cls.classification_service = TriangleClassificationService(cls.validation_service)
    
    def create_triangle_request(self, sides: Tuple[float, float, float], test_id: str = "TEST") -> TriangleRequest:
        return TriangleRequest(
            side_a=sides[0],
            side_b=sides[1], 
            side_c=sides[2],
            request_id=test_id
        )
    
    @pytest.mark.parametrize("test_case", TestDataGenerator.generate_equilateral_cases())
    def test_equilateral_classification(self, test_case: TestCase):
        """Test equilateral triangle classification"""
        request = self.create_triangle_request(test_case.sides, test_case.id)
        
        assert self.validation_service.is_valid_triangle(*test_case.sides), \
            f"Test case {test_case.id} has invalid triangle: {test_case.sides}"
        
        result = self.classification_service.classify_triangle(request)
        assert result == test_case.expected_type, \
            f"Test {test_case.id}: Expected {test_case.expected_type.value}, got {result.value} for sides {test_case.sides}"
    
    @pytest.mark.parametrize("test_case", TestDataGenerator.generate_isosceles_cases())
    def test_isosceles_classification(self, test_case: TestCase):
        """Test isosceles triangle classification"""
        request = self.create_triangle_request(test_case.sides, test_case.id)
        
        assert self.validation_service.is_valid_triangle(*test_case.sides), \
            f"Test case {test_case.id} has invalid triangle: {test_case.sides}"
        
        result = self.classification_service.classify_triangle(request)
        assert result == test_case.expected_type, \
            f"Test {test_case.id}: Expected {test_case.expected_type.value}, got {result.value} for sides {test_case.sides}"
    
    @pytest.mark.parametrize("test_case", TestDataGenerator.generate_scalene_cases())
    def test_scalene_classification(self, test_case: TestCase):
        """Test scalene triangle classification"""
        request = self.create_triangle_request(test_case.sides, test_case.id)
        
        assert self.validation_service.is_valid_triangle(*test_case.sides), \
            f"Test case {test_case.id} has invalid triangle: {test_case.sides}"
        
        result = self.classification_service.classify_triangle(request)
        assert result == test_case.expected_type, \
            f"Test {test_case.id}: Expected {test_case.expected_type.value}, got {result.value} for sides {test_case.sides}"


class TestTriangleClassificationFailures:
    """NEW: Test that failures are handled correctly"""
    
    @classmethod
    def setup_class(cls):
        cls.validation_service = TriangleValidationService()
        cls.classification_service = TriangleClassificationService(cls.validation_service)
    
    @pytest.mark.parametrize("test_case", TestDataGenerator.generate_failure_cases())
    def test_invalid_triangle_handling(self, test_case: TestCase):
        """Test that invalid triangles fail correctly"""
        print(f"\n🔍 TESTING FAILURE CASE: {test_case.id}")
        print(f"   Description: {test_case.description}")
        print(f"   Sides: {test_case.sides}")
        print(f"   Expected Error: {test_case.expected_error}")
        print(f"   Category: {test_case.category}")
        
        if test_case.expected_error == "positive numbers":
            print("   ➤ Testing request creation failure (should fail with 'positive numbers' error)")
            # These should fail during request creation
            try:
                request = TriangleRequest(
                    side_a=test_case.sides[0],
                    side_b=test_case.sides[1],
                    side_c=test_case.sides[2],
                    request_id=test_case.id
                )
                print(f"   ❌ UNEXPECTED: Request creation succeeded when it should have failed!")
                print(f"   ❌ Created request: {request}")
                pytest.fail(f"Test {test_case.id} ({test_case.description}): Request creation should have failed for sides {test_case.sides}")
                
            except ValueError as exc_info:
                print(f"   ✅ SUCCESS: Request creation failed as expected")
                print(f"   ✅ Error message: {exc_info}")
                assert "positive numbers" in str(exc_info), \
                    f"Test {test_case.id} ({test_case.description}): Expected 'positive numbers' in error message, got: {exc_info}"
            
            except Exception as unexpected_error:
                print(f"   ❌ UNEXPECTED ERROR TYPE: {type(unexpected_error).__name__}: {unexpected_error}")
                pytest.fail(f"Test {test_case.id} ({test_case.description}): Got unexpected error type {type(unexpected_error).__name__}, expected ValueError")
        
        elif test_case.expected_error == "triangle inequality":
            print("   ➤ Testing triangle inequality failure (should fail during classification)")
            # These should fail during classification
            try:
                print("   ➤ Step 1: Creating request...")
                request = TriangleRequest(
                    side_a=test_case.sides[0],
                    side_b=test_case.sides[1],
                    side_c=test_case.sides[2],
                    request_id=test_case.id
                )
                print(f"   ✅ Request created successfully: {request}")
                
                print("   ➤ Step 2: Attempting classification (should fail)...")
                try:
                    result = self.classification_service.classify_triangle(request)
                    print(f"   ❌ UNEXPECTED: Classification succeeded when it should have failed!")
                    print(f"   ❌ Result: {result}")
                    pytest.fail(f"Test {test_case.id} ({test_case.description}): Classification should have failed for invalid triangle {test_case.sides}")
                
                except ValueError as classification_error:
                    print(f"   ✅ SUCCESS: Classification failed as expected")
                    print(f"   ✅ Error message: {classification_error}")
                    error_msg = str(classification_error).lower()
                    expected_keywords = ["invalid", "triangle", "inequality"]
                    found_keywords = [kw for kw in expected_keywords if kw in error_msg]
                    print(f"   ✅ Found keywords: {found_keywords}")
                    assert any(keyword in error_msg for keyword in expected_keywords), \
                        f"Test {test_case.id} ({test_case.description}): Expected triangle inequality error keywords {expected_keywords} in message, got: {classification_error}"
                
                except Exception as unexpected_classification_error:
                    print(f"   ❌ UNEXPECTED CLASSIFICATION ERROR: {type(unexpected_classification_error).__name__}: {unexpected_classification_error}")
                    pytest.fail(f"Test {test_case.id} ({test_case.description}): Got unexpected classification error type {type(unexpected_classification_error).__name__}, expected ValueError")
            
            except ValueError as creation_error:
                print(f"   ⚠️  Request creation failed instead of classification")
                print(f"   ⚠️  Creation error: {creation_error}")
                print("   ⚠️  This is acceptable if the values are invalid during creation")
                # If it fails during creation, that's also acceptable for these cases
                assert "positive numbers" in str(creation_error), \
                    f"Test {test_case.id} ({test_case.description}): If failing during creation, should be 'positive numbers' error, got: {creation_error}"
            
            except Exception as unexpected_creation_error:
                print(f"   ❌ UNEXPECTED CREATION ERROR: {type(unexpected_creation_error).__name__}: {unexpected_creation_error}")
                pytest.fail(f"Test {test_case.id} ({test_case.description}): Got unexpected creation error type {type(unexpected_creation_error).__name__}, expected ValueError")
        
        else:
            print(f"   ❌ UNKNOWN EXPECTED ERROR TYPE: {test_case.expected_error}")
            pytest.fail(f"Test {test_case.id} ({test_case.description}): Unknown expected error type: {test_case.expected_error}")
        
        print(f"   ✅ Test {test_case.id} completed successfully\n")
    
    def test_validation_service_rejects_invalid_triangles(self):
        """Test that validation service correctly identifies invalid triangles"""
        print(f"\n🔍 TESTING VALIDATION SERVICE")
        invalid_cases = [
            (5, 5, 10),    # sum equals third side
            (1, 1, 5),     # one side too large
            (2, 3, 10),    # sum less than third side
        ]
        
        for i, sides in enumerate(invalid_cases, 1):
            print(f"   Test {i}: Sides {sides}")
            result = self.validation_service.is_valid_triangle(*sides)
            print(f"   Result: {result} (should be False)")
            
            if result == False:
                print(f"   ✅ Correctly rejected invalid triangle")
            else:
                print(f"   ❌ Should have rejected invalid triangle")
                pytest.fail(f"Validation should reject invalid triangle: {sides}")
        
        print(f"   ✅ All validation tests passed\n")
    
    def test_epsilon_boundary_precision(self):
        """Test epsilon boundary handling"""
        print(f"\n🔍 TESTING EPSILON BOUNDARY PRECISION")
        
        # Just below epsilon should be treated as equal (isosceles)
        print("   Test 1: Just below epsilon (should be ISOSCELES)")
        sides1 = (5.0, 5.0 + 1e-11, 3.0)
        print(f"   Sides: {sides1}")
        request1 = TriangleRequest(side_a=sides1[0], side_b=sides1[1], side_c=sides1[2], request_id="EPSILON_TEST1")
        result1 = self.classification_service.classify_triangle(request1)
        print(f"   Result: {result1} (should be ISOSCELES)")
        
        if result1 == TriangleType.ISOSCELES:
            print("   ✅ Correctly classified as ISOSCELES")
        else:
            print(f"   ❌ Expected ISOSCELES, got {result1}")
            pytest.fail(f"Expected ISOSCELES for epsilon boundary test, got {result1}")
        
        # Just above epsilon should be treated as different (scalene)
        print("   Test 2: Just above epsilon (should be SCALENE)")
        sides2 = (5.0, 5.0 + 1e-9, 3.0)
        print(f"   Sides: {sides2}")
        request2 = TriangleRequest(side_a=sides2[0], side_b=sides2[1], side_c=sides2[2], request_id="EPSILON_TEST2")
        result2 = self.classification_service.classify_triangle(request2)
        print(f"   Result: {result2} (should be SCALENE)")
        
        if result2 == TriangleType.SCALENE:
            print("   ✅ Correctly classified as SCALENE")
        else:
            print(f"   ❌ Expected SCALENE, got {result2}")
            pytest.fail(f"Expected SCALENE for epsilon boundary test, got {result2}")
        
        print(f"   ✅ Epsilon boundary tests passed\n")


class TestConsoleInputManipulation:
    """NEW: Test console input handling and manipulation"""
    
    @classmethod
    def setup_class(cls):
        container = ServiceContainer()
        cls.controller = container.get_console_controller()
    
    def simulate_console_input(self, inputs: List[str]) -> Tuple[Optional[TriangleRequest], List[str]]:
        """Simulate console input and capture results"""
        input_iterator = iter(inputs)
        captured_output = []
        
        def mock_input(prompt=""):
            captured_output.append(f"PROMPT: {prompt}")
            try:
                value = next(input_iterator)
                captured_output.append(f"INPUT: {value}")
                return value
            except StopIteration:
                raise EOFError("No more input")
        
        with patch('builtins.input', mock_input):
            with patch('builtins.print') as mock_print:
                mock_print.side_effect = lambda *args: captured_output.append(" ".join(str(arg) for arg in args))
                
                try:
                    result = self.controller.get_user_input()
                    return result, captured_output
                except Exception as e:
                    captured_output.append(f"ERROR: {e}")
                    return None, captured_output
    
    @pytest.mark.parametrize("test_case", TestDataGenerator.generate_input_test_cases())
    def test_console_input_scenarios(self, test_case: InputTestCase):
        """Test various console input scenarios"""
        print(f"\n🔍 TESTING INPUT CASE: {test_case.id}")
        print(f"   Description: {test_case.description}")
        print(f"   Inputs: {test_case.inputs}")
        print(f"   Should Succeed: {test_case.should_succeed}")
        print(f"   Expected Error: {test_case.expected_error}")
        
        result, output = self.simulate_console_input(test_case.inputs)
        
        print(f"   📤 Captured Output ({len(output)} lines):")
        for i, line in enumerate(output, 1):
            print(f"      {i:2d}: {line}")
        
        if test_case.should_succeed:
            print("   ➤ Expecting SUCCESS...")
            if result is not None:
                print(f"   ✅ SUCCESS: Got result: {result}")
                print(f"   ✅ Sides: A={result.side_a}, B={result.side_b}, C={result.side_c}")
                assert all(side > 0 for side in [result.side_a, result.side_b, result.side_c]), \
                    f"Test {test_case.id} ({test_case.description}): All sides should be positive, got A={result.side_a}, B={result.side_b}, C={result.side_c}"
            else:
                print(f"   ❌ FAILURE: Expected success but got None result")
                print(f"   ❌ Check output above for error details")
                pytest.fail(f"Test {test_case.id} ({test_case.description}): Expected success but got None result. Inputs: {test_case.inputs}")
        else:
            print("   ➤ Expecting FAILURE...")
            if result is None:
                print(f"   ✅ SUCCESS: Correctly failed (result is None)")
                # Verify error was captured
                error_lines = [line for line in output if "Error" in line or "ERROR:" in line]
                print(f"   ✅ Found {len(error_lines)} error line(s): {error_lines}")
                assert len(error_lines) > 0, \
                    f"Test {test_case.id} ({test_case.description}): Expected error in output but none found. Output: {output}"
            else:
                print(f"   ❌ FAILURE: Expected failure but got result: {result}")
                pytest.fail(f"Test {test_case.id} ({test_case.description}): Expected failure but got result: {result}. Inputs: {test_case.inputs}")
        
        print(f"   ✅ Test {test_case.id} completed successfully\n")
    
    def test_whitespace_normalization(self):
        """Test that whitespace is properly handled"""
        inputs = ["  5.5  ", "\t4.2\t", "\n3.1\n"]
        result, _ = self.simulate_console_input(inputs)
        
        assert result is not None
        assert result.side_a == 5.5
        assert result.side_b == 4.2
        assert result.side_c == 3.1
    
    def test_scientific_notation_handling(self):
        """Test scientific notation input"""
        inputs = ["1e1", "2E1", "1.5e1"]  # 10, 20, 15
        result, _ = self.simulate_console_input(inputs)
        
        assert result is not None
        assert result.side_a == 10.0
        assert result.side_b == 20.0
        assert result.side_c == 15.0
    
    def test_invalid_input_error_messages(self):
        """Test that invalid inputs produce appropriate error messages"""
        test_cases = [
            (["abc"], "non-numeric"),
            ([""], "empty"),
            (["-5"], "negative"),
            (["inf"], "infinity"),
        ]
        
        for inputs, error_type in test_cases:
            # Pad with valid inputs to complete the sequence
            full_inputs = inputs + ["5", "3"]
            result, output = self.simulate_console_input(full_inputs)
            
            assert result is None, f"Should fail for {error_type} input"
            assert any("Error" in line for line in output), f"Should show error for {error_type}"


class TestApplicationServiceErrorHandling:
    """Test error handling in application service"""
    
    @classmethod
    def setup_class(cls):
        cls.repository = InMemoryTriangleRepository()
        cls.validator = TriangleValidationService()
        cls.classifier = TriangleClassificationService(cls.validator)
        cls.app_service = TriangleApplicationService(cls.classifier, cls.repository)
    
    def test_successful_processing(self):
        """Test successful processing workflow"""
        request = TriangleRequest(side_a=3, side_b=4, side_c=5, request_id="SUCCESS_TEST")
        response = self.app_service.process_triangle_classification(request)
        
        assert response.is_valid == True
        assert response.triangle_type == TriangleType.SCALENE
        assert response.request_id == "SUCCESS_TEST"
        assert response.processing_time_ms > 0
    
    def test_failed_processing_error_handling(self):
        """Test that failed processing is handled gracefully"""
        # This will fail due to triangle inequality
        request = TriangleRequest(side_a=1, side_b=1, side_c=5, request_id="FAIL_TEST")
        response = self.app_service.process_triangle_classification(request)
        
        assert response.is_valid == False
        assert response.request_id == "FAIL_TEST"
        assert response.processing_time_ms > 0
        assert response.sides == (1, 1, 5)
    
    def test_side_order_independence(self):
        """Test that classification doesn't depend on side order"""
        test_permutations = [
            (3, 4, 5), (3, 5, 4), (4, 3, 5),
            (4, 5, 3), (5, 3, 4), (5, 4, 3)
        ]
        
        results = []
        for i, sides in enumerate(test_permutations):
            request = TriangleRequest(side_a=sides[0], side_b=sides[1], side_c=sides[2], request_id=f"ORDER_{i}")
            response = self.app_service.process_triangle_classification(request)
            results.append(response.triangle_type)
        
        # All should be scalene
        assert all(result == TriangleType.SCALENE for result in results), \
            f"Inconsistent results for different orders: {results}"


if __name__ == "__main__":
    """Run the focused test suite"""
    pytest.main([
        __file__,
        "-v",
        "--tb=short",
        "--capture=no"
    ])