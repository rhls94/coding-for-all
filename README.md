# Problem Analyzer Utility

## Overview

The Problem Analyzer Utility is a command-line tool designed to help users test their solutions for programming problems. It works by:
*   Displaying the problem explanation (from an `explanation.html` file).
*   Prompting the user to paste their solution code for Java and JavaScript.
*   Executing the user's solutions against a predefined set of test cases (from a `testcases.json` file).
*   Reporting the success or failure of each test case.
*   Displaying the Big O complexity mentioned in the problem's explanation.
*   Allowing users to input their self-assessed Big O complexity for their solutions.

## Prerequisites

To use this utility effectively, you will need the following software installed:

*   **Python 3.x:** The core script is written in Python.
*   **Java Development Kit (JDK):** A recent JDK is required for compiling and running Java solutions. The utility has been tested with JDK 11 but should work with other recent versions. Ensure `javac` and `java` are in your system's PATH.
*   **Node.js:** A recent version of Node.js is required for running JavaScript solutions. The utility has been tested with Node.js v14.x but should work with other recent LTS versions. Ensure `node` is in your system's PATH.
*   **Gson JAR:** The Java test runner uses the Gson library for JSON serialization/deserialization. The specific version `gson-2.10.1.jar` is included in the `java_runner_utils/` directory and is used automatically by the script.

## Setup

1.  Clone this repository to your local machine.
2.  Ensure Python 3, Java (JDK), and Node.js are installed and configured in your system's PATH.
3.  No further Python package installations are required as the script uses standard libraries (plus the included Gson JAR for Java execution).

## Problem Folder Structure

Each programming problem should be contained within its own folder, following this structure:

```
problem_folder_name/
├── explanation.html
└── testcases.json
```

*   `explanation.html`: An HTML file that contains the problem description, constraints, examples, and ideally, the time and space complexity of an optimal solution.
*   `testcases.json`: A JSON file that defines the problem metadata and the test cases for different languages.

### `testcases.json` Details

The `testcases.json` file has the following key components:

*   `problemName`: (String) The display name of the problem.
*   `java`: (Object) Configuration for Java solutions.
    *   `sourceFile`: (String, currently informational) The expected name of the user's Java source file (e.g., "TwoSum.java"). The script currently saves user input to `user_solution.java`.
    *   `className`: (String) The name of the public class the user's solution should define.
    *   `methodName`: (String) The name of the method within the class that implements the solution.
    *   `inputs`: (Array of Objects) Describes the input parameters for the method. Each object has:
        *   `name`: (String) Parameter name (used for generating runner code).
        *   `type`: (String) The Java type (e.g., "int[]", "int", "ListNode", "String").
    *   `outputType`: (String) The Java return type of the method.
    *   `testCases`: (Array of Objects) Each object defines a single test case:
        *   `name`: (String) A descriptive name for the test case.
        *   `args`: (Array) The arguments to be passed to the solution method, in order. For complex types like `ListNode`, these are represented as JSON objects.
        *   `expectedOutput`: The expected return value. For complex types, this is also a JSON object.
        *   `comparisonMode`: (String) How to compare the actual output with `expectedOutput`.
            *   `"exactOrder"`: Used for primitives, arrays of primitives, and strings. Compares for exact equality.
            *   `"linkedListExact"`: Used for linked lists. Compares the structure and values of each node.
*   `javascript`: (Object) Configuration for JavaScript solutions.
    *   `sourceFile`: (String, currently informational) The expected name of the user's JavaScript file (e.g., "twosum.js"). The script saves user input to `user_solution.js`.
    *   `functionName`: (String) The name of the function the user's solution should export.
    *   `inputs`: (Array of Objects) Describes input parameters (similar to Java's, but types are for documentation e.g. "number[]", "ListNode").
    *   `outputType`: (String) Describes the output type (for documentation).
    *   `testCases`: (Array of Objects) Similar structure to Java's test cases.

**Example Snippet of `testcases.json`:**
```json
{
  "problemName": "Two Sum",
  "java": {
    "className": "TwoSum",
    "methodName": "twoSum",
    "inputs": [
      {"name": "nums", "type": "int[]"},
      {"name": "target", "type": "int"}
    ],
    "outputType": "int[]",
    "testCases": [
      {
        "name": "Example 1",
        "args": [[2, 7, 11, 15], 9],
        "expectedOutput": [0, 1],
        "comparisonMode": "exactOrder"
      }
      // ... more test cases
    ]
  },
  "javascript": {
    "functionName": "twoSum",
    // ... similar structure
  }
}
```
(Refer to `1. Two Sum/testcases.json` and `2. adding two number - linked list/testcases.json` for complete examples.)

**Custom Types (e.g., `ListNode`):**
If a problem involves custom data structures like `ListNode`, the definition for such classes/prototypes must be part of the code pasted by the user.
*   For **Java**, if your solution uses `ListNode`, the `ListNode` class definition should be included in the code you paste. The Java runner compiles the user's pasted code (which should contain both the solution class and any helper classes like `ListNode`) together.
*   For **JavaScript**, similarly, any necessary helper class or prototype definitions (like a `ListNode` constructor or class) should be part of the pasted code.

## How to Write Testable Solutions

### Java

*   Your pasted code must define a public class matching the `className` specified in `testcases.json` (e.g., `public class TwoSum { ... }`).
*   This class must contain a public method matching the `methodName` (e.g., `public int[] twoSum(int[] nums, int target) { ... }`).
*   The method signature (parameter types and return type) must correspond to the `inputs` and `outputType` defined in `testcases.json`. The runner relies on these definitions for correct deserialization and serialization using Gson.
*   If custom classes like `ListNode` are used, their definitions must be included in the pasted code.

**Example (for "Two Sum"):**
```java
// User pastes this entire block, including ListNode if needed for other problems
// class ListNode { /* ... definition ... */ } // (if needed)

public class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        // ... your solution logic ...
        return new int[]{0, 1}; // Example
    }
}
```

### JavaScript

*   Your pasted code should export the function specified by `functionName` in `testcases.json`.
    *   You can use `module.exports = yourFunctionName;`
    *   Or `module.exports = { yourFunctionName: yourFunctionName };` (The runner tries `userSolution.functionName` first, then `userSolution` directly).
*   The function signature should accept arguments in the order specified by the `args` in the test cases.
*   If custom classes or constructor functions (e.g., for `ListNode`) are used, their definitions must be included in the pasted code.

**Example (for "Two Sum"):**
```javascript
// User pastes this entire block, including ListNode if needed for other problems
// function ListNode(val, next) { /* ... definition ... */ } // (if needed)

function twoSum(nums, target) {
    // ... your solution logic ...
    return [0, 1]; // Example
}

module.exports = twoSum;
// or: module.exports = { twoSum: twoSum };
```

## Usage

Run the script from the root of the repository using the following command:

```bash
python problem_analyzer.py <path_to_problem_folder>
```

**Interactive Process:**
1.  The script will first attempt to open the `explanation.html` file from the specified problem folder in your default web browser.
2.  You will be prompted to paste your Java solution code into the terminal. After pasting, type `EOF` on a new line and press Enter to signal the end of your input.
3.  If a Java solution is provided, it will be compiled and run against the test cases. Results (PASS/FAIL for each test, and error details) will be displayed.
4.  Next, you will be prompted to paste your JavaScript solution code (again, ending with `EOF`).
5.  If a JavaScript solution is provided, it will be run against the test cases, and results will be displayed.
6.  The script will then attempt to extract and display Time and Space complexity information found in `explanation.html`.
7.  Finally, you will be prompted to optionally enter your self-assessed Time and Space complexities for both your Java and JavaScript solutions.

## Example

To analyze the "1. Two Sum" problem:

```bash
python problem_analyzer.py "1. Two Sum"
```

## Security Note

⚠️ **Warning:** This utility executes user-provided code (Java and JavaScript) directly on your machine. This can be a security risk if you run code from untrusted sources. Only use this tool with code you have written yourself or from sources you trust. Consider running it in a sandboxed environment if you are unsure about the code's origin.

## Future Improvements

This utility is a work in progress. Potential future enhancements include:

*   **Sandboxed Execution:** Implementing stricter sandboxing for code execution to enhance security.
*   **Automated Big O Analysis:** Attempting to statically or dynamically analyze the user's code for Big O complexity.
*   **Support for More Languages:** Extending the framework to support other programming languages (e.g., C++, C#).
*   **Graphical User Interface (GUI):** Creating a GUI for a more user-friendly experience.
*   **More Comparison Modes:** Adding more sophisticated comparison modes for test cases (e.g., set equality, floating-point comparisons with tolerance).
*   **User Accounts & Progress Tracking:** (More ambitious) Allowing users to save their solutions and track progress.

```
