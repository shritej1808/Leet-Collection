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
    public ListNode reverseKGroup(ListNode head, int k) {
        ListNode dummy=new ListNode(0);
        dummy.next=head;

        
        ListNode before = dummy;
        while(true){
            ListNode kth=before;
            for(int i=0;i<k;i++){
                if(kth.next!=null){
                    kth=kth.next;
                }
                else{
                    return dummy.next;
                }
            }
            ListNode first=before.next;
            ListNode after=kth.next;
            ListNode prev=after;
            ListNode curr=first;
            while(curr!=after){
                ListNode next=curr.next;
                curr.next=prev;
                prev=curr;
                curr=next;
            }
            before.next=prev;
            before=first;
        }
    }
}