def reverse_list(head):
    prev = None
    cur = head
    while cur:
        nxt = cur.next        # сохранить ДО перезаписи
        cur.next = prev
        prev = cur
        cur = nxt
    return prev
