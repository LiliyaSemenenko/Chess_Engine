function [i] = corridor(x,y)

    hold on;

    % Define the dimensions of the hallway
    hallway_width = 70;
    hallway_height = 35;
    hallway_x = 0;
    hallway_y = 0;

    % Draw the hallway
    rectangle('Position',[hallway_x, hallway_y, hallway_width, hallway_height],'FaceColor',[1 1 1]);

    % Add a door to the top of the hallway
    door_width = 10;
    door_height = 3;
    door_x = hallway_x + (hallway_width - door_width) / 2;
    door_y = hallway_y + hallway_height - door_height;
    rectangle('Position',[door_x, door_y, door_width, door_height],'FaceColor',[0 0 0]);

    
    % Add trash cans to the hallway
    trashcan_size = 2;
    trashcan_x1 = hallway_x + 50;
    trashcan_y1 = hallway_y + hallway_height - 2 - trashcan_size;
    rectangle('Position',[trashcan_x1, trashcan_y1, trashcan_size, trashcan_size],'FaceColor',[0 0 1]);
    trashcan_x2 = trashcan_x1 + trashcan_size + 1;
    trashcan_y2 = trashcan_y1;
    rectangle('Position',[trashcan_x2, trashcan_y2, trashcan_size, trashcan_size],'FaceColor',[0.2 0.2 0.2]);
    trashcan_x3 = hallway_x + 20;
    trashcan_y3 = trashcan_y1;
    rectangle('Position',[trashcan_x3, trashcan_y3, trashcan_size, trashcan_size],'FaceColor',[0 0 1]);
    trashcan_x4 = trashcan_x3 + trashcan_size + 1;
    trashcan_y4 = trashcan_y3;
    rectangle('Position',[trashcan_x4, trashcan_y4, trashcan_size, trashcan_size],'FaceColor',[0.2 0.2 0.2]);

    % Add tents to the hallway
    tent_width = 10;
    tent_height = 10;

    tent_x1 = hallway_x + 5;
    tent_y1 = hallway_y + 2;
    rectangle('Position',[tent_x1, tent_y1, tent_width, tent_height],'FaceColor',[0.5 0.5 0.5]);
    
    tent_x2 = hallway_x + hallway_width - 5 - tent_width;
    tent_y2 = tent_y1;
    rectangle('Position',[tent_x2, tent_y2, tent_width, tent_height],'FaceColor',[0.5 0.5 0.5]);
    
    % Add extra tents
    tent_x3 = tent_x1 + tent_width + 2;
    tent_y3 = tent_y1;
    rectangle('Position',[tent_x3, tent_y3, tent_width, tent_height],'FaceColor',[0.5 0.5 0.5]);
    tent_x4 = tent_x2 - tent_width - 2;
    tent_y4 = tent_y2;
    rectangle('Position',[tent_x4, tent_y4, tent_width, tent_height],'FaceColor',[0.5 0.5 0.5]);

    % Set the axis limits
    axis([-10 80 -10 40])

    % Hide the axis ticks
    set(gca,'xtick',[])
    set(gca,'ytick',[])% Set the aspect ratio to equal

    axis equal

    % Set the background color
    set(gcf,'Color',[0.5 0.5 0.5])

    hold off;
    drawnow;

    i = 0;
end
