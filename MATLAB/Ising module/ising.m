function ising(m,seed)
    % Set the Temperature values to compute
    Tstart = 1;
    Tend = 5;
    Tstep = 0.4;
    Temps = Tstart:Tstep:Tend;
    % Storage for various expectation values at each temperature
    M = zeros(length(Temps),1);
    MM = zeros(length(Temps),1);
    E = zeros(length(Temps),1);
    EE = zeros(length(Temps),1);
    Cv = zeros(length(Temps),1);
    Ms = zeros(length(Temps),1);
    % Loop over all temperatures
    Ns=10;
    
    for k=1:length(Temps)
        % Create the Class for the Lattice
        lat = lattice(Temps(k),m,seed);
        % Call the routine to carry out the relaxation and 
        % measurement sweeps
        lat.data=round(rand(m,m))*2-1; % produce a random +1-1 matrix
        Tising(lat,Temps(k),m,Ns);
        % Gather the data and save into the arrays.
        [M(k),MM(k),E(k),EE(k)] = lat.CollectData();
      	Ms(k) = (MM(k) -M(k)*M(k))/Temps(k);
        Cv(k) = (EE(k)-E(k)*E(k))/(Temps(k)*Temps(k));
        
        % Display the information
%         fprintf(' T= %f: |M|= %f, E = %f: Ms = %f, C_v = %f \n',Temps(k),abs(M(k)),E(k),Ms(k),Cv(k) );
%         lat.image();
%         title(sprintf('T = %f\n',Temps(k)));
%         pause(0.05);
    end
    % Plot the various physical quantities vs temperature
    % Energy
    figure(2);
    plot(Temps,E);
    xlabel('T');
    ylabel('\langle{E}\rangle');
    title('Energy per spin');
    % Magnetization
    figure(3);
    plot(Temps,abs(M));
    xlabel('T');
    ylabel('|\langle{M}\rangle{}|');
    title('Magnetization per spin');
    % Specific heat
    figure(4);
    plot(Temps,Cv);
    xlabel('T');
    ylabel('C_v');
    title('Specific Heat');
    % Magnetic Susceptibility
    figure(5);
    plot(Temps,Ms);
    xlabel('T');
    ylabel('\chi');
    title('Magnetic Susceptibility');
end

function Tising(lat,T,m,Ns)
%     figure(1);
%     hold on
%     lat.image;
%     title(sprintf('T = %f\n',T));
% %     Sweep to allow the system to come to equilibrium
%     fprintf('Thermalize----\n');
T
    for k=1:1000
        lat.sweep;
        if mod(k,Ns)==0
%             lat.image;
%             fprintf('%5i: |M|= %f, E = %f\n',k,abs(lat.Magnetization),lat.Energy);
        end
    end
%     figure(1);
%     lat.image();
% %     Sweep to collect the data
%     fprintf('Collect Data\n');
    for k=1:1000
        lat.sweep;
        if mod(k,Ns)==0
            lat.stat();
        end
        if mod(k,50)==0
%             figure(1);
%             lat.image;
%             fprintf('%5i: |M|= %f, E = %f\n',k,abs(lat.Magnetization),lat.Energy);
        end
    end
    hold off
end
