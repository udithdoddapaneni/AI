#include <bits/stdc++.h>
using namespace std;

int LIMIT = 4;
int min_move(vector<vector<int>> &state, int limit, int parent_val, int sign, int player_number, int depth, int p);
int max_move(vector<vector<int>> &state, int limit, int parent_val, int sign, int player_number, int depth, int p);
vector<vector<int>> column(vector<vector<int>> &board){
    vector<vector<int>> columns;
    for (int i = 0; i < 7; i++){
        vector<int> col;
        for (int j = 0; j < 6; j++){
            col.push_back(board[j][i]);
        }
        columns.push_back(col);
    }
    return columns;
}

vector<vector<int>> diagonallr(vector<vector<int>> &board){
    vector<vector<int>> diagonals;
    int i, j;
    vector<pair<int, int>> points = { {0, 0}, {1, 0}, {2, 0}, {1, 0}, {0, 1}, {0, 2}, {0, 3} };
    for (int k = 0; k < 7; k++){
        i = points[k].first; j = points[k].second;
        vector<int> diag;
        for (i, j; i < 6 && j < 7; i++, j++){
            diag.push_back(board[i][j]);
        }
        diagonals.push_back(diag);
    }
    return diagonals;
}

vector<vector<int>> diagonalrl(vector<vector<int>> &board){
    vector<vector<int>> diagonals;
    int i, j;
    vector<pair<int, int>> points = { {5, 0}, {5, 1}, {5, 2}, {5, 3}, {4, 0}, {3, 0} };
    for (int k = 0; k < 6; k++){
        i = points[k].first; j = points[k].second;
        vector<int> diag;
        for (i, j; i > 0 && j < 7; i--, j++){
            diag.push_back(board[i][j]);
        }
        diagonals.push_back(diag);
    }
    return diagonals;
}

int count(string &s, string p){ // pattern here is of size 4
    int c = 0;
    for (int i = 0; i < s.length()-3; i++){
        if (s[i] == p[0] && s[i+1] == p[1] && s[i+2] == p[2] && s[i+3] == p[3]){
            c++;
        }
    }
    return c;
}

pair<int, int> evl(string &s, int player_number){
    int ai_value = 0;
    int enemy_value = 0;
    int o, x, y, z;
    int c, p, q, r;
    if (player_number == 1){
        o = count(s, "1111");
        x = (count(s, "1110") + count(s, "0111") + count(s, "1011") + count(s, "1101"));
        y = (count(s, "1100") + count(s, "0110") + count(s, "0011") + count(s, "1001") + count(s, "1010") + count(s, "0101"));
        z = (count(s, "1000") + count(s, "0100") + count(s, "0010") + count(s, "0001"));
        if (o > 0) return {10000000, 0};
        ai_value += x*43*43 + y*43 + z;
        c = count(s, "2222");
        p = (count(s, "2220") + count(s, "0222") + count(s, "2022") + count(s, "2202"));
        q = (count(s, "2200") + count(s, "0220") + count(s, "0022") + count(s, "2002") + count(s, "2020") + count(s, "0202"));
        r = (count(s, "2000") + count(s, "0200") + count(s, "0020") + count(s, "0002"));

        if (c > 0) return {0, 10000000};
        enemy_value += p*43*43;
        enemy_value += q*43;
        enemy_value += r;
    }
    else{
        o = count(s, "1111");
        x = (count(s, "1110") + count(s, "0111") + count(s, "1011") + count(s, "1101"));
        y = (count(s, "1100") + count(s, "0110") + count(s, "0011") + count(s, "1001") + count(s, "1010") + count(s, "0101"));
        z = (count(s, "1000") + count(s, "0100") + count(s, "0010") + count(s, "0001"));

        if (o > 0) return {0, 10000000};
        enemy_value += x*43*43;
        enemy_value += y*43;
        enemy_value += z;

        c = count(s, "2222");
        p = (count(s, "2220") + count(s, "0222") + count(s, "2022") + count(s, "2202"));
        q = (count(s, "2200") + count(s, "0220") + count(s, "0022") + count(s, "2002") + count(s, "2020") + count(s, "0202"));
        r = (count(s, "2000") + count(s, "0200") + count(s, "0020") + count(s, "0002"));

        if (c > 0) return {10000000, 0};
        ai_value += p*43*43;
        ai_value += q*43;
        ai_value += r;
    }
    return {ai_value, enemy_value};
}

vector<vector<vector<int>>> generate_moves(vector<vector<int>> &board, int player_number){
    vector<vector<vector<int>>> moves;
    vector<vector<int>> new_board;
    for (int i = 0; i < 7; i++){
        for (int j = 5; j > -1; j--){
            if (!board[j][i]){
                new_board = board;
                new_board[j][i] = player_number;
                moves.push_back(new_board);
                break;
            }
        }
    }
    return moves;
}

int change_player(int player_number){
    if (player_number == 1) return 2;
    return 1;
}

string change_to_string(vector<int> &arr){
    char ch[arr.size()];
    for (int i = 0; i < arr.size(); i++){
        if (arr[i] == 1){
            ch[i] = '1';
        }
        else if (arr[i] == 2){
            ch[i] = '2';
        }
        else{
            ch[i] = '0';
        }
    }
    string s(ch);
    return s;
}

int evaluation_function(vector<vector<int>> &board, int player_number){
    int ai_value = 0, enemy_value = 0;
    string s; pair<int, int> values;
    int a, e;
    for (vector<vector<int>> :: iterator i = board.begin(); i < board.end(); i++){
        s = change_to_string(*i);
        values = evl(s, player_number);
        a = values.first, e = values.second;
        if (a == 10000000) return 10000000;
        if (e == 10000000) return -10000000;
        ai_value += a; enemy_value += e;
    }
    vector<vector<int>> columns = column(board);
    vector<vector<int>> diagonal_lr = diagonallr(board);
    vector<vector<int>> diagonal_rl = diagonalrl(board);
    for (vector<vector<int>> :: iterator i = columns.begin(); i < columns.end(); i++){
        s = change_to_string(*i);
        values = evl(s, player_number);
        a = values.first, e = values.second;
        if (a == 10000000) return 10000000;
        if (e == 10000000) return -10000000;
        ai_value += a; enemy_value += e;
    }
    for (vector<vector<int>> :: iterator i = diagonal_lr.begin(); i < diagonal_lr.end(); i++){
        s = change_to_string(*i);
        values = evl(s, player_number);
        a = values.first, e = values.second;
        if (a == 10000000) return 10000000;
        if (e == 10000000) return -10000000;
        ai_value += a; enemy_value += e;
    }
    for (vector<vector<int>> :: iterator i = diagonal_rl.begin(); i < diagonal_rl.end(); i++){
        s = change_to_string(*i);
        values = evl(s, player_number);
        a = values.first, e = values.second;
        if (a == 10000000) return 10000000;
        if (e == 10000000) return -10000000;
        ai_value += a; enemy_value += e;
    }
    if (enemy_value == 10000000) return -10000000;
    if (ai_value == 10000000) return 10000000;
    return ai_value-enemy_value;
}

int min_move(vector<vector<int>> &state, int limit, int parent_val, int sign, int player_number, int depth, int p){

    if (sign*evaluation_function(state, p) == -10000000) return -10000000+(43*43)*depth;
    if (sign*evaluation_function(state, p) == 10000000) return 10000000-(43*43)*depth;
    vector<vector<vector<int>>> moves = generate_moves(state, player_number);
    int M = 10000000;
    int m;
    if (limit == LIMIT){
        for (vector<vector<vector<int>>> :: iterator i = moves.begin(); i < moves.end(); i++){
            m = sign*evaluation_function(*i, p);
            M = min(m, M);
        }
        if (M == -10000000) return M+(43*43)*(depth+1);
        if (M == 10000000) return M-(43*43)*(depth+1);

        return M;
    }

    for (vector<vector<vector<int>>> :: iterator i = moves.begin(); i < moves.end(); i++){
        m = max_move(*i, limit+1, M, -sign, change_player(player_number), depth+1, p);
        if (m < M) M = m;
        if (M < parent_val) break;
    }
    return M; 
}

void print_state(vector<vector<int>> &state){
    for (int i = 0; i < 6; i++){
        for (int j = 0; j < 7; j++){
            cout << state[i][j] << " ";
        }
        cout << "\n";
    }
}

int max_move(vector<vector<int>> &state, int limit, int parent_val, int sign, int player_number, int depth, int p){
    if (sign*evaluation_function(state, p) == -10000000) return -10000000+(43*43)*depth;
    if (sign*evaluation_function(state, p) == 10000000) return 10000000-(43*43)*depth;
    vector<vector<vector<int>>> moves = generate_moves(state, player_number);
    int M = -10000000;
    int m;
    if (limit == LIMIT){
        for (vector<vector<vector<int>>> :: iterator i = moves.begin(); i < moves.end(); i++){
            m = sign*evaluation_function(*i, p);
            M = max(m, M);
        }
        if (M == -10000000) return M+(43*43)*(depth+1);
        if (M == 10000000) return M-(43*43)*(depth+1);

        return M;
    }

    for (vector<vector<vector<int>>> :: iterator i = moves.begin(); i < moves.end(); i++){
        m = min_move(*i, limit+1, M, -sign, change_player(player_number), depth+1, p);
        if (m > M) M = m;
        if (M > parent_val) break;
    }
    return M; 
}

int alpha_beta_move(vector<vector<int>> &board, int player_number){
    int M, parent_val, m;
    vector<vector<int>> next_state;
    M = -100000000;
    parent_val = 0;
    vector<vector<vector<int>>> states = generate_moves(board, player_number);
    for (vector<vector<vector<int>>> :: iterator state = states.begin(); state < states.end(); state++){

        if (evaluation_function(*state, player_number) == 10000000){
            next_state = *state;
            M = 10000000;
            break;
        }
        m = min_move(*state, 1, M, -1, change_player(player_number), 1, player_number);
        if (m > M){
            M = m;
            next_state = *state;
        }
    }
    for (int i = 0; i < 6; i++){
        for (int j = 0; j < 7; j++){
            if (next_state[i][j] != board[i][j]) return j;
        }
    }
    return -1;
}

int main(){

    // communication with python file
    // make board

    vector<vector<int>> board(6);
    int player_number;
    cin >> player_number;
    for (int i = 0; i < 6; i++){
        vector<int> row(7);
        for (int j = 0; j < 7; j++){
            cin >> row[j];
        }
        board[i] = row;
    }


    cout << alpha_beta_move(board, player_number) << "\n";
}