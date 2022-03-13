% Plots the separation of two neighboring trajectories starting at y0 and z0
% as a function of time. Then plots the theoretical line with lyapunov exponent
% lambda = 0.9


y0 = [10 10 10]
z0 = [10 10.000001 10]

tspan = 0:0.004:20


[t y]=ode45(@lorenz,tspan,y0);
[t z]=ode45(@lorenz,tspan,z0);

figure(1)
plot3(y(:,1),y(:,2),y(:,3)),'b';
hold on
plot3(z(:,1),z(:,2),z(:,3),'r');

figure(2)
plot(t,y(:,1))
hold on
plot(t,z(:,1))



d = ((y(:,1)-z(:,1)).^2 + (y(:,2)-z(:,2)).^2 + (y(:,3)-z(:,3)).^2 ).^0.5;

figure(3)
semilogy(t,d);
xlabel('t','FontSize',20)
     ylabel('log\delta','FontSize',20)
     title('Separation of neighboring trajectories','FontSize',20)
     hold on

     test = d(1).*exp(0.9.*t);
     plot(t,test,'r');
     axis([0 40 0 100])

