function [ est ] = NLS( anchors, dist  )
%NLS Summary of this function goes here
%   Detailed explanation goes here
b = [5 5];
err = 0.01;
while true
    f1 = sqrt((b(1)-anchors(1,1)).^2+(b(2)-anchors(1,2)).^2);
    f2 = sqrt((b(1)-anchors(2,1)).^2+(b(2)-anchors(2,2)).^2);
    f3 = sqrt((b(1)-anchors(3,1)).^2+(b(2)-anchors(3,2)).^2);

    f=[f1;f2;f3];
    f=f-dist;
    
    J = Jacobian(b(1),b(2),anchors);
    
    p = linsolve(J'*J,-(J')*f);
    est = b + p';
    comp = norm(b-est);
    if comp<= err
        break
    end
    b = est;
end

end

