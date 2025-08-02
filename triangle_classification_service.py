"""
LAYERED ARCHITECTURE EXAMPLE - Triangle Classification Service
QA Focus: Each layer has specific testing responsibilities and quality concerns

ARCHITECTURE LAYERS:
1. Presentation Layer (UI/API) - User interaction, input/output formatting
2. Business Logic Layer (Service) - Core domain logic, business rules
3. Data Access Layer (Repository) - Data persistence, external integrations
4. Cross-Cutting Concerns - Logging, security, validation

QA TESTING STRATEGY PER LAYER:
- Presentation: UI/UX testing, input validation, user journey testing
- Business Logic: Unit testing, business rule testing, algorithm testing
- Data Access: Integration testing, data integrity testing
- Cross-Cutting: Security testing, performance testing, logging verification
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

# ============================================================================
# CROSS-CUTTING CONCERNS LAYER (Foundation)
# QA Focus: Security, logging, monitoring, error handling
# ============================================================================

class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"

class QALogger:
    """
    QA Cross-Cutting Service: Centralized logging for testing and monitoring
    Quality Focus: Audit trails, error tracking, performance monitoring
    """
    
    @staticmethod
    def log(level: LogLevel, message: str, component: str = "SYSTEM"):
        """
        QA Function: Structured logging for quality assurance
        - Enables defect traceability
        - Supports performance monitoring
        - Facilitates security auditing
        """
        timestamp = datetime.now().isoformat()
        print(f"[{timestamp}] [{level.value}] [{component}] {message}")

# ============================================================================
# DATA MODELS LAYER (Domain Entities)
# QA Focus: Data integrity, validation rules, business constraints
# ============================================================================

class TriangleType(Enum):
    EQUILATERAL = "EQUILATERAL"
    ISOSCELES = "ISOSCELES"
    SCALENE = "SCALENE"

@dataclass
class TriangleRequest:
    """
    QA Data Model: Input validation and data integrity
    Quality Focus: Type safety, constraint validation
    """
    side_a: float
    side_b: float
    side_c: float
    request_id: str = None
    
    def __post_init__(self):
        """QA Validation: Automatic data integrity checks"""
        if not all(side > 0 for side in [self.side_a, self.side_b, self.side_c]):
            raise ValueError("All sides must be positive numbers")

@dataclass
class TriangleResponse:
    """
    QA Response Model: Standardized output format
    Quality Focus: Consistent API contract, traceability
    """
    triangle_type: TriangleType
    is_valid: bool
    sides: tuple
    request_id: str
    processing_time_ms: float
    
# ============================================================================
# DATA ACCESS LAYER (Repository Pattern)
# QA Focus: Data persistence, external integrations, data quality
# ============================================================================

class TriangleRepository(ABC):
    """
    QA Interface: Abstract repository for testability
    Quality Focus: Dependency inversion, mockable interfaces
    """
    
    @abstractmethod
    def save_classification_result(self, result: TriangleResponse) -> bool:
        pass
    
    @abstractmethod
    def get_classification_history(self) -> List[TriangleResponse]:
        pass

class InMemoryTriangleRepository(TriangleRepository):
    """
    QA Implementation: In-memory storage for testing and development
    Quality Focus: Fast tests, no external dependencies
    """
    
    def __init__(self):
        self._storage: List[TriangleResponse] = []
        QALogger.log(LogLevel.INFO, "Repository initialized", "DATA_LAYER")
    
    def save_classification_result(self, result: TriangleResponse) -> bool:
        """
        QA Method: Save with validation and error handling
        """
        try:
            self._storage.append(result)
            QALogger.log(LogLevel.INFO, f"Result saved for request {result.request_id}", "DATA_LAYER")
            return True
        except Exception as e:
            QALogger.log(LogLevel.ERROR, f"Failed to save result: {e}", "DATA_LAYER")
            return False
    
    def get_classification_history(self) -> List[TriangleResponse]:
        """QA Method: Retrieve history with logging"""
        QALogger.log(LogLevel.INFO, f"Retrieved {len(self._storage)} historical records", "DATA_LAYER")
        return self._storage.copy()

# ============================================================================
# BUSINESS LOGIC LAYER (Core Domain Logic)
# QA Focus: Business rules, algorithms, domain validation
# ============================================================================

class TriangleValidationService:
    """
    QA Service: Business rule validation
    Quality Focus: Domain expertise, business constraint enforcement
    """
    
    @staticmethod
    def is_valid_triangle(a: float, b: float, c: float) -> bool:
        """
        QA Business Rule: Triangle inequality theorem
        Critical for preventing logically impossible classifications
        """
        QALogger.log(LogLevel.DEBUG, f"Validating triangle: {a}, {b}, {c}", "BUSINESS_LAYER")
        
        is_valid = (a + b > c) and (a + c > b) and (b + c > a)
        
        if not is_valid:
            QALogger.log(LogLevel.WARNING, "Invalid triangle detected", "BUSINESS_LAYER")
        
        return is_valid

class TriangleClassificationService:
    """
    QA Service: Core classification algorithm
    Quality Focus: Algorithm correctness, edge case handling
    """
    
    def __init__(self, validator: TriangleValidationService):
        self.validator = validator
        QALogger.log(LogLevel.INFO, "Classification service initialized", "BUSINESS_LAYER")
    
    def classify_triangle(self, request: TriangleRequest) -> TriangleType:
        """
        QA Algorithm: Triangle classification with comprehensive logging
        Quality Focus: Correctness, traceability, edge case handling
        """
        a, b, c = request.side_a, request.side_b, request.side_c
        
        QALogger.log(LogLevel.DEBUG, f"Classifying triangle {request.request_id}", "BUSINESS_LAYER")
        
        # QA Validation: Business rule check
        if not self.validator.is_valid_triangle(a, b, c):
            raise ValueError("Invalid triangle: violates triangle inequality")
        
        # QA Algorithm: Classification logic with epsilon comparison
        epsilon = 1e-10
        
        def are_equal(x: float, y: float) -> bool:
            return abs(x - y) < epsilon
        
        # Classification logic
        if are_equal(a, b) and are_equal(b, c):
            result = TriangleType.EQUILATERAL
        elif are_equal(a, b) or are_equal(b, c) or are_equal(a, c):
            result = TriangleType.ISOSCELES
        else:
            result = TriangleType.SCALENE
        
        QALogger.log(LogLevel.INFO, f"Classified as {result.value}", "BUSINESS_LAYER")
        return result

# ============================================================================
# APPLICATION LAYER (Use Cases / Application Services)
# QA Focus: Workflow orchestration, transaction management
# ============================================================================

class TriangleApplicationService:
    """
    QA Service: Application workflow orchestration
    Quality Focus: Transaction integrity, error handling, performance
    """
    
    def __init__(self, 
                 classification_service: TriangleClassificationService,
                 repository: TriangleRepository):
        self.classification_service = classification_service
        self.repository = repository
        QALogger.log(LogLevel.INFO, "Application service initialized", "APPLICATION_LAYER")
    
    def process_triangle_classification(self, request: TriangleRequest) -> TriangleResponse:
        """
        QA Use Case: Complete triangle processing workflow
        Quality Focus: End-to-end transaction, error handling, performance tracking
        """
        start_time = datetime.now()
        
        try:
            # QA Process: Classification with error handling
            triangle_type = self.classification_service.classify_triangle(request)
            
            # QA Response: Create standardized response
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            response = TriangleResponse(
                triangle_type=triangle_type,
                is_valid=True,
                sides=(request.side_a, request.side_b, request.side_c),
                request_id=request.request_id,
                processing_time_ms=processing_time
            )
            
            # QA Persistence: Save result with error handling
            saved = self.repository.save_classification_result(response)
            if not saved:
                QALogger.log(LogLevel.WARNING, "Failed to persist result", "APPLICATION_LAYER")
            
            QALogger.log(LogLevel.INFO, f"Request {request.request_id} processed successfully", "APPLICATION_LAYER")
            return response
            
        except Exception as e:
            # QA Error Handling: Comprehensive error response
            processing_time = (datetime.now() - start_time).total_seconds() * 1000
            
            error_response = TriangleResponse(
                triangle_type=TriangleType.SCALENE,  # Default value
                is_valid=False,
                sides=(request.side_a, request.side_b, request.side_c),
                request_id=request.request_id,
                processing_time_ms=processing_time
            )
            
            QALogger.log(LogLevel.ERROR, f"Processing failed: {e}", "APPLICATION_LAYER")
            return error_response

# ============================================================================
# PRESENTATION LAYER (User Interface / API)
# QA Focus: Input validation, output formatting, user experience
# ============================================================================

class TriangleConsoleController:
    """
    QA Controller: User interface and input/output handling
    Quality Focus: User experience, input validation, output formatting
    """
    
    def __init__(self, app_service: TriangleApplicationService):
        self.app_service = app_service
        QALogger.log(LogLevel.INFO, "Console controller initialized", "PRESENTATION_LAYER")
    
    def get_user_input(self) -> Optional[TriangleRequest]:
        """
        QA Input Handler: User input collection with validation
        Quality Focus: Input sanitization, user experience, error feedback
        """
        try:
            print("=== TRIANGLE CLASSIFICATION SERVICE ===")
            print("Enter the three sides of a triangle:")
            
            # QA Input: Collect and validate each input
            side_a = float(input("Enter side A: ").strip())
            side_b = float(input("Enter side B: ").strip())
            side_c = float(input("Enter side C: ").strip())
            
            # QA Request: Create validated request object
            request = TriangleRequest(
                side_a=side_a,
                side_b=side_b,
                side_c=side_c,
                request_id=f"REQ_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            
            QALogger.log(LogLevel.INFO, f"User input collected: {request.request_id}", "PRESENTATION_LAYER")
            return request
            
        except ValueError as e:
            print(f"Input Error: {e}")
            QALogger.log(LogLevel.WARNING, f"Invalid user input: {e}", "PRESENTATION_LAYER")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            QALogger.log(LogLevel.ERROR, f"Input collection failed: {e}", "PRESENTATION_LAYER")
            return None
    
    def display_result(self, response: TriangleResponse) -> None:
        """
        QA Output Handler: Result presentation with formatting
        Quality Focus: Consistent output, user-friendly presentation
        """
        print("\n" + "="*50)
        print("TRIANGLE CLASSIFICATION RESULT")
        print("="*50)
        
        if response.is_valid:
            print(f"Triangle Type: {response.triangle_type.value}")
            print(f"Sides: {response.sides}")
            print(f"Processing Time: {response.processing_time_ms:.2f}ms")
            print(f"Request ID: {response.request_id}")
        else:
            print("CLASSIFICATION FAILED")
            print("The provided sides do not form a valid triangle.")
        
        print("="*50)
        QALogger.log(LogLevel.INFO, f"Result displayed for {response.request_id}", "PRESENTATION_LAYER")
    
    def run_interactive_session(self) -> None:
        """
        QA Session Manager: Interactive user session with proper lifecycle
        Quality Focus: User experience, session management, graceful termination
        """
        QALogger.log(LogLevel.INFO, "Interactive session started", "PRESENTATION_LAYER")
        
        while True:
            try:
                # QA Process: Input -> Processing -> Output cycle
                request = self.get_user_input()
                
                if request:
                    response = self.app_service.process_triangle_classification(request)
                    self.display_result(response)
                
                # QA User Experience: Continue or exit
                print("\nOptions:")
                print("1. Classify another triangle")
                print("2. View classification history")
                print("3. Exit")
                
                choice = input("Choose an option (1-3): ").strip()
                
                if choice == "2":
                    self._display_history()
                elif choice == "3":
                    print("Thank you for using Triangle Classification Service!")
                    break
                elif choice != "1":
                    print("Invalid option. Please try again.")
                
                print()  # Add spacing
                
            except KeyboardInterrupt:
                print("\nSession terminated by user.")
                QALogger.log(LogLevel.INFO, "Session terminated by user", "PRESENTATION_LAYER")
                break
            except Exception as e:
                print(f"Session error: {e}")
                QALogger.log(LogLevel.ERROR, f"Session error: {e}", "PRESENTATION_LAYER")
    
    def _display_history(self) -> None:
        """QA Feature: Display classification history"""
        history = self.app_service.repository.get_classification_history()
        
        if not history:
            print("No classification history available.")
            return
        
        print("\n=== CLASSIFICATION HISTORY ===")
        for i, record in enumerate(history[-5:], 1):  # Show last 5
            status = "SUCCESS" if record.is_valid else "FAILED"
            print(f"{i}. [{status}] {record.triangle_type.value} - Sides: {record.sides}")
        print("="*30)

# ============================================================================
# DEPENDENCY INJECTION CONTAINER (Infrastructure)
# QA Focus: Testability, configuration management, dependency management
# ============================================================================

class ServiceContainer:
    """
    QA Infrastructure: Dependency injection for better testability
    Quality Focus: Testable architecture, configuration management
    """
    
    def __init__(self):
        # QA Setup: Create service dependencies
        self.repository = InMemoryTriangleRepository()
        self.validator = TriangleValidationService()
        self.classification_service = TriangleClassificationService(self.validator)
        self.app_service = TriangleApplicationService(self.classification_service, self.repository)
        self.controller = TriangleConsoleController(self.app_service)
        
        QALogger.log(LogLevel.INFO, "Service container initialized", "INFRASTRUCTURE")
    
    def get_console_controller(self) -> TriangleConsoleController:
        """QA Factory: Get configured controller"""
        return self.controller

# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

def main():
    """
    QA Entry Point: Application bootstrap with error handling
    Quality Focus: Proper initialization, error handling, cleanup
    """
    try:
        QALogger.log(LogLevel.INFO, "Application starting", "MAIN")
        
        # QA Bootstrap: Initialize service container
        container = ServiceContainer()
        controller = container.get_console_controller()
        
        # QA Execution: Run application
        controller.run_interactive_session()
        
        QALogger.log(LogLevel.INFO, "Application terminated successfully", "MAIN")
        
    except Exception as e:
        QALogger.log(LogLevel.ERROR, f"Application failed: {e}", "MAIN")
        print(f"Critical application error: {e}")

if __name__ == "__main__":
    main()