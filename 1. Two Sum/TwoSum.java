import java.util.HashMap;
import java.util.Map;
class TwoSum {
    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> numMap = new HashMap<>();
        
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            
            if (numMap.containsKey(complement)) {
                return new int[] { numMap.get(complement), i };
            }
            
            numMap.put(nums[i], i);
        }
        
        return new int[] {};
    }

    public static void main(String[] args) {
        TwoSum solution = new TwoSum();

        // Test Case 1 (Original)
        int[] nums1 = {2, 7, 11, 15};
        int target1 = 9;
        int[] result1 = solution.twoSum(nums1, target1);
        System.out.println("Test Case: nums = [2,7,11,15], target = 9");
        System.out.println("Expected: [0,1] or [1,0]");
        if (result1.length == 2) {
            System.out.println("Actual: [" + result1[0] + "," + result1[1] + "]");
        } else {
            System.out.println("No two sum solution found.");
        }
        System.out.println();

        // Test Case 2
        int[] nums2 = {3, 2, 4};
        int target2 = 6;
        int[] result2 = solution.twoSum(nums2, target2);
        System.out.println("Test Case: nums = [3,2,4], target = 6");
        System.out.println("Expected: [1,2] or [2,1]");
        if (result2.length == 2) {
            System.out.println("Actual: [" + result2[0] + "," + result2[1] + "]");
        } else {
            System.out.println("No two sum solution found.");
        }
        System.out.println();

        // Test Case 3
        int[] nums3 = {3, 3};
        int target3 = 6;
        int[] result3 = solution.twoSum(nums3, target3);
        System.out.println("Test Case: nums = [3,3], target = 6");
        System.out.println("Expected: [0,1] or [1,0]");
        if (result3.length == 2) {
            System.out.println("Actual: [" + result3[0] + "," + result3[1] + "]");
        } else {
            System.out.println("No two sum solution found.");
        }
    }
}