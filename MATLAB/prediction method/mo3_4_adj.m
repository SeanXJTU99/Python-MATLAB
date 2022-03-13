%for i=1:452
%    if DT(i,10)<100
%        DT(i,10)=DT(i,10)*100;
%    end
%end
%DT(:,2)=cos(DT(:,2));
%DT(:,7)=cos(DT(:,7));
%DT(:,12)=cos(DT(:,12));
%SD=zeros(481,1);
%ASD=zeros(481,1);
%BSD=zeros(481,1);
%CSD=zeros(481,1);
%for i=1:481
%    SD(i,1)=sum(S(96*i-95:96*i,1))/96;
%    ASD(i,1)=sum(A(96*i-95:96*i,1))/96;
%    BSD(i,1)=sum(B(96*i-95:96*i,1))/96;
%    CSD(i,1)=sum(C(96*i-95:96*i,1))/96;
%end
%SDT=[SD ASD BSD CSD];

%运行前打开SDT矩阵
Y0=SDT(1:400,1)';
SDTA0=SDT(1:400,2)';
SDTB0=SDT(1:400,3)';
SDTC0=SDT(1:400,4)';
SDTA1=SDT(401:447,2)';
SDTB1=SDT(401:447,3)';
SDTC1=SDT(401:447,4)';
[Y,outr]=mapminmax(Y0);
[X1,intr]=mapminmax(SDTB0);
X2=mapminmax('apply',SDTB1,intr);
net=newff(X1,Y,[5 12 1],{'purelin','logsig','purelin'},'traingda');
net.trainParam.show=10;
net.trainParam.lr=0.05;
net.trainParam.epochs=50000;
net.trainParam.goal=0.06;
net.divideFcn='';
sam=400;
[BPnet,tr]=train(net,X1,Y);
y=sim(BPnet,X2);
Sb=mapminmax('reverse',y,outr);