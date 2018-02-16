X = importdata("..\\active.txt");
Xp = X(:, 1:11)

for i = 1:25
    line = mat2cell(Xp(i, :), 1, ones(1, 11));
    y(i, 1) = couplageOLT(line{:});
end

dlmwrite('..\\active_c.txt', [X y], ' ')