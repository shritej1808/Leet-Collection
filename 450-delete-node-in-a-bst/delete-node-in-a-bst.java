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
    public TreeNode deleteNode(TreeNode root, int key) {
        if(root==null) return null;

        TreeNode curr=root;
        TreeNode parent=null;

        //search for node
        while(curr!=null && curr.val!=key){
            parent=curr;
            if(key<curr.val){
                curr=curr.left;
            }
            else{
                curr=curr.right;
            }
        }
        //node not found
        if(curr==null) return root;
        
        //no child
        if(curr.left==null && curr.right==null){
            if(parent==null) return null;

            if(parent.left==curr){
                parent.left=null;
            }
            else{
                parent.right=null;
            }
        }
        //one child
        else if(curr.left==null || curr.right==null){
            TreeNode child=(curr.left==null)? curr.right: curr.left;
            if(parent==null) return child;
            if(parent.left==curr){
                parent.left=child;
            }
            else{
                parent.right=child;
            }
                
            }
            else{
                TreeNode succParent=curr;
                TreeNode succ=curr.right;

                while(succ.left!=null){
                    succParent=succ;
                    succ=succ.left;
                }
                curr.val=succ.val;

                if(succParent.left==succ){
                    succParent.left=succ.right;
                }
                else{
                    succParent.right=succ.right;
                }


            }
            return root;
        }
        

    }