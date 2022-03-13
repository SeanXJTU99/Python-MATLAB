function [mu,sigma,xbin] = stat(particle,x,time)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
nt=length(time);
x_pos=reshape(particle(:,:,1),[nt*(nt+1),1]);
y_pos=reshape(particle(:,:,2),[nt*(nt+1),1]);
num_bins=100; 
mu=zeros(1,100);
sigma=zeros(1,100);
bin_width=x(end-1)/num_bins; 
xbin=[bin_width/2:bin_width:x(end-1)]; 
for i=1:num_bins
    xl=xbin(i)-bin_width/2; 
    xr=xbin(i)+bin_width/2; 
    bin_ind=find(x_pos>xl & x_pos<xr); 
    x_c=x_pos(bin_ind); 
    y_c=y_pos(bin_ind);
    mu(i)=mean(y_c);
    sigma(i)=std(y_c);
end
end

