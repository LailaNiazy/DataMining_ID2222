%% Initialize the graph
E = csvread("Dataset/example1.dat");
col1 = E(:,1);
col2 = E(:,2);
if size(E,2) == 3   
    %add weights
    G = graph(col1,col2,E(:,3),'omitselfloops');
else 
    G = graph(col1,col2,'omitselfloops'); 
end
%% First step 
%Compute the affinity matrix, which is the adjacency matrix
%another way to compute it == > A = full(adjacency(G));
max_ids = max(max(col1,col2));
As= sparse(col1, col2, 1, max_ids, max_ids); 
A= full(As);
%% Second Step
%Compute the Degree Matrix
rows = sum(A,2);
D = diag(rows);
%Compute the Laplacian Matrix
L = (D^(-0.5))*A*(D^(-0.5));
%% Third Step
%extract the eigenvector with the highest eigenvalue
[eig_vec, eig_val] = eig(L);
[sort_eig_val, index] = sort(diag(eig_val), 'descend');

% find number of clusters
gaps = abs(diff(sort_eig_val)); 
[~,k] = max(gaps);
%extract the k largest eigenvectors
X = eig_vec(:,index(1:k));
%% Fourth Step
%normalize the extracted eigenvectors
Y = zeros(size(X));
for i=1:size(X,1)
    n = sqrt(sum(X(i,:).^2));    
    Y(i,:) = X(i,:) ./ n; 
end
%% Fifth Step
%k means
idx = kmeans(Y,k);
%% Sixth step
% plot results
h = plot(G, 'Layout', 'force');
%  returns the colormap with k colors.
colors=hsv(k);
for i=1:k
    highlight(h,find(idx==i),'NodeColor', colors(i,:) )  
end 
