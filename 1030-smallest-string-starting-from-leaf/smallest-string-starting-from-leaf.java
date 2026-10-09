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
    String ans="";
    public String smallestFromLeaf(TreeNode root) {
       dfs(root,"");
       return ans;
    }
    private void dfs(TreeNode root,String path){
        if(root==null)return;
        path=(char) ('a'+root.val)+path;
        if(root.left==null&&root.right==null){
            if(ans.equals("")||path.compareTo(ans)<0){
                ans=path;
            }
            return;
        }
        dfs(root.left,path);
        dfs(root.right,path);
    }
}