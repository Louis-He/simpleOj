#include<stdio.h>
 
int main()
{
    int n;
    printf("Enter dimension");
    scanf("%d", &n);
    int i,j;
    for(i=0;1;i++)
    {
        for(j=0;j<n;j++)
            if((i+j)%2==0)
                printf("+");
            else printf(" ");
        printf("\n");
    }
    return 0;
}
