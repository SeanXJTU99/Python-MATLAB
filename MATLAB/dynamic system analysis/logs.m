function dy = logs(~,y)
%UNTITLED3 此处显示有关此函数的摘要
%   此处显示详细说明
a = 0.1;
dy = [y(1)*(--y(1)*y(1)+y(1)-y(2));y(2)*(y(1)-a)];
end
