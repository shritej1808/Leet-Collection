class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        HashMap<Integer,Integer> map=new HashMap<>();
        for(int i=0;i<nums.length;i++){
            map.merge(nums[i],1,Integer::sum);
        }
        List<Integer> list=new ArrayList<>(map.keySet());
        list.sort((a,b)-> map.get(b)-map.get(a));

        int[] result=new int[k];
        for(int j=0;j<k;j++){
            result[j]=list.get(j);
        }
        return result;

    }
}