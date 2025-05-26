class Node {
  constructor(value) {
    this.value = value;
    this.next = null;
  }
}
class LinkedList {
  constructor() {
    this.head = null;
    this.tail = null;
  }

  append(value) {
    const newNode = new Node(value);
    if (!this.head) {
      this.head = newNode;
      this.tail = newNode;
    } else {
      this.tail.next = newNode;
      this.tail = newNode;
    }
  }

  toArray() {
    const result = [];
    let current = this.head;
    while (current) {
      result.push(current.value);
      current = current.next;
    }
    return result;
  }
}

var addTwoNumbers = function(l1, l2) {
  const resultList = new LinkedList();
  let p = l1.head, q = l2.head;
  let carry = 0;

  while (p || q || carry) {
    const x = p ? p.value : 0;
    const y = q ? q.value : 0;
    const sum = x + y + carry;
    carry = Math.floor(sum / 10);
    resultList.append(sum % 10);
    if (p) p = p.next;
    if (q) q = q.next;
  }

  return resultList.toArray();
};