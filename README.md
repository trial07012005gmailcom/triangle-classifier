# Triangle Classification Service

A layered architecture demonstration implementing geometric triangle classification with comprehensive quality assurance practices.

## Architecture Overview

The application employs a clean layered architecture pattern with distinct separation of concerns:

```
┌─────────────────────────────────────┐
│        Presentation Layer           │  ← Console UI, Input/Output
├─────────────────────────────────────┤
│        Application Layer            │  ← Workflow Orchestration
├─────────────────────────────────────┤
│        Business Logic Layer         │  ← Domain Logic, Classification
├─────────────────────────────────────┤
│        Data Access Layer            │  ← Repository Pattern, Storage
├─────────────────────────────────────┤
│       Cross-Cutting Concerns        │  ← Logging, Validation, QA
└─────────────────────────────────────┘
```

## Application Showcase

The service processes triangle side measurements and determines geometric classification through epsilon-based floating-point comparison. The system validates triangle inequality constraints, applies geometric classification algorithms, and maintains audit trails with performance tracking.

**Core Functionality:**

- Geometric triangle validation using mathematical constraints
- Classification algorithm with floating-point precision handling
- Interactive console interface with session management
- Historical data persistence and retrieval capabilities
- Comprehensive logging and error handling mechanisms

## Quick Start

### Prerequisites

- Python 3.8 or higher
- No external dependencies required

### Installation & Execution

```bash
# Clone the repository
git clone <repository-url>
cd triangle-classification-service

# Run the application
python triangle_classifier.py
```

### Usage Flow

1. **Input Phase**: Enter three numeric values representing triangle sides
2. **Processing Phase**: System validates geometric constraints and classifies triangle type
3. **Output Phase**: Display classification result with performance metrics
4. **Session Management**: Continue with additional classifications or view historical data

```
=== TRIANGLE CLASSIFICATION SERVICE ===
Enter the three sides of a triangle:
Enter side A: 3.0
Enter side B: 4.0
Enter side C: 5.0

==================================================
TRIANGLE CLASSIFICATION RESULT
==================================================
Triangle Type: SCALENE
Sides: (3.0, 4.0, 5.0)
Processing Time: 1.23ms
Request ID: REQ_20250804_143021
==================================================
```

## Technical Constraints & Limitations

### Floating-Point Precision Constraints

- **Epsilon Threshold**: Fixed at `1e-10` for equality comparisons
- **IEEE 754 Limitations**: Inherent binary floating-point representation errors
- **Input Conversion Loss**: User decimal inputs may lose precision during float conversion
- **Accumulation Errors**: Mathematical operations can compound precision issues

### Algorithmic Constraints

- **Triangle Inequality**: Strict enforcement of `a + b > c` constraint for all side combinations
- **Classification Logic**: Sequential epsilon-based comparison for geometric type determination
- **Validation Boundaries**: Positive number constraint with zero-value rejection

### System Architecture Constraints

- **Memory Storage**: In-memory repository with session-scoped persistence
- **Single-User Sessions**: Console-based interface with sequential processing model
- **Error Recovery**: Graceful degradation with invalid input handling
- **Performance Tracking**: Millisecond-precision timing measurements

### Input/Output Constraints

- **Numeric Input Only**: Floating-point number parsing with validation
- **Console Interface**: Text-based interaction requiring terminal environment
- **Session Persistence**: Data retention limited to application lifecycle
- **Logging Overhead**: Comprehensive audit trails impact processing performance

## Logic Implementation Details

### Classification Algorithm

The system employs epsilon-based floating-point comparison to handle precision limitations inherent in computer arithmetic. The algorithm evaluates side equality using absolute difference thresholds rather than exact equality operators.

### Validation Strategy

Business rule enforcement occurs through triangle inequality theorem validation before classification processing. The system rejects geometrically impossible triangle configurations and provides appropriate error feedback.

### Error Handling Paradigm

Comprehensive exception handling with logging integration ensures system stability while maintaining audit trails for debugging and quality assurance purposes. Failed operations generate standardized error responses with performance metrics.

### Dependency Injection Pattern

Service container implementation enables testable architecture through dependency inversion, facilitating unit testing and component isolation strategies.

## Quality Assurance Features

- **Structured Logging**: Comprehensive audit trails with component-level traceability
- **Input Validation**: Multi-layer data integrity checks with business rule enforcement
- **Error Recovery**: Graceful degradation with meaningful error messages
- **Performance Monitoring**: Request-level timing metrics with millisecond precision
- **Transaction Integrity**: End-to-end processing with consistent state management

---

_This implementation serves as a demonstration of layered architecture principles with emphasis on quality assurance practices and maintainable code structure._
