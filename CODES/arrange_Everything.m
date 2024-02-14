% Initialize cell arrays for each field

% data = load('/Users/timeanemet/Desktop/CNN/matfiles/new_osszesitett.mat');
data = load('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data_cutted_pairs_Everything.mat');

loadeddata = data.data_cutted_pairs_Everything;




numberofcolums = 143805;

data1_imageid_cell = cell(numberofcolums, 1);
data2_imageid_cell = cell(numberofcolums, 1);
data1_ThetaRho_cell = cell(numberofcolums, 1);
data2_ThetaRho_cell = cell(numberofcolums, 1);
data1_2D_orig_cell = cell(numberofcolums, 1);
data2_2D_orig_cell = cell(numberofcolums, 1);
data1_2D_512_cell = cell(numberofcolums, 1);
data2_2D_512_cell = cell(numberofcolums, 1);
data1_2D_376_cell = cell(numberofcolums, 1);
data2_2D_376_cell = cell(numberofcolums, 1);
data1_cutedhere_cell = cell(numberofcolums, 1);
data2_cutedhere_cell = cell(numberofcolums, 1);
data_3D_cell = cell(numberofcolums, 1);








% Iterate through the cell array and extract data for each field
for i = 1:numberofcolums
    data_row = loadeddata{i, 1}; % Access each 1x1 struct

    data1_imageid_cell{i} = data_row.data1_imageid;
    data2_imageid_cell{i} = data_row.data2_imageid;

    data1_ThetaRho_cell{i} = data_row.data1_ThetaRho;
    data2_ThetaRho_cell{i} = data_row.data2_ThetaRho;
    data1_2D_orig_cell{i} = data_row.data1_2D_orig;
    data2_2D_orig_cell{i} = data_row.data2_2D_orig;
    data1_2D_512_cell{i} = data_row.data1_2D_512;
    data2_2D_512_cell{i} = data_row.data2_2D_512;
    data1_2D_376_cell{i} = data_row.data1_2D_376;
    data2_2D_376_cell{i} = data_row.data2_2D_376;
    data1_cutedhere_cell{i} = data_row.data1_cutedhere;
    data2_cutedhere_cell{i} = data_row.data2_cutedhere;
    data_3D_cell{i} = data_row.data_3D;





end

% Preallocate the cell array to hold the transformed data
Everything_2 = cell(numberofcolums, 13); % Assuming numberofcolums rows and 5 columns

% Iterate through the cell arrays and reshape the [1x1x4 double] or [1x1x6 double]
for i = 1:numberofcolums
    Everything_2{i, 1} = data1_imageid_cell{i};
    Everything_2{i, 2} = data2_imageid_cell{i};

    % Reshape second_col_data_1_cell to 1x4
    Everything_2{i, 3} = reshape(data1_ThetaRho_cell{i}, 1, 2);
    Everything_2{i, 4} = reshape(data2_ThetaRho_cell{i}, 1, 2);

    % Reshape second_col_data_2_cell to 1x4
    Everything_2{i, 5} = reshape(data1_2D_orig_cell{i}, 1, 4);
    Everything_2{i, 6} = reshape(data2_2D_orig_cell{i}, 1, 4);

    Everything_2{i, 7} = reshape(data1_2D_512_cell{i}, 1, 4);
    Everything_2{i, 8} = reshape(data2_2D_512_cell{i}, 1, 4);

    Everything_2{i, 9} = reshape(data1_2D_376_cell{i}, 1, 4);
    Everything_2{i, 10} = reshape(data2_2D_376_cell{i}, 1, 4);

    Everything_2{i, 11} = reshape(data1_cutedhere_cell{i}, 1, 2);
    Everything_2{i, 12} = reshape(data2_cutedhere_cell{i}, 1, 2);

    % Reshape third_col_data_2_cell to 1x6
    Everything_2{i, 13} = reshape(data_3D_cell{i}, 1, 6);









end