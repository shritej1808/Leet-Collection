class Solution {
    public int maxFrequency(int[] nums, int k) {
        Arrays.sort(nums);
        int left=0;
        int right=0;
        long total=0;
        long result=0;
        while(right<nums.length){
            total+=nums[right];
            
            while(nums[right]*(right-left+1L)>total+k){
                total-=nums[left];
                left++;
            }
            result=Math.max(result,right-left+1L);
            right++;
        }
return (int) result;
        
    }
}