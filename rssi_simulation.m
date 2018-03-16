%Anchor 1 coordinates 
anchor1 = [0,0];
%Anchor 2 coordinates 
anchor2 = [0,12];
%Anchor 3 coordinates 
anchor3 = [12,0];
%Anchor 4 coordinates 
anchor4 = [12,12];

%Mobile coordinate
mobile1 = [7,5];

anchors = [anchor1;anchor2;anchor3;anchor4];
nodes = [anchors;mobile1];
clf('reset')
plot(nodes(:,1),nodes(:,2),'*')
xlabel('m')
ylabel('m')
xlim([-1 13])
ylim([-1 13])
dog = strcat('  Dog: ','[',num2str(mobile1(1)),',',num2str(mobile1(2)),']');
text(mobile1(1),mobile1(2),dog)
grid on
hold on
rssi = [];

for i = 1:4
    radius = norm(anchors(i,:)-mobile1);
    [xval, yval] = radiation(radius);
    xval = xval+anchors(i,1);
    yval = yval+anchors(i,2);
    plot(xval,yval,'--')
    txt = strcat('  Anchor',num2str(i),': ');
    text(anchors(i,1),anchors(i,2),txt)
    rssi(i) = rssi_value(radius);
end

distances = distance(rssi);