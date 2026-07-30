def middle_node(head):
    slow = fast = head
    while fast and fast.next:      # даёт ВТОРОЙ центр при чётной длине
        slow = slow.next
        fast = fast.next.next
    return slow
