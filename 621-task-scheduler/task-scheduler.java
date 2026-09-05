class Solution {
    public int leastInterval(char[] tasks, int n) {
        HashMap<Character,Integer> map=new HashMap<>();
        for(char c: tasks){
            map.merge(c,1,Integer::sum);
        }
        int freqCount=0;
        for(int freq: map.values()){
            freqCount=Math.max(freqCount,freq);
        }
        int maxCount=0;
        for(int freq: map.values()){
            if(freq==freqCount){
                maxCount++;
            }
        }
        int result=(freqCount-1)*(n+1)+maxCount;
        return Math.max(result,tasks.length);

    }
}