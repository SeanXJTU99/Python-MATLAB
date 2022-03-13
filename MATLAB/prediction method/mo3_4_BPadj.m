%AT=zeros(35,5);
%BT=zeros(35,5);
%CT=zeros(35,5);
%A1(:,2)=cos(A1(:,2));
%B1(:,2)=cos(B1(:,2));
%C1(:,2)=cos(C1(:,2));
%for i=1:35
%   AT(i,:)=sum(A1((96*i-95):96*i,:))/96;
%   BT(i,:)=sum(B1((96*i-95):96*i,:))/96;
%   CT(i,:)=sum(C1((96*i-95):96*i,:))/96;
%end
%PT=[AT BT CT];
%70 74 81 105 152

%运行前打开QD2，DT2，SPT矩阵
Sa=SPT(1,:);
Sb=SPT(2,:);
Sc=SPT(3,:);
DT2(401:447,1)=Sa';
DT2(401:447,6)=Sb';
DT2(401:447,11)=Sc';
DTA=DT2(1:400,1:5)';
DTB=DT2(1:400,6:10)';
DTC=DT2(1:400,11:15)';
PTA=DT2(401:447,1:5)';
PTB=DT2(401:447,6:10)';
PTC=DT2(401:447,11:15)';
Y0=QD2(1:400,1)';
[Y,outr]=mapminmax(Y0);
[X1,intr]=mapminmax(DTB);
X2=mapminmax('apply',PTB,intr);
net=newff(X1,Y,[5 12 1],{'purelin','logsig','purelin'},'traingda');
net.trainParam.show=10;
net.trainParam.lr=0.05;
net.trainParam.epochs=50000;
net.trainParam.goal=0.06;
net.divideFcn='';
sam=400;
[BPnet,tr]=train(net,X1,Y);
y=sim(BPnet,X2);
b1=mapminmax('reverse',y,outr);
rb1=sqrt(sum(((b1'-QD2(401:447,1))/201).^2)/47);