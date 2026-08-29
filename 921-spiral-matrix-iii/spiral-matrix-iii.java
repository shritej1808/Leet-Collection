class Solution {
    public int[][] spiralMatrixIII(int rows, int cols, int rStart, int cStart) {
        int[][] result=new int[rows*cols][2];
        int index=0;
        int[] dr={0,1,0,-1};
        int[] dc={1,0,-1,0};
        int r = rStart;
        int c = cStart;
        int direction=0;
        int steps=1;

        result[index][0] = r;
        result[index][1] = c;
        index++;
        while(index< rows*cols){
            for(int count=0;count<2;count++){
                for(int i=0;i<steps;i++){
                    r+=dr[direction];
                    c+=dc[direction];

                    if(r>=0 && r<rows && c>=0 && c<cols){
                        result[index][0]=r;
                        result[index][1]=c;
                        index++;
                    }
                    if(index==rows*cols){
                        return result;
                    }

                }
                direction=(direction+1)%4;
            }
             steps++; 
            }
           
            return result;
        }
     
}