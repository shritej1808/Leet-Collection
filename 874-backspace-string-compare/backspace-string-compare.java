class Solution {
    public boolean backspaceCompare(String s, String t) {
    return getActual(s).equals(getActual(t));}
    private String getActual(String input){
        StringBuilder inputsb=new StringBuilder();
        int hashCount=0;
        for(int i=input.length()-1;i>=0;i--){
            if(input.charAt(i)=='#'){
                hashCount++;
                continue;
            }
            else if(hashCount>0){
                hashCount--;
                continue;
            }
            inputsb.insert(0,input.charAt(i));
            
        }
        return inputsb.toString();
    }
}