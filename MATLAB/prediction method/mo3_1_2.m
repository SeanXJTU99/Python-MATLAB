%运行前打开QD,A,B,C,S矩阵
%F=@(x)95.88-70.2*cos(x*0.2586)-61.58*sin(x*0.2586)+0.6364*cos(2*x*0.2586)-8.032*sin(2*x*0.2586)-7.638*cos(3*x*0.2586)+1.732*sin(3*x*0.2586);
%PD=QD(:,1);
%AD=QD(:,2);
%BD=QD(:,3);
%CD=QD(:,4);
%cap=201;
%Pa=abs(AD-PD)./cap;
%Pb=abs(BD-PD)./cap;
%Pc=abs(CD-PD)./cap;
%Ba=zeros(452,1);
%Bb=zeros(452,1);
%Bc=zeros(452,1);
%for i=1:452
%    if Pa(i,1)<0.25
%        Ba(i,1)=1;
%    end
%    if Pb(i,1)<0.25
%        Bb(i,1)=1;
%    end
%    if Pc(i,1)<0.25
%        Bc(i,1)=1;
%    end
%end
%QRa=sum(Ba)/452;
%QRb=sum(Bb)/452;
%QRc=sum(Bc)/452;
%QR=[QRa QRb QRc];     %合格率
%CRa=1-sqrt(sum(Pa(:,1).^2)./452);
%CRb=1-sqrt(sum(Pb(:,1).^2)./452);
%CRc=1-sqrt(sum(Pc(:,1).^2)./452);
%CR=[CRa CRb CRc];     %均方根
%qr1=max(QR);qr2=min(QR);
%cr1=max(CR);cr2=min(CR);
%QR=(QR-qr2)./(qr1-qr2);
%CR=(CR-cr2)./(cr1-cr2);%标准化
%SCORE=0.5.*QR+0.5.*CR;
a=(A(:,1)-S).^2;
b=(B(:,1)-S).^2;
c=(C(:,1)-S).^2;
a0=sum(a);
b0=sum(b);
c0=sum(c);
R=[a0 b0 c0];
R=sqrt(R./46271);