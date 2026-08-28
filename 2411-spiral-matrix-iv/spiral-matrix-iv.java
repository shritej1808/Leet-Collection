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
    public int[][] spiralMatrix(int m, int n, ListNode head) {
        int[][] matrix = new int[m][n];

       for(int i=0;i<m;i++){
        Arrays.fill(matrix[i], -1);
       }
        int rowBegin=0;
        int colBegin=0;
        int rowEnd=m-1;
        int colEnd=n-1;
       while(rowBegin<=rowEnd && colBegin<=colEnd && head!=null ){
        for(int j=colBegin;j<=colEnd && head!=null;j++ ){
            matrix[rowBegin][j]=head.val;
            head=head.next;

       }
       rowBegin++;
       for(int j=rowBegin;j<=rowEnd && head!=null;j++ ){
            matrix[j][colEnd]=head.val;
            head=head.next;

       }
       colEnd--;
       if(rowBegin<=rowEnd){
        for(int j=colEnd;j>=colBegin && head!=null;j--){
            matrix[rowEnd][j]=head.val;
            head=head.next;

       }
       rowEnd--;
       }
       
       if(colBegin<=colEnd){
        for(int j=rowEnd;j>=rowBegin && head!=null;j-- ){
            matrix[j][colBegin]=head.val;
            head=head.next;

       }
       colBegin++;
       }

       

       }
       return matrix;

    }
}