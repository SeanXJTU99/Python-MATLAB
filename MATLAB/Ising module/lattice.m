classdef lattice < handle
    % Class to store a 2-D lattice of "spins" and methods to perform
    % lattice update "sweeps", plot the lattice, and accumulate statistics.
    % 
    properties
        T    % Lattice temperature
        data % The 2-D lattice data (stores +1 or -1 in each location)
        ran  % The random number generator to use
        m    % The size of the lattice (m rows and m columns)
        s    % statistics
    end
    methods
        function obj = lattice(T,m,seed)
            % Constructor
            obj.T = T;
            obj.m = m;
            obj.data = zeros(m,m);
            obj.ran = NumericalRecipes.Ran(seed);
            obj.s=zeros(1,4);
        end
        %
        function M = Magnetization(obj)
            % Compute and return the magnetization/spin of the current
            % lattice 
            M=obj.s(1)/(100*obj.m^2);
         end
        %
        function E = Energy(obj)
            % Compute and return the energy/spin of the current
            % lattice 
            E=obj.s(3)/(100*obj.m^2);
        end
        %
        function e = energy(obj)
            % Compute and return the total energy of the current lattice
            e=0;
            for i=1:obj.m
                for j=1:obj.m
                    if i==obj.m
                        if j==obj.m
                            e=e+obj.data(i,j)*(obj.data(1,j)+obj.data(i,1));
                        else
                            e=e+obj.data(i,j)*(obj.data(1,j)+obj.data(i,j+1));
                        end
                    elseif j==obj.m
                        if i==obj.m
                            e=e+obj.data(i,j)*(obj.data(1,j)+obj.data(i,1));
                        else
                            e=e+obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,1));
                        end
                    else
                        e=e+obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,j+1));
                    end
                end
            end
            e=-e;
        end
        %
        function sweep(obj)
            % Apply the Metropolis algorithm to m*m randomly chosen spins.
            for i=1:obj.m^2
                point=round(rand(1,2)*(obj.m-1))+1;  % choose one dipole
                a=point(1,1);   b=point(1,2);
                obj.data(a,b)=-obj.data(a,b);
                dE=obj.DeltaEnergy(a,b);
                edE=exp(-dE/obj.T);
                if edE<rand(1)
                    obj.data(a,b)=-obj.data(a,b);
                end
            end
        end
        %
        function de = DeltaEnergy(obj,i,j)
            % Compute the change in the energy if the spin at lattice site
            % (i,j) flips
if i==obj.m 
    if j==obj.m
        de=2*(-1)*obj.data(i,j)*(obj.data(1,j)+obj.data(i,1)+obj.data(i-1,j)+obj.data(i,j-1));
    elseif j==1
        de=2*(-1)*obj.data(i,j)*(obj.data(1,j)+obj.data(i,j+1)+obj.data(i-1,j)+obj.data(i,obj.m));
    else
        de=2*(-1)*obj.data(i,j)*(obj.data(1,j)+obj.data(i,j+1)+obj.data(i-1,j)+obj.data(i,j-1));
    end
elseif i==1
    if j==obj.m
        de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,1)+obj.data(obj.m,j)+obj.data(i,j-1));
    elseif j==1
        de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,j+1)+obj.data(obj.m,j)+obj.data(i,obj.m));
    else
        de=2*(-1)*obj.data(i,j)*(obj.data(1+1,j)+obj.data(i,j+1)+obj.data(obj.m,j)+obj.data(i,j-1));
    end
elseif j==obj.m
    if i==obj.m
        de=2*(-1)*obj.data(i,j)*(obj.data(1,j)+obj.data(i,1)+obj.data(i-1,j)+obj.data(i,j-1));
    elseif i==1
        de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,1)+obj.data(obj.m,j)+obj.data(i,j-1));
    else
        de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,1)+obj.data(i-1,j)+obj.data(i,j-1));
    end
elseif j==1
    if i==obj.m
        de=2*(-1)*obj.data(i,j)*(obj.data(1,j)+obj.data(i,j+1)+obj.data(i-1,j)+obj.data(i,obj.m));
    elseif i==1
        de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,j+1)+obj.data(obj.m,j)+obj.data(i,obj.m));
    else
        de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,j+1)+obj.data(i-1,j)+obj.data(i,obj.m));
    end
else
    de=2*(-1)*obj.data(i,j)*(obj.data(i+1,j)+obj.data(i,j+1)+obj.data(i-1,j)+obj.data(i,j-1));
end
        end
        %
        function stat(obj)
            % Collect statistics for the current state of the lattice
            M=obj.s(1);
            MM=obj.s(2);
            E=obj.s(3);
            EE=obj.s(4);
            M=M+sum(sum(obj.data));
            MM=MM+M^2;
            E=E+obj.energy();
            EE=EE+E^2;
            obj.s(1)=M;
            obj.s(2)=MM;
            obj.s(3)=E;
            obj.s(4)=EE;
        end
        %
        function resetstats(obj)
            % Reset the accumulated statistics to zero.
            obj.s=zeros(1,4);
        end         
        %
        function [M,MM,E,EE] = CollectData(obj)
            % return the expectation values <M>, <M^2>, <E>, and <E^2>
            M=obj.Magnetization();
            MM=obj.s(2)/((100*obj.m^2)^2);
            E=obj.Energy();
            EE=obj.s(4)/((100*obj.m^2)^2);
        end
        %
        function image(obj)
            % Produce a visualization of the lattice
            img = uint8(floor(0.5*(obj.data+1.0)));
            colormap([0 0 1;1 0 0]);
            image(img);
            pause(0.05);
        end
    end
end