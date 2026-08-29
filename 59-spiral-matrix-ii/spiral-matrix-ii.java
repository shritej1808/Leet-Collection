class Solution {
    public int[][] generateMatrix(int n) {
        int matrix[][]=new int[n][n];
        int rowBegin=0;
        int rowEnd=n-1;
        int colBegin=0;
        int colEnd=n-1;
        int x=1;
        while(rowBegin<=rowEnd && colBegin<=colEnd){
            for(int j=colBegin;j<=colEnd;j++){
                matrix[rowBegin][j]=x;
                x++;
            }
            rowBegin++;
            for(int j=rowBegin;j<=rowEnd;j++){
                matrix[j][colEnd]=x;
                x++;
            }
            colEnd--;
            for(int j=colEnd;j>=colBegin;j--){
                matrix[rowEnd][j]=x;
                x++;
            }
            rowEnd--;
            for(int j=rowEnd;j>=rowBegin;j--){
                matrix[j][colBegin]=x;
                x++;
            }
            colBegin++;



        }
        return matrix;
    }
}