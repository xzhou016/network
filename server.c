#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
 
int main(void)
{
  int listenfd = 0,connfd = 0,n = 0;
  
  struct sockaddr_in serv_addr, client;
 
  char recvBuff[1024];  
  int numrv;  
  //socket creation:
  listenfd = socket(AF_INET, SOCK_STREAM, 0);
  printf("socket retrieve success\n");
  
  memset(&serv_addr, '0', sizeof(serv_addr));
  memset(recvBuff, '0', sizeof(recvBuff));
      
  serv_addr.sin_family = AF_INET;    
  serv_addr.sin_addr.s_addr = htonl(INADDR_ANY); 
  serv_addr.sin_port = htons(5000);    
 
  bind(listenfd, (struct sockaddr*)&serv_addr,sizeof(serv_addr));
  
  if(listen(listenfd, 10) == -1){
      printf("Failed to listen\n");
      return -1;
  }
     
  
  while(1){
      
    connfd = accept(listenfd, (struct sockaddr *)NULL, NULL); 
  
    while((n = read(connfd, recvBuff, sizeof(recvBuff)-1)) > 0){
    	recvBuff[n] = 0;
    	if(fputs(recvBuff, stdout) == EOF){
      		printf("\n Error : Fputs error");
    	}
    	printf("\n");
    }
 
    if( n < 0){
	printf("\n Read Error \n");
    }
    //strcpy(sendBuff, "Message from server33");
   close(connfd);
   sleep(1);

 //write(connfd, sendBuff, strlen(sendBuff)); 
   }
 
 
  return 0;
}
