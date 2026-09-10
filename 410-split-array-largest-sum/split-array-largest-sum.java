class Solution {
    public int splitArray(int[] nums, int k) {

        int left = 0;
        int right = 0;

        // Find search range
        for (int num : nums) {
            left = Math.max(left, num);
            right += num;
        }

        while (left < right) {

            int mid = left + (right - left) / 2;

            int subarrays = 1;
            int currentSum = 0;

            for (int num : nums) {

                if (currentSum + num > mid) {
                    subarrays++;
                    currentSum = num;
                } else {
                    currentSum += num;
                }
            }

            if (subarrays <= k) {
                // mid works, try smaller
                right = mid;
            } else {
                // mid is too small
                left = mid + 1;
            }
        }

        return left;
    }
}