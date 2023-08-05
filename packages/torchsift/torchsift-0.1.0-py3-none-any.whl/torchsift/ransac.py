from typing import Tuple
import torch
import math


@torch.jit.script
def project(
    X: torch.Tensor,
    Y: torch.Tensor,
    it: torch.Tensor = torch.tensor([32]),
    ratio: torch.Tensor = torch.tensor([0.6]),
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    parametres:
        X: (*B, N, D), B is auxiliary batch dimensions, N is the sample size, D is the feature dimension
        Y: (*B, M, D), M is the sample size, D is the feature dimension
        it: int, the number of iterations
        ratio: float, the sampling ratio for each iteration

    return:
        Hb: (*B, D + 1, D + 1), the projection matrix,
        ERb: (*B, ), the error matrix

    implementation details:

        variables:

            B (int): the auxiliary batch dimensions
            N (int): the sample size
            D (int): the feature dimension
            L (int): the number of samples for each iteration
            Xh (B, N, D + 1): X in homogeneous coordinates
            Yh (B, N, D + 1): Y in homogeneous coordinates
            P (it, L): permutation matrix
            Xs (B, it, L, D + 1): the sampled X
            Ys (B, it, L, D + 1): the sampled Y
            H (B, it, D + 1, D + 1): the projection tensor where every H[b, i] is a projection matrix
            ER (B, it): the error matrix
            I(B): the index matrix
            Hr (B, D + 1, D + 1): the projection matrix of the best iteration of each batch
            ERr (B, ): the error matrix of the best iteration of each batch
    """
    # reshape X and Y to (*B, N, D) and (*B, M, D)
    X = X.view(-1, X.shape[-2], X.shape[-1])
    Y = Y.view(-1, Y.shape[-2], Y.shape[-1])

    B, N, D = X.shape

    L = int(N * ratio[0])
    # build homogeneous coordinates
    Xh = torch.cat([X, torch.ones(B, N, 1, device=X.device)], dim=-1)
    Yh = torch.cat([Y, torch.ones(B, N, 1, device=Y.device)], dim=-1)

    # build permutation matrix to simultaneously run different iterations
    P = torch.empty(it[0], L, dtype=torch.int64, device=X.device)
    for i in torch.arange(it[0]):
        P[i] = torch.randperm(N)[:L]

    # select Xs and Ys from Xh and Yh using permutation matrix P
    Xs = Xh[:, P]
    Ys = Yh[:, P]

    # lsqrt to find the projection matrix using sampled Xh and Yh
    H = torch.linalg.lstsq(Xs, Ys).solution

    # evaluate the transformation error on the entire Xh and Yh

    #       explain for batch matrix multiplication:
    ############################################################
    # Xh has shape (B, N, D + 1) and H has shape (B, it, D + 1, D + 1)
    # we unsqueeze Xh to (B, 1, N, D + 1) so the broadcasting mechanism
    # will be equivalent to expand Xh into (B, it, N, D + 1)
    # where the original last 2 dimensions are view-copied along the 1 valued dimension (second dimension)
    # internally, this is equivalent to the following code:
    # Xh = Xh.unsqueeze(1).expand(B, it, N, D + 1).contiguous().view(B * it, N, D + 1)
    # H = H.contiguous().view(B * B, D + 1, D + 1)
    # res = torch.mm(Xh, H)
    # res = res.view(B, it, N, D + 1)
    # REMINDER: batch matrix multiplication always compare last 2 dimensions first.
    ############################################################

    DIFF = Xh.unsqueeze(1) @ H - Yh.unsqueeze(1)
    # calculate the total error for each iteration
    ER = torch.norm(DIFF, dim=(-1, -2))
    # find the best iteration of each batch
    I = torch.argmin(ER, dim=-1)
    # select the best projection matrix of each batch
    # Hb = [H[0, I[0]], H[1, I[1]], ..., H[B - 1, I[B - 1]]]
    Hb = H[torch.arange(B, device=X.device), I]
    # also select the best error associated with the best projection matrix
    ERb = ER[torch.arange(B, device=X.device), I]

    return Hb, ERb


@torch.jit.script
def select(
    X: torch.Tensor,
    Y: torch.Tensor,
    it: torch.Tensor = torch.tensor([32]),
    ratio: torch.Tensor = torch.tensor([0.6]),
) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor, torch.Tensor]:
    """
    parametres:
        X: (*B, N, D), B is auxiliary batch dimensions, N is the sample size, D is the feature dimension
        Y: (*B, N, D), M is the sample size, D is the feature dimension
        it: int, the number of iterations
        ratio: float, the sampling ratio for each iteration

    return:
        Hb: (*B, D + 1, D + 1), the projection matrix,
        Xi (B, M, D): The inlier X
        Yi (B, M, D): The inlier Y
        IX (M, D): index of inliers in X
        IY (M, D): index of inliers in Y

    implementation details:

        variables:

            B (int): the auxiliary batch dimensions
            N (int): the sample size
            D (int): the feature dimension
            DIFF (B, N, D): the difference between X and Y
            ER (B, N): the error matrix
            T (B, 1): The threshold matrix
            I (B, N): The bool index matrix for inliers
    """
    B, N, D = X.shape

    # get the best projection matrix for each batch
    # this Hb is in homogeneous coordinates
    Hb, _ = project(X, Y, it, ratio)
    # build homogeneous coordinates
    Xh = torch.cat([X, torch.ones(B, N, 1, device=X.device)], dim=-1)
    Yh = torch.cat([Y, torch.ones(B, N, 1, device=Y.device)], dim=-1)

    ############################################################
    # Xh has shape      (B, N    , D + 1)
    # and Hb has shape (B, D + 1, D + 1)
    # result =>        (B, N    , D + 1) (the result of last two dimensions is (N, D + 1) and the batch dimension is broadcasted)
    ############################################################
    DIFF = Xh @ Hb - Yh

    # calculate the total error for each sample
    ER = torch.norm(DIFF, dim=-1)
    # use the mean error of each batch as the threshold
    # since mean is greatly influenced by outliers and will shift to them,
    # we can automatically cover most of the inliers by utilizing this feature
    T = torch.mean(ER, dim=-1, keepdim=True)
    I = ER < T
    # select the inliers of X and Y
    Xi = X[I]
    Yi = Y[I]
    # select the index of inliers of X and Y
    IX = torch.nonzero(I)
    IY = torch.nonzero(I)

    return Hb, Xi, Yi, IX, IY


@torch.jit.script
def count(
    X: torch.Tensor,
    Y: torch.Tensor,
    it: torch.Tensor = torch.tensor([32]),
    ratio: torch.Tensor = torch.tensor([0.6]),
) -> torch.Tensor:
    """
    parametres:
        X: (*B, N, D), B is auxiliary batch dimensions, N is the sample size, D is the feature dimension
        Y: (*B, M, D), M is the sample size, D is the feature dimension
        it: int, the number of iterations
        ratio: float, the sampling ratio for each iteration

    return:
        MATCH (B,): the number of inliers for each batch

    implementation details:

        variables:

            B (int): the auxiliary batch dimensions
            N (int): the sample size
            D (int): the feature dimension
            DIFF (B, N, D): the difference between X and Y
            ER (B, N): the error matrix
            T (B,): The threshold matrix
            I (B,): The index matrix for inliers
    """
    B, N, D = X.shape
    # get the best projection matrix for each batch
    Hb, _ = project(X, Y, it, ratio)
    # build homogeneous coordinates
    Xh = torch.cat([X, torch.ones(B, N, 1, device=X.device)], dim=-1)
    Yh = torch.cat([Y, torch.ones(B, N, 1, device=Y.device)], dim=-1)
    ############################################################
    # Xh has shape      (B, N    , D + 1)
    # and Hb has shape (B, D + 1, D + 1)
    # result =>        (B, N    , D + 1) (the result of last two dimensions is (N, D + 1) and the batch dimension is broadcasted)
    ############################################################
    DIFF = Xh @ Hb - Yh
    # calculate the total error for each sample
    ER = torch.norm(DIFF, dim=-1)
    # use the mean error of each batch as the threshold
    # since mean is greatly influenced by outliers and will shift to them,
    # we can automatically cover most of the inliers by utilizing this feature
    T = torch.mean(ER, dim=-1, keepdim=True)
    I = ER < T
    # sum the number of inliers for each batch
    # for each pair of X[i] and Y[i], MATCH[i] is the number of inliers
    return torch.sum(I, dim=-1)




@torch.jit.script
def error(
    X: torch.Tensor,
    Y: torch.Tensor,
    it: torch.Tensor = torch.tensor([32]),
    ratio: torch.Tensor = torch.tensor([0.6]),
) -> torch.Tensor:
    """
    parametres:
        X: (*B, N, D), B is auxiliary batch dimensions, N is the sample size, D is the feature dimension
        Y: (*B, M, D), M is the sample size, D is the feature dimension
        it: int, the number of iterations
        ratio: float, the sampling ratio for each iteration

    return:
        ER (B,): the error matrix

    implementation details:

        variables:

            B (int): the auxiliary batch dimensions
            N (int): the sample size
            D (int): the feature dimension
            DIFF (B, N, D): the difference between X and Y
            ER (B, N): the error matrix
            T (B,): The threshold matrix
            I (B,): The index matrix for inliers
    """
    B, N, D = X.shape
    # get the best projection matrix for each batch
    Hb, _ = project(X, Y, it, ratio)
    # build homogeneous coordinates
    Xh = torch.cat([X, torch.ones(B, N, 1, device=X.device)], dim=-1)
    Yh = torch.cat([Y, torch.ones(B, N, 1, device=Y.device)], dim=-1)
    ############################################################
    # Xh has shape      (B, N    , D + 1)
    # and Hb has shape (B, D + 1, D + 1)
    # result =>        (B, N    , D + 1) (the result of last two dimensions is (N, D + 1) and the batch dimension is broadcasted)
    ############################################################
    DIFF = Xh @ Hb - Yh
    # calculate the total error for each sample
    ER = torch.norm(DIFF, dim=-1)
    ER = torch.mean(ER, dim=-1)
    return ER
