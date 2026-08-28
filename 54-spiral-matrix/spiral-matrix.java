class Solution {
    public List<Integer> spiralOrder(int[][] matrix) {
        List<Integer> mat=new ArrayList<>();
        int rowBegin=0;
        int colBegin=0;
        int rowEnd=matrix.length-1;
        int colEnd=matrix[0].length-1;
        while(rowBegin<= rowEnd && colBegin <= colEnd){
            for(int j=colBegin;j<=colEnd;j++){
                mat.add(matrix[rowBegin][j]);
            }
            rowBegin++;
            for(int j=rowBegin;j<=rowEnd;j++){
                mat.add(matrix[j][colEnd]);
            }
            colEnd--;
            if(rowBegin<=rowEnd){
                for(int j=colEnd;j>=colBegin;j--){
                    mat.add(matrix[rowEnd][j]);
                }
                
            }
            rowEnd--;
            
            if(colBegin<=colEnd){
                for(int j=rowEnd;j>=rowBegin;j--){
                    mat.add(matrix[j][colBegin]);
                }
                colBegin++;
            }
            

        }
        return mat;
    }
}