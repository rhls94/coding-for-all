/**
 * @param {number[]} nums
 * @param {number} target
 * @return {number[]}
 */
const twoSum = function(nums, target) {
    const numMap = new Map();
    
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        
        if (numMap.has(complement)) {
            return [numMap.get(complement), i];
        }
        
        numMap.set(nums[i], i);
    }
    
    return [];
};

// Test Case 1
const nums1 = [2, 7, 11, 15];
const target1 = 9;
const result1 = twoSum(nums1, target1);
console.log("Test Case: nums = [2,7,11,15], target = 9");
console.log("Expected: [0,1] or [1,0]");
console.log("Actual:", result1);
console.log();

// Test Case 2
const nums2 = [3, 2, 4];
const target2 = 6;
const result2 = twoSum(nums2, target2);
console.log("Test Case: nums = [3,2,4], target = 6");
console.log("Expected: [1,2] or [2,1]");
console.log("Actual:", result2);
console.log();

// Test Case 3
const nums3 = [3, 3];
const target3 = 6;
const result3 = twoSum(nums3, target3);
console.log("Test Case: nums = [3,3], target = 6");
console.log("Expected: [0,1] or [1,0]");
console.log("Actual:", result3);