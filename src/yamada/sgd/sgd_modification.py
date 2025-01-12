def apply_crossing_swap(sgd, crossing_label):

    sgd = sgd.copy()

    X = sgd.get_object(crossing_label)

    (A, i), (B, j), (C, k), (D, l) = X.adjacent

    # Swap the under-crossing strand and over-crossing strand
    X[0] = D[l]
    X[1] = A[i]
    X[2] = B[j]
    X[3] = C[k]

    return sgd
