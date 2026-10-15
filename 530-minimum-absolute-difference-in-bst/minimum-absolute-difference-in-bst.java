/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) {
 *         this.val = val;
 *         this.left = left;
 *         this.right = right;
 *     }
 * }
 */
class Solution {
    int prev=Integer.MAX_VALUE;
    int ans=Integer.MAX_VALUE;
    public int getMinimumDifference(TreeNode root) {
        inorder(root);
        return ans;
        
    }
    private int inorder(TreeNode node){
        if(node.left!=null)inorder(node.left);
        ans=Math.min(ans,Math.abs(node.val-prev));
        prev=node.val;
        if(node.right!=null) inorder(node.right);
        return ans; 

    }
}