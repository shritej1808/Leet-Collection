class Solution {
    public void gameOfLife(int[][] board) {
        int m=board.length;
        int n=board[0].length;

         int[] dr = {-1, -1, -1, 0, 0, 1, 1, 1};
        int[] dc = {-1, 0, 1, -1, 1, -1, 0, 1};
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                int liveNeighbours=0;
                for(int k=0;k<8;k++){
                    int nr=i+dr[k];
                    int nc=j+dc[k];

                    if(nr>=0 && nr<m && nc>=0 && nc<n){
                        if(board[nr][nc]==1 || board[nr][nc]==2){
                            liveNeighbours++;
                    
                }
                        
                    }
                }
                if(board[i][j]==1){
if(liveNeighbours<2 || liveNeighbours>3){
                    board[i][j]=2;
                }
                }
                
                if(board[i][j]==0){
                    if(liveNeighbours==3){
                    board[i][j]=3;
                }
                }
                
            }
        }
        for(int i=0;i<m;i++){
            for(int j=0;j<n;j++){
                if(board[i][j]==2){
                    board[i][j]=0;
                }
                if(board[i][j]==3){
                    board[i][j]=1;
                }
            }
        }

    }
}