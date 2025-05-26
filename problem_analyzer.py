import argparse
import os
import sys
import webbrowser
import subprocess
import json
import shutil
import re

def main():
    parser = argparse.ArgumentParser(description="Analyze a problem folder.")
    parser.add_argument("problem_folder", help="Path to the problem folder")
    args = parser.parse_args()

    problem_folder_path = args.problem_folder

    if not os.path.exists(problem_folder_path):
        sys.stderr.write(f"Error: Folder '{problem_folder_path}' does not exist.\n")
        sys.exit(1)

    if not os.path.isdir(problem_folder_path):
        sys.stderr.write(f"Error: '{problem_folder_path}' is not a directory.\n")
        sys.exit(1)

    explanation_html_path = os.path.join(problem_folder_path, "explanation.html")
    if not os.path.exists(explanation_html_path):
        sys.stderr.write(f"Error: File 'explanation.html' not found in '{problem_folder_path}'.\n")
        sys.exit(1)

    testcases_json_path = os.path.join(problem_folder_path, "testcases.json")
    if not os.path.exists(testcases_json_path):
        sys.stderr.write(f"Error: Problem folder '{problem_folder_path}' is missing testcases.json\n")
        sys.exit(1)

    print(f"Successfully validated problem folder contents: {problem_folder_path} (found explanation.html and testcases.json)")

    print("Attempting to open explanation.html...")
    webbrowser.open_new_tab(f"file://{os.path.abspath(explanation_html_path)}")

    user_java_solution_path = "user_solution.java"
    prompt_and_save_solution("Java", user_java_solution_path)
    if os.path.exists(user_java_solution_path): # Proceed only if Java solution was saved
        execute_java_solution(problem_folder_path, user_java_solution_path)

    user_js_solution_path = "user_solution.js"
    prompt_and_save_solution("JavaScript", user_js_solution_path)
    if os.path.exists(user_js_solution_path):
        execute_javascript_solution(problem_folder_path, user_js_solution_path)

    extract_and_display_big_o_from_explanation(problem_folder_path)

    print("\n--- User's Solution Complexity (Self-Assessed) ---")
    user_java_time = input("Optional: What is the estimated Time Complexity of your Java solution? (e.g., O(n), O(n log n)): ")
    if user_java_time:
        print(f"User's Java Time Complexity: {user_java_time}")
    else:
        print("User's Java Time Complexity: User did not provide.")

    user_java_space = input("Optional: What is the estimated Space Complexity of your Java solution? (e.g., O(n), O(n log n)): ")
    if user_java_space:
        print(f"User's Java Space Complexity: {user_java_space}")
    else:
        print("User's Java Space Complexity: User did not provide.")

    user_js_time = input("Optional: What is the estimated Time Complexity of your JavaScript solution? (e.g., O(n), O(n log n)): ")
    if user_js_time:
        print(f"User's JavaScript Time Complexity: {user_js_time}")
    else:
        print("User's JavaScript Time Complexity: User did not provide.")

    user_js_space = input("Optional: What is the estimated Space Complexity of your JavaScript solution? (e.g., O(n), O(n log n)): ")
    if user_js_space:
        print(f"User's JavaScript Space Complexity: {user_js_space}")
    else:
        print("User's JavaScript Space Complexity: User did not provide.")


def extract_and_display_big_o_from_explanation(problem_folder_path):
    print("\n--- Reference Solution Complexity (from explanation.html) ---")
    explanation_html_path = os.path.join(problem_folder_path, "explanation.html")
    
    if not os.path.exists(explanation_html_path):
        print(f"explanation.html not found at {explanation_html_path}")
        return

    try:
        with open(explanation_html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except IOError as e:
        print(f"Error reading explanation.html: {e}")
        return

    time_complexity_match = re.search(r"Time Complexity:\s*O\((.*?)\)", content, re.IGNORECASE)
    space_complexity_match = re.search(r"Space Complexity:\s*O\((.*?)\)", content, re.IGNORECASE)

    found = False
    if time_complexity_match:
        print(f"Time Complexity: O({time_complexity_match.group(1)})")
        found = True
    if space_complexity_match:
        print(f"Space Complexity: O({space_complexity_match.group(1)})")
        found = True
    
    if not found:
        print("Could not automatically extract complexity from explanation.html.")


def execute_javascript_solution(problem_folder_path, user_js_file_path):
    print(f"\n--- Executing JavaScript Solution for {problem_folder_path} ---")

    testcases_json_path = os.path.join(problem_folder_path, "testcases.json")
    if not os.path.exists(testcases_json_path):
        sys.stderr.write(f"Error: testcases.json not found in {problem_folder_path}\n")
        return

    try:
        with open(testcases_json_path, 'r') as f:
            problem_data = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Invalid JSON in {testcases_json_path}: {e}\n")
        return
    except IOError as e:
        sys.stderr.write(f"Error: Could not read {testcases_json_path}: {e}\n")
        return

    js_config = problem_data.get("javascript")
    if not js_config:
        sys.stderr.write(f"Error: 'javascript' configuration not found in {testcases_json_path}\n")
        return

    function_name = js_config.get("functionName")
    # inputs_config = js_config.get("inputs", []) # For type checking or future use
    # output_type_config = js_config.get("outputType") # For type checking or future use
    test_cases = js_config.get("testCases", [])

    if not all([function_name, test_cases]): # inputs_config and output_type_config are optional for JS execution
        sys.stderr.write(f"Error: Missing JavaScript configuration (functionName or testCases) in {testcases_json_path}\n")
        return

    temp_js_dir = "temp_js_runner_output"
    if os.path.exists(temp_js_dir):
        shutil.rmtree(temp_js_dir)
    os.makedirs(temp_js_dir, exist_ok=True)

    # Copy user's solution to the temp directory
    temp_user_solution_path = os.path.join(temp_js_dir, "user_module.js")
    try:
        shutil.copy(user_js_file_path, temp_user_solution_path)
    except IOError as e:
        sys.stderr.write(f"Error: Could not copy user's JS solution to temp directory: {e}\n")
        shutil.rmtree(temp_js_dir)
        return
        
    print(f"Found {len(test_cases)} JavaScript test case(s) for function {function_name}.")
    all_tests_passed = True

    for i, test_case in enumerate(test_cases):
        test_name = test_case.get('name', f"Test Case {i+1}")
        print(f"\n--- Running: {test_name} ---")

        runner_script_content = f"""
const userSolution = require('./user_module.js');
const fs = require('fs'); // For potential complex object logging, not strictly needed for stdout

const funcToTest = userSolution.{function_name} || userSolution; // Handle direct export or object export

try {{
    const args = process.argv.slice(2).map(arg => JSON.parse(arg));
    const result = funcToTest(...args);
    process.stdout.write(JSON.stringify(result !== undefined ? result : null)); // Ensure undefined is null for JSON
}} catch (e) {{
    const errorOutput = {{
        error: e.message || "An unknown error occurred",
        stacktrace_preview: e.stack ? e.stack.split('\\n')[0] + (e.stack.split('\\n')[1] ? " " + e.stack.split('\\n')[1].trim() : "") : "No stack trace"
    }};
    process.stdout.write(JSON.stringify(errorOutput)); // Send error as JSON on stdout
}}
"""
        runner_script_path = os.path.join(temp_js_dir, "user_solution_runner.js")
        try:
            with open(runner_script_path, "w") as f:
                f.write(runner_script_content)
        except IOError as e:
            sys.stderr.write(f"Error: Could not write generated JS runner script: {e}\n")
            all_tests_passed = False
            continue

        serialized_args = [json.dumps(arg) for arg in test_case["args"]]
        
        execute_command = [
            "node",
            runner_script_path
        ] + serialized_args
        
        try:
            execute_proc = subprocess.run(execute_command, capture_output=True, text=True, timeout=5) # 5 second timeout
        except subprocess.TimeoutExpired:
            sys.stderr.write(f"Test {test_name}: FAIL - Execution timed out.\n")
            all_tests_passed = False
            continue

        if execute_proc.stderr:
            sys.stderr.write(f"Warning: Execution STDERR for {test_name}:\n{execute_proc.stderr}\n")

        raw_output = execute_proc.stdout.strip()
        if not raw_output: # Handle cases where stdout might be empty
            sys.stderr.write(f"Test {test_name}: FAIL - No output from script.\n")
            all_tests_passed = False
            continue

        try:
            actual_output_json = json.loads(raw_output)
            if isinstance(actual_output_json, dict) and "error" in actual_output_json:
                error_details = actual_output_json["error"]
                stacktrace_preview = actual_output_json.get("stacktrace_preview", "")
                sys.stderr.write(f"Test {test_name}: FAIL - Execution error in user code: {error_details}. Preview: {stacktrace_preview}\n")
                all_tests_passed = False
                continue
        except json.JSONDecodeError:
            sys.stderr.write(f"Test {test_name}: FAIL - Output was not valid JSON: {raw_output}\n")
            all_tests_passed = False
            continue
            
        expected_output = test_case["expectedOutput"]
        comparison_mode = test_case.get("comparisonMode", "exactOrder")

        if comparison_mode == "exactOrder":
            if actual_output_json == expected_output:
                print(f"Test {test_name}: PASS")
            else:
                print(f"Test {test_name}: FAIL")
                print(f"  Expected: {json.dumps(expected_output)}")
                print(f"  Actual  : {json.dumps(actual_output_json)}")
                all_tests_passed = False
        elif comparison_mode == "linkedListExact":
            if _compare_linked_lists(actual_output_json, expected_output):
                print(f"Test {test_name}: PASS")
            else:
                print(f"Test {test_name}: FAIL")
                print(f"  Expected: {json.dumps(expected_output)}")
                print(f"  Actual  : {json.dumps(actual_output_json)}")
                all_tests_passed = False
        else:
            print(f"Warning: Unknown comparisonMode '{comparison_mode}' for {test_name}. Skipping comparison.")
            all_tests_passed = False

    # Cleanup
    if os.path.exists(temp_js_dir):
        shutil.rmtree(temp_js_dir)

    if all_tests_passed:
        print("\nAll JavaScript tests passed!")
    else:
        print("\nSome JavaScript tests failed.")


def execute_java_solution(problem_folder_path, user_java_file_path):
    print(f"\n--- Executing Java Solution for {problem_folder_path} ---")
    
    testcases_json_path = os.path.join(problem_folder_path, "testcases.json")
    if not os.path.exists(testcases_json_path):
        sys.stderr.write(f"Error: testcases.json not found in {problem_folder_path}\n")
        return

    try:
        with open(testcases_json_path, 'r') as f:
            problem_data = json.load(f)
    except json.JSONDecodeError as e:
        sys.stderr.write(f"Error: Invalid JSON in {testcases_json_path}: {e}\n")
        return
    except IOError as e:
        sys.stderr.write(f"Error: Could not read {testcases_json_path}: {e}\n")
        return

    java_config = problem_data.get("java")
    if not java_config:
        sys.stderr.write(f"Error: 'java' configuration not found in {testcases_json_path}\n")
        return

    user_class_name = java_config.get("className")
    method_name = java_config.get("methodName")
    # input_types_config = java_config.get("inputs", []) # [{name: "nums", type: "int[]"}, ...]
    # output_type_config = java_config.get("outputType") # "int[]"
    test_cases = java_config.get("testCases", [])

    if not all([user_class_name, method_name, test_cases]):
        sys.stderr.write(f"Error: Missing Java configuration (className, methodName, or testCases) in {testcases_json_path}\n")
        return

    temp_compile_dir = "temp_java_compile_output"
    gson_jar_path = "java_runner_utils/gson.jar"

    if not os.path.exists(gson_jar_path):
        sys.stderr.write(f"Error: Gson JAR not found at {gson_jar_path}. Please ensure it's downloaded.\n")
        return

    if os.path.exists(temp_compile_dir):
        shutil.rmtree(temp_compile_dir)
    os.makedirs(temp_compile_dir, exist_ok=True)

    try:
        with open("java_runner_utils/UserSolutionRunner_template.java", "r") as f_template:
            runner_template_content = f_template.read()
    except IOError as e:
        sys.stderr.write(f"Error: Could not read UserSolutionRunner_template.java: {e}\n")
        return

    print(f"Found {len(test_cases)} Java test case(s) for method {method_name}.")

    all_tests_passed = True
    for i, test_case in enumerate(test_cases):
        test_name = test_case.get('name', f"Test Case {i+1}")
        print(f"\n--- Running: {test_name} ---")

        # 1. Generate UserSolutionRunner.java from template
        user_imports_str = "" # TODO: Potentially extract from user solution or config
        gson_type_vars_str = ""
        arg_deserialization_str = ""
        method_call_args_str = []
        
        input_types_config = java_config.get("inputs", [])
        
        # Prepare Gson TypeTokens and argument deserialization
        for idx, input_conf in enumerate(input_types_config):
            java_type, gson_token_str, _ = _get_java_type_and_gson_token(input_conf["type"])
            if not java_type:
                sys.stderr.write(f"Error: Unsupported Java type '{input_conf['type']}' for input '{input_conf['name']}'.\n")
                all_tests_passed = False
                continue # to next test case
            
            gson_type_vars_str += f"    static Type {input_conf['name']}Type = {gson_token_str};\n"
            arg_deserialization_str += f"            {java_type} {input_conf['name']}_arg = gson.fromJson(args[{idx}], {input_conf['name']}Type);\n"
            method_call_args_str.append(f"{input_conf['name']}_arg")

        method_call_str = f"result = solution.{method_name}({', '.join(method_call_args_str)});"

        output_type_config = java_config.get("outputType")
        output_java_type, output_gson_token_str, output_primitive_class = _get_java_type_and_gson_token(output_type_config)
        if not output_java_type:
            sys.stderr.write(f"Error: Unsupported Java type '{output_type_config}' for output.\n")
            all_tests_passed = False
            continue

        if output_primitive_class: # e.g. int.class
            result_serialization_str = f"System.out.print(gson.toJson(result, {output_primitive_class}));"
        else: # e.g. new TypeToken<int[]>() {}.getType()
            gson_type_vars_str += f"    static Type resultType = {output_gson_token_str};\n"
            result_serialization_str = "System.out.print(gson.toJson(result, resultType));"


        runner_code = runner_template_content.replace("{{USER_IMPORTS}}", user_imports_str)
        runner_code = runner_code.replace("{{GSON_TYPE_VARIABLES}}", gson_type_vars_str)
        runner_code = runner_code.replace("{{USER_CLASS_NAME}}", user_class_name)
        runner_code = runner_code.replace("{{ARGUMENT_DESERIALIZATION_AND_METHOD_CALL}}", arg_deserialization_str + "            " + method_call_str)
        runner_code = runner_code.replace("{{RESULT_SERIALIZATION}}", result_serialization_str)
        # TODO: Handle {{HELPER_CLASSES}} if necessary, for now it's empty

        runner_java_path = os.path.join(temp_compile_dir, "UserSolutionRunner.java")
        try:
            with open(runner_java_path, "w") as f_runner:
                f_runner.write(runner_code)
        except IOError as e:
            sys.stderr.write(f"Error: Could not write generated UserSolutionRunner.java: {e}\n")
            all_tests_passed = False
            continue

        # 2. Compile
        # javac -cp java_runner_utils/gson.jar -d temp_java_compile_output temp_java_compile_output/UserSolutionRunner.java <user_java_file_path>
        compile_command = [
            "javac",
            "-cp", f"{gson_jar_path}{os.pathsep}{temp_compile_dir}", # Add temp_compile_dir to classpath for user solution
            "-d", temp_compile_dir,
            runner_java_path,
            user_java_file_path
        ]
        # print(f"Compile command: {' '.join(compile_command)}")
        compile_proc = subprocess.run(compile_command, capture_output=True, text=True)

        if compile_proc.returncode != 0:
            sys.stderr.write(f"Error: Compilation failed for {test_name}.\n")
            sys.stderr.write("Compiler STDOUT:\n" + compile_proc.stdout + "\n")
            sys.stderr.write("Compiler STDERR:\n" + compile_proc.stderr + "\n")
            all_tests_passed = False
            continue # To next test case

        # 3. Execute
        serialized_args = []
        for arg_value in test_case["args"]:
            serialized_args.append(json.dumps(arg_value))
        
        execute_command = [
            "java",
            "-cp", f"{temp_compile_dir}{os.pathsep}{gson_jar_path}",
            "UserSolutionRunner"
        ] + serialized_args
        # print(f"Execute command: {' '.join(execute_command)}")
        
        try:
            execute_proc = subprocess.run(execute_command, capture_output=True, text=True, timeout=5) # 5 second timeout
        except subprocess.TimeoutExpired:
            sys.stderr.write(f"Test {test_name}: FAIL - Execution timed out.\n")
            all_tests_passed = False
            continue

        if execute_proc.stderr: # Java runner might print its own errors to stderr, or JVM errors
            sys.stderr.write(f"Warning: Execution STDERR for {test_name}:\n{execute_proc.stderr}\n")

        raw_output = execute_proc.stdout.strip()
        # print(f"Raw output: {raw_output}")
        
        try:
            actual_output_json = json.loads(raw_output)
            if "error" in actual_output_json:
                error_details = actual_output_json["error"]
                stacktrace_preview = actual_output_json.get("stacktrace_preview", "")
                sys.stderr.write(f"Test {test_name}: FAIL - Execution error in user code: {error_details}. Preview: {stacktrace_preview}\n")
                all_tests_passed = False
                continue
        except json.JSONDecodeError:
            sys.stderr.write(f"Test {test_name}: FAIL - Output was not valid JSON: {raw_output}\n")
            all_tests_passed = False
            continue
            
        # 4. Compare results
        expected_output = test_case["expectedOutput"]
        comparison_mode = test_case.get("comparisonMode", "exactOrder")

        # For now, only "exactOrder" for basic types / arrays of primitives
        # TODO: Implement "linkedListExact" and other modes
        if comparison_mode == "exactOrder":
            if actual_output_json == expected_output:
                print(f"Test {test_name}: PASS")
            else:
                print(f"Test {test_name}: FAIL")
                print(f"  Expected: {json.dumps(expected_output)}")
                print(f"  Actual  : {json.dumps(actual_output_json)}")
                all_tests_passed = False
        elif comparison_mode == "linkedListExact":
            # Placeholder for ListNode comparison
            if _compare_linked_lists(actual_output_json, expected_output):
                print(f"Test {test_name}: PASS")
            else:
                print(f"Test {test_name}: FAIL")
                print(f"  Expected: {json.dumps(expected_output)}")
                print(f"  Actual  : {json.dumps(actual_output_json)}")
                all_tests_passed = False
        else:
            print(f"Warning: Unknown comparisonMode '{comparison_mode}' for {test_name}. Skipping comparison.")
            all_tests_passed = False # Consider unknown as fail for safety

    # Cleanup
    if os.path.exists(temp_compile_dir):
        shutil.rmtree(temp_compile_dir)

    if all_tests_passed:
        print("\nAll Java tests passed!")
    else:
        print("\nSome Java tests failed.")


def _get_java_type_and_gson_token(type_str):
    """Maps a type string from testcases.json to Java type and Gson TypeToken string."""
    if type_str == "int[]":
        return "int[]", "new TypeToken<int[]>() {}.getType()", None
    elif type_str == "int":
        return "int", "int.class", "int.class" # Primitive needs special handling for gson.toJson
    elif type_str == "String":
        return "String", "String.class", "String.class"
    elif type_str == "String[]":
        return "String[]", "new TypeToken<String[]>() {}.getType()", None
    elif type_str == "ListNode":
        # Assuming ListNode class is defined by the user or will be injected.
        # The UserSolutionRunner_template.java expects ListNode to be available.
        return "ListNode", "new TypeToken<ListNode>() {}.getType()", None
    # Add more types as needed: double, boolean, List<Integer>, Map<String, String> etc.
    # For List<Integer>: "List<Integer>", "new TypeToken<List<Integer>>() {}.getType()", None
    else:
        return None, None, None # Unsupported type

def _compare_linked_lists(list1_json, list2_json):
    """Compares two linked lists represented as JSON objects (Python dicts)."""
    # Traverses the lists node by node, comparing 'val' and structure.
    # Handles null lists or differing lengths.
    current1 = list1_json
    current2 = list2_json

    while current1 and current2:
        if current1.get("val") != current2.get("val"):
            return False # Values differ
        current1 = current1.get("next")
        current2 = current2.get("next")

    # If one list is longer than the other
    if current1 or current2:
        return False 
    
    return True # Both lists are exhausted and all values matched


def prompt_and_save_solution(language_name, filename):
    """Prompts the user for a solution in a given language and saves it to a file."""
    print(f"\nPlease paste your {language_name} solution code below. Type 'EOF' on a new line and press Enter when done:")
    lines = []
    while True:
        try:
            line = input()
            if line == "EOF":
                break
            lines.append(line)
        except EOFError: # This can happen if input is redirected from a file that ends prematurely
            break
    
    solution_code = "\n".join(lines)

    try:
        with open(filename, "w") as f:
            f.write(solution_code)
        print(f"{language_name} solution saved to {filename}")
    except IOError as e:
        sys.stderr.write(f"Error: Could not save {language_name} solution to {filename}: {e}\n")

if __name__ == "__main__":
    main()
