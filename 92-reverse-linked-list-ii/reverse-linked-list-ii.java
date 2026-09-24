/**
 * Definition for singly-linked list.
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
class Solution {
    public ListNode reverseBetween(ListNode head, int left, int right) {
        ListNode dummy=new ListNode(0);
        dummy.next=head;
        ListNode before=dummy;
        for(int i=1;i<left;i++){
            before=before.next;
        }
        
        ListNode after=before.next;
        for(int i=0;i<right-left+1;i++){
            after=after.next;
        }
        ListNode prev=before;
        ListNode curr=before.next;
        ListNode first=curr;
        while(curr!=after){
            ListNode next=curr.next;
            curr.next=prev;
            prev=curr;
            curr=next;
        }
        before.next=prev;
        first.next=after;
        
        return dummy.next;
    }}