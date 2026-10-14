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
        Queue<TreeNode> queue = new LinkedList<>();
        queue.add(root);

          // Traversing using queue 
        // To Traverse all the element according to the Level
        while (!queue.isEmpty()) {
            TreeNode tempNode = queue.poll();
            map.merge(tempNode.val,1, Integer::sum);

            if (tempNode.left != null)
                queue.add(tempNode.left);

            if (tempNode.right != null)
                queue.add(tempNode.right);}
                int max = Integer.MIN_VALUE;
List<Integer> result = new ArrayList<>();

for (int key : map.keySet()) {
    int val = map.get(key);

    if (val > max) {
        max = val;
        result.clear();
        result.add(key);
    } else if (val == max) {
        result.add(key);
    }
}

int[] arr = new int[result.size()];

for (int i = 0; i < result.size(); i++) {
    arr[i] = result.get(i);
}

return arr;
    }
}