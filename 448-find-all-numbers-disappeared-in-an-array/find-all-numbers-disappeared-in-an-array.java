class Solution {
    public List<Integer> findDisappearedNumbers(int[] nums) {
        int n=nums.length;
        ArrayList<Integer> list=new ArrayList<>();
        HashMap<Integer,Integer> map=new HashMap<>();
        for(int i=0;i<n;i++){
            map.put(nums[i],i);
        }
        for(int j=1;j<=n;j++){
            if(!map.containsKey(j)){
                list.add(j);
            }
        }
return list;

    }
}