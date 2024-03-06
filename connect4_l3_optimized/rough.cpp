#include <bits/stdc++.h>
using namespace std;

int count(string &s, string p){ // pattern here is of size 4
    int c = 0;
    for (int i = 0; i < s.length()-3; i++){
        cout << s[i] << " " << s[i+1] << " " << s[i+2] << " " << s[i+3] << "\n";
        if (s[i] == p[0] && s[i+1] == p[1] && s[i+2] == p[2] && s[i+3] == p[3]){
            c++;
        }
    }
    return c;
}

int main(){
    string s = "0000001";
    count(s, "1000");
    // cout << count(s, "0001") << "\n";
}