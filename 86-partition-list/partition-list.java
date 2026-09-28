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
    public ListNode partition(ListNode head, int x) {
        ListNode smallDummy=new ListNode(0);
        ListNode greaterDummy=new ListNode(0);
        ListNode small=smallDummy;
        ListNode great=greaterDummy;

        ListNode curr=head;
        while(curr!=null){
            if(curr.val<x){
                small.next=curr;
                small=small.next;
            }
            else{
                great.next=curr;
                great=great.next;
            }
            curr=curr.next;
        }
        great.next=null;
        small.next=greaterDummy.next;
        return smallDummy.next;
    }
}