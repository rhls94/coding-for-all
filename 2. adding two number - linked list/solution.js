// Definition for singly-linked list.
function ListNode(val, next) {
    this.val = (val===undefined ? 0 : val);
    this.next = (next===undefined ? null : next);
}

/**
 * @param {ListNode} l1
 * @param {ListNode} l2
 * @return {ListNode}
 */
var addTwoNumbers = function(l1, l2) {
    let dummyHead = new ListNode(0);
    let p = l1, q = l2, current = dummyHead;
    let carry = 0;

    while (p !== null || q !== null) {
        const x = (p !== null) ? p.val : 0;
        const y = (q !== null) ? q.val : 0;
        const sum = carry + x + y;
        carry = Math.floor(sum / 10);
        current.next = new ListNode(sum % 10);
        current = current.next;
        if (p !== null) p = p.next;
        if (q !== null) q = q.next;
    }

    if (carry > 0) {
        current.next = new ListNode(carry);
    }
    return dummyHead.next;
};

function printList(node) {
    if (!node) {
        return "[]";
    }
    const result = [];
    while (node !== null) {
        result.push(node.val);
        node = node.next;
    }
    return "[" + result.join(",") + "]";
}

// Example 1: l1 = [2,4,3], l2 = [5,6,4], Expected: [7,0,8]
let l1_ex1 = new ListNode(2, new ListNode(4, new ListNode(3)));
let l2_ex1 = new ListNode(5, new ListNode(6, new ListNode(4)));
let expected_ex1 = new ListNode(7, new ListNode(0, new ListNode(8)));
let result_ex1 = addTwoNumbers(l1_ex1, l2_ex1);
console.log("Example 1:");
console.log("l1:", printList(l1_ex1));
console.log("l2:", printList(l2_ex1));
console.log("Expected:", printList(expected_ex1));
console.log("Actual:", printList(result_ex1));
console.log();

// Example 2: l1 = [0], l2 = [0], Expected: [0]
let l1_ex2 = new ListNode(0);
let l2_ex2 = new ListNode(0);
let expected_ex2 = new ListNode(0);
let result_ex2 = addTwoNumbers(l1_ex2, l2_ex2);
console.log("Example 2:");
console.log("l1:", printList(l1_ex2));
console.log("l2:", printList(l2_ex2));
console.log("Expected:", printList(expected_ex2));
console.log("Actual:", printList(result_ex2));
console.log();

// Example 3: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9], Expected: [8,9,9,9,0,0,0,1]
let l1_ex3 = new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9)))))));
let l2_ex3 = new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9))));
let expected_ex3 = new ListNode(8, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(0, new ListNode(0, new ListNode(0, new ListNode(1))))))));
let result_ex3 = addTwoNumbers(l1_ex3, l2_ex3);
console.log("Example 3:");
console.log("l1:", printList(l1_ex3));
console.log("l2:", printList(l2_ex3));
console.log("Expected:", printList(expected_ex3));
console.log("Actual:", printList(result_ex3));
console.log();