#include <iostream>
#include <stdio.h>
#include <windows.h>

#define inFile "GUI1Data.txt"
#define outFile "Player1Data.txt"

using namespace std;

int getData(int player2Plan[5][2],int &player2ChessID,int &flag,int &pointNum)
{
    static int unMoveCount=-1;
    static int used[22]={0};
    int error=-1;
    char line[1024];
    while (error==-1){
        Sleep(1000);
        FILE *f=fopen(inFile,"r");
        fgets(line,1024,f);
        int i,j;
        for (i=0;i<5;i++) for (j=0;j<2;j++) player2Plan[i][j]=-1;
        sscanf(line,"%d%d%d%d%d%d%d%d%d%d%",&player2Plan[0][0],&player2Plan[0][1],&player2Plan[1][0],&player2Plan[1][1],&player2Plan[2][0],&player2Plan[2][1],&player2Plan[3][0],&player2Plan[3][1],&player2Plan[4][0],&player2Plan[4][1]);
        for (i=0;i<5;i++)
            if (player2Plan[i][0]==-1){
                i--;
                break;
            }
        pointNum=(i==5)?i:i+1;
        fscanf(f,"%d",&player2ChessID);
        error=fscanf(f,"%d",&flag);
        fclose(f);
        if (error==-1)continue;
        if (flag==1){
            if (used[player2ChessID])
                error=-1;
            else{
                used[player2ChessID]=1;
                error=0;
            }
        }
        if (flag==0)
            if (player2ChessID>unMoveCount){
                unMoveCount=player2ChessID;
                error=0;
            }
            else error=-1;
    }
    return pointNum;
}
int plan2dat(int plan[5][2],int ChessID,int flag)
{
    FILE *f=fopen(outFile,"w");
    if (flag==0){
        ; //flag=0 is for readin.
    }
    if (flag==1){
        int i;
        for (i=0;i<5;i++)
            if (plan[i][0]!=-1)
                fprintf(f,"%d %d ",plan[i][0],plan[i][1]);
        fprintf(f,"\n%d\n%d",ChessID,flag);
    }
    if (flag==2){
        fprintf(f,"-1 -1\n0\n2");
    }
    fclose(f);
}

int main()
{
    /****************** for test input and output function************************
    int player2Plan[5][2];
    int player2ChessID;
    int flag;
    int pointNum;

    cout<<"Program Begin = = Z.Q. = ="<<endl;
    getData(player2Plan,player2ChessID,flag,pointNum);
    plan2dat(player2Plan,player2ChessID,flag);
    cout<<player2ChessID<<' '<<flag<<' '<<pointNum<<endl;
    getData(player2Plan,player2ChessID,flag,pointNum);
    plan2dat(player2Plan,player2ChessID,flag);
    cout<<player2ChessID<<' '<<flag<<' '<<pointNum<<endl;
    getData(player2Plan,player2ChessID,flag,pointNum);
    plan2dat(player2Plan,player2ChessID,flag);
    cout<<player2ChessID<<' '<<flag<<' '<<pointNum<<endl;
    ********************************************************************************/

    return 0;
}
