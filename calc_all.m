X = importdata("IN11_10000.txt");

for i = 1:10000
    line = mat2cell(X(i, :), 1, ones(1, 11));
    y(i, 1) = couplageOLT(line{:});
end

dlmwrite('all.txt', [X y], ' ')