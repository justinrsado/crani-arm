wd = pwd;

input_folder = 'data\';
fullMatFileName = fullfile(input_folder,  'S2_E3_A1.mat')
if ~exist(fullMatFileName, 'file')
  message = sprintf('%s does not exist', fullMatFileName);
  uiwait(warndlg(message));
else
  data = load(fullMatFileName);
end

output_folder = 'output\';
extension = '.csv';
prefix = "S2_E3_A1_";

names = fieldnames(data);
for n = 1:length(names)
    field = names{n};
    if field ~= "subject" || field ~= "exercise"
        filename = fullfile(output_folder, prefix + field + extension);
        csvwrite(filename, data.(field));
    end
end