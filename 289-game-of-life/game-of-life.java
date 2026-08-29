class Solution {
    public void gameOfLife(int[][] board) {

        int m = board.length;
        int n = board[0].length;

        int[][] copy = new int[m][n];

        // Copy current board
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {
                copy[i][j] = board[i][j];
            }
        }
        // Check every cell
        for (int i = 0; i < m; i++) {
            for (int j = 0; j < n; j++) {

                int liveNeighbors = 0;

                // Check 8 directions
                for (int x = i - 1; x <= i + 1; x++) {
                    for (int y = j - 1; y <= j + 1; y++) {

                        // Skip current cell
                        if (x == i && y == j) {
                            continue;
                        }

                        // Check boundaries
                        if (x >= 0 && x < m && y >= 0 && y < n) {
                            if (copy[x][y] == 1) {
                                liveNeighbors++;
                            }
                        }
                    }
                }

                // Apply rules
                if (copy[i][j] == 1) {

                    // Live cell dies
                    if (liveNeighbors < 2 || liveNeighbors > 3) {
                        board[i][j] = 0;
                    }

                    // Live cell stays alive for 2 or 3 neighbors
                    else {
                        board[i][j] = 1;
                    }

                } else {

                    // Dead cell becomes alive with exactly 3 neighbors
                    if (liveNeighbors == 3) {
                        board[i][j] = 1;
                    }
                }
            }
        }
    }
}