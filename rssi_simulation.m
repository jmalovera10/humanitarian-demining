%Anchor 1 coordinates 
anchor1 = [0,0];
%Anchor 2 coordinates 
anchor2 = [0,10];
%Anchor 3 coordinates 
anchor3 = [10,0];
%Anchor 4 coordinates 
anchor4 = [10,10];

%Mobile coordinates
mobile1 = [3,6];

anchors = [anchor1;anchor2;anchor3;anchor4;mobile1];
plot(anchors(:,1),anchors(:,2),'*')
xlabel('m')
ylabel('m')
xlim([-1 11])
ylim([-1 11])
dog = '  Dog';
text(mobile1(1),mobile1(2),dog)
grid on
hold on

for i = 1:4
    radius = norm(anchors(i,:)-mobile1);
    [xval, yval] = radiation(radius);
    xval = xval+anchors(i,1);
    yval = yval+anchors(i,2);
    plot(xval,yval,'--')
    txt = strcat('  Anchor',num2str(i));
    text(anchors(i,1),anchors(i,2),txt)
end




