class Solution {
    public String frequencySort(String s) {
        HashMap<Character,Integer> map=new HashMap<>();
        for (char c : s.toCharArray()) {
            map.merge(c, 1, Integer::sum);
        }

     List<Character> list=new ArrayList<>(map.keySet());
     list.sort((a,b)->map.get(b)-map.get(a));
     String result="";
     for(char c: list ){
        for(int i=0;i<map.get(c);i++){
            result+=c;
        }
     }
     return result;

    }
}