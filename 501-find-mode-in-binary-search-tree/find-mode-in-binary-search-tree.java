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
    public int[] findMode(TreeNode root) {
        Map<Integer,Integer> map=new HashMap<>();
      Queue<TreeNode> queue=new LinkedList<>();
      queue.add(root);
      while(!queue.isEmpty()){
        TreeNode node=queue.poll();
        map.merge(node.val,1,Integer::sum);

        if(node.left!=null) queue.add(node.left);
        if(node.right!=null) queue.add(node.right);

      }
      int max=Integer.MIN_VALUE;
      List<Integer> list=new ArrayList<>();
      for(int key:map.keySet()){
        int val=map.get(key);
        if(val>max){
            max=val;
            list.clear();
            list.add(key);
        }else if(val==max){
            list.add(key);
        }
        

      }
      int[] arr=new int[list.size()];
        for(int i=0;i<list.size();i++){
            arr[i]=list.get(i);
        }
        return arr;
    }
}