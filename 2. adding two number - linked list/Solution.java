class Solution{
    class Node {
        int data;
        Node next;
        
        Node(int data) {
            this.data = data;
            this.next = null;
        }
    }
    class LinkedList {
        Node head;
        
        void insert(int data) {
            Node newNode = new Node(data);
            if (head == null) {
                head = newNode;
            } else {
                Node current = head;
                while (current.next != null) {
                    current = current.next;
                }
                current.next = newNode;
            }
        }
        
        void printList() {
            Node current = head;
            while (current != null) {
                System.out.print(current.data + " ");
                current = current.next;
            }
            System.out.println();
        }
    }
    public LinkedList addTwoNumbers(LinkedList l1, LinkedList l2) {
        LinkedList result = new LinkedList();
        Node p1 = l1.head;
        Node p2 = l2.head;
        int carry = 0;

        while (p1 != null || p2 != null || carry > 0) {
            int sum = carry;
            if (p1 != null) {
                sum += p1.data;
                p1 = p1.next;
            }
            if (p2 != null) {
                sum += p2.data;
                p2 = p2.next;
            }
            carry = sum / 10;
            result.insert(sum % 10);
        }

        return result;
    }
}