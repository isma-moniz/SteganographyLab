import cv2
import numpy as np
from scipy.stats import entropy
import argparse


def load_grayscale(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

    if img is None:
        raise ValueError(f"Could not load image: {path}")

    return img


def compute_residual(img, method="gaussian"):
    """
    residual image:
        residual = |original - denoised|
    """

    if method == "gaussian":
        denoised = cv2.GaussianBlur(img, (5, 5), 0)

    elif method == "median":
        denoised = cv2.medianBlur(img, 5)

    else:
        raise ValueError("Unknown denoising method")

    residual = cv2.absdiff(img, denoised)

    return residual


def residual_variance(residual):
    return np.var(residual)


def residual_entropy(residual):
    """
    Shannon entropy of residual histogram.
    """

    hist = cv2.calcHist([residual], [0], None, [256], [0, 256])
    hist = hist.flatten()

    hist_norm = hist / hist.sum()

    return entropy(hist_norm, base=2)


def neighbor_correlation(img):
    """
    Horizontal neighbor correlation.
    """

    left = img[:, :-1].flatten().astype(np.float64)
    right = img[:, 1:].flatten().astype(np.float64)

    correlation = np.corrcoef(left, right)[0, 1]

    return correlation


def analyze_image(path, method):
    img = load_grayscale(path)

    residual = compute_residual(img, method)

    variance = residual_variance(residual)
    ent = residual_entropy(residual)
    corr = neighbor_correlation(img)

    print(f"\n=== Analysis: {path} ===")
    print(f"Residual variance:      {variance:.4f}")
    print(f"Residual entropy:       {ent:.4f}")
    print(f"Neighbor correlation:   {corr:.6f}")

    cv2.imwrite(f"{path}_residual.png", residual)

    print(f"Residual image written to: {path}_residual.png")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("images", nargs="+")
    parser.add_argument(
        "--method",
        default="gaussian",
        choices=["gaussian", "median"]
    )

    args = parser.parse_args()

    for image_path in args.images:
        analyze_image(image_path, args.method)
