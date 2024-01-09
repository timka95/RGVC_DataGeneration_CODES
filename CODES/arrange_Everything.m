% Initialize cell arrays for each field

% data = load('/Users/timeanemet/Desktop/CNN/matfiles/new_osszesitett.mat');
data = load('/project/ntimea/l2d2/IMAGE_PAIR_GT/CODES/Data_Generation/Matfiles/data_cutted_pairs_Everything.mat');

loadeddata = data.data_cutted_pairs_Everything;




numberofcolums = 143805;

image_id_1_cell = cell(numberofcolums, 1);
image_id_2_cell = cell(numberofcolums, 1);
data1_ThetaRho_cell = cell(numberofcolums, 1);
data2_ThetaRho_cell = cell(numberofcolums, 1);
second_col_data_1_cell = cell(numberofcolums, 1);
second_col_data_2_cell = cell(numberofcolums, 1);
data1_2D_512_cell = cell(numberofcolums, 1);
data2_2D_512_cell = cell(numberofcolums, 1);
data1_2D_orig_cell = cell(numberofcolums, 1);
data2_2D_orig_cell = cell(numberofcolums, 1);
data1_cutedhere_cell = cell(numberofcolums, 1);
data2_cutedhere_cell = cell(numberofcolums, 1);
third_col_data_2_cell = cell(numberofcolums, 1);








% Iterate through the cell array and extract data for each field
for i = 1:numberofcolums
    data_row = loadeddata{i, 1}; % Access each 1x1 struct

    image_id_1_cell{i} = data_row.image_id_1;
    image_id_2_cell{i} = data_row.image_id_2;

    data1_ThetaRho_cell{i} = data_row.data1_ThetaRho;
    data2_ThetaRho_cell{i} = data_row.data2_ThetaRho;
    second_col_data_1_cell{i} = data_row.second_col_data_1;
    second_col_data_2_cell{i} = data_row.second_col_data_2;
    data1_2D_512_cell{i} = data_row.data1_2D_512;
    data2_2D_512_cell{i} = data_row.data2_2D_512;
    data1_2D_orig_cell{i} = data_row.data1_2D_orig;
    data2_2D_orig_cell{i} = data_row.data2_2D_orig;
    data1_cutedhere_cell{i} = data_row.data1_cutedhere;
    data2_cutedhere_cell{i} = data_row.data2_cutedhere;
    third_col_data_2_cell{i} = data_row.third_col_data_2;





end

% Preallocate the cell array to hold the transformed data
Everything_2 = cell(numberofcolums, 13); % Assuming numberofcolums rows and 5 columns

% Iterate through the cell arrays and reshape the [1x1x4 double] or [1x1x6 double]
for i = 1:numberofcolums
    Everything_2{i, 1} = image_id_1_cell{i};
    Everything_2{i, 2} = image_id_2_cell{i};

    % Reshape second_col_data_1_cell to 1x4
    Everything_2{i, 3} = reshape(data1_ThetaRho_cell{i}, 1, 2);
    Everything_2{i, 4} = reshape(data2_ThetaRho_cell{i}, 1, 2);

    % Reshape second_col_data_2_cell to 1x4
    Everything_2{i, 5} = reshape(second_col_data_1_cell{i}, 1, 4);
    Everything_2{i, 6} = reshape(second_col_data_2_cell{i}, 1, 4);

    Everything_2{i, 7} = reshape(data1_2D_512_cell{i}, 1, 4);
    Everything_2{i, 8} = reshape(data2_2D_512_cell{i}, 1, 4);

    Everything_2{i, 9} = reshape(data1_2D_orig_cell{i}, 1, 4);
    Everything_2{i, 10} = reshape(data2_2D_orig_cell{i}, 1, 4);

    Everything_2{i, 11} = reshape(data1_cutedhere_cell{i}, 1, 2);
    Everything_2{i, 12} = reshape(data2_cutedhere_cell{i}, 1, 2);

    % Reshape third_col_data_2_cell to 1x6
    Everything_2{i, 13} = reshape(third_col_data_2_cell{i}, 1, 6);









end