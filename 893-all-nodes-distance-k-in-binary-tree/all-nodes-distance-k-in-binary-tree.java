/**
 * Definition for a binary tree node.
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    Map<TreeNode, TreeNode> parentMap=new HashMap<>();
    public List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
        findParent(root,null);
        Queue<TreeNode> queue=new LinkedList<>();
        Set<TreeNode> visited=new HashSet<>();
        queue.offer(target);
        visited.add(target);
        int distance=0;
        while(!queue.isEmpty()){
            int size=queue.size();
            if(distance==k) break;
            
            for(int i=0;i<size;i++){
                TreeNode curr=queue.poll();
                if(curr.left!=null && visited.add(curr.left)){
                queue.offer(curr.left);
            }
            if(curr.right!=null && visited.add(curr.right)){
                queue.offer(curr.right);
            }
            TreeNode parent=parentMap.get(curr);
            if(parent!=null && visited.add(parent)){
                queue.offer(parent);
            }
            }
          distance++;
        }
        List<Integer> list=new ArrayList<>();
         while (!queue.isEmpty()) {
            list.add(queue.poll().val);
        }
        return list;

        
    }
    private void findParent(TreeNode root,TreeNode p){
        if(root==null) return;
        parentMap.put(root,p);
        findParent(root.left,root);
        findParent(root.right,root);
    }
}