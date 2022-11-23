def elbow_kmeans(data, max_k):

    import matplotlib.pyplot as plt

    from sklearn.cluster import KMeans

    means = []

    inertias = []

    for k in range(1, max_k):

        kmeans = KMeans(n_clusters=k)

        kmeans.fit(data)

        means.append(k)

        inertias.append(kmeans.inertia_)

    fig = plt.subplots(figsize=(10, 5))

    plt.plot(means, inertias, 'o-')

    plt.xlabel('Number of Clusters')

    plt.ylabel('Inertia')

    plt.grid(True)

    plt.show()


