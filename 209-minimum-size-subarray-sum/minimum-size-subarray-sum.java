class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left=0;
        int right=0;
        int minSubLen=Integer.MAX_VALUE;
        int currSum=0;
        while(right<nums.length){
            currSum+=nums[right];
            right++;
            while(currSum>=target){
                int MaxWindow=right-left;
                minSubLen=Math.min(minSubLen,MaxWindow);
                currSum-=nums[left];
                left++;
            }
        }
        return minSubLen==Integer.MAX_VALUE ? 0:minSubLen;
    }
}