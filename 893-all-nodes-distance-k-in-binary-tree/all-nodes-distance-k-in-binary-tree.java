class Solution {

    Map<TreeNode, TreeNode> parent = new HashMap<>();

    public List<Integer> distanceK(TreeNode root, TreeNode target, int k) {

        // Store parent of every node
        findParent(root, null);

        Queue<TreeNode> queue = new LinkedList<>();
        Set<TreeNode> visited = new HashSet<>();

        queue.offer(target);
        visited.add(target);

        int distance = 0;

        while (!queue.isEmpty()) {

            int size = queue.size();

            if (distance == k) break;

            for (int i = 0; i < size; i++) {

                TreeNode curr = queue.poll();

                if (curr.left != null && visited.add(curr.left))
                    queue.offer(curr.left);

                if (curr.right != null && visited.add(curr.right))
                    queue.offer(curr.right);

                TreeNode p = parent.get(curr);

                if (p != null && visited.add(p))
                    queue.offer(p);
            }

            distance++;
        }

        List<Integer> result = new ArrayList<>();

        while (!queue.isEmpty()) {
            result.add(queue.poll().val);
        }

        return result;
    }

    private void findParent(TreeNode root, TreeNode p) {

        if (root == null) return;

        parent.put(root, p);

        findParent(root.left, root);
        findParent(root.right, root);
    }
}