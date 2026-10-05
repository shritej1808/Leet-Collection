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
    public List<String> binaryTreePaths(TreeNode root) {
        List<String> answer=new ArrayList<>();
        dfs(root,"",answer);
        return answer;
    }
    private void dfs(TreeNode node,String path,List<String> answer){
        if(node.left==null&&node.right==null) answer.add(path+node.val);
        if(node.left!=null) dfs(node.left,path+node.val+"->",answer);
        if(node.right!=null) dfs(node.right,path+node.val+"->",answer);
        
    }
}