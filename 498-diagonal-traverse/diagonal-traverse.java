class Solution {
    public int[] findDiagonalOrder(int[][] mat) {
        if(mat==null || mat.length==0) return new int[0];
        int row=0;
        int col=0;
        int m=mat.length;
        int n=mat[0].length;
        int[] result=new int[m*n];
        for(int i=0;i<m*n;i++){
            result[i]=mat[row][col];
            if((row+col)%2==0){//even means top right
                if(col==n-1) row++;
                else if(row==0)col++;
                else{row--;col++;}
            }
            else{ //bottom left
                if(row==m-1) col++;
                else if(col==0) row++;
                else{row++;col--;}
            }
        }
        return result;
    }
}