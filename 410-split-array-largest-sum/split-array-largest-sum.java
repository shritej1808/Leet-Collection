class Solution {
    public int splitArray(int[] nums, int k) {

        int left=0;
        int right=0;
        for(int num:nums){
            left=Math.max(left,num);
            right+=num;
        }
        while(left<right){
            int mid=left+(right-left)/2;
            int currSum=0;
            int subarrays=1;
            for(int num:nums){
                if(currSum+num>mid){
                    subarrays++;
                    currSum=num;
                }
                else{
                    currSum+=num;
                }
            }
            if(subarrays<=k){
                right=mid;
            }
            else{
                left=mid+1;
            }


        }
        return left;
    }
}