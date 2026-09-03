class Solution {
    public int[] topKFrequent(int[] nums, int k) {
        HashMap<Integer,Integer> map=new HashMap<>();
        for(int i=0;i<nums.length;i++){
                map.merge(nums[i],1,Integer::sum);
        }
        List<Integer> list = new ArrayList<>(map.keySet());

        list.sort((a, b) -> map.get(b) - map.get(a));

        int[] result=new int[k];
        for (int i = 0; i < k; i++) {
    result[i] = list.get(i);
}
return result;
    }
}