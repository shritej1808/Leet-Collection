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
    TreeNode dummy=new TreeNode(0);
    
    
    public List<Integer> inorderTraversal(TreeNode root) {
        dummy.right=root;
        TreeNode prev=dummy, curr=root;
        while(curr!=null){
            if(curr.left!=null){
                TreeNode left=curr.left;
            TreeNode temp=left;
            while(temp.right!=null)temp=temp.right;
            temp.right=curr;
            prev.right=left;
            curr.left=null;
            curr=left;}
        
        else{
          prev=curr;
          curr=curr.right;
        }}
        List<Integer> list=new ArrayList<>();
        TreeNode x=dummy.right;
        while(x!=null){
            list.add(x.val);
            x=x.right;
        }
        return list;

    }
}