nneighbors = [64,128,256,512,1024]
results = {}
metrics = ['cosine_distance', 'manhattan', 'euclidean', 'seuclidean', 'mahalanobis']
for metric in metrics:
    hist = {}
    summary = {}
    nearest_neighbors = NearestNeighbors(n_neighbors=1024, n_jobs=16)
    neighbors = nearest_neighbors.fit(X)
    distances, _ = neighbors.kneighbors(x)
    for n in nneighbors:
        histogram =  np.histogram(distances[:,:n-1].ravel(), bins=100, density=True)
        summary = {'min': distances[:,:n-1].min(), 'max': distances[:,:n-1].max(), 'mean': distances$
        hist.update({n: histogram})
    results.update({metric: 'summary': summary, 'histogram': histogram})

