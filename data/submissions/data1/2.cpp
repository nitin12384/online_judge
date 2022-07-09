#include <iostream>
int main(){
    int m,n;
    std::cin>>m>>n;
    int max=0;
    for(int i=0; i<m; i++){
        int cur=0;
        for(int j=0; j<n; j++){
            int temp;
            std::cin>>temp;
            cur+=temp;
        }
        if(max<cur){
            max=cur;
        }
    }
    std::cout << max << std::endl;
}

