class Solution {
    public int leastInterval(char[] tasks, int n) {
        HashMap<Character,Integer> map=new HashMap<>();
        for(char c: tasks){
            map.merge(c,1,Integer::sum);
        }
        int freqMax=0;
        for(int freq: map.values()){
            freqMax=Math.max(freqMax,freq);
        }
        int maxCount=0;
        for(int freq: map.values()){
            if(freq==freqMax){
                maxCount++;
            }
        }
        int result=(freqMax-1)*(n+1)+maxCount;
        return Math.max(result,tasks.length);
    }
}