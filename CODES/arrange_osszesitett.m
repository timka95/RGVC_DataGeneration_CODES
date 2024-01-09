% Initialize cell arrays for each field

numberofcolums = 10384;


% data = load('/Users/timeanemet/Desktop/CNN/matfiles/new_osszesitett.mat');
data = load('/project/ntimea/l2d2/IMAGE_PAIR_GT/matlab/new_osszesitett.mat');

new_osszesitett = data.new_osszesitett;


image_id_1_cell = cell(numberofcolums, 1);
lines2d_cell = cell(numberofcolums, 1);
lines3d_cell = cell(numberofcolums, 1);
PoseMatrix_cell = cell(numberofcolums, 1);
CalibMatrix_cell = cell(numberofcolums, 1);
mistakes_cell = cell(numberofcolums, 1);







% Iterate through the cell array and extract data for each field
for i = 1:numberofcolums
    data_row = new_osszesitett{i, 1}; % Access each 1x1 struct


    image_id_1_cell{i} = data_row.ID;
    lines2d_cell{i} = data_row.lines_2D;
    lines3d_cell{i} = data_row.lines_3D;
    PoseMatrix_cell{i} = data_row.PoseMatrix;
    CalibMatrix_cell{i} = data_row.CalibMatrix;
    mistakes_cell{i} = data_row.Mistake;




end

% Preallocate the cell array to hold the transformed data
new_osszesitett_2 = cell(numberofcolums, 6); % Assuming numberofcolums rows and 5 columns

% Iterate through the cell arrays and reshape the [1x1x4 double] or [1x1x6 double]
for i = 1:numberofcolums
    new_osszesitett_2{i, 1} = image_id_1_cell{i};
    new_osszesitett_2{i, 2} = lines2d_cell{i};
    new_osszesitett_2{i, 3} = lines3d_cell{i};
    new_osszesitett_2{i, 4} = PoseMatrix_cell{i};
    new_osszesitett_2{i, 5} = CalibMatrix_cell{i};
    new_osszesitett_2{i, 6} = mistakes_cell{i};








end