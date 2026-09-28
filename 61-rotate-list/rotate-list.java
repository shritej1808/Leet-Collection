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
    public ListNode rotateRight(ListNode head, int k) {
        ListNode end=head;
        int len=1;
        if(head==null||head.next==null||k==0) return head;
        while(end.next!=null){
            end=end.next;
            len++;
        }
         
        k%=len;
        end.next=head;
        int steps=len-k;
        ListNode newend=head;
        for(int i=1;i<steps;i++) newend=newend.next;
        ListNode newhead=newend.next;
        newend.next=null;
        return newhead;

    }}