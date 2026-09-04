class Solution {
    public int leastInterval(char[] tasks, int n) {
        HashMap<Character,Integer> map=new HashMap<>();
        for(char c: tasks){
            map.merge(c,1,Integer::sum);
        }
        int maxfreq=0;
        for(int freq: map.values()){
            maxfreq=Math.max(maxfreq,freq);
        }
        int maxCount=0;
        for(int freq:map.values()){
            if(freq==maxfreq){
                maxCount++;
            }
        }
        int result=(maxfreq-1)*(n+1)+maxCount;
        return Math.max(result,tasks.length);
    }
}