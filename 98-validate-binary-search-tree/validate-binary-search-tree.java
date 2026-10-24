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
    public boolean isValidBST(TreeNode root) {
        TreeNode curr=root,prev=dummy;
        dummy.right=root;
        while(curr!=null){
            if(curr.left!=null){
                TreeNode left=curr.left;
                TreeNode temp=left;
                while(temp.right!=null) temp=temp.right;
                temp.right=curr;
                prev.right=left;
                curr.left=null;
                curr=left;
            }
            else{
                prev=curr;
                curr=curr.right;
            }

        }
        TreeNode x=dummy.right;
        while (x != null && x.right != null) {
            if (x.val >= x.right.val) {
                return false;
            }
            x = x.right;
        }

        return true;
    }


        
    }
