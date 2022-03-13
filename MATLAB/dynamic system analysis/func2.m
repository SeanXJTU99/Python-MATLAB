function dy = func2(~,y)
%UNTITLED2 此处显示有关此函数的摘要
%   此处显示详细说明
b=0.5;
dy = [y(2);-b*y(2)+sin(y(1))];
end

