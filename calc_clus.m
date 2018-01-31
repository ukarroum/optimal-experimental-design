X = importdata("samples\\clusters.txt");
Xp = X(:, 1:11)

for i = 1:25
    line = mat2cell(Xp(i, :), 1, ones(1, 11));
    y(i, 1) = couplageOLT(line{:});
end

dlmwrite('clusters_c.txt', [X y], ' ')