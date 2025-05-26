// Definition for singly-linked list.
class ListNode {
    int val;
    ListNode next;
    ListNode() {}
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}

class Solution {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode dummyHead = new ListNode(0);
        ListNode p = l1, q = l2, current = dummyHead;
        int carry = 0;

        while (p != null || q != null) {
            int x = (p != null) ? p.val : 0;
            int y = (q != null) ? q.val : 0;
            int sum = carry + x + y;
            carry = sum / 10;
            current.next = new ListNode(sum % 10);
            current = current.next;
            if (p != null) p = p.next;
            if (q != null) q = q.next;
        }

        if (carry > 0) {
            current.next = new ListNode(carry);
        }
        return dummyHead.next;
    }

    public static void printList(ListNode node) {
        if (node == null) {
            System.out.println("[]");
            return;
        }
        System.out.print("[");
        while (node != null) {
            System.out.print(node.val);
            if (node.next != null) {
                System.out.print(",");
            }
            node = node.next;
        }
        System.out.println("]");
    }

    public static void main(String[] args) {
        Solution solution = new Solution();

        // Example 1: l1 = [2,4,3], l2 = [5,6,4], Expected: [7,0,8]
        ListNode l1_ex1 = new ListNode(2, new ListNode(4, new ListNode(3)));
        ListNode l2_ex1 = new ListNode(5, new ListNode(6, new ListNode(4)));
        ListNode expected_ex1 = new ListNode(7, new ListNode(0, new ListNode(8)));
        ListNode result_ex1 = solution.addTwoNumbers(l1_ex1, l2_ex1);
        System.out.println("Example 1:");
        System.out.print("l1: "); printList(l1_ex1);
        System.out.print("l2: "); printList(l2_ex1);
        System.out.print("Expected: "); printList(expected_ex1);
        System.out.print("Actual: "); printList(result_ex1);
        System.out.println();

        // Example 2: l1 = [0], l2 = [0], Expected: [0]
        ListNode l1_ex2 = new ListNode(0);
        ListNode l2_ex2 = new ListNode(0);
        ListNode expected_ex2 = new ListNode(0);
        ListNode result_ex2 = solution.addTwoNumbers(l1_ex2, l2_ex2);
        System.out.println("Example 2:");
        System.out.print("l1: "); printList(l1_ex2);
        System.out.print("l2: "); printList(l2_ex2);
        System.out.print("Expected: "); printList(expected_ex2);
        System.out.print("Actual: "); printList(result_ex2);
        System.out.println();

        // Example 3: l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9], Expected: [8,9,9,9,0,0,0,1]
        ListNode l1_ex3 = new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9)))))));
        ListNode l2_ex3 = new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(9))));
        ListNode expected_ex3 = new ListNode(8, new ListNode(9, new ListNode(9, new ListNode(9, new ListNode(0, new ListNode(0, new ListNode(0, new ListNode(1))))))));
        ListNode result_ex3 = solution.addTwoNumbers(l1_ex3, l2_ex3);
        System.out.println("Example 3:");
        System.out.print("l1: "); printList(l1_ex3);
        System.out.print("l2: "); printList(l2_ex3);
        System.out.print("Expected: "); printList(expected_ex3);
        System.out.print("Actual: "); printList(result_ex3);
        System.out.println();
    }
}