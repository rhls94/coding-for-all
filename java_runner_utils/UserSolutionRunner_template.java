import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.gson.JsonSyntaxException;
import java.lang.reflect.Type;
import com.google.gson.reflect.TypeToken;

// {{USER_IMPORTS}} // User's solution might require specific imports for ListNode, etc.

// If ListNode is used, its definition is expected to be in the user's solution file.
// For example:
/*
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}
*/

public class UserSolutionRunner {

    // {{GSON_TYPE_VARIABLES}}
    // e.g. static Type intArrType = new TypeToken<int[]>() {}.getType();
    //      static Type listNodeType = new TypeToken<ListNode>() {}.getType();


    public static void main(String[] args) {
        Gson gson = new GsonBuilder().serializeNulls().create();
        // {{USER_CLASS_NAME}} solution = new {{USER_CLASS_NAME}}(); // User's class instantiation
        Object result = null;
        String errorOutput = null;

        try {
            // {{ARGUMENT_DESERIALIZATION_AND_METHOD_CALL}}
            // Example for a method `int[] twoSum(int[] nums, int target)`:
            // int[] nums_arg = gson.fromJson(args[0], intArrType);
            // int target_arg = gson.fromJson(args[1], int.class);
            // result = solution.twoSum(nums_arg, target_arg);

        } catch (JsonSyntaxException e) {
            errorOutput = "{\"error\": \"JSON deserialization failed: " + e.getMessage().replace("\"", "\\\"") + "\"}";
        } catch (Exception e) {
            String exceptionType = e.getClass().getSimpleName();
            String exceptionMsg = e.getMessage() != null ? e.getMessage().replace("\"", "\\\"") : "No message";
            errorOutput = "{\"error\": \"Execution failed: " + exceptionType + " - " + exceptionMsg + "\", \"stacktrace_preview\": \"" + getStackTracePreview(e) + "\"}";
        }

        if (errorOutput != null) {
            System.out.print(errorOutput); // Use print instead of println to avoid extra newline
        } else {
            // {{RESULT_SERIALIZATION}}
            // Example for `int[]` return type:
            // System.out.print(gson.toJson(result, intArrType));
            // Example for `ListNode` return type:
            // System.out.print(gson.toJson(result, listNodeType));
            // Example for primitive return type like `int`:
            // System.out.print(gson.toJson(result, int.class));
        }
    }

    private static String getStackTracePreview(Exception e) {
        StackTraceElement[] stackTrace = e.getStackTrace();
        if (stackTrace.length > 0) {
            StackTraceElement element = stackTrace[0];
            return element.getClassName() + "." + element.getMethodName() + " (Line " + element.getLineNumber() + ")";
        }
        return "No stack trace available";
    }

    // {{HELPER_CLASSES}}
    // e.g. ListNode class definition might be injected here if not provided by user,
    // or if a standard one is needed for testing.
    // However, the current approach expects user to provide it.
}
